# -*- coding: utf-8 -*-
"""
Expands Day 1 to 40 questions total:
- Morning: 20 Part 5 questions (high-yield TOEIC 860+ grammar & error bank traps)
- Afternoon: 20 questions (6 Recall + 8 Traps + 6 Part 7 questions across 2 passages)
"""

import master_curriculum

day1 = master_curriculum.DAYS_DATA[1]

# ==========================================
# MORNING BOOST: 20 PART 5 QUESTIONS
# ==========================================
day1["morning"]["part5"] = [
    {
        "id": 1,
        "target_seconds": 15,
        "question": "________ the unexpected budget cuts, the marketing team managed to launch the product on schedule.",
        "options": {
            "A": "Although",
            "B": "In spite of",
            "C": "Even if",
            "D": "Nevertheless"
        },
        "answer": "B",
        "analysis": "視覺錨點：空格後為 'the unexpected budget cuts'（純名詞片語無動詞），秒選介系詞。Although 與 Even if 後須接完整 S+V 子句；Nevertheless 為轉折副詞，不可放句首直接接名詞。",
        "translation": "儘管預算遭到意外縮減，行銷團隊仍成功如期推出該產品。"
    },
    {
        "id": 2,
        "target_seconds": 15,
        "question": "The board has appointed Ms. Alvarez to ________ the newly established division in Tokyo.",
        "options": {
            "A": "oversee",
            "B": "oversight",
            "C": "overseeing",
            "D": "overseen"
        },
        "answer": "A",
        "analysis": "看到不定詞結構 'to + [原形動詞]' 帶出受詞 'the newly established division'。oversee 為動詞（監督/負責）。oversight 為名詞（疏忽），語法與語意皆不合。",
        "translation": "董事會已指派 Alvarez 女士負責監督東京新成立的部門。"
    },
    {
        "id": 3,
        "target_seconds": 15,
        "question": "Only employees who have served for over two consecutive years are ________ for the corporate leadership program.",
        "options": {
            "A": "capable",
            "B": "eligible",
            "C": "accustomed",
            "D": "pertinent"
        },
        "answer": "B",
        "analysis": "介系詞搭配秒殺：看到空格後的 'for'，直接聯想語塊 'be eligible for'（符合……資格）。capable 搭配 of；accustomed 搭配 to；pertinent 搭配 to。",
        "translation": "只有連續任職超過兩年的員工，才符合參加企業領導培訓計畫的資格。"
    },
    {
        "id": 4,
        "target_seconds": 15,
        "question": "Customers receiving damaged merchandise are ________ to a full monetary refund within thirty days.",
        "options": {
            "A": "entitle",
            "B": "entitled",
            "C": "entitlement",
            "D": "entitling"
        },
        "answer": "B",
        "analysis": "固定片語結構秒殺：be entitled to + 名詞（有權獲得……）。are 為 be 動詞，後接過去分詞形容詞 entitled。entitlement 為名詞。",
        "translation": "收到瑕疵受損商品的顧客有權在 30 天內獲得全額退款。"
    },
    {
        "id": 5,
        "target_seconds": 15,
        "question": "Non-profit educational institutions are automatically ________ from state property taxes.",
        "options": {
            "A": "exempting",
            "B": "exemption",
            "C": "exempted",
            "D": "exempts"
        },
        "answer": "C",
        "analysis": "固定被動搭配：be exempted from + 名詞（被免除……義務/賦稅）。故選 (C) exempted。",
        "translation": "非營利教育機構自動免繳州財產稅。"
    },
    {
        "id": 6,
        "target_seconds": 15,
        "question": "Before installing the firmware update, please verify that it is fully ________ with your current operating system.",
        "options": {
            "A": "compatible",
            "B": "compliant",
            "C": "comparative",
            "D": "competitive"
        },
        "answer": "A",
        "analysis": "介系詞秒殺搭配：空格後為 'with'，秒選 compatible with（與……相容）。compliant 表合規；competitive 具競爭力的。",
        "translation": "在安裝韌體更新之前，請確認其與您目前的作業系統完全相容。"
    },
    {
        "id": 7,
        "target_seconds": 15,
        "question": "The newly established oncology laboratory was constructed under the direct ________ of Dr. Morales.",
        "options": {
            "A": "direct",
            "B": "director",
            "C": "direction",
            "D": "directed"
        },
        "answer": "C",
        "analysis": "商務高頻片語：under the direction of + 人物（在某人的領導/指導之下）。形容詞 direct 後需接名詞 direction。director 指主任，語意不通。",
        "translation": "新成立的腫瘤學實驗室是在莫拉萊斯博士的直接領導下建造的。"
    },
    {
        "id": 8,
        "target_seconds": 15,
        "question": "The regional vice president will ________ oversee the launch of the new logistics center in Frankfurt.",
        "options": {
            "A": "personal",
            "B": "personally",
            "C": "personality",
            "D": "personalize"
        },
        "answer": "B",
        "analysis": "視覺錨點：will ________ oversee（助動詞 will 與動詞原形 oversee 之間的夾心位置，100% 填入副詞 -ly）。故選 (B) personally（親自地）。",
        "translation": "區域副總裁將親自監督法蘭克福新物流中心的啟用典禮。"
    },
    {
        "id": 9,
        "target_seconds": 15,
        "question": "________ severe traffic disruptions along Highway 101, several keynote speakers arrived late for the morning session.",
        "options": {
            "A": "Because",
            "B": "Owing to",
            "C": "Although",
            "D": "Even if"
        },
        "answer": "B",
        "analysis": "空格後為 'severe traffic disruptions'（名詞片語無動詞），屬於介系詞受詞，表原因選 (B) Owing to。(A) Because、(C) Although、(D) Even if 後方均需接完整的 S+V 子句。",
        "translation": "由於 101 號高速公路沿線嚴重的交通中斷，幾位專題演講者在上午的會議中遲到了。"
    },
    {
        "id": 10,
        "target_seconds": 15,
        "question": "Due to an administrative ________, the revised purchase order was sent to the wrong equipment supplier.",
        "options": {
            "A": "oversee",
            "B": "oversight",
            "C": "oversaw",
            "D": "overseeing"
        },
        "answer": "B",
        "analysis": "an administrative ________（冠詞 + 形容詞 + 名詞受詞位置）。語意為『行政上的疏失/遺漏』，名詞選 (B) oversight。(A) oversee 是動詞；(C) oversaw 為過去式動詞。",
        "translation": "由於行政上的疏漏，修改後的採購訂單被寄到了錯誤的設備供應商手中。"
    },
    {
        "id": 11,
        "target_seconds": 15,
        "question": "The CEO approved the commercial loan ________ the terms were strictly verified by the legal department.",
        "options": {
            "A": "provided that",
            "B": "in the event of",
            "C": "regardless",
            "D": "in spite of"
        },
        "answer": "A",
        "analysis": "空格後為 'the terms were strictly verified'（S+V 完整子句），表條件假設選從屬連接詞 (A) provided that（只要 / 在……條件下）。(B) 與 (D) 是介系詞片語，後接名詞。",
        "translation": "只要條款經過法律部門嚴格審查，執行長便批准了該筆商業貸款。"
    },
    {
        "id": 12,
        "target_seconds": 15,
        "question": "All conference attendees are strongly requested to refrain ________ taking flash photographs during the presentation.",
        "options": {
            "A": "for",
            "B": "from",
            "C": "by",
            "D": "at"
        },
        "answer": "B",
        "analysis": "介系詞搭配秒殺：refrain from + V-ing（克制/避免做某事）。故選 (B) from。",
        "translation": "強烈要求所有與會者在演講進行期間請勿使用閃光燈拍照。"
    },
    {
        "id": 13,
        "target_seconds": 15,
        "question": "Laboratory technicians must strictly adhere ________ safety regulations when handling flammable chemicals.",
        "options": {
            "A": "to",
            "B": "with",
            "C": "in",
            "D": "for"
        },
        "answer": "A",
        "analysis": "介系詞秒殺搭配：adhere to + 名詞（嚴格遵守……規定）。comply 接 with；abide 接 by。故選 (A) to。",
        "translation": "實驗室技術人員在處理易燃化學品時，必須嚴格遵守安全規程。"
    },
    {
        "id": 14,
        "target_seconds": 15,
        "question": "Mr. Davies will step ________ from his executive role after twenty years of service to the organization.",
        "options": {
            "A": "out",
            "B": "over",
            "C": "down",
            "D": "back"
        },
        "answer": "C",
        "analysis": "片語語意秒殺：step down from + 職位（辭職/卸任）。step down 表下台卸任；step out 暫時離開；take over 接管。故選 (C)。",
        "translation": "在為該機構服務二十年後，戴維斯先生將卸下其主管職位。"
    },
    {
        "id": 15,
        "target_seconds": 15,
        "question": "Ms. Vance has agreed to take ________ the responsibilities of department director effective immediately.",
        "options": {
            "A": "in",
            "B": "over",
            "C": "off",
            "D": "up"
        },
        "answer": "B",
        "analysis": "片語搭配：take over the responsibilities（接管/承接職責）。take over 表接任；take off 起飛/脫下。故選 (B)。",
        "translation": "萬斯女士已同意立即接管部門主管的職責。"
    },
    {
        "id": 16,
        "target_seconds": 15,
        "question": "Management decided to hold ________ on new capital expenditure until quarterly sales improve.",
        "options": {
            "A": "off",
            "B": "out",
            "C": "up",
            "D": "down"
        },
        "answer": "A",
        "analysis": "高頻片語：hold off on + 名詞/V-ing（暫緩推遲……）。hold off on spending 表暫緩資本支出。故選 (A)。",
        "translation": "管理層決定在季度銷售額改善之前，暫緩新的資本支出。"
    },
    {
        "id": 17,
        "target_seconds": 15,
        "question": "The steering committee ________ seven department heads and two external financial advisors.",
        "options": {
            "A": "consists of",
            "B": "is consisted of",
            "C": "persists in",
            "D": "insists on"
        },
        "answer": "A",
        "analysis": "consist of（由……組成）為不及物動詞片語，絕無被動態 (is consisted of ❌)！委員會由七位主管組成，選 (A)。persist in 堅持；insist on 堅持要求。",
        "translation": "指導委員會由七位部門主管與兩位外部財務顧問組成。"
    },
    {
        "id": 18,
        "target_seconds": 15,
        "question": "The safety inspector insisted ________ reviewing the facility's emergency evacuation protocols.",
        "options": {
            "A": "to",
            "B": "on",
            "C": "in",
            "D": "at"
        },
        "answer": "B",
        "analysis": "介系詞秒殺搭配：insist on + V-ing/名詞（堅持要求……）。persist 接 in；depend 接 on。故選 (B)。",
        "translation": "安全檢查員堅持要審查該設施的緊急疏散協議。"
    },
    {
        "id": 19,
        "target_seconds": 15,
        "question": "While one elevator is under maintenance, building tenants should use ________ elevators located near the north entrance.",
        "options": {
            "A": "another",
            "B": "other",
            "C": "others",
            "D": "one another"
        },
        "answer": "B",
        "analysis": "不定代名詞範圍：空格後為複數名詞 'elevators'，修飾複數名詞秒選 (B) other。another 只能修飾單數名詞；others 是代名詞後不可接名詞；one another 表彼此（受詞）。",
        "translation": "當一台電梯在維修時，大樓租戶應使用位於北側入口處的其他電梯。"
    },
    {
        "id": 20,
        "target_seconds": 15,
        "question": "The human resources department praised the newly recruited manager for handling complex disputes ________.",
        "options": {
            "A": "capable",
            "B": "capably",
            "C": "capability",
            "D": "capacitate"
        },
        "answer": "B",
        "analysis": "修飾動詞片語 'handling complex disputes' 需用副詞。capably 表『稱職地 / 幹練地』。故選 (B)。",
        "translation": "人力資源部讚揚新招聘的經理幹練且稱職地處理了複雜的爭議。"
    }
]

