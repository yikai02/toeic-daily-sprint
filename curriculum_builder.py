# -*- coding: utf-8 -*-
"""
Full 25-Day TOEIC Curriculum Data Generator
Ensures every word, phrase, and grammar trap in the user's priority error bank
is fully realized across Day 1 to Day 25.
"""

from curriculum_data import DAYS_DATA

ADDITIONAL_DAYS = {
    6: {
        "day": 6,
        "date": "11/09",
        "phase": 1,
        "phase_name": "錯題庫清零與語感校正",
        "topic": "詞性秒殺 (will + adv. + V) ｜ 職務交接與承擔",
        "morning": {
            "chunks": [
                {
                    "chunk": "in charge of logistics",
                    "meaning": "負責物流營運",
                    "scenario": "Mr. Chen was placed in charge of logistics for the Asia-Pacific territory.",
                    "paraphrase": "in charge of = responsible for = overseeing",
                    "alert": ""
                },
                {
                    "chunk": "on behalf of the committee",
                    "meaning": "代表委員會全體",
                    "scenario": "The spokesperson spoke on behalf of the committee during the press briefing.",
                    "paraphrase": "on behalf of = representing",
                    "alert": ""
                },
                {
                    "chunk": "in addition to bonuses",
                    "meaning": "除績效獎金之外（還有）",
                    "scenario": "In addition to bonuses, employees receive subsidized commuting passes.",
                    "paraphrase": "in addition to = besides = as well as",
                    "alert": "視覺錨點：in addition to 後接名詞 / V-ing，表『除了…還有…』！"
                },
                {
                    "chunk": "step down from the board",
                    "meaning": "辭去董事會職位",
                    "scenario": "The founder announced plans to step down from the board next spring.",
                    "paraphrase": "step down = resign = retire from",
                    "alert": ""
                },
                {
                    "chunk": "take over the department",
                    "meaning": "接管該部門業務",
                    "scenario": "A veteran manager will take over the department following the restructuring.",
                    "paraphrase": "take over = assume control of",
                    "alert": ""
                },
                {
                    "chunk": "hold off on hiring",
                    "meaning": "暫緩招聘新進人員",
                    "scenario": "Management decided to hold off on hiring until third-quarter forecasts improve.",
                    "paraphrase": "hold off on = delay = defer = postpone",
                    "alert": ""
                },
                {
                    "chunk": "put off the negotiation",
                    "meaning": "推遲雙邊談判會議",
                    "scenario": "Both parties agreed to put off the negotiation until legal reviews are complete.",
                    "paraphrase": "put off = postpone = defer",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "助動詞與動詞中間的「夾心餅乾」位置？",
                "rule_1": "👀 看到 will ________ [動詞原形] ➔ 夾心位置 100% 填入「副詞 (-ly)」！",
                "rule_2": "👀 同樣適用：has/have ________ [V-en]、be ________ [V-ed / V-ing] ➔ 通通塞副詞！",
                "golden_rule": "⚡ 教練金句：看到動詞前後有破洞，抓 -ly 副詞填補！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "The senior partners will ________ review the proposed merger terms before making an announcement.",
                    "options": {
                        "A": "careful",
                        "B": "carefully",
                        "C": "carefulness",
                        "D": "caring"
                    },
                    "answer": "B",
                    "analysis": "will ________ review（助動詞 + 空格 + 原形動詞），中間唯一能修飾動詞 review 的只有副詞 (B) carefully。",
                    "translation": "資深合夥人將在發布公告前仔細審視擬議的併購條款。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "Ms. Gomez will ________ the role of chief financial officer starting next month.",
                    "options": {
                        "A": "step down",
                        "B": "take over",
                        "C": "hold off",
                        "D": "back down"
                    },
                    "answer": "B",
                    "analysis": "語意搭配：take over the role（接管/接任職位）。step down 需接 from（辭去）；hold off 表暫緩；back down 表退讓。",
                    "translation": "Gomez 女士將從下個月起接任財務長一職。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "________ to offering comprehensive medical coverage, the firm provides retirement matching funds.",
                    "options": {
                        "A": "In addition",
                        "B": "In addition to",
                        "C": "Beside",
                        "D": "Furthermore"
                    },
                    "answer": "B",
                    "analysis": "空格後為動名詞片語 'offering comprehensive medical coverage'。In addition 為副詞不能直接帶受詞；In addition to 為介系詞片語，後接 V-ing/N，表『除……之外』。",
                    "translation": "除了提供全面的醫療保險外，該公司還提供退休金提撥對等基金。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "Mr. Davies will step ________ [辭職] from his post as director.",
                    "clue": "介副詞，往下的感覺",
                    "answer": "down (step down)"
                },
                {
                    "prompt": "She was chosen to take ________ [接管] the marketing division.",
                    "clue": "接替、接管",
                    "answer": "over (take over)"
                },
                {
                    "prompt": "Let us hold ________ [暫緩] on signing the lease until inspection.",
                    "clue": "推遲暫緩",
                    "answer": "off (hold off on)"
                },
                {
                    "prompt": "In addition ________ [介系詞] salary, we provide travel subsidies.",
                    "clue": "除了……之外還有",
                    "answer": "to (in addition to)"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "The board has ________ approved the capital allocation for the renewable project.",
                    "options": {
                        "A": "unanimous",
                        "B": "unanimously",
                        "C": "unanimity",
                        "D": "unanimousness"
                    },
                    "answer": "B",
                    "trap_point": "has ________ approved（完成式夾心餅乾，秒選副詞 -ly！）",
                    "analysis": "has 與 approved 之間修飾動詞，選副詞 (B) unanimously（全體一致地）。"
                },
                {
                    "id": 2,
                    "question": "The contractor was held liable ________ failing to adhere to fire code regulations.",
                    "options": {
                        "A": "for",
                        "B": "to",
                        "C": "with",
                        "D": "in"
                    },
                    "answer": "A",
                    "trap_point": "be held liable for（對……負有責任）。",
                    "analysis": "be liable for + 事由。故選 (A) for。"
                }
            ],
            "part7": {
                "text_type": "Corporate Leadership Announcement (企業高層任命公告)",
                "title": "Transition of Chief Executive Officer",
                "content": "To: All Global Staff\nFrom: Board of Directors\nDate: November 9\n\nAfter fifteen years of distinguished service, CEO Arthur Pendelton has decided to step down from his executive role on December 31. The board is thrilled to announce that Executive VP Brenda Vance will take over the chief executive position effective January 1.\n\n*Special Advisory: All departmental budgetary requests normally overseen by Mr. Pendelton will be held off until January 15, unless they pertain directly to ongoing client deliverables already scheduled in Q4.",
                "questions": [
                    {
                        "question": "What is scheduled to happen on January 1?",
                        "options": {
                            "A": "Arthur Pendelton will renew his executive contract.",
                            "B": "Brenda Vance will assume the role of CEO.",
                            "C": "A global staff meeting will be convened.",
                            "D": "All Q4 client deliverables will be canceled."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：同義字替換 take over the position ＝ assume the role！",
                        "analysis": "公告說明 Brenda Vance 將在 1 月 1 日起接掌執行長職務（take over = assume the role），故選 (B)。"
                    },
                    {
                        "question": "Which budget requests may be approved before January 15?",
                        "options": {
                            "A": "Requests for employee wellness programs.",
                            "B": "Applications for newly proposed IT infrastructure.",
                            "C": "Those directly relevant to already planned Q4 projects.",
                            "D": "Submissions personally endorsed by Brenda Vance."
                        },
                        "answer": "C",
                        "radar": "🔍 防漏看雷達：除外條件句 'unless they pertain directly to ongoing client deliverables already scheduled in Q4'！pertain to ＝ relevant to！",
                        "analysis": "末尾星號清楚註明：預算審核延後至 1/15，除非直接與 Q4 已排定客戶交付成果相關，故選 (C)。"
                    }
                ]
            }
        }
    },
    7: {
        "day": 7,
        "date": "11/10",
        "phase": 1,
        "phase_name": "錯題庫清零與語感校正",
        "topic": "不完全及物動詞 (find + O + OC) ｜ 規章遵守與超時加班",
        "morning": {
            "chunks": [
                {
                    "chunk": "putting in overtime",
                    "meaning": "持續加班工作",
                    "scenario": "Staff members were putting in overtime to meet the rigorous software rollout date.",
                    "paraphrase": "putting in overtime = working extra hours",
                    "alert": ""
                },
                {
                    "chunk": "refrain from smoking",
                    "meaning": "請勿抽煙 / 克制避免",
                    "scenario": "Guests are kindly requested to refrain from smoking on the outdoor terrace.",
                    "paraphrase": "refrain from = abstain from = avoid",
                    "alert": "必考介系詞：refrain 固定搭配 from + V-ing/N！"
                },
                {
                    "chunk": "adhere to guidelines",
                    "meaning": "遵守各項準則",
                    "scenario": "All laboratory personnel must adhere to guidelines set by the safety commission.",
                    "paraphrase": "adhere to = comply with = abide by = follow",
                    "alert": "必考介系詞：adhere 固定搭配 to！"
                },
                {
                    "chunk": "be bound to happen",
                    "meaning": "必然會發生",
                    "scenario": "With market volatility at record highs, price fluctuations are bound to happen.",
                    "paraphrase": "be bound to = be certain to = inevitable",
                    "alert": ""
                },
                {
                    "chunk": "back down from demands",
                    "meaning": "從訴求中退讓妥協",
                    "scenario": "Neither negotiating team was willing to back down from demands.",
                    "paraphrase": "back down = yield = concede",
                    "alert": ""
                },
                {
                    "chunk": "throughout the day",
                    "meaning": "一整天持續不斷",
                    "scenario": "Refreshments and snacks will be served in the foyer throughout the day.",
                    "paraphrase": "throughout the day = all day long",
                    "alert": ""
                },
                {
                    "chunk": "and vice versa",
                    "meaning": "反之亦然",
                    "scenario": "A successful marketing campaign benefits sales figures, and vice versa.",
                    "paraphrase": "vice versa = the reverse is also true",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "看到 find / keep / make / deem + 受詞 ➔ 後面接什麼？",
                "rule_1": "👀 看到 find + 受詞 + ________ ➔ 80% 考「形容詞 (OC 受詞補語)」！",
                "rule_2": "👀 例：find the manual ________ ➔ 選 helpful / useful（覺得手冊很實用）！",
                "golden_rule": "⚡ 教練金句：find/keep/make 後面帶受詞，補語秒挑形容詞！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "Most new recruits found the company's interactive onboarding software surprisingly ________.",
                    "options": {
                        "A": "help",
                        "B": "helpful",
                        "C": "helpfully",
                        "D": "helpfulness"
                    },
                    "answer": "B",
                    "analysis": "句型判定：found（find 的過去式）+ the software（受詞）+ ________（受詞補語）。受詞補語需用形容詞，故選 (B) helpful。副詞 helpfully 只能修飾動作，不能修飾受詞狀態。",
                    "translation": "大多數新進員工覺得公司的互動式到職培訓軟體出奇地實用。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "All laboratory technicians must strictly adhere ________ established biosafety procedures.",
                    "options": {
                        "A": "to",
                        "B": "with",
                        "C": "in",
                        "D": "for"
                    },
                    "answer": "A",
                    "analysis": "介系詞秒殺：adhere to（遵守）。comply 才接 with；abide 接 by。",
                    "translation": "所有實驗室技術人員必須嚴格遵守既定的生物安全程序。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "Please refrain ________ using mobile phones inside the auditorium during the keynote speech.",
                    "options": {
                        "A": "for",
                        "B": "from",
                        "C": "by",
                        "D": "at"
                    },
                    "answer": "B",
                    "analysis": "語塊秒殺：refrain from + V-ing（克制/避免做某事）。故選 (B) from。",
                    "translation": "在專題演講期間，請勿在禮堂內使用手機。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "Employees must adhere ________ [介系詞] safety rules.",
                    "clue": "遵守……",
                    "answer": "to (adhere to)"
                },
                {
                    "prompt": "Visitors must refrain ________ [介系詞] taking photos.",
                    "clue": "克制、避免",
                    "answer": "from (refrain from)"
                },
                {
                    "prompt": "The auditors found the accounting data ________ [精準的/令人滿意的].",
                    "clue": "find + O + 形容詞",
                    "answer": "accurate / satisfactory"
                },
                {
                    "prompt": "Engineers have been putting ________ [加班] overtime this week.",
                    "clue": "投入加班時間",
                    "answer": "in (putting in overtime)"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "The revised interface makes the order submission process noticeably ________.",
                    "options": {
                        "A": "simple",
                        "B": "simply",
                        "C": "simplicity",
                        "D": "simplification"
                    },
                    "answer": "A",
                    "trap_point": "make + 受詞 + [形容詞受詞補語]。noticeably 是副詞修飾形容詞 simple！",
                    "analysis": "make + the process（受詞）+ noticeably（副詞）+ [形容詞]。故選 (A) simple。"
                },
                {
                    "id": 2,
                    "question": "The contractor decided not to ________ down from the agreed warranty terms.",
                    "options": {
                        "A": "step",
                        "B": "back",
                        "C": "hold",
                        "D": "put"
                    },
                    "answer": "B",
                    "trap_point": "片語搭配：back down（妥協/退縮）；step down（辭職下台）。",
                    "analysis": "由語意知承包商不願從保固條款中讓步妥協，故選 back down。"
                }
            ],
            "part7": {
                "text_type": "Workplace Policy Circular (工作場所規章公文)",
                "title": "Overtime Compensation and Wellness Regulations",
                "content": "To: All Operations Division Staff\nFrom: Human Resources\nDate: November 10\n\nWith peak holiday shipping underway, employees putting in overtime are entitled to time-and-a-half pay for every hour exceeding the standard 40-hour workweek. To preserve workplace safety, all personnel must adhere strictly to rest break mandates.\n\n*Mandatory Condition: No team member is permitted to work more than 12 consecutive hours in a single 24-hour cycle. Any supervisor attempting to enforce shifts beyond this threshold without prior authorization from the division head will be subject to disciplinary review.",
                "questions": [
                    {
                        "question": "How are employees compensated for working over 40 hours a week?",
                        "options": {
                            "A": "With additional vacation days.",
                            "B": "At 1.5 times their regular hourly rate.",
                            "C": "Through annual stock bonus options.",
                            "D": "With complimentary meal vouchers."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：抓住 'time-and-a-half pay'（1.5 倍工資）的同義替換！",
                        "analysis": "第一段第二句寫道 'entitled to time-and-a-half pay for every hour exceeding... 40-hour workweek'，即 1.5 倍工資，故選 (B)。"
                    },
                    {
                        "question": "What is the maximum number of consecutive hours an employee may work?",
                        "options": {
                            "A": "8 hours.",
                            "B": "10 hours.",
                            "C": "12 hours.",
                            "D": "14 hours."
                        },
                        "answer": "C",
                        "radar": "🔍 防漏看雷達：星號附註具體數字條件 'more than 12 consecutive hours'！",
                        "analysis": "文末星號清楚標示門檻：任何員工不得在單一 24 小時週期內連續工作超過 12 小時，故選 (C)。"
                    }
                ]
            }
        }
    },
    8: {
        "day": 8,
        "date": "11/11",
        "phase": 1,
        "phase_name": "錯題庫清零與語感校正",
        "topic": "名詞動詞同形誤判 (damage) ｜ 差旅與服裝規範",
        "morning": {
            "chunks": [
                {
                    "chunk": "compensate for damage",
                    "meaning": "賠償所造成的損失",
                    "scenario": "The courier promised to compensate for damage sustained during transit.",
                    "paraphrase": "damage = harm = destruction; 多義字：damage (n.) 損害; damage (v.) 破壞",
                    "alert": "文法陷阱：damage 當『損害』時為不可數名詞！damages 複數時指『法律賠償金』！"
                },
                {
                    "chunk": "book luxury accommodation",
                    "meaning": "預訂奢華住宿設施",
                    "scenario": "Travel coordinators booked luxury accommodation for the visiting delegates.",
                    "paraphrase": "accommodation = lodging = housing",
                    "alert": "不可數名詞：accommodation（住宿）多益常考不可數！"
                },
                {
                    "chunk": "walking down the aisle",
                    "meaning": "沿著走道走過去",
                    "scenario": "Please keep luggage clear while walking down the aircraft aisle.",
                    "paraphrase": "aisle = walkway = corridor = passageway",
                    "alert": ""
                },
                {
                    "chunk": "anticipate the demand",
                    "meaning": "預先掌握市場需求",
                    "scenario": "Retailers must anticipate the demand for winter coats before the freeze.",
                    "paraphrase": "anticipate = foresee = expect = predict",
                    "alert": ""
                },
                {
                    "chunk": "wear professional attire",
                    "meaning": "穿著專業商務服飾",
                    "scenario": "Consultants are expected to wear professional attire during client presentations.",
                    "paraphrase": "attire = clothing = garments = apparel",
                    "alert": "不可數名詞：attire 為不可數；attired (adj.) 穿著……服裝的。"
                },
                {
                    "chunk": "commercial kitchen appliance",
                    "meaning": "商用廚房家電器具",
                    "scenario": "The restaurant replaced its outdated commercial kitchen appliance.",
                    "paraphrase": "appliance = device = machine = equipment",
                    "alert": ""
                },
                {
                    "chunk": "attired in business suits",
                    "meaning": "身著商務套裝",
                    "scenario": "All convention attendees were neatly attired in business suits.",
                    "paraphrase": "attired in = dressed in",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "看到 damage / access / schedule / contact ➔ 先看位置定詞性！",
                "rule_1": "👀 前面有 a / the / cause / assess ➔ 它是「名詞」受詞！（assess the damage）",
                "rule_2": "👀 前面有 will / could / to ➔ 它是「動詞」原形！（will damage the engine）",
                "golden_rule": "⚡ 教練金句：不要先入為主背死詞性，看前看後判斷它是動還是名！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "The heavy downpour caused substantial ________ to the exterior roof structure.",
                    "options": {
                        "A": "damage",
                        "B": "damages",
                        "C": "damaged",
                        "D": "damaging"
                    },
                    "answer": "A",
                    "analysis": "形容詞 'substantial' 後接名詞受詞。此處指『實體損壞』，damage 為不可數名詞，不可加 s，故選 (A)。damages 複數專指法院判決的賠償金。",
                    "translation": "暴雨對建築外層屋頂結構造成了重大損害。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "The hotel offers complimentary shuttle bus service between the terminal and guest ________.",
                    "options": {
                        "A": "accommodate",
                        "B": "accommodations",
                        "C": "accommodating",
                        "D": "accommodator"
                    },
                    "answer": "B",
                    "analysis": "複合名詞 guest accommodations（客房住宿設施），多益亦常以 accommodations 複數型指各類房間設施。故選 (B)。",
                    "translation": "該飯店提供航廈與客房住宿設施之間的免費接駁巴士服務。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "All personnel attending the banquet must be formally ________ in evening wear.",
                    "options": {
                        "A": "attire",
                        "B": "attired",
                        "C": "attiring",
                        "D": "attires"
                    },
                    "answer": "B",
                    "analysis": "be + formally + attired in... 表『穿著……服裝』，attired 在此作為過去分詞形容詞用，選 (B)。",
                    "translation": "所有參加晚宴的人員皆須正式著晚禮服出席。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "Severe hail caused severe ________ [名詞：損壞] to the vehicle.",
                    "clue": "不可數名詞，指破壞損壞",
                    "answer": "damage"
                },
                {
                    "prompt": "All sales staff are expected to wear proper business ________ [服飾].",
                    "clue": "a 開頭不可數名詞",
                    "answer": "attire"
                },
                {
                    "prompt": "We were seated across the ________ [走道] on the train.",
                    "clue": "以 a 開頭的通道走廊",
                    "answer": "aisle"
                },
                {
                    "prompt": "We failed to ________ [預料/預期] such high consumer demand.",
                    "clue": "a 開頭動詞，同義 foresee",
                    "answer": "anticipate"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "Improper operation of the crane may ________ the underlying concrete floor.",
                    "options": {
                        "A": "damage",
                        "B": "damaging",
                        "C": "damages",
                        "D": "damaged"
                    },
                    "answer": "A",
                    "trap_point": "助動詞 may + 原形動詞！此處 damage 為動詞。",
                    "analysis": "may 後接動詞原形，帶出受詞 the concrete floor，故選 (A) damage。"
                },
                {
                    "id": 2,
                    "question": "Ms. Lawson found the candidate's portfolio extremely ________.",
                    "options": {
                        "A": "impress",
                        "B": "impressive",
                        "C": "impressively",
                        "D": "impression"
                    },
                    "answer": "B",
                    "trap_point": "Day 7 錨點複習：found + O + [形容詞受詞補語]！",
                    "analysis": "found + the portfolio（受詞）+ extremely（副詞）+ [形容詞]。選 (B) impressive。"
                }
            ],
            "part7": {
                "text_type": "Travel & Logistics Directive (商務差旅物流指引)",
                "title": "Corporate Conference Travel & Attire Guidelines",
                "content": "To: Global Sales Representatives\nFrom: Corporate Events Planning\nDate: November 11\n\nAll representatives attending the annual summit in Chicago will be provided with hotel accommodation at the Grand Plaza. Representatives should anticipate heavy traffic when traveling from the airport.\n\nAttire Requirements: Standard business attire is mandatory for daytime panel sessions. However, casual garments are permitted exclusively during the Friday evening networking dinner on the outdoor pavilion.\n\n*Luggage Allowance: The company will reimburse luggage fees for up to two checked bags, provided that luggage receipts are submitted within 7 days of trip conclusion.",
                "questions": [
                    {
                        "question": "What is permitted exclusively during Friday evening's event?",
                        "options": {
                            "A": "Formal tuxedos and gowns.",
                            "B": "Casual clothing.",
                            "C": "Complimentary shuttle rides.",
                            "D": "Unscheduled product demonstrations."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：限制副詞 exclusively！'casual garments are permitted exclusively during the Friday evening networking dinner'！garments ＝ clothing！",
                        "analysis": "文中明確表示週五晚宴時允許休閒便服（casual garments = casual clothing），故選 (B)。"
                    },
                    {
                        "question": "What must employees do to receive baggage fee reimbursement?",
                        "options": {
                            "A": "Share accommodation with another delegate.",
                            "B": "Submit baggage receipts within seven days.",
                            "C": "Limit their luggage to a single carry-on.",
                            "D": "Travel solely on designated corporate airlines."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：星號附註條件 'provided that luggage receipts are submitted within 7 days'！",
                        "analysis": "文末行李條款說明費用核銷條件：必須在行程結束後 7 天內繳交收據，故選 (B)。"
                    }
                ]
            }
        }
    },
    9: {
        "day": 9,
        "date": "11/12",
        "phase": 1,
        "phase_name": "錯題庫清零與語感校正",
        "topic": "不定代名詞範圍判定 ｜ 文宣手冊與容量承載",
        "morning": {
            "chunks": [
                {
                    "chunk": "one another in the team",
                    "meaning": "團隊彼此互相（三人以上）",
                    "scenario": "Colleagues are encouraged to assist one another in the team during peak hours.",
                    "paraphrase": "one another = each other",
                    "alert": "文法考點：one another 與 each other 是代名詞，通常當受詞，不能直接當主詞！"
                },
                {
                    "chunk": "broaden client outreach",
                    "meaning": "拓展客戶觸及範圍",
                    "scenario": "The marketing team launched campaigns to broaden client outreach in suburban districts.",
                    "paraphrase": "broaden = expand = widen",
                    "alert": ""
                },
                {
                    "chunk": "promotional brochure or flier",
                    "meaning": "宣傳小冊或傳單",
                    "scenario": "Volunteers distributed a promotional brochure or flier at the subway exit.",
                    "paraphrase": "brochure = pamphlet = booklet = flier / flyer",
                    "alert": "多益常考三胞胎：brochure / pamphlet / flier 通通是文宣小冊子！"
                },
                {
                    "chunk": "reach maximum capacity",
                    "meaning": "達到最大容納量 / 產能",
                    "scenario": "The auditorium reached maximum capacity minutes before the keynote address.",
                    "paraphrase": "capacity = volume = maximum occupancy",
                    "alert": ""
                },
                {
                    "chunk": "perform tasks capably",
                    "meaning": "幹練稱職地執行任務",
                    "scenario": "Despite her young age, she performed tasks capably under intense deadline pressure.",
                    "paraphrase": "capably = competently = adeptly",
                    "alert": ""
                },
                {
                    "chunk": "hire a local caterer",
                    "meaning": "聘請當地外燴廠商",
                    "scenario": "The event coordinator decided to hire a local caterer for the banquet dinner.",
                    "paraphrase": "caterer = food service provider",
                    "alert": ""
                },
                {
                    "chunk": "temporary road closure",
                    "meaning": "臨時道路封閉",
                    "scenario": "Commuters were alerted to a temporary road closure along Main Street.",
                    "paraphrase": "closure = shutdown = blockage",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "不定代名詞秒殺：看後面有沒有名詞，以及是單數還是複數？",
                "rule_1": "👀 空格後有【單數名詞】➔ 選 another（another branch 另一家分行）",
                "rule_2": "👀 空格後有【複數名詞】➔ 選 other（other branches 其他分行）",
                "rule_3": "👀 空格後【沒有名詞，自己獨立站著】➔ 選 others（其他的人事物）或 the others（剩下的全部）",
                "golden_rule": "⚡ 教練金句：後有單數選 another，後有複數選 other，後無名詞選 others！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "While one of the printers is being serviced, staff members may use ________ machines located on the third floor.",
                    "options": {
                        "A": "another",
                        "B": "other",
                        "C": "others",
                        "D": "one another"
                    },
                    "answer": "B",
                    "analysis": "空格後面是複數名詞 'machines'，修飾複數名詞用 (B) other。another 只能修飾單數名詞；others 是代名詞，後方不能接名詞；one another 表彼此（受詞）。",
                    "translation": "當其中一台印表機在維修時，同仁可以使用位於三樓的其他機器。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "The conference center was renovated to accommodate ________ of up to 1,500 delegates.",
                    "options": {
                        "A": "capacity",
                        "B": "a capacity",
                        "C": "capable",
                        "D": "capably"
                    },
                    "answer": "B",
                    "analysis": "accommodate 后接名詞受詞，'a capacity of + 數字' 為固定搭配，表示『達……人的容納量』。故選 (B)。",
                    "translation": "該會議中心已進行整修，可容納多達 1,500 名代表。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "Please refer to the enclosed ________ for detailed specifications regarding the new solar generator.",
                    "options": {
                        "A": "brochure",
                        "B": "closure",
                        "C": "caterer",
                        "D": "attire"
                    },
                    "answer": "A",
                    "analysis": "enclosed 后接名詞，說明包含詳細規格，(A) brochure（小冊子）最合語意。(B) closure 關閉；(C) caterer 外燴業者；(D) attire 服裝。",
                    "translation": "有關新型太陽能發電機的詳細規格，請參閱隨函附上的手冊。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "Team members must communicate openly with one ________ [彼此].",
                    "clue": "one... 彼此",
                    "answer": "another (one another)"
                },
                {
                    "prompt": "We need to print 500 copies of the marketing ________ [傳單/小冊].",
                    "clue": "b 或 p 或 f 開頭",
                    "answer": "brochure / pamphlet / flier"
                },
                {
                    "prompt": "The ballroom has an official seating ________ [容納人數] of 300.",
                    "clue": "c 開頭名詞",
                    "answer": "capacity"
                },
                {
                    "prompt": "Traffic was diverted due to sudden tunnel ________ [封閉].",
                    "clue": "close 的名詞",
                    "answer": "closure"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "Some participants preferred the morning session, while ________ chose the afternoon workshop.",
                    "options": {
                        "A": "other",
                        "B": "others",
                        "C": "another",
                        "D": "each other"
                    },
                    "answer": "B",
                    "trap_point": "後方沒有名詞，獨立當主詞，且對照前面 Some！",
                    "analysis": "Some... while others...（一些人……而其他人……）。空格獨立作主詞，後面沒有名詞，選代名詞 (B) others。"
                },
                {
                    "id": 2,
                    "question": "The newly hired administrative assistant handles all complex scheduling ________.",
                    "options": {
                        "A": "capable",
                        "B": "capably",
                        "C": "capability",
                        "D": "capacitate"
                    },
                    "answer": "B",
                    "trap_point": "修飾動詞 handles scheduling 需用副詞！",
                    "analysis": "及物動詞 handles + 受詞 scheduling，句尾修飾動作需要副詞，選 (B) capably（稱職地）。"
                }
            ],
            "part7": {
                "text_type": "Community Information Flier (社區文宣傳單)",
                "title": "Downtown Harbor Plaza Refurbishment Notice",
                "content": "Attention Residents & Business Owners,\n\nThe City Council will initiate structural upgrades at Harbor Plaza beginning Monday, November 14. To broaden public pedestrian space, construction crews will enforce a temporary closure of the southern vehicle lane.\n\n*Business Operating Notice: All retail tenants and restaurants will remain open during normal hours. Deliveries from food caterers and suppliers are permitted before 9:00 AM daily, provided that vehicles do not exceed a gross weight capacity of 3 tons.",
                "questions": [
                    {
                        "question": "What is the primary purpose of the plaza construction project?",
                        "options": {
                            "A": "To build a new underground parking structure.",
                            "B": "To expand pedestrian walkway space.",
                            "C": "To repair damages caused by severe weather.",
                            "D": "To introduce new retail caterers."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：同義字替換 broaden public pedestrian space ＝ expand pedestrian walkway space！",
                        "analysis": "傳單中說明施工目的：'To broaden public pedestrian space'，broaden 即 expand，故選 (B)。"
                    },
                    {
                        "question": "When may suppliers make deliveries to plaza businesses?",
                        "options": {
                            "A": "At any time throughout the weekend.",
                            "B": "Exclusively after 5:00 PM.",
                            "C": "Prior to 9:00 AM on weekdays.",
                            "D": "Only if escorted by city council staff."
                        },
                        "answer": "C",
                        "radar": "🔍 防漏看雷達：時間條件 'permitted before 9:00 AM daily'！prior to ＝ before！",
                        "analysis": "末段特別標註：供應商送貨僅限於每日早上 9:00 前（before 9:00 AM），故選 (C)。"
                    }
                ]
            }
        }
    },
    10: {
        "day": 10,
        "date": "11/13",
        "phase": 1,
        "phase_name": "錯題庫清零與語感校正",
        "topic": "Phase 1 綜合驗收 ｜ 表揚、全面與當代商務",
        "morning": {
            "chunks": [
                {
                    "chunk": "commend the staff",
                    "meaning": "大力表揚全體員工",
                    "scenario": "The regional director commended the staff for exceeding quarterly sales benchmarks.",
                    "paraphrase": "commend = praise = applaud = compliment",
                    "alert": "易混淆：commend (v.) 表揚讚賞 vs. comment (v./n.) 評論！"
                },
                {
                    "chunk": "a competent manager",
                    "meaning": "一位能幹稱職的經理",
                    "scenario": "Hiring a competent manager helped stabilize the company's manufacturing unit.",
                    "paraphrase": "competent = capable = skilled = proficient",
                    "alert": ""
                },
                {
                    "chunk": "comprehensive training guide",
                    "meaning": "詳盡全面的培訓手冊",
                    "scenario": "The human resources department compiled a comprehensive training guide.",
                    "paraphrase": "comprehensive = thorough = complete = exhaustive",
                    "alert": "易混淆：comprehensive (adj.) 全面的 vs. comprehensible (adj.) 可理解的！"
                },
                {
                    "chunk": "conclusive laboratory evidence",
                    "meaning": "決定性的實驗室證據",
                    "scenario": "Researchers presented conclusive laboratory evidence supporting the new formula.",
                    "paraphrase": "conclusive = definitive = decisive",
                    "alert": ""
                },
                {
                    "chunk": "considerable growth",
                    "meaning": "相當可觀的成長幅度",
                    "scenario": "The pharmaceutical sector achieved considerable growth over the past two quarters.",
                    "paraphrase": "considerable = substantial = significant",
                    "alert": "易混淆：considerable (adj.) 相當多的/可觀的 vs. considerate (adj.) 體貼的！"
                },
                {
                    "chunk": "contemporary office design",
                    "meaning": "當代現代化辦公室設計",
                    "scenario": "The architecture firm specializes in sustainable and contemporary office design.",
                    "paraphrase": "contemporary = modern = current",
                    "alert": ""
                },
                {
                    "chunk": "corridor leading to",
                    "meaning": "通往……的走廊通道",
                    "scenario": "Exit signs are installed along the corridor leading to the emergency stairwell.",
                    "paraphrase": "corridor = hallway = passageway",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "Phase 1 四大陷阱終極合體雷達",
                "rule_1": "1️⃣ 看到空格後無動詞 ➔ 介系詞（despite, in spite of, owing to, prior to）",
                "rule_2": "2️⃣ 看到 while/once 帶受詞 ➔ 主動 -ing，被動 -ed",
                "rule_3": "3️⃣ 看到 will / has + 空格 + 動詞 ➔ 夾心塞副詞 -ly",
                "golden_rule": "⚡ 教練金句：秒殺題靠位置，語意題靠語塊搭配！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "The CEO publicly ________ the engineering team for resolving the system crash within minutes.",
                    "options": {
                        "A": "commented",
                        "B": "commended",
                        "C": "commanded",
                        "D": "commenced"
                    },
                    "answer": "B",
                    "analysis": "語意辨析：commend 表『稱讚 / 表揚某人』，固定搭配 commend someone for something。comment 表評論（comment on）；command 表命令；commence 表開始。",
                    "translation": "執行長公開表揚工程團隊在數分鐘內解決了系統當機問題。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "Prior to opening the overseas branch, the executives conducted a ________ market assessment.",
                    "options": {
                        "A": "comprehensible",
                        "B": "comprehensive",
                        "C": "comprehensively",
                        "D": "comprehension"
                    },
                    "answer": "B",
                    "analysis": "修飾名詞 market assessment 需要形容詞。comprehensive assessment 表『全面詳盡的評估』，為多益經典考題。comprehensible 指可理解的。",
                    "translation": "在開設海外分公司之前，主管們進行了全面的市場評估。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "The firm reported ________ profits in the renewable energy sector despite rising supply costs.",
                    "options": {
                        "A": "considerate",
                        "B": "considerable",
                        "C": "considerably",
                        "D": "consideration"
                    },
                    "answer": "B",
                    "analysis": "修飾名詞 profits 需用形容詞。considerable 表示『相當可觀的 / 大量的』。considerate 意為『體貼周到的』，語意不通。",
                    "translation": "儘管原物料成本上漲，該公司仍公佈了在再生能源領域的可觀獲利。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "The president ________ [表揚] the sales director for outstanding results.",
                    "clue": "c 開頭動詞，表讚揚",
                    "answer": "commended (commend someone for)"
                },
                {
                    "prompt": "Our company offers a ________ [全面的/詳盡的] medical insurance package.",
                    "clue": "c 開頭形容詞，全面性的",
                    "answer": "comprehensive"
                },
                {
                    "prompt": "The project generated ________ [相當可觀的] revenue for the branch.",
                    "clue": "c 開頭形容詞，同義 substantial",
                    "answer": "considerable"
                },
                {
                    "prompt": "Please do not leave briefcases unattended in the ________ [走廊].",
                    "clue": "走廊、通道，c 開頭",
                    "answer": "corridor"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "While ________ the warehouse inventory, the logistics manager discovered three misplaced pallets.",
                    "options": {
                        "A": "inspect",
                        "B": "inspecting",
                        "C": "inspected",
                        "D": "inspection"
                    },
                    "answer": "B",
                    "trap_point": "Day 5 分詞構句複習：while 接主動 V-ing 帶受詞！",
                    "analysis": "經理主動清點庫存並帶受詞 the warehouse inventory，while 後用現在分詞 (B) inspecting。"
                },
                {
                    "id": 2,
                    "question": "The proposed tax reform will ________ impact the financial sector across the region.",
                    "options": {
                        "A": "drastic",
                        "B": "drastically",
                        "C": "drasticness",
                        "D": "drastical"
                    },
                    "answer": "B",
                    "trap_point": "Day 6 夾心餅乾複習：will ________ impact（助動詞 + 空格 + 動詞原形）！",
                    "analysis": "will 與 impact 之間只能填入副詞 (B) drastically（劇烈地 / 大幅度地）。"
                }
            ],
            "part7": {
                "text_type": "Executive Commendation Memo (高層嘉獎備忘錄)",
                "title": "Excellence in Client Service Award - Q3",
                "content": "To: All Corporate Staff\nFrom: Executive Committee\nDate: November 13\n\nThe Executive Committee is pleased to commend the Quality Assurance Division for achieving a 99.8% customer satisfaction rate. Under the direction of Chief Inspector Elena Rostova, the division completed a comprehensive audit that reduced product return rates considerably.\n\n*Bonus Distribution Detail: All full-time inspectors within the division are eligible for a merit bonus of $1,200. Eligible personnel must confirm their banking information with payroll before Friday, November 18, to ensure prompt disbursement.",
                "questions": [
                    {
                        "question": "Why is the Quality Assurance Division being commended?",
                        "options": {
                            "A": "For relocating to a contemporary facility.",
                            "B": "For achieving outstanding customer satisfaction.",
                            "C": "For recruiting several competent managers.",
                            "D": "For drafting a new legal compliance charter."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：同義替換 99.8% customer satisfaction rate ＝ outstanding customer satisfaction！",
                        "analysis": "第一段第一句明確寫道嘉獎原因：'for achieving a 99.8% customer satisfaction rate'，故選 (B)。"
                    },
                    {
                        "question": "What must inspectors do to receive their bonus on time?",
                        "options": {
                            "A": "Submit a comprehensive customer feedback survey.",
                            "B": "Complete 40 hours of advanced quality training.",
                            "C": "Verify their bank account details prior to November 18.",
                            "D": "Obtain written approval from Elena Rostova."
                        },
                        "answer": "C",
                        "radar": "🔍 防漏看雷達：星號附註細節 'must confirm their banking information with payroll before Friday, November 18'！confirm = verify, before = prior to！",
                        "analysis": "末尾星號明確說明領取獎金的前提：在 11 月 18 日前向薪酬組確認銀行帳戶資訊，故選 (C)。"
                    }
                ]
            }
        }
    }
}

# Merge ADDITIONAL_DAYS into DAYS_DATA
DAYS_DATA.update(ADDITIONAL_DAYS)
