# -*- coding: utf-8 -*-
"""
TOEIC 25-Day Golden Certificate (860+) Curriculum Data
Covers:
- Phase 1 (Day 1-10): 錯題庫清零與語感校正 (Error Bank Zeroing & Visual Anchors)
- Phase 2 (Day 11-18): 860 金色證書進階擴充與同義字轉換 (Expansion & Paraphrasing)
- Phase 3 (Day 19-25): 考前全真高壓實戰與防粗心特訓 (Full Simulation & Trap Radar)
"""

DAYS_DATA = {
    1: {
        "day": 1,
        "date": "11/04",
        "phase": 1,
        "phase_name": "錯題庫清零與語感校正",
        "topic": "連介秒殺 ｜ 監督 vs. 疏忽 ｜ 資格與授權語塊",
        "morning": {
            "chunks": [
                {
                    "chunk": "oversee the project",
                    "meaning": "監督這項專案",
                    "scenario": "Ms. Lin was appointed to oversee the project due to her extensive management experience.",
                    "paraphrase": "oversee = supervise = manage",
                    "alert": "注意：oversight 是名詞，指『疏忽 / 遺漏』！"
                },
                {
                    "chunk": "an unfortunate oversight",
                    "meaning": "一個令人遺憾的疏忽",
                    "scenario": "Due to an unfortunate oversight, the revised invoice was sent to the wrong vendor.",
                    "paraphrase": "oversight = mistake = omission",
                    "alert": ""
                },
                {
                    "chunk": "eligible for promotion",
                    "meaning": "符合升遷資格",
                    "scenario": "Only full-time staff who complete the leadership workshop are eligible for promotion.",
                    "paraphrase": "eligible for = qualified for",
                    "alert": "必考介系詞：eligible 後方固定搭配 for + 名詞！"
                },
                {
                    "chunk": "entitled to a refund",
                    "meaning": "有權獲得退款",
                    "scenario": "Customers receiving damaged items are entitled to a refund within 14 business days.",
                    "paraphrase": "entitled to = have the right to",
                    "alert": "必考介系詞：be entitled to + 名詞 / 原形動詞"
                },
                {
                    "chunk": "exempted from the fee",
                    "meaning": "免除此筆費用",
                    "scenario": "Attendees registering before Friday are automatically exempted from the fee.",
                    "paraphrase": "exempted from = excused from",
                    "alert": "必考介系詞：exempted 後方固定搭配 from！"
                },
                {
                    "chunk": "compatible with the system",
                    "meaning": "與該系統相容",
                    "scenario": "Please verify that the software update is compatible with the operating system.",
                    "paraphrase": "compatible with = adaptable to = work with",
                    "alert": "必考介系詞：compatible 固定搭配 with！"
                },
                {
                    "chunk": "under the direction of",
                    "meaning": "在……指導／領導之下",
                    "scenario": "The new research lab was constructed under the direction of Dr. Morales.",
                    "paraphrase": "under the direction of = under the leadership of",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "看到空格後有沒有「動詞」？",
                "rule_1": "👀 空格後有【主詞 + 動詞】➔ 秒選手拉手的「連接詞」（although, because, even if）",
                "rule_2": "👀 空格後只有【名詞 / V-ing】➔ 秒選單兵作戰的「介系詞」（in spite of, despite, owing to, prior to）",
                "golden_rule": "⚡ 教練金句：有動詞選「連」，沒動詞選「介」！"
            },
            "part5": [
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
                    "analysis": "空格後為 'the unexpected budget cuts'（名詞片語），後方接逗號，完全沒有動詞，因此必須填入介系詞。(A) Although 與 (C) Even if 後方須接 S+V；(D) Nevertheless 是轉折副詞，不可直接接名詞。",
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
                    "analysis": "看到不定詞結構 'to + [原形動詞]' 帶出受詞 'the newly established division'。oversee 為動詞（監督/管理）。oversight 為名詞（疏忽），語法與語意皆不符。",
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
                    "analysis": "直接依介系詞 'for' 秒殺搭配詞：be eligible for（符合……資格）。capable 搭配 of；accustomed 搭配 to；pertinent 搭配 to。",
                    "translation": "只有連續任職超過兩年的員工，才符合參加企業領導培訓計畫的資格。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "Ms. Lin was appointed to ________ [監督] the project.",
                    "clue": "動詞，字首為 o",
                    "answer": "oversee (oversee the project)"
                },
                {
                    "prompt": "Due to an unfortunate ________ [疏忽], the parcel was delayed.",
                    "clue": "名詞，不可與 oversee 混淆",
                    "answer": "oversight (an unfortunate oversight)"
                },
                {
                    "prompt": "Attendees registering today are exempted ________ [介系詞] the fee.",
                    "clue": "免除……費用",
                    "answer": "from (exempted from)"
                },
                {
                    "prompt": "All long-term contractors are entitled ________ [介系詞] parking privileges.",
                    "clue": "有權獲得……",
                    "answer": "to (entitled to)"
                }
            ],
            "spaced_traps": [
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
                    "trap_point": "名詞詞性判斷：a minor + [名詞]。overseer 是監工（人），oversight 才是疏忽（事物）。",
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
                }
            ],
            "part7": {
                "text_type": "Internal Policy Notice (內部政策公告)",
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
                        "analysis": "題目針對特定群體（temporary interns）。文中星號標記明確指出 interns 'are entitled to a modified subsidy of $150, provided that their application is submitted prior to November 15'，故正確選項為 (C)。"
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
                        "radar": "🔍 防漏看雷達：首句開頭細節 'completed at least six months of service'。",
                        "analysis": "第一句提及 'All permanent employees who have completed at least six months of service... are eligible for an annual health subsidy'，與 (A) 意思完全相符。"
                    }
                ]
            }
        }
    },
    2: {
        "day": 2,
        "date": "11/05",
        "phase": 1,
        "phase_name": "錯題庫清零與語感校正",
        "topic": "原因與轉折結構 ｜ proceed vs. procedure ｜ 堅持與組成",
        "morning": {
            "chunks": [
                {
                    "chunk": "proceed with caution",
                    "meaning": "謹慎繼續進行",
                    "scenario": "Engineers were advised to proceed with caution during the structural inspection.",
                    "paraphrase": "proceed = continue = go ahead",
                    "alert": "易混淆：proceed (v.) 繼續進行 vs. procedure (n.) 程序步驟！"
                },
                {
                    "chunk": "standard operating procedure",
                    "meaning": "標準作業程序 (SOP)",
                    "scenario": "Employees must adhere to the standard operating procedure when handling toxic chemicals.",
                    "paraphrase": "procedure = protocol = routine",
                    "alert": ""
                },
                {
                    "chunk": "consist of five modules",
                    "meaning": "由五個模組組成",
                    "scenario": "The executive training program consists of five rigorous modules.",
                    "paraphrase": "consist of = be composed of = comprise",
                    "alert": "必考用法：consist of 永遠沒有被動態 (is consisted of ❌)！"
                },
                {
                    "chunk": "persist in efforts",
                    "meaning": "堅持不懈地努力",
                    "scenario": "The sales team persisted in efforts despite facing severe market contraction.",
                    "paraphrase": "persist in = continue steadfastly",
                    "alert": "介系詞搭配：persist 固定接 in！"
                },
                {
                    "chunk": "insist on compliance",
                    "meaning": "堅持要求合規",
                    "scenario": "The safety auditor insisted on immediate compliance with environmental standards.",
                    "paraphrase": "insist on = demand firmly",
                    "alert": "介系詞搭配：insist 固定接 on！"
                },
                {
                    "chunk": "prior to departure",
                    "meaning": "在出發之前",
                    "scenario": "All travelers must submit visa documentation prior to departure.",
                    "paraphrase": "prior to = before = ahead of",
                    "alert": "視覺錨點：prior to 是介系詞片語，後接名詞或 V-ing！"
                },
                {
                    "chunk": "delegate tasks capably",
                    "meaning": "幹練地委派任務",
                    "scenario": "A great supervisor knows how to delegate tasks capably to team members.",
                    "paraphrase": "delegate = assign = entrust; capably = skillfully",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "原因詞：because vs. owing to 秒殺",
                "rule_1": "👀 空格後為【S + V (完整句子)】➔ 選 because / since / as",
                "rule_2": "👀 空格後為【名詞 / 代名詞】➔ 選 owing to / due to / on account of / because of",
                "golden_rule": "⚡ 教練金句：看到 owing to 後面有逗號沒動詞，千萬不要選 because！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "The flight to Chicago was postponed ________ severe inclement weather across the Midwest.",
                    "options": {
                        "A": "because",
                        "B": "owing to",
                        "C": "since",
                        "D": "as"
                    },
                    "answer": "B",
                    "analysis": "空格後為 'severe inclement weather'（名詞片語），沒有任何動詞，屬於介系詞受詞，故選介系詞片語 (B) owing to。(A)、(C)、(D) 皆為從屬連接詞，後需接完整子句。",
                    "translation": "由於中西部遭遇嚴重惡劣天氣，飛往芝加哥的航班已被延誤。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "Please review the updated safety ________ before operating the factory machinery.",
                    "options": {
                        "A": "proceed",
                        "B": "procedure",
                        "C": "proceedings",
                        "D": "procedural"
                    },
                    "answer": "B",
                    "analysis": "空格前為形容詞 'safety'，受詞位置需名詞。此處指『安全規程 / 程序』，選 (B) procedure。(A) proceed 為動詞；(D) procedural 為形容詞。",
                    "translation": "在操作工廠機械之前，請先檢閱最新的安全程序。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "The steering committee ________ seven senior department heads and two external advisors.",
                    "options": {
                        "A": "consists of",
                        "B": "is consisted of",
                        "C": "persists in",
                        "D": "insists on"
                    },
                    "answer": "A",
                    "analysis": "consist of（由……組成）為不及物動詞片語，絕對沒有被動態，排除 (B)。語意為委員會由數名主管組成，故選 (A)。(C) persist in 堅持；(D) insist on 堅持要求。",
                    "translation": "指導委員會由七位資深部門主管及兩位外部顧問組成。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "The committee consists ________ [介系詞] five voting members.",
                    "clue": "由……組成",
                    "answer": "of (consist of)"
                },
                {
                    "prompt": "Management insists ________ [介系詞] absolute punctuality.",
                    "clue": "堅持要求",
                    "answer": "on (insist on)"
                },
                {
                    "prompt": "The research team persisted ________ [介系詞] their clinical trials.",
                    "clue": "執著堅持於",
                    "answer": "in (persist in)"
                },
                {
                    "prompt": "All travel vouchers must be signed prior ________ [介系詞] booking.",
                    "clue": "在……之前",
                    "answer": "to (prior to)"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "The production team will ________ with the original rollout timeline once the client gives approval.",
                    "options": {
                        "A": "procedure",
                        "B": "proceed",
                        "C": "process",
                        "D": "proceeding"
                    },
                    "answer": "B",
                    "trap_point": "助動詞 will + 原形動詞。易誤選名詞 procedure。",
                    "analysis": "will 後接原形動詞，且搭配 with，表達『繼續進行』，選 (B) proceed。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "________ the negotiations were difficult, the union representatives eventually reached an agreement.",
                    "options": {
                        "A": "In spite of",
                        "B": "Although",
                        "C": "Owing to",
                        "D": "Regardless"
                    },
                    "answer": "B",
                    "trap_point": "Day 1 錨點間隔複習：看後面有沒有動詞！",
                    "analysis": "空格後為 'the negotiations were difficult'（主詞 + were 動詞），有動詞秒選連接詞 (B) Although！"
                }
            ],
            "part7": {
                "text_type": "Executive Memorandum (主管備忘錄)",
                "title": "Facility Upgrade and Lab Maintenance",
                "content": "To: All Research Associates\nFrom: Facilities Director\nDate: November 5\n\nRoutine laboratory maintenance is scheduled to take place between November 10 and November 12. Personnel may proceed with regular office activities; however, cleanroom 3B will remain strictly off-limits owing to ventilation repairs. \n\n*Important: Any project requiring chemical testing must be held off until Monday, November 15, unless prior written authorization has been granted by Dr. Sandra Bullock.",
                "questions": [
                    {
                        "question": "Why is Cleanroom 3B unavailable?",
                        "options": {
                            "A": "Due to scheduled ventilation repairs.",
                            "B": "Because of annual inventory auditing.",
                            "C": "Owing to chemical contamination.",
                            "D": "To prepare for an executive visit."
                        },
                        "answer": "A",
                        "radar": "🔍 防漏看雷達：抓住原因連接結構 'owing to ventilation repairs'！",
                        "analysis": "文中第二句結尾明確寫道 'cleanroom 3B will remain strictly off-limits owing to ventilation repairs'，故選 (A)。"
                    },
                    {
                        "question": "Under what condition may chemical testing continue before November 15?",
                        "options": {
                            "A": "If the test is completed in Cleanroom 3B.",
                            "B": "With written approval from Dr. Sandra Bullock.",
                            "C": "Provided that it takes place before November 10.",
                            "D": "If an extra safety technician is present."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：除外條款 'unless prior written authorization has been granted by Dr. Sandra Bullock'！",
                        "analysis": "文末星號強調測試必須延後，'unless prior written authorization has been granted by Dr. Sandra Bullock'（除非取得書面核准），故選 (B)。"
                    }
                ]
            }
        }
    },
    3: {
        "day": 3,
        "date": "11/06",
        "phase": 1,
        "phase_name": "錯題庫清零與語感校正",
        "topic": "條件假設連接詞 ｜ intent vs. intention ｜ 評估與顧問",
        "morning": {
            "chunks": [
                {
                    "chunk": "letter of intent",
                    "meaning": "意向書 (LOI)",
                    "scenario": "Both firms signed a letter of intent to finalize the cross-border merger.",
                    "paraphrase": "intent = commitment / purpose",
                    "alert": "商務固定名詞搭配：letter of intent（意向書），不可用 intention 替換！"
                },
                {
                    "chunk": "without clear intention",
                    "meaning": "缺乏明確的意圖",
                    "scenario": "Investing capital without clear intention frequently leads to poor returns.",
                    "paraphrase": "intention = objective = aim",
                    "alert": "單獨指個人意圖、打算時，通常用 intention。"
                },
                {
                    "chunk": "annual convention center",
                    "meaning": "年度大會中心",
                    "scenario": "Over 3,000 delegates will gather at the annual convention center.",
                    "paraphrase": "convention = conference = assembly",
                    "alert": "多義字：convention 可指『大型會議/年會』或『慣例/傳統』。"
                },
                {
                    "chunk": "assess the damage",
                    "meaning": "評估損失 / 災情",
                    "scenario": "Insurance adjusters arrived early to assess the damage caused by the storm.",
                    "paraphrase": "assess = evaluate = appraise = gauge",
                    "alert": ""
                },
                {
                    "chunk": "evaluate market potential",
                    "meaning": "評估市場潛力",
                    "scenario": "The consulting firm will evaluate market potential before greenlighting the launch.",
                    "paraphrase": "evaluate = estimate = analyze",
                    "alert": ""
                },
                {
                    "chunk": "in the event that",
                    "meaning": "萬一 / 如果發生……",
                    "scenario": "In the event that the server crashes, backup generators will activate instantly.",
                    "paraphrase": "in the event that = if = in case",
                    "alert": "視覺錨點：in the event that 後接完整句子 S+V；in the event of 後接名詞！"
                },
                {
                    "chunk": "provided that terms are met",
                    "meaning": "只要符合條件",
                    "scenario": "The contract will be renewed provided that terms are met satisfactorily.",
                    "paraphrase": "provided that = as long as = on condition that",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "條件句三劍客：that 尾巴 vs. of 尾巴",
                "rule_1": "👀 看到 in the event that / provided that / given that ➔ 後面必接【完整句子 (S+V)】",
                "rule_2": "👀 看到 in the event of / in case of ➔ 後面必接【名詞片語 / V-ing】",
                "golden_rule": "⚡ 教練金句：字尾帶 that 接句子，字尾帶 of 接名詞！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "The manufacturer will replace defective parts free of charge ________ the warranty claim is filed within one year.",
                    "options": {
                        "A": "provided that",
                        "B": "in the event of",
                        "C": "regardless",
                        "D": "in spite of"
                    },
                    "answer": "A",
                    "analysis": "空格後為 'the warranty claim is filed'（主詞 + 被動動詞），為完整子句，故選連接詞 (A) provided that（只要 / 在……條件下）。(B) 與 (D) 為介系詞片語，只能接名詞。",
                    "translation": "只要保固申請在一年內提出，製造商將免費更換瑕疵零件。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "The CEO signed a formal letter of ________ outlining the preliminary purchase price.",
                    "options": {
                        "A": "intend",
                        "B": "intent",
                        "C": "intentionally",
                        "D": "intended"
                    },
                    "answer": "B",
                    "analysis": "商務固定語塊秒殺：letter of intent（意向書）。(A) 為動詞；(C) 為副詞；(D) 為過去分詞。",
                    "translation": "執行長簽署了一份正式意向書，概述初步收購價格。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "Before finalizing the budget, the financial director hired an independent analyst to ________ recent revenue projections.",
                    "options": {
                        "A": "advise",
                        "B": "evaluate",
                        "C": "persist",
                        "D": "oversee"
                    },
                    "answer": "B",
                    "analysis": "空格後接名詞 'recent revenue projections'（營收預測）。evaluate projections 指『評估預測數值』，語意最精準。advise 後接人（建議某人）；persist 接 in。",
                    "translation": "在敲定預算之前，財務總監聘請了一位獨立分析師來評估近期的營收預估。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "Both parties signed a letter of ________ [意向書].",
                    "clue": "名詞，4 個字母",
                    "answer": "intent (letter of intent)"
                },
                {
                    "prompt": "________ [只要] terms are accepted, production will start tomorrow.",
                    "clue": "p 開頭的條件連接詞",
                    "answer": "Provided that (or Providing that)"
                },
                {
                    "prompt": "The claim will be processed in the event ________ [介系詞] rain.",
                    "clue": "in the event 後接名詞之介系詞",
                    "answer": "of (in the event of)"
                },
                {
                    "prompt": "Independent experts were hired to ________ [評估] the facility's safety.",
                    "clue": "e 或 a 開頭的動詞",
                    "answer": "evaluate / assess"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "In the event ________ an emergency system failure, technicians must notify the operations director immediately.",
                    "options": {
                        "A": "that",
                        "B": "of",
                        "C": "to",
                        "D": "as"
                    },
                    "answer": "B",
                    "trap_point": "看空格後有沒有動詞！後方為 'an emergency system failure'（純名詞）。",
                    "analysis": "後面純名詞片語，沒有任何動詞，故選介系詞片語 in the event of。若選 that，後面必須有動詞。"
                },
                {
                    "id": 2,
                    "question": "The newly released handheld device is highly ________ with standard USB-C peripherals.",
                    "options": {
                        "A": "compatible",
                        "B": "eligible",
                        "C": "exempted",
                        "D": "proficient"
                    },
                    "answer": "A",
                    "trap_point": "Day 1 語塊重現：看到 with 秒答！",
                    "analysis": "compatible with（相容於）。eligible 搭配 for；exempted 搭配 from；proficient 搭配 in。"
                }
            ],
            "part7": {
                "text_type": "Vendor Service Agreement Excerpt (供應商協議摘要)",
                "title": "Equipment Lease Terms and Cancellation Policy",
                "content": "Apex Catering agrees to provide commercial kitchen appliances for the duration of the international food convention. In the event that equipment malfunction occurs through no fault of the lessee, replacement units will be dispatched within three hours.\n\n*Cancellation Notice: The lessee may terminate this contract without penalty provided that written notice is submitted at least 48 hours prior to the event commencement date. Cancellations made after this threshold are subject to a mandatory 25% restocking surcharge.",
                "questions": [
                    {
                        "question": "What happens if leased kitchen machinery fails due to non-operator error?",
                        "options": {
                            "A": "A replacement is delivered within three hours.",
                            "B": "The contract is canceled with a full refund.",
                            "C": "Apex Catering sends a technician the next morning.",
                            "D": "The lessee must pay a 25% restocking penalty."
                        },
                        "answer": "A",
                        "radar": "🔍 防漏看雷達：定位到 'equipment malfunction occurs through no fault of the lessee' ➔ 'replacement units will be dispatched within three hours'！",
                        "analysis": "首段第二句清楚說明：若非承租人之過失發生故障，替代設備將在 3 小時內送達，故選 (A)。"
                    },
                    {
                        "question": "When can a lessee cancel the agreement without incurring any fees?",
                        "options": {
                            "A": "Within 24 hours of convention conclusion.",
                            "B": "At least 48 hours before the event begins.",
                            "C": "In the event that attendance is low.",
                            "D": "Whenever written approval is signed by the council."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：小字免責細節 'without penalty provided that written notice is submitted at least 48 hours prior to the event commencement date'！",
                        "analysis": "文中星號標記處指出免罰金條件為 'at least 48 hours prior to the event commencement date'，故選 (B)。"
                    }
                ]
            }
        }
    },
    4: {
        "day": 4,
        "date": "11/07",
        "phase": 1,
        "phase_name": "錯題庫清零與語感校正",
        "topic": "分詞修飾名詞 (V-ing vs V-ed) ｜ 召回、庫存與保險範圍",
        "morning": {
            "chunks": [
                {
                    "chunk": "extensive media coverage",
                    "meaning": "廣泛的媒體報導",
                    "scenario": "The tech summit received extensive media coverage across North America.",
                    "paraphrase": "coverage = reporting = broadcast; 多義字：coverage 亦指『保險理賠範圍』！",
                    "alert": ""
                },
                {
                    "chunk": "recall faulty appliances",
                    "meaning": "召回故障家電",
                    "scenario": "The distributor decided to recall faulty appliances to avoid legal liability.",
                    "paraphrase": "recall = withdraw = call back; faulty = defective",
                    "alert": ""
                },
                {
                    "chunk": "under warranty conditions",
                    "meaning": "在保固條件限制下",
                    "scenario": "Repairs are conducted free of charge under warranty conditions.",
                    "paraphrase": "conditions = terms = stipulations",
                    "alert": ""
                },
                {
                    "chunk": "keep items in stock",
                    "meaning": "備有現貨庫存",
                    "scenario": "The warehouse strives to keep high-demand merchandise in stock.",
                    "paraphrase": "in stock = available = on hand",
                    "alert": ""
                },
                {
                    "chunk": "conduct an investigation",
                    "meaning": "執行內部調查",
                    "scenario": "The compliance division was authorized to conduct an investigation into the leak.",
                    "paraphrase": "conduct = carry out = perform = execute",
                    "alert": ""
                },
                {
                    "chunk": "promote brand awareness",
                    "meaning": "提昇品牌知名度",
                    "scenario": "Digital campaigns were launched to promote brand awareness among young professionals.",
                    "paraphrase": "promote = boost = enhance; 多義字：promote 亦指『升遷 / 提拔』！",
                    "alert": ""
                },
                {
                    "chunk": "promising prospective clients",
                    "meaning": "有潛力的潛在客戶",
                    "scenario": "The sales representative scheduled meetings with several promising prospective clients.",
                    "paraphrase": "prospective = potential = future; promising = favorable",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "分詞當形容詞：看被修飾名詞是「主動發出」還是「被動承受」",
                "rule_1": "👀 名詞自己能做動作 ➔ 選 V-ing（demanding job 費力的工作, promising future 有前途的未來）",
                "rule_2": "👀 名詞是被做的 / 承受動作 ➔ 選 V-ed（damaged goods 受損貨品, revised contract 修改後的合約）",
                "golden_rule": "⚡ 教練金句：主動發光選 -ing，被動受傷選 -ed！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "The quality assurance department decided to recall all ________ toasters manufactured last month.",
                    "options": {
                        "A": "faulty",
                        "B": "fault",
                        "C": "faultless",
                        "D": "faultiness"
                    },
                    "answer": "A",
                    "analysis": "修飾名詞 toasters（烤麵包機）需形容詞，faulty 表示『有瑕疵的 / 故障的』，為多益極高頻單字。fault 為名詞；faultless 為無瑕疵的。",
                    "translation": "品保部門決定召回上個月製造的所有故障烤麵包機。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "Customers should note that the replacement policy only applies to goods ________ in their original packaging.",
                    "options": {
                        "A": "return",
                        "B": "returned",
                        "C": "returning",
                        "D": "returns"
                    },
                    "answer": "B",
                    "analysis": "修飾名詞 'goods'（貨物），貨物是被顧客退回的（承受動作），使用過去分詞 (B) returned 當後位修飾語（減化自 which are returned）。",
                    "translation": "顧客請注意，換貨政策僅適用於以原始包裝退回的商品。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "The newly hired PR consultant will ________ a comprehensive study to evaluate user engagement.",
                    "options": {
                        "A": "conduct",
                        "B": "persist",
                        "C": "insist",
                        "D": "consist"
                    },
                    "answer": "A",
                    "analysis": "搭配受詞 'a comprehensive study'（全面性研究），conduct a study / survey 為絕對必考商務語塊！persist/insist/consist 後皆須接介系詞才能帶受詞。",
                    "translation": "新聘請的公關顧問將執行一項全面研究，以評估使用者的參與度。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "The company issued a notice to ________ [召回] the defective vehicle.",
                    "clue": "動詞，r 開頭",
                    "answer": "recall (recall the vehicle)"
                },
                {
                    "prompt": "The magazine provided in-depth ________ [報導/範疇] of the merger.",
                    "clue": "c 開頭名詞，亦可指保險理賠",
                    "answer": "coverage (in-depth coverage)"
                },
                {
                    "prompt": "The warranty only covers products ________ [用原包裝退回] by users.",
                    "clue": "分詞修飾，被退回",
                    "answer": "returned (goods returned)"
                },
                {
                    "prompt": "Our primary objective is to ________ [執行] a rigorous market audit.",
                    "clue": "c 開頭動詞，帶出 study 或 audit",
                    "answer": "conduct (conduct an audit)"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "________ the client requested several amendments, the legal counsel finalized the agreement within two hours.",
                    "options": {
                        "A": "In spite of",
                        "B": "Because of",
                        "C": "Even if",
                        "D": "Owing to"
                    },
                    "answer": "C",
                    "trap_point": "後方有動詞 'requested'，秒殺介系詞 (A), (B), (D)！",
                    "analysis": "空格後為 'the client requested'（主詞 + 動詞），介系詞片語通通淘汰，秒選從屬連接詞 (C) Even if。"
                },
                {
                    "id": 2,
                    "question": "The sales team met with a group of ________ investors who showed interest in the sustainable energy project.",
                    "options": {
                        "A": "prospect",
                        "B": "prospective",
                        "C": "prospectus",
                        "D": "prospectively"
                    },
                    "answer": "B",
                    "trap_point": "修飾名詞 investors 需要形容詞。",
                    "analysis": "prospective 為形容詞，意指『有前途的 / 預期的 / 潛在的』。prospective investors = potential investors。"
                }
            ],
            "part7": {
                "text_type": "Product Recall & Safety Bulletin (商品召回安全公告)",
                "title": "Voluntary Recall Notice: SmartChef Kitchen Appliance Series 400",
                "content": "Dear Valued Customer,\n\nIn cooperation with the Consumer Protection Commission, HomeVibe Technologies is voluntarily initiating a recall of all Series 400 blenders sold between May and September. An internal inspection revealed that a faulty motor seal may cause unexpected overheating under continuous operation.\n\nCustomers in possession of an affected model are entitled to a complimentary replacement unit or a full refund. \n\n*Important Condition: Proof of purchase is required solely for customers seeking monetary refunds. Free product replacements will be honored immediately upon handing in the defective blender at any authorized retailer, regardless of receipt status.",
                "questions": [
                    {
                        "question": "What prompted HomeVibe Technologies to announce the recall?",
                        "options": {
                            "A": "A decline in overall sales figures.",
                            "B": "A potential motor overheating hazard.",
                            "C": "Changes in local environmental laws.",
                            "D": "Inability to keep replacement parts in stock."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：原因句定位 'revealed that a faulty motor seal may cause unexpected overheating'！",
                        "analysis": "公告說明召回原因為內部檢查發現瑕疵馬達密封可能導致在連續運轉下異常過熱（overheating），故選 (B)。"
                    },
                    {
                        "question": "Who must present a proof of purchase?",
                        "options": {
                            "A": "Anyone bringing a blender to an authorized retailer.",
                            "B": "Customers requesting a cash refund.",
                            "C": "Consumers seeking a complimentary replacement.",
                            "D": "Users who purchased the blender after September."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：星號附註細節 'Proof of purchase is required solely for customers seeking monetary refunds'！solely ＝ 僅限！",
                        "analysis": "文末標註強調只有尋求退款者（seeking monetary refunds）才需要購買證明；更換新機者即使沒發票也能直接換，故選 (B)。"
                    }
                ]
            }
        }
    },
    5: {
        "day": 5,
        "date": "11/08",
        "phase": 1,
        "phase_name": "錯題庫清零與語感校正",
        "topic": "減化子句與分詞構句 (while + V-ing) ｜ 政策規範與熟練搭配",
        "morning": {
            "chunks": [
                {
                    "chunk": "proficient in Mandarin",
                    "meaning": "精通中文",
                    "scenario": "Candidates proficient in Mandarin and English are preferred for the regional role.",
                    "paraphrase": "proficient in = skilled in = fluent in",
                    "alert": "必考介系詞：proficient 後方固定搭配 in！"
                },
                {
                    "chunk": "accustomed to changes",
                    "meaning": "習慣於各種變動",
                    "scenario": "Staff members quickly became accustomed to changes in remote work guidelines.",
                    "paraphrase": "accustomed to = used to",
                    "alert": "注意：be accustomed to 後方的 to 是介系詞，接名詞或 V-ing！"
                },
                {
                    "chunk": "resistant to heat",
                    "meaning": "耐熱的 / 抗熱的",
                    "scenario": "The new kitchen apron is made of synthetic fibers highly resistant to heat.",
                    "paraphrase": "resistant to = impervious to",
                    "alert": "介系詞搭配：resistant 固定接 to！"
                },
                {
                    "chunk": "vulnerable to attacks",
                    "meaning": "易遭受攻擊",
                    "scenario": "Unpatched database servers are vulnerable to cyber attacks.",
                    "paraphrase": "vulnerable to = susceptible to = exposed to",
                    "alert": "介系詞搭配：vulnerable 固定接 to！"
                },
                {
                    "chunk": "pertinent to the case",
                    "meaning": "與本案直接相關",
                    "scenario": "Please disclose all files pertinent to the ongoing patent dispute.",
                    "paraphrase": "pertinent to = relevant to = related to",
                    "alert": "介系詞搭配：pertinent 固定接 to！"
                },
                {
                    "chunk": "government mandate",
                    "meaning": "政府的強制命令",
                    "scenario": "The factory complied strictly with the government mandate on emission limits.",
                    "paraphrase": "mandate = directive = order = regulation",
                    "alert": "多義字：mandate 可作名詞（授權/指令）亦可作動詞（強制規定）。"
                },
                {
                    "chunk": "a deliberate attempt",
                    "meaning": "一項蓄意/深思熟慮的企圖",
                    "scenario": "The firm made a deliberate attempt to capture market share in rural regions.",
                    "paraphrase": "deliberate = intentional = calculated",
                    "alert": "多義字：deliberate (adj.) 蓄意的/審慎的；(v.) 仔細考慮/研議。"
                }
            ],
            "visual_anchor": {
                "title": "看到 while / when / once 後面直接接分詞？",
                "rule_1": "👀 主詞主動做動作 ➔ while + V-ing（while reviewing the file, she found a typo）",
                "rule_2": "👀 主詞被動被處理 ➔ once / when + V-ed（once approved, the budget will be released）",
                "golden_rule": "⚡ 教練金句：看到 while 接空格帶受詞，90% 秒選 -ing！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "While ________ the quarterly balance sheets, the internal auditor discovered an unaccounted variance.",
                    "options": {
                        "A": "examine",
                        "B": "examining",
                        "C": "examined",
                        "D": "examination"
                    },
                    "answer": "B",
                    "analysis": "分詞構句減化考點：while 後方省略了主詞 the auditor，稽核員主動檢視報表並帶出受詞 'the quarterly balance sheets'，故使用現在分詞 (B) examining。",
                    "translation": "在審查季度資產負債表時，內部稽核員發現了一筆未入帳的差額。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "Applicants must be fully proficient ________ data analysis tools, including SQL and Python.",
                    "options": {
                        "A": "at",
                        "B": "in",
                        "C": "with",
                        "D": "for"
                    },
                    "answer": "B",
                    "analysis": "介系詞秒殺搭配：be proficient in + 領域/語言/技能。故選 (B) in。",
                    "translation": "應徵者必須完全精通數據分析工具，包含 SQL 與 Python。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "Documents ________ to the upcoming merger must be archived in a password-protected directory.",
                    "options": {
                        "A": "pertinent",
                        "B": "pertinence",
                        "C": "pertinently",
                        "D": "pertinency"
                    },
                    "answer": "A",
                    "analysis": "修飾名詞 Documents 的後位形容詞片語：[Documents that are] pertinent to the merger。pertinent 為形容詞，搭配 to 表『相關的』。",
                    "translation": "與即將進行的併購案相關的文件必須封存在受密碼保護的資料夾中。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "She is remarkably proficient ________ [介系詞] digital marketing.",
                    "clue": "精通於……",
                    "answer": "in (proficient in)"
                },
                {
                    "prompt": "Senior executives are accustomed ________ [介系詞] frequent travel.",
                    "clue": "習慣於……",
                    "answer": "to (accustomed to)"
                },
                {
                    "prompt": "Please supply all papers pertinent ________ [介系詞] the inquiry.",
                    "clue": "與……相關",
                    "answer": "to (pertinent to)"
                },
                {
                    "prompt": "The fabric is specially treated to be resistant ________ [介系詞] moisture.",
                    "clue": "抗……的 / 耐……的",
                    "answer": "to (resistant to)"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "Once ________ by the executive council, the proposed dress code policy will take effect next Monday.",
                    "options": {
                        "A": "ratifying",
                        "B": "ratified",
                        "C": "ratify",
                        "D": "ratification"
                    },
                    "answer": "B",
                    "trap_point": "主詞是 policy（政策），政策是被 council 批准的，選被動分詞 V-ed！",
                    "analysis": "分詞構句減化：政策被理事會核准，once [it is] ratified，主被動判斷選 (B) ratified。"
                },
                {
                    "id": 2,
                    "question": "The contractor insisted ________ using top-grade steel for the exterior framing.",
                    "options": {
                        "A": "on",
                        "B": "in",
                        "C": "to",
                        "D": "at"
                    },
                    "answer": "A",
                    "trap_point": "Day 2 語塊複習：insist on vs persist in！",
                    "analysis": "insist 後接 on；persist 才接 in。故選 (A) on。"
                }
            ],
            "part7": {
                "text_type": "IT Security Protocol Memo (資訊安全規章備忘錄)",
                "title": "Corporate Network Vulnerability and Access Mandate",
                "content": "To: All Department Personnel\nFrom: Information Security Directorate\nDate: November 8\n\nRecent diagnostics indicate that our legacy database systems have become increasingly vulnerable to external intrusion. In accordance with the newly passed cybersecurity mandate, all staff members must transition to two-factor authentication (2FA) by this Friday at 5:00 PM.\n\n*Important Exception: Employees who are currently stationed abroad on corporate assignments are exempted from the Friday deadline, provided that they submit an official extension query via the IT helpdesk before departure.",
                "questions": [
                    {
                        "question": "What is the primary reason for mandating two-factor authentication?",
                        "options": {
                            "A": "To upgrade employee laptop hardware.",
                            "B": "Because legacy systems are susceptible to intrusions.",
                            "C": "To comply with international travel regulations.",
                            "D": "Due to a recent budget reduction in IT operations."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：同義字替換 vulnerable to external intrusion ＝ susceptible to intrusions！",
                        "analysis": "文中第二句指出 'legacy database systems have become increasingly vulnerable to external intrusion'，susceptible 為 vulnerable 的同義字，故選 (B)。"
                    },
                    {
                        "question": "Who can postpone setting up two-factor authentication past Friday?",
                        "options": {
                            "A": "Contract workers hired on a temporary basis.",
                            "B": "Staff working abroad who filed an extension query.",
                            "C": "All personnel in the Information Security Directorate.",
                            "D": "Employees who undergo IT training next week."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：星號附註條件 'stationed abroad... exempted from the Friday deadline, provided that they submit an official extension query'！",
                        "analysis": "末尾星號清楚規定外派員工若事前提出展延申請即可免除週五死線，故選 (B)。"
                    }
                ]
            }
        }
    }
}