# ==========================================
# AFTERNOON REVIEW: 20 QUESTIONS TOTAL
# 6 Recall + 8 Traps + 6 Part 7 across 2 texts
# ==========================================
day1["afternoon"]["quick_recall"] = [
    {
        "prompt": "Ms. Lin was appointed to ________ [監督] the infrastructure project.",
        "clue": "動詞，字首為 o，監督主管",
        "answer": "oversee (oversee the project)"
    },
    {
        "prompt": "Due to an administrative ________ [疏失], the invoice was sent to the wrong vendor.",
        "clue": "名詞，字首為 o，不可與 oversee 混淆",
        "answer": "oversight (an unfortunate oversight)"
    },
    {
        "prompt": "Staff members must meet tenure requirements to be eligible ________ [介系詞] the annual bonus.",
        "clue": "符合……資格",
        "answer": "for (eligible for)"
    },
    {
        "prompt": "Customers are entitled ________ [介系詞] a full replacement for defective items.",
        "clue": "有權獲得……",
        "answer": "to (entitled to)"
    },
    {
        "prompt": "VIP ticket holders are exempted ________ [介系詞] paying baggage surcharges.",
        "clue": "被免除……費用",
        "answer": "from (exempted from)"
    },
    {
        "prompt": "Please ensure that the newly purchased scanner is compatible ________ [介系詞] our network.",
        "clue": "與……相容",
        "answer": "with (compatible with)"
    }
]

