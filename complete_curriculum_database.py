# -*- coding: utf-8 -*-
"""
Generates master curriculum database for Days 13 to 25.
Imports DAYS_DATA from curriculum_data and build_full_curriculum,
adds remaining days, and saves to master_curriculum.json.
"""

from curriculum_data import DAYS_DATA
from build_full_curriculum import DAYS_11_TO_25
import json

DAYS_DATA.update(DAYS_11_TO_25)

MORE_DAYS = {
    13: {
        "day": 13,
        "date": "11/16",
        "phase": 2,
        "phase_name": "860 金色證書進階擴充與同義字轉換",
        "topic": "條件讓步結構 (even if vs as though) ｜ 強化、專屬與高層決策",
        "morning": {
            "chunks": [
                {
                    "chunk": "enhance product quality",
                    "meaning": "強化產品質感與品質",
                    "scenario": "R&D engineers adopted new polymers to enhance product quality.",
                    "paraphrase": "enhance = improve = upgrade",
                    "alert": ""
                },
                {
                    "chunk": "exclusive distribution rights",
                    "meaning": "獨家經銷權",
                    "scenario": "The retail group secured exclusive distribution rights across Asia.",
                    "paraphrase": "exclusive = sole = unique",
                    "alert": ""
                },
                {
                    "chunk": "executive committee meeting",
                    "meaning": "高階主管執行委員會議",
                    "scenario": "The quarterly financial forecast was presented during the executive committee meeting.",
                    "paraphrase": "executive = senior leadership = managerial",
                    "alert": ""
                },
                {
                    "chunk": "request a deadline extension",
                    "meaning": "申請延後繳交期限",
                    "scenario": "The project lead submitted a memo to request a deadline extension.",
                    "paraphrase": "extension = postponement = prolongation",
                    "alert": "多義字：extension (n.) 延期；分機號碼！"
                },
                {
                    "chunk": "inspect the exterior wall",
                    "meaning": "檢查建築物外牆",
                    "scenario": "Safety inspectors were dispatched to inspect the exterior wall for micro-cracks.",
                    "paraphrase": "exterior = outer = outside",
                    "alert": ""
                },
                {
                    "chunk": "formerly known as",
                    "meaning": "前身為 / 昔日稱作",
                    "scenario": "Apex Energy, formerly known as PowerCorp, rebranded its commercial operations.",
                    "paraphrase": "formerly = previously = earlier",
                    "alert": ""
                },
                {
                    "chunk": "even if sales drop",
                    "meaning": "即使銷售量下滑",
                    "scenario": "The CEO affirmed dividend payouts even if sales drop in the final quarter.",
                    "paraphrase": "even if = even though = despite the possibility that",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "甚至如果 vs. 宛如彷彿：even if vs. as though",
                "rule_1": "👀 看到表達「縱使 / 哪怕某事發生」➔ 選 even if（從屬連接詞，後接真實假設句）",
                "rule_2": "👀 看到表達「看起來彷彿 / 好像是…」➔ 選 as though / as if（通常搭配 look / seem / behave）",
                "golden_rule": "⚡ 教練金句：有退讓意味選 even if，看動作神態選 as though！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "The contractor will complete the exterior facade on schedule ________ heavy rain continues tomorrow.",
                    "options": {
                        "A": "even if",
                        "B": "as though",
                        "C": "in spite of",
                        "D": "instead"
                    },
                    "answer": "A",
                    "analysis": "空格後為 'heavy rain continues tomorrow'（S+V 完整子句），句意表達『即使明天持續暴雨，也會如期完工』，選讓步連接詞 (A) even if。(B) as though 彷彿；(C) in spite of 為介系詞後不能接子句；(D) instead 為副詞。",
                    "translation": "即使明天暴雨持續，承包商仍將如期完成外牆施工。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "Members of the VIP rewards program enjoy ________ access to the rooftop business lounge.",
                    "options": {
                        "A": "exclude",
                        "B": "exclusive",
                        "C": "exclusively",
                        "D": "exclusion"
                    },
                    "answer": "B",
                    "analysis": "修飾名詞 access（使用權/通行權）需用形容詞，exclusive access 表『專屬/獨享的使用權』。故選 (B)。",
                    "translation": "貴賓尊爵會員享有頂樓商務休息室的獨家使用權。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "The technology giant, ________ known as DataMatrix, announced a global brand consolidation.",
                    "options": {
                        "A": "formal",
                        "B": "formally",
                        "C": "formerly",
                        "D": "formation"
                    },
                    "answer": "C",
                    "analysis": "修飾過去分詞 known，表示『過去/以前被稱作』，需用時間副詞 (C) formerly（以前 / 從前）。(B) formally 表正式地，語意不合。",
                    "translation": "這家昔日名為 DataMatrix 的科技巨頭宣布了全球品牌整合計畫。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "The luxury club offers ________ [獨家的/專屬的] perks to members.",
                    "clue": "e 開頭形容詞",
                    "answer": "exclusive"
                },
                {
                    "prompt": "The hotel was ________ [以前/昔日] a historic postal office.",
                    "clue": "f 開頭副詞，表示先前",
                    "answer": "formerly"
                },
                {
                    "prompt": "She requested a two-week ________ [延期] on her research thesis.",
                    "clue": "e 開頭名詞，延長延期",
                    "answer": "extension"
                },
                {
                    "prompt": "The building's ________ [外側的/外部的] walls were repainted.",
                    "clue": "e 開頭形容詞，外部的",
                    "answer": "exterior"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "He spoke ________ he were personally familiar with the company's financial books.",
                    "options": {
                        "A": "even if",
                        "B": "as though",
                        "C": "in case",
                        "D": "unless"
                    },
                    "answer": "B",
                    "trap_point": "看到 spoke + he were（虛擬語氣彷彿…）！",
                    "analysis": "動詞 spoke 搭配虛擬語氣 he were，表示『彷彿、宛如他親自熟稔財務帳冊一樣』，選 (B) as though。"
                },
                {
                    "id": 2,
                    "question": "Please dial ________ 402 if you require technical assistance after office hours.",
                    "options": {
                        "A": "extension",
                        "B": "extend",
                        "C": "extensive",
                        "D": "extensively"
                    },
                    "answer": "A",
                    "trap_point": "dial extension + 號碼（撥打分機）。",
                    "analysis": "extension 402 指 402 號分機，名詞搭配選 (A)。"
                }
            ],
            "part7": {
                "text_type": "Executive Real Estate Advisory (高階商用不動產公告)",
                "title": "Lease Renewal and Facade Refurbishment Schedule",
                "content": "To: Corporate Office Tenants\nFrom: Plaza Property Management\nDate: November 16\n\nManagement has contracted StoneCraft Ltd. to conduct structural waterproofing on the building's exterior facade between November 22 and December 5. All elevator banks will remain accessible; however, window washing will be suspended throughout the period.\n\n*Lease Extension Notice: Tenants seeking to renew their multi-year lease agreements prior to December 1 will receive exclusive access to reserved basement parking at no additional increment.",
                "questions": [
                    {
                        "question": "What maintenance work is scheduled to begin on November 22?",
                        "options": {
                            "A": "Elevator mechanical upgrades.",
                            "B": "Exterior waterproofing repairs.",
                            "C": "Replacement of office carpet tiles.",
                            "D": "Basement parking repaving."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：抓住第一段第一句 'conduct structural waterproofing on the building's exterior facade'！",
                        "analysis": "文中明確寫道 11 月 22 日展開的工程為外牆防水結構施工（exterior waterproofing repairs），故選 (B)。"
                    },
                    {
                        "question": "How can commercial tenants obtain free reserved basement parking?",
                        "options": {
                            "A": "By filing an official noise grievance.",
                            "B": "By renewing their commercial lease before December 1.",
                            "C": "By paying a one-time maintenance increment.",
                            "D": "By relocating to the top floor suites."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：星號附註條件 'Tenants seeking to renew their multi-year lease agreements prior to December 1'！",
                        "analysis": "末尾重要通知清楚指名：在 12 月 1 日前續約的房客享有專屬地下室停車位且免加收費用，故選 (B)。"
                    }
                ]
            }
        }
    },
    14: {
        "day": 14,
        "date": "11/17",
        "phase": 2,
        "phase_name": "860 金色證書進階擴充與同義字轉換",
        "topic": "關係子句簡化 ｜ 履行承諾、加盟與迫切情勢",
        "morning": {
            "chunks": [
                {
                    "chunk": "fulfill customer orders",
                    "meaning": "履行並完成客戶訂單",
                    "scenario": "The automated center works around the clock to fulfill customer orders on time.",
                    "paraphrase": "fulfill = complete = satisfy = carry out",
                    "alert": ""
                },
                {
                    "chunk": "open a new franchise",
                    "meaning": "開設一家新的加盟特許店",
                    "scenario": "The restaurateur secured capital to open a new franchise in Manchester.",
                    "paraphrase": "franchise = chain branch = licensed outlet",
                    "alert": ""
                },
                {
                    "chunk": "an imminent deadline",
                    "meaning": "迫在眉睫的截止期限",
                    "scenario": "Staff members accelerated reviews due to an imminent deadline.",
                    "paraphrase": "imminent = impending = approaching = near",
                    "alert": "易混淆：imminent (adj.) 迫近的 vs. eminent (adj.) 傑出的/顯赫的！"
                },
                {
                    "chunk": "it is imperative that",
                    "meaning": "迫切必要的是……",
                    "scenario": "It is imperative that all patient records remain confidential.",
                    "paraphrase": "imperative = vital = crucial = essential",
                    "alert": "文法陷阱：It is imperative that S + (should) + [原形動詞]！"
                },
                {
                    "chunk": "salary increment",
                    "meaning": "薪資加給幅度",
                    "scenario": "High-performing engineers are awarded an annual salary increment.",
                    "paraphrase": "increment = increase = addition = raise",
                    "alert": ""
                },
                {
                    "chunk": "manufacture cotton garments",
                    "meaning": "製造棉質服飾成品",
                    "scenario": "The textile plant specializes in manufacturing cotton garments for export.",
                    "paraphrase": "garments = apparel = clothing",
                    "alert": ""
                },
                {
                    "chunk": "indeed a success",
                    "meaning": "確實非常成功",
                    "scenario": "The inaugural tech showcase was indeed a success by all measures.",
                    "paraphrase": "indeed = truly = certainly",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "It is imperative that ➔ 後面動詞秒選「原形」！",
                "rule_1": "👀 看到 imperative / essential / crucial / mandatory / important + that 子句 ➔ 動詞一律「原形」！",
                "rule_2": "👀 哪怕主詞是單數 he / the manager，動詞也不加 s，不變過去式！（省略了 should）",
                "golden_rule": "⚡ 教練金句：看到 imperative that，動詞打回原形！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "Because of severe supply chain disruptions, it is imperative that each department ________ its inventory weekly.",
                    "options": {
                        "A": "audits",
                        "B": "audit",
                        "C": "audited",
                        "D": "auditing"
                    },
                    "answer": "B",
                    "analysis": "看到 'it is imperative that + S + (should) + [原形動詞]' 假設法句型。主詞雖然是 each department，動詞仍必須使用原形 (B) audit！",
                    "translation": "由於嚴重的供應鏈中斷，各部門每週盤點庫存是極為迫切必要的。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "Due to the ________ launch of the electric vehicle, engineers worked through the weekend.",
                    "options": {
                        "A": "imminent",
                        "B": "eminent",
                        "C": "imminently",
                        "D": "eminence"
                    },
                    "answer": "A",
                    "analysis": "修飾名詞 launch（發表會）需用形容詞。imminent 表示『迫在眉睫的 / 即將發生的』。eminent 意為知名卓越的，不合句意。故選 (A)。",
                    "translation": "由於電動車上市在即，工程師們整個週末都在加班。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "The newly opened logistics depot has the processing capacity to ________ over 10,000 packages daily.",
                    "options": {
                        "A": "fulfill",
                        "B": "fulfillment",
                        "C": "fulfilled",
                        "D": "fulfilling"
                    },
                    "answer": "A",
                    "analysis": "to + [原形動詞] + over 10,000 packages。fulfill 表示『完成/履行訂單或包裹寄送』。故選 (A)。",
                    "translation": "新啟用的物流轉運中心擁有每日處理並完成超過一萬件包裹寄送的產能。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "It is imperative that the supervisor ________ [出席，填原形] the briefing.",
                    "clue": "attend 的形態",
                    "answer": "attend (imperative that + 原形)"
                },
                {
                    "prompt": "Severe weather posed an ________ [迫在眉睫的] threat to navigation.",
                    "clue": "i 開頭形容詞，指即將來臨的危險",
                    "answer": "imminent"
                },
                {
                    "prompt": "Our factory manufactures high-end outdoor ________ [服飾/衣物].",
                    "clue": "g 開頭名詞複數",
                    "answer": "garments"
                },
                {
                    "prompt": "Employees received a 4% salary ________ [加薪幅度/增額] this year.",
                    "clue": "i 開頭名詞，增量增額",
                    "answer": "increment"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "The bakery chain plans to sell ten regional ________ to experienced local operators.",
                    "options": {
                        "A": "franchises",
                        "B": "franchisees",
                        "C": "franchising",
                        "D": "franchised"
                    },
                    "answer": "A",
                    "trap_point": "franchise（加盟店經營權/加盟店）vs franchisee（加盟者本人）。",
                    "analysis": "動詞 sell 十家區域加盟店，指加盟業務經營權，使用 (A) franchises。"
                },
                {
                    "id": 2,
                    "question": "The keynote speaker was indeed an ________ scholar in renewable agriculture.",
                    "options": {
                        "A": "imminent",
                        "B": "eminent",
                        "C": "imminently",
                        "D": "eminently"
                    },
                    "answer": "B",
                    "trap_point": "修飾學者 scholar 需用『傑出的/顯赫的』！",
                    "analysis": "eminent scholar（德高望重的傑出學者）。imminent 指迫近的，不能用來修飾學者身分。故選 (B)。"
                }
            ],
            "part7": {
                "text_type": "Retail Expansion Memo (零售擴展備忘錄)",
                "title": "EcoWear Garments: Regional Franchise Launch",
                "content": "To: Prospective Franchise Investors\nFrom: EcoWear Development Directorate\nDate: November 17\n\nEcoWear Garments is proud to announce franchise licensing opportunities across the Pacific Northwest. Our manufacturing partners are committed to sustainable organic fabrics, ensuring timely supply to fulfill customer demand across all regional outlets.\n\n*Mandatory Information Session: Because licensing applications are closing soon, it is imperative that prospective franchisees attend our orientation seminar on December 2. Applications submitted without attendance certification will be summarily dismissed.",
                "questions": [
                    {
                        "question": "What is EcoWear Garments offering to investors?",
                        "options": {
                            "A": "Subsidized organic cotton farming grants.",
                            "B": "Regional franchise licensing opportunities.",
                            "C": "Free garment repair workshops.",
                            "D": "Custom executive attire fittings."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：第一段第一句明確點出 'announce franchise licensing opportunities'！",
                        "analysis": "備忘錄開門見山宣佈開放加盟授權機會（franchise licensing opportunities），故選 (B)。"
                    },
                    {
                        "question": "What will happen to applications submitted without seminar attendance?",
                        "options": {
                            "A": "They will incur a $200 review penalty.",
                            "B": "They will be placed on a standby registry.",
                            "C": "They will be rejected immediately.",
                            "D": "They will require endorsement by the city council."
                        },
                        "answer": "C",
                        "radar": "🔍 防漏看雷達：星號重要細節與同義替換！'summarily dismissed' ＝ rejected immediately！",
                        "analysis": "文末星號強調沒參加研討會者其申請將會被 summarily dismissed（立刻駁回不予受理），即 rejected immediately，故選 (C)。"
                    }
                ]
            }
        }
    }
}

DAYS_DATA.update(MORE_DAYS)
print(f"Total days configured so far: {len(DAYS_DATA)}")
