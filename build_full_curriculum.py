# -*- coding: utf-8 -*-
"""
Script to build full 25-day dataset into curriculum_data.py.
Combines Days 1-10 with detailed definitions for Days 11-25.
"""

from curriculum_data import DAYS_DATA
import json

# Days 11 to 25 definition dictionary
DAYS_11_TO_25 = {
    11: {
        "day": 11,
        "date": "11/14",
        "phase": 2,
        "phase_name": "860 金色證書進階擴充與同義字轉換",
        "topic": "轉折副詞秒殺 (otherwise / therefore) ｜ 扣除、分派與可靠性",
        "morning": {
            "chunks": [
                {
                    "chunk": "deduct from the invoice",
                    "meaning": "從發票款項中扣除",
                    "scenario": "The accounting department will deduct shipping fees from the total invoice.",
                    "paraphrase": "deduct = subtract = discount",
                    "alert": ""
                },
                {
                    "chunk": "a dependable supplier",
                    "meaning": "一家可靠值得信賴的供應商",
                    "scenario": "Global Chem has proven to be a dependable supplier of raw polymers.",
                    "paraphrase": "dependable = reliable = trustworthy",
                    "alert": ""
                },
                {
                    "chunk": "designate as an emergency exit",
                    "meaning": "指定為緊急出口",
                    "scenario": "Management decided to designate the rear staircase as an emergency exit.",
                    "paraphrase": "designate = assign = name = appoint",
                    "alert": ""
                },
                {
                    "chunk": "a diligent researcher",
                    "meaning": "一位勤勉認真的研究員",
                    "scenario": "Thanks to a diligent researcher, the clinical trial anomalies were flagged early.",
                    "paraphrase": "diligent = conscientious = hardworking = thorough",
                    "alert": ""
                },
                {
                    "chunk": "membership dues",
                    "meaning": "會員常年會費",
                    "scenario": "All annual membership dues must be settled prior to the voting convention.",
                    "paraphrase": "dues = fees = subscription",
                    "alert": "多義字：dues 複數型指『會費』；due to 指『由於』；due on 指『在…到期』！"
                },
                {
                    "chunk": "act otherwise",
                    "meaning": "否則 / 採取相反做法",
                    "scenario": "Please register by noon; otherwise, your reserved seat will be forfeited.",
                    "paraphrase": "otherwise = if not = or else",
                    "alert": ""
                },
                {
                    "chunk": "densely populated district",
                    "meaning": "人口稠密的區域",
                    "scenario": "The retail chain opened a flagship store in a densely populated district.",
                    "paraphrase": "densely = heavily = thickly",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "轉折副詞：看到「分號 (;) + 空格 + 逗號 (,)」？",
                "rule_1": "👀 [句子] ; ________ , [句子] ➔ 100% 填入轉折副詞！（therefore, otherwise, however, nevertheless）",
                "rule_2": "👀 注意：although, because 是連接詞，絕對不能放在 ; ________ , 的位置！",
                "golden_rule": "⚡ 教練金句：看到分號在前逗號在後，秒選轉折副詞 (therefore / otherwise)！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "All attendees must arrive by 9:00 AM; ________, admission into the auditorium cannot be guaranteed.",
                    "options": {
                        "A": "otherwise",
                        "B": "although",
                        "C": "despite",
                        "D": "because"
                    },
                    "answer": "A",
                    "analysis": "看到標點符號位置：分號 ; 後、逗號 , 前。唯一能在此連接兩完整句子的轉折副詞為 (A) otherwise（否則）。(B)、(D) 是從屬連接詞，(C) 是介系詞，均不可放此位置。",
                    "translation": "所有參加者必須在上午 9:00 前抵達；否則，將無法保證能進入禮堂。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "Members who fail to pay their annual ________ by the deadline will forfeit voting privileges.",
                    "options": {
                        "A": "due",
                        "B": "dues",
                        "C": "duly",
                        "D": "dueness"
                    },
                    "answer": "B",
                    "analysis": "pay their annual dues（繳交年度會費）。dues 複數形式作名詞，表『會費 / 應繳款項』。故選 (B)。",
                    "translation": "未在截止日期前繳交年度會費的會員將喪失投票權。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "The board unanimously chose to ________ Ms. Alvarez as the official corporate spokesperson.",
                    "options": {
                        "A": "designate",
                        "B": "designation",
                        "C": "designated",
                        "D": "designative"
                    },
                    "answer": "A",
                    "analysis": "chose to + 原形動詞。designate A as B（任命/指定 A 為 B）。故選 (A)。",
                    "translation": "董事會一致通過指定 Alvarez 女士為官方企業發言人。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "You must confirm your seat; ________ [否則], it will be given away.",
                    "clue": "轉折副詞，o 開頭",
                    "answer": "otherwise"
                },
                {
                    "prompt": "Annual membership ________ [會費] must be paid in January.",
                    "clue": "d 開頭四個字母，加 s",
                    "answer": "dues"
                },
                {
                    "prompt": "He is a ________ [勤勉負責的] and punctual employee.",
                    "clue": "d 開頭形容詞，同義 hardworking",
                    "answer": "diligent"
                },
                {
                    "prompt": "The room was ________ [指定] as a private consultation room.",
                    "clue": "d 開頭動詞被動態",
                    "answer": "designated"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "The accounting fee will be ________ from your final reimbursement check.",
                    "options": {
                        "A": "deducted",
                        "B": "deducting",
                        "C": "deductible",
                        "D": "deduction"
                    },
                    "answer": "A",
                    "trap_point": "be + [過去分詞] from... 費用被扣除！",
                    "analysis": "費用被從支票中扣除，用被動態 be deducted from，故選 (A)。"
                },
                {
                    "id": 2,
                    "question": "Reliable Tech is known as a highly ________ vendor for cloud infrastructure.",
                    "options": {
                        "A": "depend",
                        "B": "dependable",
                        "C": "dependably",
                        "D": "dependence"
                    },
                    "answer": "B",
                    "trap_point": "修飾名詞 vendor 需用形容詞！",
                    "analysis": "a highly dependable vendor（極度可靠的廠商），選形容詞 (B) dependable。"
                }
            ],
            "part7": {
                "text_type": "Association Membership Renewal Notice (同業工會會費續約通知)",
                "title": "International Logistics Association: 2027 Membership Dues",
                "content": "Dear Corporate Partner,\n\nAnnual membership dues for the 2027 fiscal year are now payable. Remitting your dues by December 1 ensures uninterrupted access to our proprietary tariff database. To expedite payment, companies may deduct a 5% early-bird discount directly from their total.\n\n*Important Billing Clause: Member organizations must submit proof of tax exemption prior to December 1; otherwise, standard value-added tax (VAT) will be automatically calculated into the final statement.",
                "questions": [
                    {
                        "question": "How can corporate partners qualify for a 5% discount?",
                        "options": {
                            "A": "By sponsoring the annual logistics conference.",
                            "B": "By paying their dues before December 1.",
                            "C": "By recruiting two new member organizations.",
                            "D": "By switching to quarterly automatic billing."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：條件定位 'Remitting your dues by December 1... deduct a 5% early-bird discount'！",
                        "analysis": "第一段說明在 12 月 1 日前繳交會費即可享有 5% 早鳥折扣，故選 (B)。"
                    },
                    {
                        "question": "What happens if a tax exemption certificate is not submitted on time?",
                        "options": {
                            "A": "Membership access will be suspended immediately.",
                            "B": "An administrative penalty of $100 will be charged.",
                            "C": "Value-added tax will be added to the invoice.",
                            "D": "The organization loses its voting eligibility."
                        },
                        "answer": "C",
                        "radar": "🔍 防漏看雷達：星號附註轉折詞 'otherwise, standard value-added tax (VAT) will be automatically calculated'！",
                        "analysis": "末尾重要條款註明：若未如期繳交免稅證明，加值稅將自動計入帳單，故選 (C)。"
                    }
                ]
            }
        }
    },
    12: {
        "day": 12,
        "date": "11/15",
        "phase": 2,
        "phase_name": "860 金色證書進階擴充與同義字轉換",
        "topic": "同義字大替換 ｜ 翻新、改善與急件處理",
        "morning": {
            "chunks": [
                {
                    "chunk": "drastically reduce costs",
                    "meaning": "大幅度降低成本",
                    "scenario": "Automating warehouse packing helped drastically reduce costs.",
                    "paraphrase": "drastically = dramatically = significantly = substantially",
                    "alert": ""
                },
                {
                    "chunk": "duplicate the key document",
                    "meaning": "複印 / 備份重要文件",
                    "scenario": "Always duplicate the key document before forwarding the master file.",
                    "paraphrase": "duplicate = copy = replicate",
                    "alert": ""
                },
                {
                    "chunk": "ease traffic congestion",
                    "meaning": "緩解交通堵塞問題",
                    "scenario": "The new bypass highway was constructed to ease traffic congestion.",
                    "paraphrase": "ease = alleviate = relieve = mitigate",
                    "alert": ""
                },
                {
                    "chunk": "elaborate on the proposal",
                    "meaning": "詳細闡述這項提案",
                    "scenario": "The project architect will elaborate on the proposal during the hearing.",
                    "paraphrase": "elaborate on = expand on = explain in detail",
                    "alert": "多義字：elaborate (v.) 詳細說明；(adj.) 精心製作的/複雜詳盡的。"
                },
                {
                    "chunk": "expedite the shipment",
                    "meaning": "加急處理這批貨物",
                    "scenario": "We paid a premium fee to expedite the shipment of critical microchips.",
                    "paraphrase": "expedite = accelerate = speed up = rush",
                    "alert": ""
                },
                {
                    "chunk": "enhance system performance",
                    "meaning": "提升系統運行效能",
                    "scenario": "Firmware upgrades were installed to enhance system performance.",
                    "paraphrase": "enhance = improve = upgrade = boost",
                    "alert": ""
                },
                {
                    "chunk": "refurbish the historical hotel",
                    "meaning": "整修這家歷史悠久的飯店",
                    "scenario": "Investors invested millions to refurbish the historical hotel.",
                    "paraphrase": "refurbish = renovate = remodel = restore",
                    "alert": "金色必考同義替換：refurbish ＝ renovate ＝ remodel！"
                }
            ],
            "visual_anchor": {
                "title": "動詞同義替換防線：看到 accelerate 聯想 expedite！",
                "rule_1": "👀 題目看到 speed up / accelerate ➔ 選項找 expedite（加速 / 急件處理）",
                "rule_2": "👀 題目看到 renovate / remodel ➔ 選項找 refurbish（翻修 / 翻新）",
                "golden_rule": "⚡ 教練金句：860 分不考罕見冷僻字，專考商務同義詞瞬間對應！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "To ________ the delivery of medical supplies, the distributor arranged for direct air courier transport.",
                    "options": {
                        "A": "expedite",
                        "B": "expedition",
                        "C": "expeditious",
                        "D": "expedient"
                    },
                    "answer": "A",
                    "analysis": "不定詞片語表目的：To + [動詞原形] + the delivery。expedite（加速/加急辦理）。故選 (A)。",
                    "translation": "為了加速醫療用品的運送，經銷商安排了直接的航空快遞運輸。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "The newly installed solar arrays have ________ reduced our factory's dependence on grid power.",
                    "options": {
                        "A": "drastic",
                        "B": "drastically",
                        "C": "drasticness",
                        "D": "drastical"
                    },
                    "answer": "B",
                    "analysis": "have ________ reduced（完成式夾心餅乾，塞入副詞修飾動詞）。故選 (B) drastically（急劇地 / 大幅度地）。",
                    "translation": "新安裝的太陽能電池板已大幅減少我們工廠對電網電力的依賴。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "The boutique resort will temporarily close in February to ________ its guest suites and dining hall.",
                    "options": {
                        "A": "renovate",
                        "B": "dismiss",
                        "C": "deduct",
                        "D": "vacate"
                    },
                    "answer": "A",
                    "analysis": "受詞為 guest suites and dining hall（客房套房與餐廳），搭配動詞 (A) renovate（整修 / 翻新）。dismiss 解僱；deduct 扣除；vacate 空出/撤出。",
                    "translation": "該精品度假村將於二月暫時關閉，以翻修其客房套房與餐廳。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "We requested the warehouse to ________ [加速/急送] the order.",
                    "clue": "e 開頭動詞，加速處理",
                    "answer": "expedite"
                },
                {
                    "prompt": "The developers plan to ________ [翻新/整修] the old warehouse.",
                    "clue": "r 開頭動詞，同義 renovate",
                    "answer": "refurbish (or renovate)"
                },
                {
                    "prompt": "Software upgrades helped to ________ [提升] data processing speed.",
                    "clue": "e 開頭動詞，改善提昇",
                    "answer": "enhance"
                },
                {
                    "prompt": "The manager asked him to ________ [詳加闡述] on the timeline.",
                    "clue": "e 開頭動詞，接 on",
                    "answer": "elaborate (elaborate on)"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "The contractor provided an ________ estimate of the reconstruction costs.",
                    "options": {
                        "A": "elaborate",
                        "B": "elaborating",
                        "C": "elaborateness",
                        "D": "elaborately"
                    },
                    "answer": "A",
                    "trap_point": "修飾名詞 estimate 需用形容詞！elaborate 本身即可作形容詞（詳盡的）。",
                    "analysis": "an elaborate estimate（詳盡的估算）。elaborate 作形容詞時讀作 [-it]，意為詳盡精細的。故選 (A)。"
                },
                {
                    "id": 2,
                    "question": "The new bridge is intended to ________ severe bottlenecks at the city entrance.",
                    "options": {
                        "A": "ease",
                        "B": "easy",
                        "C": "easily",
                        "D": "easiness"
                    },
                    "answer": "A",
                    "trap_point": "to + [原形動詞] + bottlenecks。ease 可作及物動詞表示『減緩 / 減輕』！",
                    "analysis": "to ease bottlenecks（緩解交通瓶頸）。ease 作動詞表減緩，故選 (A)。"
                }
            ],
            "part7": {
                "text_type": "Renovation Press Release (翻新改建新聞發布稿)",
                "title": "Grand Horizon Hotel Announces Multi-Million Dollar Refurbishment",
                "content": "Chicago — The historic Grand Horizon Hotel today confirmed a $12 million project to renovate its 400 guest rooms and rooftop lounge. Construction will commence on January 10.\n\nTo ease disruptions for long-term corporate clients, noisy structural work will be restricted strictly to weekdays between 10:00 AM and 3:00 PM. \n\n*Important Reservation Policy: Existing guests whose reservations are affected by room closures will be accommodated at the adjacent boutique sister property at no extra surcharge, provided that they confirm their alternate room selection prior to December 20.",
                "questions": [
                    {
                        "question": "What is the primary objective of the $12 million project?",
                        "options": {
                            "A": "To acquire adjacent real estate.",
                            "B": "To refurbish hotel suites and social areas.",
                            "C": "To develop a new reservation software system.",
                            "D": "To compensate corporate guests for past delays."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：Paraphrase 同義替換！文中 'renovate its 400 guest rooms and rooftop lounge' ＝ 選項 'refurbish hotel suites and social areas'！",
                        "analysis": "第一段表明 1,200 萬美元是用來 renovate guest rooms & lounge，同義替換為 refurbish suites and social areas，故選 (B)。"
                    },
                    {
                        "question": "What must affected guests do to secure free accommodation at the sister hotel?",
                        "options": {
                            "A": "File a written dispute with hotel management.",
                            "B": "Confirm their room preference before December 20.",
                            "C": "Pay a 10% refundable security deposit.",
                            "D": "Present a corporate travel discount card."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：星號附註細節 'provided that they confirm their alternate room selection prior to December 20'！",
                        "analysis": "文末條款載明：受影響旅客若要在姐妹飯店獲得免費升級住宿，必須在 12 月 20 日前確認換房選擇，故選 (B)。"
                    }
                ]
            }
        }
    }
}

# Update DAYS_DATA with Day 11 and 12
DAYS_DATA.update(DAYS_11_TO_25)