day1["afternoon"]["spaced_traps"] = [
    {
        "id": 1,
        "question": "The auditor noted that the accounting discrepancy was a minor ________ rather than intentional fraud.",
        "options": {
            "A": "oversee",
            "B": "oversight",
            "C": "overseer",
            "D": "overseeing"
        },
        "answer": "B",
        "trap_point": "名詞詞性與意義辨析：a minor + [名詞]。overseer 是監工（人），oversight 才是疏失（事物）。",
        "analysis": "句中對比 'rather than intentional fraud'（而非蓄意詐欺），空格需填入指『無心疏失』的名詞，故選 (B) oversight。"
    },
    {
        "id": 2,
        "question": "The proposed software upgrade is not fully ________ with older office workstations.",
        "options": {
            "A": "proficient",
            "B": "compatible",
            "C": "vulnerable",
            "D": "exempted"
        },
        "answer": "B",
        "trap_point": "介系詞搭配陷阱：with 出現，秒選 compatible。",
        "analysis": "compatible with（與……相容）。proficient 接 in；vulnerable 接 to；exempted 接 from。"
    },
    {
        "id": 3,
        "question": "________ Mr. Henderson worked through the night, he was unable to finalize the client proposal before the morning deadline.",
        "options": {
            "A": "Despite",
            "B": "Although",
            "C": "In spite of",
            "D": "Owing to"
        },
        "answer": "B",
        "trap_point": "看空格後有沒有動詞！後方有完整動詞 'worked'，絕不能選介系詞 (A), (C), (D)！",
        "analysis": "空格後為 'Mr. Henderson worked through the night'（主詞 + 動詞 worked），句意表轉折讓步，秒選從屬連接詞 (B) Although！"
    },
    {
        "id": 4,
        "question": "The lead mechanical engineer will ________ inspect the turbine before authorizing operational testing.",
        "options": {
            "A": "thorough",
            "B": "thoroughly",
            "C": "thoroughness",
            "D": "through"
        },
        "answer": "B",
        "trap_point": "will ________ inspect（助動詞與動詞原形之間的夾心餅乾，塞入副詞 -ly）！",
        "analysis": "修飾動詞 inspect，需用副詞 (B) thoroughly（徹底地 / 仔細地）。"
    },
    {
        "id": 5,
        "question": "In the event ________ an emergency power failure, the backup generators will activate automatically.",
        "options": {
            "A": "that",
            "B": "of",
            "C": "as",
            "D": "for"
        },
        "answer": "B",
        "trap_point": "後面是純名詞片語 'an emergency power failure'，無動詞！",
        "analysis": "純名詞片語選介系詞片語 in the event of。若有 S+V 句子才選 in the event that。"
    },
    {
        "id": 6,
        "question": "All research assistants must adhere strictly ________ established biohazard containment protocols.",
        "options": {
            "A": "to",
            "B": "with",
            "C": "in",
            "D": "for"
        },
        "answer": "A",
        "trap_point": "adhere 永遠搭配 to（遵守）！不可誤選 with。",
        "analysis": "adhere strictly to... 為商務英文最高頻必考片語，故選 (A)。"
    },
    {
        "id": 7,
        "question": "While ________ the quarterly budget sheets, the controller discovered an unaccounted deficit.",
        "options": {
            "A": "examine",
            "B": "examining",
            "C": "examined",
            "D": "examination"
        },
        "answer": "B",
        "trap_point": "分詞構句減化：主詞 主動 檢視報表並帶出受詞 'the budget sheets'！",
        "analysis": "主動做動作且帶受詞，while 後方減化分詞選現在分詞 (B) examining。"
    },
    {
        "id": 8,
        "question": "Contractual guidelines require departing commercial tenants to ________ the office suites by month-end.",
        "options": {
            "A": "vacate",
            "B": "vacant",
            "C": "vacantly",
            "D": "vacancy"
        },
        "answer": "A",
        "trap_point": "to + [動詞原形] + the office suites！",
        "analysis": "不定詞後接動詞原形，vacate（騰空/搬出物業）。vacant 為形容詞；vacancy 為名詞職缺。"
    }
]

