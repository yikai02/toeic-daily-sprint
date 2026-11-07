# -*- coding: utf-8 -*-
"""
Master Vocabulary & Deduplication Manager (`vocabulary_manager.py`)
-------------------------------------------------------------------
1. Merges existing TOEIC curriculum vocabulary with `860_antigravity.md` (97 words + confusion pairs).
2. Automatically deduplicates overlapping words/phrases so identical words are never stored twice;
   instead, existing entries are enriched with the new collocations and trap notes.
3. Assigns TOEIC frequency & simplicity priority tiers (`freq_tier` 1-3) so common/high-frequency
   words and user-missed words are scheduled more frequently.
4. Supports ongoing vocabulary expansion via CLI (`--import-file`) or Telegram messages (`新增單字 ...`).
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_DIR = Path(__file__).resolve().parent
VOCAB_DB_PATH = PROJECT_DIR / "master_vocab_db.json"
MD_860_PATH = PROJECT_DIR / "860_antigravity.md"

# High-frequency common TOEIC core words (shorter/simpler & extremely common on TOEIC -> Tier 3 highest base frequency)
ULTRA_HIGH_FREQ_WORDS = {
    "exclusive", "complimentary", "imperative", "discreet", "discrete", "neglect",
    "proximity", "exposure", "venue", "unveil", "namely", "thereby", "nonetheless",
    "termination", "clause", "whereas", "however", "though", "as if", "even though",
    "regardless of", "in the event that", "discretion", "discrepancy", "as far as",
    "in order that", "even if", "subject", "confine", "abstain", "unanimous",
    "inclusive", "takeout", "courier", "pedestrians", "task", "garment", "brochure",
    "complex", "committee", "spare", "premises", "alternative", "inclement",
    "temps", "incentive", "intention", "urgent", "quote", "dedication", "scrutinize",
    "acquisition", "template", "alteration", "literature", "prohibit", "relinquish",
    "discharge", "exempt", "mandatory", "stringent", "the remainder", "within reach",
    "a combined total of", "alike", "oversee", "oversight", "eligible", "entitled",
    "compatible", "proceed", "procedure", "consist of", "persist in", "insist on",
    "prior to", "owing to", "provided that",
}


def normalize_headword(text: str) -> str:
    """Normalize a word or phrase for strict deduplication."""
    s = text.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s


def compute_freq_tier(word: str) -> int:
    """
    Assign TOEIC frequency tier (1 to 3):
    - Tier 3 (Ultra-High Frequency & Common Core): Common, shorter, or top-tested TOEIC words (appear most frequently).
    - Tier 2 (High-Frequency Business Core): Standard TOEIC 800-860 words.
    - Tier 1 (Advanced 860-990 Vocabulary): Longer specialized vocabulary.
    """
    norm = normalize_headword(word)
    if norm in ULTRA_HIGH_FREQ_WORDS:
        return 3
    for uw in ULTRA_HIGH_FREQ_WORDS:
        if len(uw) >= 4 and (norm == uw or norm.startswith(uw + " ") or norm.endswith(" " + uw)):
            return 3
    if len(norm) <= 8:
        return 3
    if len(norm) <= 12:
        return 2
    return 1


# Authentic TOEIC 860+ example sentences for words from 860_antigravity.md
EXAMPLES_860 = {
    "exclusive": "Platinum cardholders enjoy exclusive access to the airport VIP lounge, which is exclusive of guest pass fees.",
    "prominent": "Dr. Evelyn Sato, a prominent macroeconomist, will deliver the opening keynote address at the Zurich summit.",
    "complimentary": "All conference registrants are entitled to a complimentary buffet breakfast and high-speed Wi-Fi at the venue.",
    "deficient": "The safety audit revealed that the warehouse ventilation system was severely deficient in air-filtration capacity.",
    "imperative": "It is imperative that all international shipping manifests be verified before the cargo vessel departs.",
    "ascertain": "Forensic accountants were retained to ascertain the exact cause of the third-quarter inventory discrepancy.",
    "discreet": "Executive recruiters must remain strictly discreet when approaching senior candidates from competing firms.",
    "accumulative": "The accumulative effect of minor assembly-line delays resulted in a significant production backlog.",
    "pervasive": "With cloud-based collaboration tools becoming pervasive across the industry, remote auditing is now standard practice.",
    "conscientiously": "Ms. Lin conscientiously reviewed every clause of the vendor agreement before authorizing the wire transfer.",
    "neglect": "Tenants who neglect to submit their lease renewal forms thirty days in advance may forfeit their security deposit.",
    "subsequently": "The prototype initially failed thermal testing; subsequently, the engineering team redesigned the cooling fan.",
    "succession": "After winning the industry quality award for four years in succession, the plant expanded its production capacity.",
    "proximity": "Located in close proximity to the central rail terminal, the new office complex attracts top regional talent.",
    "exposure": "Sponsoring the international marathon gave our sportswear brand extensive media exposure across Europe.",
    "venue": "Due to overwhelming ticket demand, organizers relocated the trade symposium to a larger downtown venue.",
    "unveil": "The automaker plans to unveil its next-generation autonomous delivery van at the Frankfurt Motor Show.",
    "autonomous": "Each regional subsidiary operates as an autonomous business unit while adhering to corporate financial guidelines.",
    "namely": "Only two departments exceeded their quarterly cost-reduction targets, namely Procurement and Logistics.",
    "thereby": "The firm consolidated three regional warehouses into a single automated hub, thereby cutting transit costs by 22%.",
    "nonetheless": "The construction project encountered severe inclement weather in March; nonetheless, the contractor finished on schedule.",
    "somewhat": "Although third-quarter retail sales were somewhat lower than projected, annual net profit reached a record high.",
    "termination": "Either party may initiate contract termination by providing sixty days' written notice to the other party.",
    "clause": "Our legal counsel inserted a penalty clause into the supply contract to protect against late deliveries.",
    "whereas": "Domestic sales of desktop computers declined by five percent, whereas enterprise cloud subscriptions surged.",
    "however": "The proposed software upgrade offers enhanced security; however, it is not compatible with older terminals.",
    "though": "Though the initial investment was substantial, the solar array paid for itself within three fiscal years.",
    "as if": "The newly renovated lobby looks as if it were designed by an award-winning contemporary architect.",
    "even though": "Even though raw material prices fluctuated wildly, the manufacturer maintained stable wholesale pricing.",
    "regardless of": "All visitors must present photo identification at the security desk, regardless of their corporate title.",
    "in the event that": "In the event that the primary server experiences an outage, backup systems will activate within five seconds.",
    "discretion": "Department managers may approve remote-work requests at their own discretion during severe weather alerts.",
    "discrepancy": "The auditor discovered a $4,200 discrepancy between the digital invoice ledger and the bank statement.",
    "discrimination": "Our corporate charter enforces a zero-tolerance policy regarding any form of workplace discrimination.",
    "persistent": "Despite persistent supply chain bottlenecks, the electronics division fulfilled all holiday pre-orders.",
    "as far as": "As far as the quarterly marketing budget is concerned, no further expenditure can be authorized this month.",
    "in order that": "Please upload your presentation slides by Wednesday in order that our technical crew can test compatibility.",
    "even if": "Even if the municipal permit arrives tomorrow, road repaving cannot begin until the rain subsides.",
    "collateral": "The commercial lender required the startup to pledge its manufacturing equipment as loan collateral.",
    "fluctuation": "To protect profit margins against currency fluctuation, the exporter signed fixed-rate forward contracts.",
    "subject": "All international flight schedules and boarding gate assignments are subject to change without prior notice.",
    "resent": "Several senior technicians resented being excluded from the software architecture planning committee.",
    "confine": "Please confine your presentation remarks to the ten-minute slot allocated on the symposium agenda.",
    "abstain": "Three board members abstained from voting on the merger resolution due to potential conflicts of interest.",
    "unanimous": "Following two hours of deliberation, the selection committee reached a unanimous decision on the new CEO.",
    "inclusive": "The quoted banquet package price of $85 per guest is fully inclusive of service charges and local taxes.",
    "takeout": "To reduce plastic waste, the restaurant chain now offers a ten-percent discount on takeout orders using reusable containers.",
    "courier": "Sensitive legal contracts must be dispatched via an insured overnight courier rather than standard mail.",
    "repaving": "During the highway repaving project, northbound commuter buses will be detoured through Oak Avenue.",
    "pedestrians": "The downtown shopping boulevard is closed to motor vehicles on weekends to create a safe zone for pedestrians.",
    "stroll down": "Conference attendees can stroll down the scenic waterfront boardwalk during the two-hour midday break.",
    "task": "The newly appointed compliance officer was immediately tasked with revising the data privacy manual.",
    "garment": "Every waterproof garment manufactured at our Milan facility undergoes rigorous seam-sealing inspection.",
    "scatter": "Technicians had to gather dozens of inventory barcodes that had been scattered across the loading dock.",
    "along the coast": "Several luxury resort hotels along the coast reported ninety-five percent occupancy during the summer festival.",
    "brochure": "Please refer to the enclosed tourist brochure for a detailed map of historical landmarks and shuttle stops.",
    "complex": "The municipal council approved plans to convert the historic textile mill into a modern retail and office complex.",
    "committee": "The safety steering committee convenes on the first Tuesday of every month to review incident reports.",
    "stapler": "Please order three heavy-duty staplers and ten reams of recycled paper from the office supply catalog.",
    "spare": "Field maintenance technicians always carry spare hydraulic valves in their service vans for emergency repairs.",
    "premises": "Smoking and the use of unauthorized recording devices are strictly prohibited anywhere on the company premises.",
    "circular economy": "By refurbishing returned electronics, our company actively contributes to a sustainable circular economy.",
    "alternative": "When the main freight port was closed, the logistics team arranged rail transport as a cost-effective alternative.",
    "inclement": "Owing to severe inclement weather across the North Atlantic, several cargo vessels were delayed by two days.",
    "periodically": "To prevent mechanical breakdowns, factory cooling towers must be descaled and inspected periodically.",
    "collision": "All fleet delivery trucks are now equipped with radar sensors designed to prevent rear-end collisions.",
    "temps": "To handle the surge in year-end tax filings, the accounting firm hired fifteen certified seasonal temps.",
    "incentive": "The utility provider offers a generous cash incentive to commercial landlords who install rooftop solar panels.",
    "rehearsal": "All keynote speakers must attend the technical dress rehearsal in the main auditorium at 8:00 A.M.",
    "intention": "The pharmaceutical conglomerate announced its intention to acquire two regional diagnostic laboratories.",
    "urgent": "Please forward any urgent client inquiries directly to the on-call shift supervisor for immediate handling.",
    "negligence": "The insurance claim was rejected because the water damage resulted from the tenant's gross negligence.",
    "saturated": "Because the domestic smartphone market is already highly saturated, the brand is expanding into Latin America.",
    "editorial": "In Sunday's lead editorial, the financial newspaper praised the central bank's interest-rate policy.",
    "quote": "Before selecting a commercial roofing contractor, facilities management obtained written quotes from four vendors.",
    "dedication": "The retiring laboratory director was honored for her forty years of unwavering dedication to cancer research.",
    "scrutinize": "Customs inspectors closely scrutinize all agricultural imports to prevent the introduction of invasive pests.",
    "testament": "Our98% client renewal rate is a clear testament to the reliability and responsiveness of our support team.",
    "perseverance": "Through remarkable perseverance, the R&D engineers overcame three years of material durability challenges.",
    "devastating": "Last winter's frost had a devastating effect on citrus harvests across the southern agricultural belt.",
    "acquisition": "Following the acquisition of Nordic Freight, our firm became the largest cold-chain operator in Scandinavia.",
    "distinguish": "Our proprietary optical sensor can accurately distinguish between genuine banknotes and sophisticated counterfeits.",
    "template": "All department heads must use the standardized budget template when submitting next year's expenditure requests.",
    "alteration": "Tailors at our flagship boutique provide complimentary hemline alterations on all full-price business suits.",
    "culinary": "Graduates of the Geneva Culinary Institute have been recruited by five-star hotels around the globe.",
    "literature": "Sales representatives distributed updated product literature to prospective buyers at the medical device trade fair.",
    "monumental": "Completing the cross-harbor suspension bridge six months ahead of schedule was a monumental engineering feat.",
    "narrate": "A renowned broadcast journalist was hired to narrate the corporate documentary celebrating our centennial.",
    "manifestation": "The surge in repeat enterprise orders is a direct manifestation of our improved quality control protocols.",
    "resourceful": "Thanks to a resourceful warehouse supervisor, the chilled cargo was transferred to backup freezers during the blackout.",
    "prohibit": "Corporate cybersecurity guidelines strictly prohibit employees from installing unverified browser extensions.",
    "relinquish": "Under the terms of the settlement, the holding company agreed to relinquish its voting majority on the board.",
    "concede": "After reviewing the independent lab results, the supplier had to concede that the alloy batch was defective.",
    "discharge": "The hospital Board praised the nursing staff for discharging their clinical duties with exceptional professionalism.",
    "exempt": "Small businesses with annual revenues below the statutory threshold are exempt from the new municipal surcharge.",
    "mandatory": "Attendance at Friday's cybersecurity awareness workshop is mandatory for all personnel handling client data.",
    "stringent": "Medical device manufacturers must comply with stringent sterilization standards prior to product distribution.",
    "the remainder": "The keynote lecture will occupy the first hour, and the remainder of the morning will be devoted to workshops.",
    "within reach": "With fourth-quarter pre-orders exceeding expectations, our annual sales milestone is now well within reach.",
    "a combined total of": "The three regional charity galas raised a combined total of four hundred thousand dollars for children's hospitals.",
    "alike": "The new ergonomic office chairs have received enthusiastic feedback from executives and administrative staff alike.",
}


def build_or_update_master_vocab_db() -> dict:
    """Build or update the deduplicated master vocabulary database."""
    from master_curriculum import DAYS_DATA

    vocab_map: Dict[str, dict] = {}
    headword_index: Dict[str, str] = {}

    # 1. First load all 97 items + 4 confusion table extras from 860_antigravity.md
    if MD_860_PATH.exists():
        md_text = MD_860_PATH.read_text(encoding="utf-8")
        rows = re.findall(
            r"\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|",
            md_text,
        )
        for num, word, pos, mean, note in rows:
            w_clean = word.strip()
            norm = normalize_headword(w_clean)
            if norm in vocab_map:
                continue
            vid = f"860-{num}"
            entry = {
                "id": vid,
                "word": w_clean,
                "pos": pos.strip(),
                "meaning": mean.strip(),
                "collocations": note.strip().replace("`", ""),
                "trap_note": note.strip().replace("`", ""),
                "example": EXAMPLES_860.get(norm, f"Please review the corporate usage of '{w_clean}' in official documentation."),
                "source": "860_antigravity.md",
                "freq_tier": compute_freq_tier(w_clean),
            }
            vocab_map[norm] = entry
            headword_index[norm] = norm

    # Add the 4 additional confusion table items from Section II.4 of 860_antigravity.md
    extra_confusion_items = [
        ("860-C1", "the remainder", "n.", "其餘的人或物；剩餘款項／時間", "the remainder of the payment / meeting", "⚠️ 易混淆陷阱：切勿與 remains（遺體、歷史遺蹟、殘渣）混淆！表合約剩餘款項或會議剩餘時間一律用 the remainder。"),
        ("860-C2", "within reach", "prep. phr.", "指日可待、觸手可及", "within reach of the annual target", "⚠️ 易混淆陷阱：反義片語為 out of reach（遙不可及、能力所不及）。"),
        ("860-C3", "a combined total of", "phr.", "總計共達……（後接金額或數量）", "a combined total of $5 million", "⚠️ 易混淆陷阱：固定商業搭配詞，切勿誤選非正規搭配 combined totaling。"),
        ("860-C4", "alike", "adv.", "兩者皆然、一視同仁（置於 A and B 之後）", "customers and employees alike", "⚠️ 易混淆陷阱：A and B alike 置於兩個對等名詞之後；like A and B 則置於名詞之前。"),
    ]
    for cid, w_clean, pos, mean, colloc, trap in extra_confusion_items:
        norm = normalize_headword(w_clean)
        if norm not in vocab_map:
            vocab_map[norm] = {
                "id": cid,
                "word": w_clean,
                "pos": pos,
                "meaning": mean,
                "collocations": colloc,
                "trap_note": trap,
                "example": EXAMPLES_860.get(norm, ""),
                "source": "860_antigravity.md",
                "freq_tier": 3,
            }
            headword_index[norm] = norm

    # 2. Merge existing 170 curriculum chunks, deduplicating if the core word is already in vocab_map
    core_idx = 1
    for d in range(1, 26):
        for c in DAYS_DATA[d]["morning"]["chunks"]:
            chunk_str = c["chunk"].strip()
            norm_chunk = normalize_headword(chunk_str)
            # Check if exact phrase or headword is already represented in vocab_map
            words_in_chunk = [w.lower() for w in re.findall(r"[a-zA-Z-]+", chunk_str) if len(w) > 3]
            matched_existing_norm = None
            if norm_chunk in vocab_map:
                matched_existing_norm = norm_chunk
            else:
                for w_tok in words_in_chunk:
                    if w_tok in vocab_map:
                        matched_existing_norm = w_tok
                        break

            if matched_existing_norm:
                # Enrich existing entry without creating a duplicate!
                existing = vocab_map[matched_existing_norm]
                if chunk_str.lower() not in existing["collocations"].lower():
                    existing["collocations"] = f"{existing['collocations']} ｜ 延伸語塊：{chunk_str}（{c['meaning']}；{c['paraphrase']}）"
                if c.get("alert") and c["alert"] not in existing["trap_note"]:
                    existing["trap_note"] = f"{existing['trap_note']} ｜ {c['alert']}"
                continue

            vid = f"CORE-{core_idx:03d}"
            core_idx += 1
            vocab_map[norm_chunk] = {
                "id": vid,
                "word": chunk_str,
                "pos": "商務核心語塊 (phr.)",
                "meaning": c["meaning"],
                "collocations": c.get("paraphrase", chunk_str),
                "trap_note": c.get("alert") or f"核心替換：{c.get('paraphrase', '')}",
                "example": c.get("scenario", ""),
                "source": f"Day {d:02d} Core",
                "freq_tier": compute_freq_tier(chunk_str),
            }

    db_obj = {
        "total_unique_entries": len(vocab_map),
        "entries": list(vocab_map.values()),
    }
    VOCAB_DB_PATH.write_text(json.dumps(db_obj, ensure_ascii=False, indent=2), encoding="utf-8")
    return db_obj


def import_custom_vocab_lines(raw_text: str) -> Tuple[int, int, List[str]]:
    """
    Parse custom vocabulary lines from a user-supplied file or Telegram message
    and merge non-duplicate words into `master_vocab_db.json`.
    Returns (added_count, skipped_duplicate_count, added_words_list).
    """
    if VOCAB_DB_PATH.exists():
        db_obj = json.loads(VOCAB_DB_PATH.read_text(encoding="utf-8"))
    else:
        db_obj = build_or_update_master_vocab_db()

    existing_norms = {normalize_headword(e["word"]): e for e in db_obj.get("entries", [])}
    added_words = []
    skipped_dups = 0

    # Support markdown table rows OR "word | pos | meaning | note" OR "word - meaning"
    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith(">") or line.startswith("---"):
            continue
        # Markdown table row
        m_row = re.match(r"\|\s*(?:\*\*\d+\*\*\s*\|)?\s*\*\*?([a-zA-Z][a-zA-Z\s-]*?)\*\*?\s*\|\s*(.+?)\s*\|\s*(.+?)\s*(?:\|\s*(.+?)\s*)?\|", line)
        if m_row:
            word, pos, mean, note = m_row.group(1).strip(), m_row.group(2).strip(), m_row.group(3).strip(), (m_row.group(4) or "").strip()
        else:
            # Simple "word : meaning" or "word - meaning"
            m_simple = re.match(r"^([a-zA-Z][a-zA-Z\s-]{1,30})\s*[:：\-—]\s*(.+)$", line)
            if not m_simple:
                continue
            word, pos, mean, note = m_simple.group(1).strip(), "核心字彙", m_simple.group(2).strip(), "使用者自訂新增單字"

        if word.lower() in ("單字", "word", "編號"):
            continue
        norm = normalize_headword(word)
        if norm in existing_norms:
            skipped_dups += 1
            continue

        new_id = f"USER-{len(existing_norms) + 1:03d}"
        entry = {
            "id": new_id,
            "word": word,
            "pos": pos,
            "meaning": mean,
            "collocations": note or word,
            "trap_note": note or "使用者自訂重點強化單字",
            "example": EXAMPLES_860.get(norm, f"The executive committee emphasized the importance of {word} in the quarterly report."),
            "source": "User Custom Import",
            "freq_tier": 3,  # Newly added user words start at highest priority tier
            "is_user_added": True,
        }
        db_obj["entries"].append(entry)
        existing_norms[norm] = entry
        added_words.append(word)

    db_obj["total_unique_entries"] = len(db_obj["entries"])
    VOCAB_DB_PATH.write_text(json.dumps(db_obj, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(added_words), skipped_dups, added_words


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="TOEIC Master Vocabulary & Deduplication Manager")
    ap.add_argument("--import-file", type=str, help="Path to a .md / .txt vocabulary file to merge & deduplicate")
    args = ap.parse_args()

    db = build_or_update_master_vocab_db()
    print(f"✅ Master Vocabulary DB initialized: {db['total_unique_entries']} unique deduplicated entries.")
    if args.import_file:
        text = Path(args.import_file).read_text(encoding="utf-8")
        added, skipped, words = import_custom_vocab_lines(text)
        print(f"📥 Imported {args.import_file}: Added {added} new words, Skipped {skipped} already-existing duplicates.")