day1["afternoon"]["part7"] = {
    "passages": [
        {
            "text_type": "Internal Policy Notice",
            "title": "Annual Health & Wellness Subsidy Guidelines",
            "content": "All permanent employees who have completed at least six months of service under the direction of a certified team lead are eligible for an annual health subsidy of up to $500. This fund can be applied toward gym memberships or ergonomically approved home-office furniture. \n\n*Note: Part-time staff and temporary interns are exempted from the mandatory activity log but are entitled to a modified subsidy of $150, provided that their application is submitted prior to November 15.",
            "questions": [
                {
                    "question": "What is required for temporary interns to receive a subsidy?",
                    "options": {
                        "A": "Complete six months of full-time service.",
                        "B": "Maintain a daily workout log.",
                        "C": "Apply before November 15.",
                        "D": "Purchase certified gym equipment."
                    },
                    "answer": "C",
                    "radar": "🔍 防漏看雷達：看到 *Note 星號附註中的條件句 'provided that their application is submitted prior to November 15'！實習生不必滿 6 個月，但必須在 11/15 前提出申請。",
                    "analysis": "文中星號標記明確指出實習生享有修改後的補助，前提是申請在 11 月 15 日前提出（prior to November 15 = before November 15），故選 (C)。"
                },
                {
                    "question": "What is TRUE about permanent employees regarding the subsidy?",
                    "options": {
                        "A": "They must have at least six months of continuous tenure.",
                        "B": "They can claim up to $1,000 annually.",
                        "C": "They are exempted from submitting wellness receipts.",
                        "D": "They must purchase their own office laptops."
                    },
                    "answer": "A",
                    "radar": "🔍 防漏看雷達：首句開頭細節 'completed at least six months of service'！",
                    "analysis": "第一句提及 'All permanent employees who have completed at least six months of service... are eligible'，與 (A) 意思完全相符。"
                },
                {
                    "question": "Which item is eligible for reimbursement under this wellness policy?",
                    "options": {
                        "A": "Standard home office stationery supplies.",
                        "B": "Ergonomically certified home-office furniture.",
                        "C": "Monthly public transit commuting cards.",
                        "D": "Uncertified personal recreational items."
                    },
                    "answer": "B",
                    "radar": "🔍 防漏看雷達：內文具體名詞替換！'applied toward gym memberships or ergonomically approved home-office furniture' ＝ 'Ergonomically certified home-office furniture'！",
                    "analysis": "文中第一段第二句清楚列出補助可用於健身房會籍或人體工學核准家具，故選 (B)。"
                }
            ]
        },
        {
            "text_type": "Corporate Travel & Attire Memo",
            "title": "Summit Logistics: Dress Code and Baggage Allowance",
            "content": "To: Regional Sales Representatives\nFrom: Events Planning Directorate\nDate: November 4\n\nAll representatives attending the annual Chicago summit will be provided accommodation at the Grand Plaza. Standard business attire is mandatory for daytime panel sessions. However, casual garments are permitted exclusively during the Friday evening networking reception.\n\n*Luggage Allowance: The company will reimburse luggage fees for up to two checked bags, provided that luggage receipts are submitted within 7 days of trip conclusion. Claims submitted after this 7-day threshold will be rejected without exception.",
            "questions": [
                {
                    "question": "What type of clothing is permitted exclusively on Friday evening?",
                    "options": {
                        "A": "Formal evening tuxedos and gowns.",
                        "B": "Casual clothing.",
                        "C": "Branded sports jerseys.",
                        "D": "Traditional ethnic costumes."
                    },
                    "answer": "B",
                    "radar": "🔍 防漏看雷達：限制副詞 exclusively！'casual garments are permitted exclusively during the Friday evening networking reception'！garments ＝ clothing！",
                    "analysis": "文中指出週五晚間社交酒會唯一允許休閒便服（casual garments = casual clothing），故選 (B)。"
                },
                {
                    "question": "How many checked bags can delegates have reimbursed?",
                    "options": {
                        "A": "One bag only.",
                        "B": "Up to two checked bags.",
                        "C": "Three checked bags.",
                        "D": "Unlimited bags with manager approval."
                    },
                    "answer": "B",
                    "radar": "🔍 防漏看雷達：具體數字細節 'reimburse luggage fees for up to two checked bags'！",
                    "analysis": "行李補助條款明確載明可報銷至多兩件托運行李（up to two checked bags），故選 (B)。"
                },
                {
                    "question": "Under what condition will a luggage reimbursement claim be denied?",
                    "options": {
                        "A": "If the representative flew on an unapproved airline.",
                        "B": "If receipts are submitted more than 7 days after the trip ends.",
                        "C": "If the delegate traveled alone without a colleague.",
                        "D": "If checked bags weighed over 20 kilograms each."
                    },
                    "answer": "B",
                    "radar": "🔍 防漏看雷達：星號附註最後一句 'Claims submitted after this 7-day threshold will be rejected without exception'！rejected ＝ denied！",
                    "analysis": "文末星號強調若超過 7 天期限繳交收據，報銷申請將毫無例外地遭到拒絕（rejected = denied），故選 (B)。"
                }
            ]
        }
    ]
}

# Write back to master_curriculum.py
with open("master_curriculum.py", "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""\nMaster 25-Day TOEIC Golden Certificate (860+) Curriculum\n"""\n\n')
    f.write("DAYS_DATA = " + repr(master_curriculum.DAYS_DATA) + "\n")

print("Successfully updated Day 1 to 40 questions (20 Morning + 20 Afternoon)!")
