# -*- coding: utf-8 -*-
"""
Generates the complete 25 days into a clean, standalone, unified master_curriculum.py.
"""

from complete_curriculum_database import DAYS_DATA
from curriculum_builder import ADDITIONAL_DAYS
import json

DAYS_15_TO_25 = {
    15: {
        "day": 15,
        "date": "11/18",
        "phase": 2,
        "phase_name": "860 金色證書進階擴充與同義字轉換",
        "topic": "隱藏除外條款 ｜ 發起、親密與高利潤法規",
        "morning": {
            "chunks": [
                {
                    "chunk": "initiate the investigation",
                    "meaning": "啟動正式調查程序",
                    "scenario": "Regulatory authorities voted to initiate the investigation into antitrust claims.",
                    "paraphrase": "initiate = launch = begin = commence",
                    "alert": ""
                },
                {
                    "chunk": "inspect factory equipment",
                    "meaning": "仔細檢查工廠設備",
                    "scenario": "Technicians must inspect factory equipment before every production shift.",
                    "paraphrase": "inspect = examine = check = scrutinize",
                    "alert": ""
                },
                {
                    "chunk": "an intimate knowledge of",
                    "meaning": "對……有極為精深透徹的了解",
                    "scenario": "The senior consultant possesses an intimate knowledge of local tax laws.",
                    "paraphrase": "intimate = profound = comprehensive = deep",
                    "alert": "商務高階考點：intimate knowledge 意指『透徹深入的知識』，非感情關係！"
                },
                {
                    "chunk": "comply with new legislation",
                    "meaning": "遵守最新通過的法規法令",
                    "scenario": "All pharmaceutical imports must comply with new legislation passed last month.",
                    "paraphrase": "legislation = law = statute = regulation",
                    "alert": ""
                },
                {
                    "chunk": "a lucrative business venture",
                    "meaning": "一項利潤極為豐厚的商業投資",
                    "scenario": "Investing in biotechnology proved to be a highly lucrative business venture.",
                    "paraphrase": "lucrative = profitable = rewarding",
                    "alert": ""
                },
                {
                    "chunk": "display imported merchandise",
                    "meaning": "陳列展示進口商品",
                    "scenario": "The boutique set up glass counters to display imported merchandise neatly.",
                    "paraphrase": "merchandise = goods = products = commodities",
                    "alert": "不可數名詞：merchandise 為不可數名詞，不可加 s！"
                },
                {
                    "chunk": "mundane administrative tasks",
                    "meaning": "繁瑣平凡的例行行政事務",
                    "scenario": "Automating mundane administrative tasks frees up time for strategic planning.",
                    "paraphrase": "mundane = routine = tedious = everyday",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "不可數商品名詞三劍客：merchandise vs equipment vs baggage",
                "rule_1": "👀 merchandise / equipment / luggage / baggage / furniture ➔ 100% 不可數名詞！",
                "rule_2": "👀 前方絕不可加 a/an，字尾絕不可加 -s！（例如 an equipment ❌, merchandises ❌）",
                "golden_rule": "⚡ 教練金句：看到 merchandise 帶 s 直接判出局！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "The new tariff policy has turned the domestic manufacturing industry into a highly ________ market for investors.",
                    "options": {
                        "A": "lucrative",
                        "B": "lucratively",
                        "C": "lucrativeness",
                        "D": "lucre"
                    },
                    "answer": "A",
                    "analysis": "a highly ________ market（冠詞 + 副詞 + 空格 + 名詞），空格需要形容詞。lucrative（有利可圖的/賺錢的）。故選 (A)。",
                    "translation": "新的關稅政策使國內製造業成為對投資者而言利潤極為豐厚的市場。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "All returned ________ must be cataloged in the inventory tracking database within 24 hours.",
                    "options": {
                        "A": "merchandises",
                        "B": "merchandise",
                        "C": "merchandising",
                        "D": "merchant"
                    },
                    "answer": "B",
                    "analysis": "修飾詞 returned 後接名詞受詞，指被退回的商品。merchandise 為不可數名詞，不加 s，故選 (B)。",
                    "translation": "所有退回的商品必須在 24 小時內登錄於庫存追蹤資料庫中。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "The candidate was selected because of her ________ knowledge of regional maritime trade regulations.",
                    "options": {
                        "A": "intimate",
                        "B": "intimately",
                        "C": "intimacy",
                        "D": "intimidation"
                    },
                    "answer": "A",
                    "analysis": "修飾名詞 knowledge 需用形容詞，an intimate knowledge of 表示『對……有透徹精闢的了解』。故選 (A)。",
                    "translation": "該候選人因對區域海事貿易法規具有深厚透徹的了解而獲選。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "The contract turned out to be extremely ________ [有利可圖的/賺錢的].",
                    "clue": "l 開頭形容詞，指利潤豐厚",
                    "answer": "lucrative"
                },
                {
                    "prompt": "Unsold ________ [不可數名詞：商品] will be stored in warehouse B.",
                    "clue": "m 開頭不可數名詞",
                    "answer": "merchandise"
                },
                {
                    "prompt": "She has an ________ [精深熟稔的] understanding of tax codes.",
                    "clue": "i 開頭形容詞，表示深入透徹",
                    "answer": "intimate"
                },
                {
                    "prompt": "The firm plans to ________ [啟動] legal proceedings tomorrow.",
                    "clue": "i 開頭動詞，發起啟動",
                    "answer": "initiate"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "The new safety ________ requires all builders to wear reinforced hard hats.",
                    "options": {
                        "A": "legislate",
                        "B": "legislation",
                        "C": "legislator",
                        "D": "legislative"
                    },
                    "answer": "B",
                    "trap_point": "主詞位置填名詞！legislation（法規）vs legislator（立法委員）。",
                    "analysis": "句中動詞為 requires，主詞指法規法案本身，選 (B) legislation。"
                },
                {
                    "id": 2,
                    "question": "Staff spent the morning completing ________ paperwork before the executive meeting.",
                    "options": {
                        "A": "mundane",
                        "B": "mundanely",
                        "C": "mundaneness",
                        "D": "mundanity"
                    },
                    "answer": "A",
                    "trap_point": "修飾名詞 paperwork 需用形容詞！",
                    "analysis": "mundane paperwork 表日常繁瑣的文書工作，選形容詞 (A) mundane。"
                }
            ],
            "part7": {
                "text_type": "Retail Partnership Memorandum (零售夥伴合作備忘錄)",
                "title": "Consignment Terms for Artisanal Merchandise",
                "content": "To: Consignment Vendors\nFrom: Metropolitan Goods\nDate: November 18\n\nMetropolitan Goods agrees to display vendor handcrafted merchandise in our prime downtown showroom. Vendors will receive 70% of gross proceeds from all sales executed through our registers.\n\n*Exceptional Clause: All defective or unsold goods will be returned to the vendor at the end of each fiscal quarter at no restocking penalty, except when inventory loss is proven to stem from transit packaging negligence on the part of the vendor.",
                "questions": [
                    {
                        "question": "What percentage of sales revenue is paid to consignment vendors?",
                        "options": {
                            "A": "30%",
                            "B": "50%",
                            "C": "70%",
                            "D": "100%"
                        },
                        "answer": "C",
                        "radar": "🔍 防漏看雷達：第一段第二句清楚數字 'Vendors will receive 70% of gross proceeds'！",
                        "analysis": "備忘錄第一段寫明廠商可獲得總銷售額的 70%，故選 (C)。"
                    },
                    {
                        "question": "Under what circumstance might a vendor be penalized for returned items?",
                        "options": {
                            "A": "If the merchandise fails to sell within 30 days.",
                            "B": "When damage results from inadequate shipping packaging.",
                            "C": "If the boutique fails to meet its sales quota.",
                            "D": "Whenever items are sold at a holiday discount."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：除外條款 'except when inventory loss is proven to stem from transit packaging negligence'！",
                        "analysis": "末尾重要除外條款：原則上不收懲罰金，但若損失可歸咎於廠商運送包裝疏忽時則除外，故選 (B)。"
                    }
                ]
            }
        }
    },
    16: {
        "day": 16,
        "date": "11/19",
        "phase": 2,
        "phase_name": "860 金色證書進階擴充與同義字轉換",
        "topic": "時間軸與變更陷阱 ｜ 取得、佔用與新生訓練",
        "morning": {
            "chunks": [
                {
                    "chunk": "obtainable through distributors",
                    "meaning": "可透過經銷商取得",
                    "scenario": "Replacement parts are easily obtainable through authorized regional distributors.",
                    "paraphrase": "obtainable = available = accessible",
                    "alert": ""
                },
                {
                    "chunk": "occupy the top floor",
                    "meaning": "進駐佔據頂樓空間",
                    "scenario": "The multinational law firm will occupy the top two floors of the tower.",
                    "paraphrase": "occupy = inhabit = take up = reside in",
                    "alert": ""
                },
                {
                    "chunk": "employee orientation session",
                    "meaning": "新進員工培訓說明會",
                    "scenario": "All new hires must attend the orientation session this coming Monday.",
                    "paraphrase": "orientation = induction = introduction = training",
                    "alert": ""
                },
                {
                    "chunk": "broaden community outreach",
                    "meaning": "擴大社區關懷與外展服務",
                    "scenario": "The non-profit launched medical clinics to broaden community outreach.",
                    "paraphrase": "outreach = involvement = engagement",
                    "alert": ""
                },
                {
                    "chunk": "perceive as a strength",
                    "meaning": "視為一項競爭優勢",
                    "scenario": "Clients perceive our 24/7 customer support as a major operational strength.",
                    "paraphrase": "perceive = view = regard = consider",
                    "alert": ""
                },
                {
                    "chunk": "neatly arranged files",
                    "meaning": "整齊排列的文件檔案",
                    "scenario": "Auditors were impressed by the neatly arranged financial records.",
                    "paraphrase": "neatly = tidily = orderly = methodically",
                    "alert": ""
                },
                {
                    "chunk": "numerous complaints received",
                    "meaning": "收到眾多的客戶投訴",
                    "scenario": "The customer care division logged numerous complaints regarding the delay.",
                    "paraphrase": "numerous = many = countless = multiple",
                    "alert": "文法考點：numerous 修飾可數複數名詞！修飾不可數請用 much / considerable。"
                }
            ],
            "visual_anchor": {
                "title": "修飾詞可數與不可數快速二分法",
                "rule_1": "👀 后方是【可數複數名詞 (complaints, items, branches)】➔ 選 numerous / many / few",
                "rule_2": "👀 后方是【不可數名詞 (information, equipment, advice, damage)】➔ 選 considerable / much / little",
                "golden_rule": "⚡ 教練金句：看到名詞帶 s 找 numerous，名詞光禿禿找 considerable！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "Tickets for the international economic forum are ________ online through the official ticketing portal.",
                    "options": {
                        "A": "obtain",
                        "B": "obtainable",
                        "C": "obtainably",
                        "D": "obtainment"
                    },
                    "answer": "B",
                    "analysis": "be 動詞 are 後面需形容詞作主詞補語。obtainable（可取得的 / 可買到的）。故選 (B)。",
                    "translation": "國際經濟論壇的門票可透過官方售票網站線上取得。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "The HR director scheduled an ________ session for recent college graduates joining the company.",
                    "options": {
                        "A": "orient",
                        "B": "orientation",
                        "C": "orientated",
                        "D": "orienting"
                    },
                    "answer": "B",
                    "analysis": "複合名詞 orientation session（新生培訓說明會），多益最高頻商務名詞之一。故選 (B)。",
                    "translation": "人力資源總監為剛加入公司的大學畢業生安排了一場到職培訓會。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "Management received ________ inquiries regarding the proposed change in remote work policies.",
                    "options": {
                        "A": "numerous",
                        "B": "much",
                        "C": "amount of",
                        "D": "little"
                    },
                    "answer": "A",
                    "analysis": "後方受詞為 inquiries（複數可數名詞），修飾可數名詞用 (A) numerous。(B) much、(C) amount of、(D) little 均只能修飾不可數名詞。",
                    "translation": "管理層收到了許多關於遠距辦公政策擬議變更的詢問。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "The manual is ________ [可取得的] in digital format.",
                    "clue": "o 開頭形容詞，同義 available",
                    "answer": "obtainable"
                },
                {
                    "prompt": "All new hires must attend employee ________ [培訓說明會].",
                    "clue": "o 開頭名詞，到職說明",
                    "answer": "orientation"
                },
                {
                    "prompt": "She received ________ [眾多的] awards for engineering excellence.",
                    "clue": "n 開頭形容詞，修飾複數名詞",
                    "answer": "numerous"
                },
                {
                    "prompt": "The office was ________ [整齊地] organized by the receptionist.",
                    "clue": "n 開頭副詞，乾淨整齊地",
                    "answer": "neatly"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "The corporate headquarters will ________ four consecutive floors in the new skyscraper.",
                    "options": {
                        "A": "occupy",
                        "B": "occupation",
                        "C": "occupant",
                        "D": "occupational"
                    },
                    "answer": "A",
                    "trap_point": "will + [原形動詞] + 受詞 four floors！",
                    "analysis": "will 後接動詞原形，occupy four floors 表進駐佔用四個樓層，選 (A)。"
                },
                {
                    "id": 2,
                    "question": "Customer service representatives are trained to ________ customer frustration capably.",
                    "options": {
                        "A": "perceive",
                        "B": "perceptive",
                        "C": "perception",
                        "D": "perceptibly"
                    },
                    "answer": "A",
                    "trap_point": "to + [原形動詞] + customer frustration。",
                    "analysis": "不定詞結構接原形動詞，perceive frustration 表敏銳察覺客戶沮喪情緒，故選 (A)。"
                }
            ],
            "part7": {
                "text_type": "Event Rescheduling Notice (活動時間變更通知)",
                "title": "New Hire Orientation and Tech Distribution Schedule",
                "content": "To: November Onboarding Cohort\nFrom: Talent Operations\nDate: November 19\n\nPlease note that the orientation session originally slated for Thursday at 9:00 AM in Conference Room 2B has been moved to Friday at 10:30 AM in the Main Plaza Auditorium. This adjustment allows IT technicians to neatly configure company laptops prior to distribution.\n\n*Important Schedule Condition: ID badge photo sessions will take place immediately following Friday's orientation. Staff members unable to attend Friday's rescheduled session must complete a self-paced orientation module online before 5:00 PM on Friday.",
                "questions": [
                    {
                        "question": "When will the rescheduled orientation session take place?",
                        "options": {
                            "A": "Thursday at 9:00 AM.",
                            "B": "Thursday at 10:30 AM.",
                            "C": "Friday at 9:00 AM.",
                            "D": "Friday at 10:30 AM."
                        },
                        "answer": "D",
                        "radar": "🔍 防漏看雷達：時間變更陷阱！'originally slated for Thursday... moved to Friday at 10:30 AM'！",
                        "analysis": "原定週四，但通知明確指出已改期至週五上午 10:30（Friday at 10:30 AM），故選 (D)。"
                    },
                    {
                        "question": "What must employees do if they miss Friday's live orientation?",
                        "options": {
                            "A": "Submit an appeal to Talent Operations.",
                            "B": "Complete an online training module by 5:00 PM Friday.",
                            "C": "Re-apply for their employee badge in December.",
                            "D": "Wait for the January orientation cohort."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：星號附註條件 'unable to attend Friday's rescheduled session must complete a self-paced orientation module online before 5:00 PM on Friday'！",
                        "analysis": "末尾重要條件清楚指出：無法參加者必須在週五下午 5 點前完成線上培訓模組，故選 (B)。"
                    }
                ]
            }
        }
    },
    17: {
        "day": 17,
        "date": "11/20",
        "phase": 2,
        "phase_name": "860 金色證書進階擴充與同義字轉換",
        "topic": "星號小字與折扣資格 ｜ 聲望、地緣親近與精確",
        "morning": {
            "chunks": [
                {
                    "chunk": "a prestigious award",
                    "meaning": "一項享譽盛名的殊榮",
                    "scenario": "The senior architect received a prestigious award for green urban design.",
                    "paraphrase": "prestigious = renowned = acclaimed = esteemed",
                    "alert": ""
                },
                {
                    "chunk": "in close proximity to",
                    "meaning": "鄰近於 / 距離……極近",
                    "scenario": "The warehouse is strategically located in close proximity to the seaport.",
                    "paraphrase": "in close proximity to = close to = near = adjacent to",
                    "alert": "商務必考片語：in close proximity to + 名詞！"
                },
                {
                    "chunk": "the sole proprietor",
                    "meaning": "獨資企業主 / 唯一業主",
                    "scenario": "Mr. Higgins is the sole proprietor of the downtown specialty bakery.",
                    "paraphrase": "proprietor = owner = possessor",
                    "alert": ""
                },
                {
                    "chunk": "preserve architectural integrity",
                    "meaning": "維護並保存建築的完整性",
                    "scenario": "Renovations were planned carefully to preserve architectural integrity.",
                    "paraphrase": "preserve = protect = maintain = conserve",
                    "alert": ""
                },
                {
                    "chunk": "the principal reason",
                    "meaning": "最主要的原因",
                    "scenario": "High reliability was the principal reason why clients selected our software.",
                    "paraphrase": "principal = primary = main = chief",
                    "alert": "易混淆：principal (adj.) 主要的 / (n.) 校長 vs. principle (n.) 原則！"
                },
                {
                    "chunk": "prompt reply required",
                    "meaning": "需要即時的回覆",
                    "scenario": "Due to tight printing schedules, a prompt reply is required by 3:00 PM.",
                    "paraphrase": "prompt = swift = immediate = timely",
                    "alert": ""
                },
                {
                    "chunk": "precise calculations",
                    "meaning": "極其精準的計算數據",
                    "scenario": "Structural engineering demands precise calculations of wind load.",
                    "paraphrase": "precise = exact = accurate = meticulous",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "principal (主要的) vs. principle (原則)",
                "rule_1": "👀 principal (尾巴是 -pal) ➔ 當形容詞指「主要的」，當名詞指「校長」！",
                "rule_2": "👀 principle (尾巴是 -ple) ➔ 100% 名詞，指「原則 / 信條」！（on principle 基於原則）",
                "golden_rule": "⚡ 教練金句：修飾名詞選 -pal，堅持信條選 -ple！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "The research facility was deliberately built in close ________ to the university medical center.",
                    "options": {
                        "A": "proximate",
                        "B": "proximity",
                        "C": "proximately",
                        "D": "proximities"
                    },
                    "answer": "B",
                    "analysis": "固定片語秒殺：in close proximity to（鄰近於……）。proximity 為名詞，表接近/鄰近。故選 (B)。",
                    "translation": "該研究設施刻意建造在緊鄰大學醫學中心之處。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "Cost efficiency was the ________ factor that influenced our decision to outsource assembly.",
                    "options": {
                        "A": "principle",
                        "B": "principal",
                        "C": "principled",
                        "D": "principality"
                    },
                    "answer": "B",
                    "analysis": "修飾名詞 factor（因素）需用形容詞，表示『主要的因素』，選 (B) principal。(A) principle 只能當名詞（原則）。",
                    "translation": "成本效益是影響我們決定將組裝外包的主要因素。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "The university recognized Professor Miller for her ________ contributions to renewable chemistry.",
                    "options": {
                        "A": "prestige",
                        "B": "prestigious",
                        "C": "prestigiously",
                        "D": "prestigeful"
                    },
                    "answer": "B",
                    "analysis": "修飾名詞 contributions 需用形容詞，prestigious contributions（享有盛譽的卓越貢獻）。故選 (B)。",
                    "translation": "該大學表彰米勒教授在綠色化學領域所做出的卓越盛譽貢獻。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "Our factory is in close ________ [鄰近於] to the harbor.",
                    "clue": "p 開頭名詞，與 in close... to 連用",
                    "answer": "proximity (in close proximity to)"
                },
                {
                    "prompt": "Quality assurance is our ________ [主要的] operational concern.",
                    "clue": "p 開頭形容詞，指主要的",
                    "answer": "principal"
                },
                {
                    "prompt": "The founder is the sole ________ [企業業主/老闆] of the firm.",
                    "clue": "p 開頭名詞，同義 owner",
                    "answer": "proprietor"
                },
                {
                    "prompt": "We appreciate your ________ [即時迅速的] response to our inquiry.",
                    "clue": "p 開頭形容詞，即刻快速的",
                    "answer": "prompt"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "The committee established strict ethical ________ for clinical experimentation.",
                    "options": {
                        "A": "principals",
                        "B": "principles",
                        "C": "principally",
                        "D": "principled"
                    },
                    "answer": "B",
                    "trap_point": "道德準則/原則 ➔ principles！",
                    "analysis": "ethical principles 表『倫理原則』。principals 指校長或主要當事人，語意不合。選 (B)。"
                },
                {
                    "id": 2,
                    "question": "The historic facade must be ________ with utmost care during construction.",
                    "options": {
                        "A": "preserve",
                        "B": "preserved",
                        "C": "preserving",
                        "D": "preservation"
                    },
                    "answer": "B",
                    "trap_point": "must be + [過去分詞]！建築外觀被妥善維護保存。",
                    "analysis": "be 動詞後接被動態過去分詞 preserved，選 (B)。"
                }
            ],
            "part7": {
                "text_type": "Commercial Office Lease Brochure (商辦租賃行銷手冊)",
                "title": "Summit Plaza: Premium Executive Office Suites",
                "content": "Summit Plaza offers premier office leasing in close proximity to Metro Station 4. Designed by an acclaimed architectural firm, the building blends prestigious contemporary style with energy-efficient systems.\n\n*Special Introductory Incentive: Tenants signing a minimum two-year lease by December 15 are entitled to one month of complimentary rent. \n\n*Fine Print Restriction: This promotion applies solely to primary proprietors and new commercial tenants. Existing leaseholders seeking internal suite relocations are explicitly exempted from this rebate.",
                "questions": [
                    {
                        "question": "What is mentioned as a key benefit of Summit Plaza's location?",
                        "options": {
                            "A": "It is located next to an international airport.",
                            "B": "It is situated near a metro station.",
                            "C": "It overlooks a historic municipal park.",
                            "D": "It offers free rooftop commuter shuttle pads."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：Paraphrase 同義替換！'in close proximity to Metro Station 4' ＝ 'situated near a metro station'！",
                        "analysis": "第一段首句即指出鄰近捷運四號站（in close proximity to Metro Station 4），故選 (B)。"
                    },
                    {
                        "question": "Who is ineligible for the one-month free rent promotion?",
                        "options": {
                            "A": "Companies signing two-year leases.",
                            "B": "New commercial tenants moving in from abroad.",
                            "C": "Current building tenants relocating to a different suite.",
                            "D": "Sole proprietors opening their first office."
                        },
                        "answer": "C",
                        "radar": "🔍 防漏看雷達：小字除外限制 Fine Print Restriction！'Existing leaseholders seeking internal suite relocations are explicitly exempted from this rebate'！",
                        "analysis": "文末細則明確將『欲在內部更換辦公室的既有承租戶（Existing leaseholders seeking internal suite relocations）』排除在外，故選 (C)。"
                    }
                ]
            }
        }
    },
    18: {
        "day": 18,
        "date": "11/21",
        "phase": 2,
        "phase_name": "860 金色證書進階擴充與同義字轉換",
        "topic": "Phase 2 大驗收 ｜ 諮詢、限制與嚴格規範",
        "morning": {
            "chunks": [
                {
                    "chunk": "submit a formal query",
                    "meaning": "提出正式的業務諮詢",
                    "scenario": "Clients may submit a formal query regarding billing discrepancies.",
                    "paraphrase": "query = inquiry = question",
                    "alert": ""
                },
                {
                    "chunk": "restrict vehicle access",
                    "meaning": "限制車輛通行權限",
                    "scenario": "Security will restrict vehicle access to authorized delivery vans only.",
                    "paraphrase": "restrict = limit = confine = curb",
                    "alert": ""
                },
                {
                    "chunk": "undergo rigorous testing",
                    "meaning": "接受極度嚴格的品管測試",
                    "scenario": "Every medical monitor must undergo rigorous testing prior to distribution.",
                    "paraphrase": "rigorous = stringent = strict = demanding",
                    "alert": ""
                },
                {
                    "chunk": "reveal the survey results",
                    "meaning": "公布消費者調查結果",
                    "scenario": "The research team will reveal the survey results at tomorrow's press briefing.",
                    "paraphrase": "reveal = disclose = unveil = publish",
                    "alert": ""
                },
                {
                    "chunk": "revise the draft agreement",
                    "meaning": "修改合約草案內容",
                    "scenario": "Corporate legal counsel was instructed to revise the draft agreement.",
                    "paraphrase": "revise = amend = modify = update",
                    "alert": ""
                },
                {
                    "chunk": "a run-down building",
                    "meaning": "一棟年久失修的老舊建築",
                    "scenario": "The development group purchased a run-down building to transform it into lofts.",
                    "paraphrase": "run-down = dilapidated = neglected = deteriorated",
                    "alert": ""
                },
                {
                    "chunk": "performed rather well",
                    "meaning": "表現得相當出色",
                    "scenario": "Despite fierce regional competition, the local division performed rather well.",
                    "paraphrase": "rather well = fairly well = quite impressively",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "「嚴格嚴謹」形容詞三劍客：rigorous vs. stringent vs. strict",
                "rule_1": "👀 看到 tests / inspection / audit ➔ 最常搭配 rigorous / stringent（嚴格的）！",
                "rule_2": "👀 看到 guidelines / laws / standards ➔ 同義替換找 strict / stringent！",
                "golden_rule": "⚡ 教練金句：嚴格測試找 rigorous，嚴格法令找 stringent！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "Before any automotive model is certified for mass production, it must pass ________ safety trials.",
                    "options": {
                        "A": "rigorous",
                        "B": "rigorously",
                        "C": "rigor",
                        "D": "rigorousness"
                    },
                    "answer": "A",
                    "analysis": "修飾名詞 safety trials（安全測試）需用形容詞，rigorous safety trials（嚴格的安全試驗）。故選 (A)。",
                    "translation": "任何汽車車型在獲准量產之前，都必須通過嚴格的安全測試。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "The spokesperson declined to ________ the exact acquisition price until the regulatory audit concludes.",
                    "options": {
                        "A": "restrict",
                        "B": "reveal",
                        "C": "revise",
                        "D": "refurbish"
                    },
                    "answer": "B",
                    "analysis": "語意搭配：declined to reveal the exact price（拒絕透露具體收購金額）。restrict 限制；revise 修改；refurbish 翻新。故選 (B)。",
                    "translation": "發言人拒絕在監管審查結束之前透露具體的收購價格。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "If you have any ________ concerning the revised invoice, please reach out to accounts payable.",
                    "options": {
                        "A": "queries",
                        "B": "querying",
                        "C": "queried",
                        "D": "querist"
                    },
                    "answer": "A",
                    "analysis": "any 後接可數名詞複數 queries（疑問 / 諮詢）。concerning 為介系詞表關於。故選 (A)。",
                    "translation": "若您對修改後的發票有任何疑問，請聯絡應付帳款部門。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "The lab subjected the vaccine to ________ [嚴謹嚴格的] testing.",
                    "clue": "r 開頭形容詞，同義 strict",
                    "answer": "rigorous"
                },
                {
                    "prompt": "The developer converted the ________ [年久失修破舊的] warehouse into luxury lofts.",
                    "clue": "複合形容詞，r 開頭",
                    "answer": "run-down"
                },
                {
                    "prompt": "The CEO refused to ________ [透露/公開] future dividend forecasts.",
                    "clue": "r 開頭動詞，同義 disclose",
                    "answer": "reveal"
                },
                {
                    "prompt": "Please direct any technical ________ [諮詢/問題] to our helpdesk.",
                    "clue": "q 開頭名詞複數",
                    "answer": "queries"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "Access to the server room is strictly ________ to authorized network engineers.",
                    "options": {
                        "A": "restrict",
                        "B": "restricted",
                        "C": "restricting",
                        "D": "restriction"
                    },
                    "answer": "B",
                    "trap_point": "be strictly restricted to（被嚴格限制在…）被動態！",
                    "analysis": "is + strictly + [過去分詞] + to，表通行權限受限於特定人士，選 (B) restricted。"
                },
                {
                    "id": 2,
                    "question": "The legal department had to ________ the partnership clause three times.",
                    "options": {
                        "A": "revise",
                        "B": "revision",
                        "C": "revising",
                        "D": "revised"
                    },
                    "answer": "A",
                    "trap_point": "had to + [原形動詞]！",
                    "analysis": "had to 後接動詞原形 revise（修改修訂），選 (A)。"
                }
            ],
            "part7": {
                "text_type": "Quality Audit Memorandum (品管稽核內部備忘錄)",
                "title": "Annual Laboratory Certification and Device Rigor",
                "content": "To: Manufacturing Engineers\nFrom: Regulatory Compliance Bureau\nDate: November 21\n\nAll automated robotic arms currently installed in Plant 4 must undergo rigorous re-calibration to comply with updated international safety thresholds. Technical staff will restrict access to Assembly Floor B starting tomorrow morning at 8:00 AM.\n\n*Inquiry Protocol: Personnel with specific technical queries regarding calibrating equipment may contact Lead Engineer Marcus Vance. All questions must be submitted via the internal portal rather than by email to ensure transparent logging.",
                "questions": [
                    {
                        "question": "Why is access to Assembly Floor B being restricted?",
                        "options": {
                            "A": "To accommodate an executive client tour.",
                            "B": "To perform rigorous equipment re-calibration.",
                            "C": "Due to structural failure in the exterior facade.",
                            "D": "To install new employee orientation kiosks."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：原因定位 'undergo rigorous re-calibration... restrict access to Assembly Floor B'！",
                        "analysis": "備忘錄第一段說明為了對機器手臂進行嚴格重新校準，因而管制該樓層通行，故選 (B)。"
                    },
                    {
                        "question": "How must staff members submit technical queries?",
                        "options": {
                            "A": "Through direct phone calls to Marcus Vance.",
                            "B": "Via the internal electronic portal.",
                            "C": "By sending email messages to compliance.",
                            "D": "During the weekly department breakfast."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：除外細節 'must be submitted via the internal portal rather than by email'！rather than ＝ 而非！",
                        "analysis": "末尾重要指示規定必須透過內部網站（internal portal）提交疑問而非寄信，故選 (B)。"
                    }
                ]
            }
        }
    },
    19: {
        "day": 19,
        "date": "11/22",
        "phase": 3,
        "phase_name": "考前全真高壓實戰與防粗心特訓",
        "topic": "Part 5 極速衝刺 ｜ 策略計畫、部門板塊與唯一依據",
        "morning": {
            "chunks": [
                {
                    "chunk": "a bold marketing scheme",
                    "meaning": "一項大膽的行銷計畫",
                    "scenario": "The startup devised a bold marketing scheme to rival established competitors.",
                    "paraphrase": "scheme = plan = strategy = project",
                    "alert": ""
                },
                {
                    "chunk": "the public sector",
                    "meaning": "公家機關 / 公共部門領域",
                    "scenario": "Many technology firms now supply cloud services to the public sector.",
                    "paraphrase": "sector = domain = industry = sphere",
                    "alert": ""
                },
                {
                    "chunk": "severely disrupted by storms",
                    "meaning": "受到暴風雨極為嚴重的干擾",
                    "scenario": "Regional rail traffic was severely disrupted by weekend storms.",
                    "paraphrase": "severely = gravely = drastically = seriously",
                    "alert": ""
                },
                {
                    "chunk": "emphasize the simplicity of",
                    "meaning": "強調……的簡潔便利性",
                    "scenario": "The presentation emphasized the simplicity of our mobile check-in interface.",
                    "paraphrase": "simplicity = ease of use = clarity",
                    "alert": ""
                },
                {
                    "chunk": "an interactive slideshow",
                    "meaning": "互動式投影片簡報",
                    "scenario": "The trainer demonstrated the workflow using an interactive slideshow.",
                    "paraphrase": "slideshow = slide presentation",
                    "alert": ""
                },
                {
                    "chunk": "rely solely on donations",
                    "meaning": "完全僅僅依賴各界捐款",
                    "scenario": "The non-profit wildlife foundation relies solely on donations from the public.",
                    "paraphrase": "solely = exclusively = entirely = purely",
                    "alert": ""
                },
                {
                    "chunk": "scheduled training session",
                    "meaning": "排定舉行的培訓會議",
                    "scenario": "All branch staff are required to attend the scheduled training session.",
                    "paraphrase": "session = meeting = gathering = workshop",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "副詞秒殺：solely (僅僅/唯一地) ＝ exclusively",
                "rule_1": "👀 看到 rely / depend + ________ + on ➔ 80% 填入 solely / heavily / exclusively！",
                "rule_2": "👀 solely = only = exclusively，多益最愛放在動詞與介系詞中間考修飾！",
                "golden_rule": "⚡ 教練金句：看到 rely on 中間挖空，秒挑 solely！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "The community foundation depends ________ on corporate sponsorships to maintain its youth outreach programs.",
                    "options": {
                        "A": "sole",
                        "B": "solely",
                        "C": "soleness",
                        "D": "solitary"
                    },
                    "answer": "B",
                    "analysis": "depends ________ on（動詞與介系詞之間的夾心修飾位置，填入副詞）。solely 表『僅僅 / 完全只靠』。故選 (B)。",
                    "translation": "該社區基金會完全依靠企業贊助來維持其青年外展計畫。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "Flight departures were ________ delayed following an unexpected computer network glitch.",
                    "options": {
                        "A": "severely",
                        "B": "severe",
                        "C": "severity",
                        "D": "severeness"
                    },
                    "answer": "A",
                    "analysis": "were ________ delayed（被動態夾心餅乾，塞入副詞修飾 delayed）。severely 表『嚴重地』。故選 (A)。",
                    "translation": "在一場突發的電腦網路故障後，航班起飛受到了嚴重延誤。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "The software engineer redesigned the navigation bar to enhance the ________ of the application.",
                    "options": {
                        "A": "simple",
                        "B": "simplicity",
                        "C": "simplify",
                        "D": "simplistic"
                    },
                    "answer": "B",
                    "analysis": "the ________ of the application（冠詞 the 與介系詞 of 之間，100% 填入名詞）。simplicity（簡潔/單純）。故選 (B)。",
                    "translation": "軟體工程師重新設計了導航列，以提升該應用程式的簡潔易用度。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "Our funding depends ________ [完全僅限於] on government grants.",
                    "clue": "s 開頭副詞，同義 exclusively",
                    "answer": "solely"
                },
                {
                    "prompt": "Operations were ________ [嚴重地] hampered by the power outage.",
                    "clue": "s 開頭副詞，嚴重嚴厲地",
                    "answer": "severely"
                },
                {
                    "prompt": "The speaker delivered an inspiring ________ [幻燈片簡報].",
                    "clue": "s 開頭複合字，投影片秀",
                    "answer": "slideshow"
                },
                {
                    "prompt": "The renewable energy ________ [產業領域/板塊] experienced rapid expansion.",
                    "clue": "s 開頭名詞，同義 industry",
                    "answer": "sector"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "The developer introduced a new pension ________ for long-term employees.",
                    "options": {
                        "A": "scheme",
                        "B": "schema",
                        "C": "schematic",
                        "D": "scheming"
                    },
                    "answer": "A",
                    "trap_point": "pension scheme（退休金計畫方案）。",
                    "analysis": "pension scheme 為英式商務英文經典片語，表示退休金計畫方案。故選 (A)。"
                },
                {
                    "id": 2,
                    "question": "The keynote speaker summarized his findings during the closing ________.",
                    "options": {
                        "A": "session",
                        "B": "section",
                        "C": "sector",
                        "D": "segment"
                    },
                    "answer": "A",
                    "trap_point": "closing session（閉幕研討會/大會閉幕環節）。",
                    "analysis": "指會議的時段與環節，使用 session。故選 (A)。"
                }
            ],
            "part7": {
                "text_type": "Government Grant Proposal Notice (政府補助計畫公告)",
                "title": "Clean Energy Technology Grant Scheme - 2027",
                "content": "To: Clean Tech Innovators\nFrom: Department of Energy and Public Infrastructure\nDate: November 22\n\nThe Department has officially launched the Clean Energy Grant Scheme to encourage private sector investment in carbon-neutral manufacturing. Up to $2 million in matching funds is available per qualified firm.\n\n*Eligibility Criterion: Grants are awarded solely to organizations with verified domestic manufacturing facilities. Enterprises relying entirely on overseas contract manufacturing are strictly exempted from consideration.",
                "questions": [
                    {
                        "question": "What is the primary goal of the Clean Energy Grant Scheme?",
                        "options": {
                            "A": "To construct government-owned solar parks.",
                            "B": "To stimulate private investment in carbon-neutral factories.",
                            "C": "To train public sector employees in green logistics.",
                            "D": "To fund overseas battery assembly plants."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：主旨定位 'encourage private sector investment in carbon-neutral manufacturing'！stimulate ＝ encourage！",
                        "analysis": "第一段表明目的：鼓勵民間私營部門對碳中和製造進行投資，故選 (B)。"
                    },
                    {
                        "question": "Which business is NOT eligible to apply for this grant?",
                        "options": {
                            "A": "A domestic solar panel manufacturer.",
                            "B": "A local factory developing electric charging piles.",
                            "C": "A company manufacturing products exclusively abroad.",
                            "D": "An eco-friendly textile plant located in Chicago."
                        },
                        "answer": "C",
                        "radar": "🔍 防漏看雷達：星號附註排除條款 'Enterprises relying entirely on overseas contract manufacturing are strictly exempted'！",
                        "analysis": "末尾重要條件清楚排除完全依靠海外代工製造的企業，故選 (C)。"
                    }
                ]
            }
        }
    },
    20: {
        "day": 20,
        "date": "11/23",
        "phase": 3,
        "phase_name": "考前全真高壓實戰與防粗心特訓",
        "topic": "Part 6 插入句前後脈絡 ｜ 有形資產、門檻與承租人",
        "morning": {
            "chunks": [
                {
                    "chunk": "subsequent market analysis",
                    "meaning": "隨後進行的市場分析",
                    "scenario": "A subsequent market analysis revealed a shift toward sustainable packaging.",
                    "paraphrase": "subsequent = following = later = succeeding",
                    "alert": ""
                },
                {
                    "chunk": "tangible business benefits",
                    "meaning": "切實可見的商業效益",
                    "scenario": "The new inventory software yielded tangible business benefits within months.",
                    "paraphrase": "tangible = concrete = measurable = real",
                    "alert": ""
                },
                {
                    "chunk": "protect tenant rights",
                    "meaning": "保障承租人 / 房客的權益",
                    "scenario": "The revised commercial lease agreement was designed to protect tenant rights.",
                    "paraphrase": "tenant = leaseholder = occupant = renter",
                    "alert": ""
                },
                {
                    "chunk": "cross the revenue threshold",
                    "meaning": "跨越營收設定門檻",
                    "scenario": "The startup was profitable once it crossed the annual revenue threshold.",
                    "paraphrase": "threshold = benchmark = limit = minimum level",
                    "alert": ""
                },
                {
                    "chunk": "manage current status",
                    "meaning": "控管目前的專案進度與狀態",
                    "scenario": "Team leads met every morning to track and manage current project status.",
                    "paraphrase": "status = state = condition = progress",
                    "alert": ""
                },
                {
                    "chunk": "subtraction of handling fees",
                    "meaning": "扣除各項手續費",
                    "scenario": "The net refund was calculated after the subtraction of handling fees.",
                    "paraphrase": "subtraction = deduction = withholding",
                    "alert": ""
                },
                {
                    "chunk": "somehow managed to finish",
                    "meaning": "不知何故/設法順利完成",
                    "scenario": "Despite the severe storm, the delivery team somehow managed to finish on time.",
                    "paraphrase": "somehow = by some means = in some way",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "subsequent (隨後的) vs. prior (先前的)",
                "rule_1": "👀 subsequent ➔ 指「後續的 / 接下來發生的」！（subsequent events 後續事件）",
                "rule_2": "👀 prior ➔ 指「先前的 / 在前的」！（prior experience 先前經驗）",
                "golden_rule": "⚡ 教練金句：看到事件前後發生，先 prior 後 subsequent！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "The initial launch was unsuccessful; however, ________ product revisions led to record-breaking sales.",
                    "options": {
                        "A": "subsequent",
                        "B": "subsequently",
                        "C": "subsequence",
                        "D": "subsequentness"
                    },
                    "answer": "A",
                    "analysis": "修飾名詞 product revisions 需用形容詞，subsequent 表示『隨後/後來進行的』。故選 (A)。",
                    "translation": "最初的發表並不成功；然而，後續的產品修改帶來了創紀錄的銷售額。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "The investment board requires ________ evidence of revenue growth before authorizing additional funding.",
                    "options": {
                        "A": "tangible",
                        "B": "tangibly",
                        "C": "tangibility",
                        "D": "tangibleness"
                    },
                    "answer": "A",
                    "analysis": "修飾名詞 evidence（證據）需用形容詞，tangible evidence 指『實質具體的證據』。故選 (A)。",
                    "translation": "投資委員會在核准額外資金之前，需要看到營收成長的實質具體證據。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "Corporate bonuses are only disbursed to managers who exceed their annual performance ________.",
                    "options": {
                        "A": "threshold",
                        "B": "subtraction",
                        "C": "simplicity",
                        "D": "aisle"
                    },
                    "answer": "A",
                    "analysis": "exceed their annual performance threshold（超越年度績效門檻）。threshold 表門檻/基準點，語意最合。故選 (A)。",
                    "translation": "企業獎金僅發放給超越年度績效門檻的經理人員。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "The project delivered ________ [實質具體的] results in six months.",
                    "clue": "t 開頭形容詞，看得見摸得著的",
                    "answer": "tangible"
                },
                {
                    "prompt": "The commercial ________ [承租人/房客] renewed the five-year lease.",
                    "clue": "t 開頭名詞，指租戶",
                    "answer": "tenant"
                },
                {
                    "prompt": "Sales reached the minimum qualifying ________ [門檻基準].",
                    "clue": "t 開頭名詞，門檻",
                    "answer": "threshold"
                },
                {
                    "prompt": "The meeting was cancelled; ________ [隨後的] discussions took place via email.",
                    "clue": "s 開頭形容詞，後來的",
                    "answer": "subsequent"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "The final statement reflects the net payout after the ________ of administrative fees.",
                    "options": {
                        "A": "subtraction",
                        "B": "subtract",
                        "C": "subtracting",
                        "D": "subtracted"
                    },
                    "answer": "A",
                    "trap_point": "the + [名詞] + of 結構！",
                    "analysis": "the subtraction of fees（手續費之扣除）。冠詞與介系詞中間填入名詞 (A) subtraction。"
                },
                {
                    "id": 2,
                    "question": "Please update the project ________ board before the daily standup meeting.",
                    "options": {
                        "A": "status",
                        "B": "statue",
                        "C": "stature",
                        "D": "statute"
                    },
                    "answer": "A",
                    "trap_point": "易混淆名詞：status（狀態）vs statue（雕像）vs statute（法規）！",
                    "analysis": "project status board 指專案進度看板，選 (A) status。"
                }
            ],
            "part7": {
                "text_type": "Commercial Property Management Notice (商用大樓物業通知)",
                "title": "Tenant Lease Renewal and Performance Incentives",
                "content": "To: All Commercial Plaza Tenants\nFrom: Apex Realty Asset Management\nDate: November 23\n\nApex Realty values long-term partnerships with our retail and office tenants. To reward thriving enterprises, tenants whose gross sales cross the annual threshold of $500,000 will be granted a 10% rebate on base rent for subsequent quarters.\n\n*Submission Guidelines: Gross sales documentation must be verified by an accredited public accountant. Statements submitted without official certification will be subject to the subtraction of all prospective promotional credits.",
                "questions": [
                    {
                        "question": "How can tenants qualify for a 10% rebate on base rent?",
                        "options": {
                            "A": "By signing a ten-year commercial lease.",
                            "B": "By generating more than $500,000 in gross sales.",
                            "C": "By paying annual maintenance dues in advance.",
                            "D": "By relocating to the top floor suites."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：門檻條件 'gross sales cross the annual threshold of $500,000'！",
                        "analysis": "第一段說明取得 10% 回饋的條件：總營業額跨越 50 萬美元門檻，故選 (B)。"
                    },
                    {
                        "question": "What is required for the sales statement to be accepted?",
                        "options": {
                            "A": "Verification by an accredited public accountant.",
                            "B": "Endorsement by the city trade council.",
                            "C": "Submission prior to November 1.",
                            "D": "Personal delivery to the building superintendent."
                        },
                        "answer": "A",
                        "radar": "🔍 防漏看雷達：星號附註要求 'must be verified by an accredited public accountant'！",
                        "analysis": "文末繳交指引明確載明：財務證明必須經過合格會計師查核認證，故選 (A)。"
                    }
                ]
            }
        }
    },
    21: {
        "day": 21,
        "date": "11/24",
        "phase": 3,
        "phase_name": "考前全真高壓實戰與防粗心特訓",
        "topic": "Part 7 雙篇交叉比對 ｜ 騰空撤離、有效期限與供應商",
        "morning": {
            "chunks": [
                {
                    "chunk": "a unanimous vote",
                    "meaning": "全體一致無異議通過的表決",
                    "scenario": "The board reached a unanimous vote to acquire the medical device manufacturer.",
                    "paraphrase": "unanimous = undisputed = in complete agreement",
                    "alert": ""
                },
                {
                    "chunk": "undergo extensive renovations",
                    "meaning": "經歷大規模全面整修",
                    "scenario": "The flagship retail store will undergo extensive renovations in January.",
                    "paraphrase": "undergo = experience = go through = endure",
                    "alert": ""
                },
                {
                    "chunk": "vacate the premises",
                    "meaning": "騰空並撤出該場所物業",
                    "scenario": "The tenant was required to vacate the premises upon lease expiration.",
                    "paraphrase": "vacate = leave = empty = abandon",
                    "alert": ""
                },
                {
                    "chunk": "a valid identification card",
                    "meaning": "一張有效的身分證件",
                    "scenario": "Visitors must present a valid identification card at the front security gate.",
                    "paraphrase": "valid = authentic = legitimate = current",
                    "alert": ""
                },
                {
                    "chunk": "various promotional strategies",
                    "meaning": "各式各樣的促銷策略",
                    "scenario": "The marketing department tested various promotional strategies across regions.",
                    "paraphrase": "various = diverse = numerous = assorted",
                    "alert": ""
                },
                {
                    "chunk": "a reliable external vendor",
                    "meaning": "一家值得信賴的外部供應商",
                    "scenario": "We contracted a reliable external vendor to handle server maintenance.",
                    "paraphrase": "vendor = supplier = provider = seller",
                    "alert": ""
                },
                {
                    "chunk": "upon lease termination",
                    "meaning": "合約終止屆滿之時",
                    "scenario": "Security deposits are returned within 30 days upon lease termination.",
                    "paraphrase": "termination = expiration = end = conclusion",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "vacate (撤離/空出) vs. vacant (空著的)",
                "rule_1": "👀 vacate ➔ 動詞原形（vacate the room 搬出房間）",
                "rule_2": "👀 vacant ➔ 形容詞（vacant position 職缺, vacant room 空房）",
                "golden_rule": "⚡ 教練金句：有動詞位置選 vacate，修飾名詞選 vacant！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "Outgoing tenants are contractually required to ________ the property by midnight on the final day of the month.",
                    "options": {
                        "A": "vacate",
                        "B": "vacant",
                        "C": "vacantly",
                        "D": "vacancy"
                    },
                    "answer": "A",
                    "analysis": "to + [動詞原形] + the property。vacate 表示『騰空撤出房屋物業』。故選 (A)。",
                    "translation": "合約要求搬遷房客必須在該月最後一天的午夜前騰空並撤出該物業。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "The merger proposal was approved following a ________ decision by the shareholder council.",
                    "options": {
                        "A": "unanimous",
                        "B": "unanimously",
                        "C": "unanimity",
                        "D": "unanimousness"
                    },
                    "answer": "A",
                    "analysis": "修飾名詞 decision（決策）需用形容詞，unanimous decision 指『全體一致的決議』。故選 (A)。",
                    "translation": "該併購提案在股東大會做出全體一致的決議後獲得通過。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "The parking pass is ________ for one full calendar year from the date of issuance.",
                    "options": {
                        "A": "valid",
                        "B": "validity",
                        "C": "validate",
                        "D": "validly"
                    },
                    "answer": "A",
                    "analysis": "be 動詞 is 後面需填形容詞作補語。valid 表示『有效的』。故選 (A)。",
                    "translation": "該停車證自發發之日起整整一個日曆年內有效。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "The board made a ________ [全體一致的] decision.",
                    "clue": "u 開頭形容詞，無異議的",
                    "answer": "unanimous"
                },
                {
                    "prompt": "Tenants must ________ [騰空搬出] the office before June 30.",
                    "clue": "v 開頭動詞，搬空撤出",
                    "answer": "vacate"
                },
                {
                    "prompt": "The coupon is no longer ________ [有效的].",
                    "clue": "v 開頭形容詞，有效的",
                    "answer": "valid"
                },
                {
                    "prompt": "The hospital will ________ [經歷/接受] a state health inspection.",
                    "clue": "u 開頭動詞，經歷接受",
                    "answer": "undergo"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "There are currently two ________ positions available in our accounting department.",
                    "options": {
                        "A": "vacant",
                        "B": "vacate",
                        "C": "vacated",
                        "D": "vacancy"
                    },
                    "answer": "A",
                    "trap_point": "修飾複數名詞 positions 需用形容詞 vacant（空缺的）！",
                    "analysis": "vacant positions 表職缺，選形容詞 (A) vacant。"
                },
                {
                    "id": 2,
                    "question": "The procurement team reached out to several potential ________ for raw aluminum supplies.",
                    "options": {
                        "A": "vendors",
                        "B": "vending",
                        "C": "vendor",
                        "D": "vended"
                    },
                    "answer": "A",
                    "trap_point": "several potential + [複數名詞]！",
                    "analysis": "several 修飾複數可數名詞 vendors（供應商），故選 (A)。"
                }
            ],
            "part7": {
                "text_type": "Double Passage: Lease Expiration Notice & Vendor Confirmation",
                "title": "Passage 1: Lease Termination Letter | Passage 2: Moving Vendor Confirmation",
                "content": "[Passage 1: Memo from Landlord]\nDear Mr. Sterling,\nYour commercial lease for Suite 402 at Horizon Tower expires on November 30. You must vacate the premises and return all keys by 5:00 PM on that date to be eligible for a full deposit return of $3,000.\n\n[Passage 2: SwiftMovers Booking Confirmation]\nCustomer: Mr. Sterling\nScheduled Move Date: November 29, 10:00 AM\nService Details: Packing and furniture transport for Suite 402 Horizon Tower to new offices in Midtown.\nStatus: Confirmed",
                "questions": [
                    {
                        "question": "Why did Mr. Sterling schedule his move for November 29?",
                        "options": {
                            "A": "To take advantage of weekend discount rates.",
                            "B": "To ensure the premises are vacated before his lease expires.",
                            "C": "Because the landlord requested early access.",
                            "D": "To avoid midtown rush-hour traffic."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：雙篇交叉比對！Passage 1 規定 11/30 必須搬空 ➔ Passage 2 預約 11/29 搬家，目的是為了在租約期滿前撤出以保證領回押金！",
                        "analysis": "比對第一篇的最後搬遷期限（11 月 30 日）與第二篇搬家預約（11 月 29 日），可知其目的是確保在合約期滿前搬空，故選 (B)。"
                    },
                    {
                        "question": "What must Mr. Sterling do on November 30 to get his $3,000 deposit back?",
                        "options": {
                            "A": "Pay an administrative termination fee.",
                            "B": "Hire an approved cleaning contractor.",
                            "C": "Return all office keys by 5:00 PM.",
                            "D": "Sign an extension for SwiftMovers."
                        },
                        "answer": "C",
                        "radar": "🔍 防漏看雷達：第一篇具體條件 'return all keys by 5:00 PM on that date to be eligible for a full deposit return'！",
                        "analysis": "第一篇明確指出領回保證金的條件：在當天下午 5:00 前歸還所有鑰匙，故選 (C)。"
                    }
                ]
            }
        }
    },
    22: {
        "day": 22,
        "date": "11/25",
        "phase": 3,
        "phase_name": "考前全真高壓實戰與防粗心特訓",
        "topic": "多義詞情境切換 ｜ coverage, condition, stock, conduct",
        "morning": {
            "chunks": [
                {
                    "chunk": "comprehensive insurance coverage",
                    "meaning": "全面的保險理賠範疇",
                    "scenario": "The policy provides comprehensive insurance coverage against flood damage.",
                    "paraphrase": "coverage = protection = insurance scope; (對比：media coverage 媒體報導)",
                    "alert": ""
                },
                {
                    "chunk": "in pristine condition",
                    "meaning": "保存得如同全新一般的狀態",
                    "scenario": "The leased equipment was returned in pristine condition.",
                    "paraphrase": "condition = state = shape; (對比：under the condition that 在…條件下)",
                    "alert": ""
                },
                {
                    "chunk": "stock the inventory shelves",
                    "meaning": "在存貨貨架上備貨補貨",
                    "scenario": "Workers arrived early to stock the inventory shelves before the black Friday sale.",
                    "paraphrase": "stock = supply = store = replenish; (對比：stock options 股票選擇權)",
                    "alert": ""
                },
                {
                    "chunk": "conduct a market survey",
                    "meaning": "執行一項市場問卷調查",
                    "scenario": "The brand engaged an agency to conduct a market survey in major cities.",
                    "paraphrase": "conduct = carry out = execute; (對比：code of conduct 行為準則)",
                    "alert": ""
                },
                {
                    "chunk": "promote to general manager",
                    "meaning": "晉升拔擢為總經理",
                    "scenario": "Ms. Harper was promoted to general manager after a stellar performance year.",
                    "paraphrase": "promote = advance = elevate; (對比：promote products 促銷產品)",
                    "alert": ""
                },
                {
                    "chunk": "delegate voting authority",
                    "meaning": "委派代理投票權限",
                    "scenario": "Shareholders unable to attend may delegate voting authority to a proxy.",
                    "paraphrase": "delegate = assign = entrust; (對比：conference delegate 與會代表)",
                    "alert": ""
                },
                {
                    "chunk": "under the current mandate",
                    "meaning": "在現行的政策授權命令下",
                    "scenario": "Under the current mandate, public buses must transition to electric engines.",
                    "paraphrase": "mandate = directive = order = authority",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "多義字瞬間切換指南",
                "rule_1": "👀 coverage ➔ 接 media 指「新聞報導」；接 policy / insurance 指「保險保障範圍」！",
                "rule_2": "👀 promote ➔ 接 person to 職位指「升職」；接 product / sale 指「行銷促銷」！",
                "golden_rule": "⚡ 教練金句：多義字看它身邊跟著誰，人升職、物促銷；媒報導、保險理賠！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "The commercial policy does not provide ________ for losses resulting from civil unrest.",
                    "options": {
                        "A": "coverage",
                        "B": "covering",
                        "C": "coverable",
                        "D": "cover"
                    },
                    "answer": "A",
                    "analysis": "名詞受詞：provide coverage for...（為……提供保險理賠保障）。故選 (A)。",
                    "translation": "該商業保單不為因內亂導致的損失提供保險保障。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "To ________ the holiday clearance sale, the marketing team ran digital banner advertisements across major news sites.",
                    "options": {
                        "A": "promote",
                        "B": "promotion",
                        "C": "promoted",
                        "D": "promoter"
                    },
                    "answer": "A",
                    "analysis": "To + [動詞原形] + the holiday clearance sale（不定詞表目的）。promote 搭配促銷活動，表『宣傳促銷』。故選 (A)。",
                    "translation": "為了宣傳節日清倉拍賣，行銷團隊在各大新聞網站投放了數位橫幅廣告。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "The executive committee will ________ an external audit into accounting irregularities.",
                    "options": {
                        "A": "conduct",
                        "B": "conducted",
                        "C": "conducting",
                        "D": "conductive"
                    },
                    "answer": "A",
                    "analysis": "will + [原形動詞] + an external audit。conduct an audit 表『執行審計稽核』。故選 (A)。",
                    "translation": "執行委員會將針對會計異常情況展開外部審計。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "The insurance policy includes full collision ________ [保險範圍].",
                    "clue": "c 開頭名詞，保險範圍",
                    "answer": "coverage"
                },
                {
                    "prompt": "She was ________ [升職] to director of international sales.",
                    "clue": "p 開頭動詞過去式，升遷",
                    "answer": "promoted"
                },
                {
                    "prompt": "The supermarket needs to ________ [備貨補貨] the shelves before evening.",
                    "clue": "s 開頭動詞，儲備備貨",
                    "answer": "stock"
                },
                {
                    "prompt": "The compliance team will ________ [執行] a rigorous security check.",
                    "clue": "c 開頭動詞，執行進行",
                    "answer": "conduct"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "All company employees are bound by the strict code of ________ outlined in the handbook.",
                    "options": {
                        "A": "conduct",
                        "B": "conduction",
                        "C": "conductive",
                        "D": "conductance"
                    },
                    "answer": "A",
                    "trap_point": "code of conduct（行為守則/規範）。",
                    "analysis": "固定名詞片語 code of conduct（員工行為守則），選 (A)。"
                },
                {
                    "id": 2,
                    "question": "Over 200 international ________ attended the climate summit in Geneva.",
                    "options": {
                        "A": "delegates",
                        "B": "delegations",
                        "C": "delegated",
                        "D": "delegating"
                    },
                    "answer": "A",
                    "trap_point": "delegates（與會代表，指人）vs delegations（代表團，指整體組織）。",
                    "analysis": "200 多名與會代表（可數人），選 (A) delegates。"
                }
            ],
            "part7": {
                "text_type": "Insurance Policy & Claim Inquiry (保險條款與理賠諮詢對話)",
                "title": "Commercial Fleet Insurance Policy Excerpt",
                "content": "Policyholder: Apex Logistics Inc.\nCoverage Section 4: Vehicle Loss and Damage\nThis policy provides comprehensive coverage for fleet vehicles operating under normal transport conditions. In the event of a collision, repairs conducted at certified network facilities are reimbursed 100% after a $500 deductible.\n\n*Special Exclusion: Coverage is explicitly void if damage occurs while a vehicle is operated by an unlisted driver or during deliberate off-road transit.",
                "questions": [
                    {
                        "question": "What is the policyholder required to pay for certified collision repairs?",
                        "options": {
                            "A": "The full repair cost up front.",
                            "B": "A $500 deductible.",
                            "C": "A 10% administrative surcharge.",
                            "D": "Nothing, as repairs are 100% complimentary."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：自負額細節 'reimbursed 100% after a $500 deductible'！",
                        "analysis": "條款明確寫出：在扣除 500 美元自負額（deductible）後，修車費用可獲得 100% 補償，故被保險人需自付 500 美元，選 (B)。"
                    },
                    {
                        "question": "Under what condition would an insurance claim be denied?",
                        "options": {
                            "A": "If the vehicle was damaged by severe hail.",
                            "B": "If repairs are completed within 48 hours.",
                            "C": "If an unlisted person was driving at the time of the incident.",
                            "D": "If the fleet has more than ten registered vans."
                        },
                        "answer": "C",
                        "radar": "🔍 防漏看雷達：星號除外條款 'Coverage is explicitly void if damage occurs while a vehicle is operated by an unlisted driver'！void ＝ denied！",
                        "analysis": "末尾重要除外規定指出：若車輛是由非登錄駕駛人（unlisted driver）所駕駛，理賠無效，故選 (C)。"
                    }
                ]
            }
        }
    },
    23: {
        "day": 23,
        "date": "11/26",
        "phase": 3,
        "phase_name": "考前全真高壓實戰與防粗心特訓",
        "topic": "Part 7 三篇閱讀獵殺 ｜ 資訊定位與反向排除",
        "morning": {
            "chunks": [
                {
                    "chunk": "cross-reference the data",
                    "meaning": "交叉比對各項數據",
                    "scenario": "Auditors cross-referenced the invoice data with the shipping receipts.",
                    "paraphrase": "cross-reference = verify = double-check",
                    "alert": ""
                },
                {
                    "chunk": "an unprecedented demand",
                    "meaning": "空前未有的巨大需求",
                    "scenario": "The new hybrid vehicle met with an unprecedented demand from consumers.",
                    "paraphrase": "unprecedented = unmatched = record-setting",
                    "alert": ""
                },
                {
                    "chunk": "streamline operational flow",
                    "meaning": "簡化並優化營運作業流程",
                    "scenario": "Adopting cloud ERP helped streamline operational flow across divisions.",
                    "paraphrase": "streamline = simplify = optimize",
                    "alert": ""
                },
                {
                    "chunk": "strictly confidential information",
                    "meaning": "極度機密的內部資訊",
                    "scenario": "Patent designs are classified as strictly confidential information.",
                    "paraphrase": "confidential = secret = classified = proprietary",
                    "alert": ""
                },
                {
                    "chunk": "contingent upon approval",
                    "meaning": "視核准結果而定 / 取決於",
                    "scenario": "The merger timeline is contingent upon approval by federal regulators.",
                    "paraphrase": "contingent upon = dependent on = subject to",
                    "alert": "金色必考片語：be contingent upon = be subject to = depend on！"
                },
                {
                    "chunk": "in compliance with standards",
                    "meaning": "完全符合各項法規標準",
                    "scenario": "The assembly plant operates in compliance with international green standards.",
                    "paraphrase": "in compliance with = in accordance with = conforming to",
                    "alert": ""
                },
                {
                    "chunk": "provisional project timeline",
                    "meaning": "臨時暫定的專案時程表",
                    "scenario": "The director presented a provisional project timeline during the kickoff.",
                    "paraphrase": "provisional = tentative = temporary",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "三篇閱讀獵殺法：先看題幹人名與數字，再回文精準定位！",
                "rule_1": "👀 遇到三篇閱讀，絕對不要從頭逐字讀到尾（時間必定爆炸）！",
                "rule_2": "👀 先看題目問題問誰（Mr. X）、問什麼日期/數字，直接跳到該篇比對！",
                "golden_rule": "⚡ 教練金句：三篇文章是一家人，答案往往在第一篇與第三篇的交會點！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "The signing of the corporate lease is ________ upon final inspection by the city fire marshal.",
                    "options": {
                        "A": "contingent",
                        "B": "contingence",
                        "C": "contingently",
                        "D": "contingency"
                    },
                    "answer": "A",
                    "analysis": "be ________ upon...（以……為條件 / 取決於）。contingent upon ＝ dependent upon。故選形容詞 (A) contingent。",
                    "translation": "商業租約的簽署取決於市消防局長的最終檢查結果。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "The manufacturing facility was modified to operate in strict ________ with international environmental accords.",
                    "options": {
                        "A": "comply",
                        "B": "compliant",
                        "C": "compliance",
                        "D": "compliantly"
                    },
                    "answer": "C",
                    "analysis": "in strict ________ with（介系詞與介系詞之間的受詞名詞）。in compliance with 表『遵守/符合』。故選 (C) compliance。",
                    "translation": "該製造設施已進行改造，以嚴格符合國際環境協議。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "The project managers distributed a ________ agenda subject to amendment by the board.",
                    "options": {
                        "A": "provision",
                        "B": "provisional",
                        "C": "provisionally",
                        "D": "provisos"
                    },
                    "answer": "B",
                    "analysis": "修飾名詞 agenda（議程）需用形容詞，provisional agenda 表『暫定議程』。故選 (B)。",
                    "translation": "專案經理分發了一份尚待董事會修改的暫定議程。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "The budget is contingent ________ [介系詞] board approval.",
                    "clue": "取決於……",
                    "answer": "upon (or on) (contingent upon)"
                },
                {
                    "prompt": "All waste disposal must be in ________ [遵守合規] with local laws.",
                    "clue": "in... with 遵守",
                    "answer": "compliance (in compliance with)"
                },
                {
                    "prompt": "The schedule is only ________ [暫定的/臨時的] at this stage.",
                    "clue": "p 開頭形容詞，同義 tentative",
                    "answer": "provisional"
                },
                {
                    "prompt": "The new technology met with ________ [空前未有的] acclaim.",
                    "clue": "u 開頭形容詞，史無前例的",
                    "answer": "unprecedented"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "The consulting firm helped ________ the company's internal logistics operations.",
                    "options": {
                        "A": "streamline",
                        "B": "streamlined",
                        "C": "streamlining",
                        "D": "streamliner"
                    },
                    "answer": "A",
                    "trap_point": "helped + (to) + [原形動詞]！",
                    "analysis": "help 後方可直接接動詞原形，helped streamline operations，故選 (A)。"
                },
                {
                    "id": 2,
                    "question": "All personnel must keep client financial records strictly ________.",
                    "options": {
                        "A": "confidential",
                        "B": "confident",
                        "C": "confidentiality",
                        "D": "confidentially"
                    },
                    "answer": "A",
                    "trap_point": "keep + 受詞 + [形容詞受詞補語]！confidential (機密的) vs confident (有自信的)。",
                    "analysis": "keep + records（受詞）+ strictly（副詞）+ [形容詞]。使紀錄保持機密，選 (A) confidential。"
                }
            ],
            "part7": {
                "text_type": "Triple Passage: Job Listing, Applicant Email, Interview Confirmation",
                "title": "Passage 1: Senior Auditor Posting | Passage 2: Cover Note | Passage 3: Interview Slot",
                "content": "[Passage 1: Job Spec]\nRequired Qualifications: Minimum 5 years of forensic accounting experience. CPA certification is mandatory. Candidates proficient in Spanish will receive priority consideration.\n\n[Passage 2: Email from Clara Gomez]\nDear Hiring Manager,\nI am applying for the Senior Auditor role. I have spent seven years in corporate risk auditing and hold an active CPA license. I am a native Spanish speaker and eager to contribute to your global team.\n\n[Passage 3: Automated HR Invitation]\nDear Ms. Gomez,\nYour credentials match our priority profile. We would like to invite you for an executive interview on Thursday at 2:00 PM.",
                "questions": [
                    {
                        "question": "Why did Clara Gomez receive a priority interview invitation?",
                        "options": {
                            "A": "She was recommended by the CEO.",
                            "B": "She has over ten years of auditing experience.",
                            "C": "She holds a CPA license and is fluent in Spanish.",
                            "D": "She completed an internal training workshop."
                        },
                        "answer": "C",
                        "radar": "🔍 防漏看雷達：三篇交叉比對！Passage 1 開出條件：CPA + Spanish 優先 ➔ Passage 2 Clara 具備 CPA 且是西班牙語母語者 ➔ Passage 3 證實其符合 priority profile！",
                        "analysis": "交叉比對第一篇與第二篇的條件，Clara 同時符合執照與語言優先條件，故選 (C)。"
                    },
                    {
                        "question": "What is Clara Gomez's total experience in risk auditing?",
                        "options": {
                            "A": "3 years.",
                            "B": "5 years.",
                            "C": "7 years.",
                            "D": "9 years."
                        },
                        "answer": "C",
                        "radar": "🔍 防漏看雷達：第二篇具體數字 'spent seven years in corporate risk auditing'！",
                        "analysis": "第二篇信件中 Clara 表明自己已擁有七年經驗（seven years），故選 (C)。"
                    }
                ]
            }
        }
    },
    24: {
        "day": 24,
        "date": "11/27",
        "phase": 3,
        "phase_name": "考前全真高壓實戰與防粗心特訓",
        "topic": "考前 48 小時錯題庫極速回放 ｜ 4 大盲區極速自檢",
        "morning": {
            "chunks": [
                {
                    "chunk": "oversee operations vs oversight",
                    "meaning": "監督營運 vs 疏忽遺漏",
                    "scenario": "The auditor was hired to oversee operations and eliminate any careless oversight.",
                    "paraphrase": "oversee (v.) 監督; oversight (n.) 疏忽",
                    "alert": "考前必背：oversee 是動詞；oversight 是名詞（疏忽）！"
                },
                {
                    "chunk": "eligible for vs entitled to",
                    "meaning": "符合……資格 vs 有權享受……",
                    "scenario": "Employees eligible for benefits are entitled to four weeks of annual leave.",
                    "paraphrase": "eligible for + N; entitled to + N / V",
                    "alert": ""
                },
                {
                    "chunk": "exempted from the duty",
                    "meaning": "免除此項職責/關稅",
                    "scenario": "Certain non-profit organizations are exempted from the duty.",
                    "paraphrase": "exempted from = excused from",
                    "alert": ""
                },
                {
                    "chunk": "compatible with the network",
                    "meaning": "與該網路完全相容",
                    "scenario": "All remote laptops must be compatible with the network security firewall.",
                    "paraphrase": "compatible with = consistent with",
                    "alert": ""
                },
                {
                    "chunk": "adhere strictly to rules",
                    "meaning": "嚴格遵守各項規範",
                    "scenario": "Contractors must adhere strictly to safety rules at all times.",
                    "paraphrase": "adhere to = abide by = comply with",
                    "alert": ""
                },
                {
                    "chunk": "refrain from interruptions",
                    "meaning": "請勿打斷發言 / 克制避免",
                    "scenario": "Attendees were asked to refrain from interruptions during the keynote.",
                    "paraphrase": "refrain from = avoid = abstain from",
                    "alert": ""
                },
                {
                    "chunk": "in spite of the delay",
                    "meaning": "儘管有所延遲（介系詞）",
                    "scenario": "In spite of the delay, customer satisfaction remained exceptionally high.",
                    "paraphrase": "in spite of = despite = regardless of",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "考前 48 小時四大秒殺條件金律",
                "rule_1": "1. 空格後【無動詞】➔ 介系詞（in spite of, despite, owing to, prior to）",
                "rule_2": "2. will / has + 空格 + 動詞 ➔ 夾心餅乾填【副詞 -ly】",
                "rule_3": "3. find / make / keep + 受詞 + 空格 ➔ 補語填【形容詞】",
                "golden_rule": "⚡ 教練金句：看到題目先看選項詞性，再抓句中核心動詞！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "________ the severe power outage, the automated backup system prevented any loss of financial data.",
                    "options": {
                        "A": "In spite of",
                        "B": "Although",
                        "C": "Even if",
                        "D": "Whereas"
                    },
                    "answer": "A",
                    "analysis": "空格後為 'the severe power outage'（名詞片語無動詞），唯一可放句首接名詞的只有介系詞 (A) In spite of。(B)、(C)、(D) 皆為從屬連接詞，後需接完整子句。",
                    "translation": "儘管遭遇嚴重停電，自動備份系統仍防止了任何財務資料的遺失。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "The supervisor discovered an accounting ________ that resulted in an inadvertent overpayment.",
                    "options": {
                        "A": "oversee",
                        "B": "oversight",
                        "C": "overseer",
                        "D": "overseeing"
                    },
                    "answer": "B",
                    "analysis": "an accounting ________（名詞受詞位置）。oversight 指『會計疏失 / 疏漏』，導致意外多付了錢。故選 (B)。",
                    "translation": "主管發現了一筆導致意外多付款項的會計疏失。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "Contractors are reminded to adhere ________ the building's hazardous waste disposal protocols.",
                    "options": {
                        "A": "to",
                        "B": "with",
                        "C": "in",
                        "D": "for"
                    },
                    "answer": "A",
                    "analysis": "adhere 固定搭配介系詞 to（遵守）。comply 接 with；abide 接 by。故選 (A)。",
                    "translation": "提醒承包商務必遵守該大樓的危險廢棄物處理規程。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "Staff members must refrain ________ [介系詞] sharing passwords.",
                    "clue": "克制避免",
                    "answer": "from (refrain from)"
                },
                {
                    "prompt": "She was chosen to ________ [監督] the regional marketing branch.",
                    "clue": "動詞，監督",
                    "answer": "oversee"
                },
                {
                    "prompt": "The discrepancy was due to an unfortunate ________ [疏失].",
                    "clue": "名詞，疏忽",
                    "answer": "oversight"
                },
                {
                    "prompt": "The product is compatible ________ [介系詞] legacy systems.",
                    "clue": "相容於",
                    "answer": "with (compatible with)"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "The newly hired analysts found the internal financial guidelines extremely ________.",
                    "options": {
                        "A": "informative",
                        "B": "informatively",
                        "C": "inform",
                        "D": "information"
                    },
                    "answer": "A",
                    "trap_point": "found + the guidelines（受詞）+ extremely（副詞）+ [形容詞受詞補語]！",
                    "analysis": "受詞補語填入形容詞 (A) informative（極具參考價值的/獲益良多的）。"
                },
                {
                    "id": 2,
                    "question": "The merger will ________ broaden our international distribution network.",
                    "options": {
                        "A": "drastic",
                        "B": "drastically",
                        "C": "drastical",
                        "D": "drasticness"
                    },
                    "answer": "B",
                    "trap_point": "will ________ broaden（夾心餅乾，塞副詞）！",
                    "analysis": "助動詞 will 與動詞原形 broaden 之間填入副詞 (B) drastically。"
                }
            ],
            "part7": {
                "text_type": "Exam Simulation Micro-Reading (考前全真防漏看微閱讀)",
                "title": "Corporate Conference Logistics and Refund Clause",
                "content": "To: All Global Summit Delegates\nFrom: International Trade Council\nDate: November 27\n\nAll registered attendees are entitled to admission for all keynote speeches and networking dinners between December 5 and December 7. Delegates requiring special dietary accommodations must notify the caterer prior to November 30.\n\n*Cancellation and Refund Policy: Registration fees are 100% refundable provided that formal cancellation is received at least 72 hours prior to the event commencement date. However, cancellations submitted after this threshold are subject to a mandatory 20% administrative deduction, with no exceptions granted.",
                "questions": [
                    {
                        "question": "What must delegates requiring special meals do?",
                        "options": {
                            "A": "Pay an extra catering surcharge.",
                            "B": "Contact the food service provider before November 30.",
                            "C": "Bring their own meals to the networking dinners.",
                            "D": "Apply for an exemption through the council."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：Paraphrase 同義替換！'notify the caterer prior to November 30' ＝ 'Contact the food service provider before November 30'！",
                        "analysis": "文中明確寫道飲食特殊需求者必須在 11 月 30 日前通知外燴廠商（caterer = food service provider），故選 (B)。"
                    },
                    {
                        "question": "What fee applies to registrations cancelled 48 hours before the event?",
                        "options": {
                            "A": "No fee is charged.",
                            "B": "A 10% processing penalty.",
                            "C": "A 20% administrative deduction.",
                            "D": "The full registration is non-refundable."
                        },
                        "answer": "C",
                        "radar": "🔍 防漏看雷達：時間門檻陷阱！48 小時少於 72 小時門檻 ➔ 'cancellations submitted after this threshold are subject to a mandatory 20% administrative deduction'！",
                        "analysis": "因為在活動前 48 小時取消已超過 72 小時早鳥門檻，依規定必須扣除 20% 行政手續費，故選 (C)。"
                    }
                ]
            }
        }
    },
    25: {
        "day": 25,
        "date": "11/28",
        "phase": 3,
        "phase_name": "考前全真高壓實戰與防粗心特訓",
        "topic": "考前 24 小時金色證書配速心法與實戰答題手冊",
        "morning": {
            "chunks": [
                {
                    "chunk": "pacing strategy for 860+",
                    "meaning": "突破 860 分的配速節奏策略",
                    "scenario": "A disciplined pacing strategy ensures you finish all 200 questions with 10 minutes to spare.",
                    "paraphrase": "pacing = time management = speed control",
                    "alert": ""
                },
                {
                    "chunk": "maintain mental composure",
                    "meaning": "保持沈著冷靜的應考心理素質",
                    "scenario": "Top scorers maintain mental composure even when encountering unfamiliar vocabulary.",
                    "paraphrase": "composure = calm = serenity = poise",
                    "alert": ""
                },
                {
                    "chunk": "rule out incorrect options",
                    "meaning": "反向排除錯誤選項",
                    "scenario": "When stuck between two choices, rule out incorrect options based on grammatical anchors.",
                    "paraphrase": "rule out = eliminate = dismiss",
                    "alert": ""
                },
                {
                    "chunk": "scan the questions first",
                    "meaning": "先快速掃描題目與關鍵字",
                    "scenario": "In Part 7, always scan the questions first before diving into lengthy business memos.",
                    "paraphrase": "scan = skim = preview",
                    "alert": ""
                },
                {
                    "chunk": "verify the fine print",
                    "meaning": "特別檢查星號與除外附註",
                    "scenario": "High-scoring test takers verify the fine print to avoid missing condition traps.",
                    "paraphrase": "fine print = footnotes = qualifying clauses",
                    "alert": ""
                },
                {
                    "chunk": "reach the golden milestone",
                    "meaning": "達成金色證書的輝煌里程碑",
                    "scenario": "Consistent practice over 25 days will empower you to reach the golden milestone.",
                    "paraphrase": "milestone = landmark = achievement",
                    "alert": ""
                },
                {
                    "chunk": "trust your trained instincts",
                    "meaning": "相信你這 25 天磨練出的語感本能",
                    "scenario": "Walk into the examination room with confidence and trust your trained instincts.",
                    "paraphrase": "instincts = intuition = reflex",
                    "alert": ""
                }
            ],
            "visual_anchor": {
                "title": "明天考場 75 分鐘閱讀配速終極黃金律",
                "rule_1": "⏱️ Part 5 (30 題)：10 分鐘完食（每題 15-20 秒秒殺，不糾結）",
                "rule_2": "⏱️ Part 6 (16 題)：8 分鐘搞定（抓句子前後轉折與時態）",
                "rule_3": "⏱️ Part 7 (54 題)：52 分鐘穩拿（單篇 25 分鐘，雙篇/三篇 27 分鐘，留 5 分鐘塗卡檢查）",
                "golden_rule": "⚡ 教練金句：遇到難題果斷猜一個標記好，絕不在一題停超過 40 秒！"
            },
            "part5": [
                {
                    "id": 1,
                    "target_seconds": 15,
                    "question": "The executive committee is confident that the newly implemented training program will ________ boost employee efficiency.",
                    "options": {
                        "A": "substantial",
                        "B": "substantially",
                        "C": "substantiate",
                        "D": "substantiality"
                    },
                    "answer": "B",
                    "analysis": "will ________ boost（助動詞與原形動詞之間的夾心餅乾，塞入副詞修飾 boost）。substantially 表『顯著地 / 大幅度地』。故選 (B)。",
                    "translation": "執行委員會確信，新實施的培訓計畫將大幅提升員工的工作效率。"
                },
                {
                    "id": 2,
                    "target_seconds": 15,
                    "question": "All personnel must adhere strictly ________ confidential data security protocols.",
                    "options": {
                        "A": "to",
                        "B": "with",
                        "C": "for",
                        "D": "at"
                    },
                    "answer": "A",
                    "analysis": "adhere strictly to...（嚴格遵守……）。adhere 固定搭配 to，故選 (A)。",
                    "translation": "所有人員必須嚴格遵守機密資料安全規程。"
                },
                {
                    "id": 3,
                    "target_seconds": 15,
                    "question": "The board unanimously approved the budget ________ the proposal was revised to address regulatory concerns.",
                    "options": {
                        "A": "once",
                        "B": "in spite of",
                        "C": "prior to",
                        "D": "owing to"
                    },
                    "answer": "A",
                    "analysis": "空格後為 'the proposal was revised'（完整子句 S+V），表『一旦……就……』，選從屬連接詞 (A) once。(B)、(C)、(D) 皆為介系詞，後方不能接動詞子句。",
                    "translation": "一旦該提案經過修改以解決法規疑慮，董事會便一致通過了預算。"
                }
            ]
        },
        "afternoon": {
            "quick_recall": [
                {
                    "prompt": "Part 5 target speed: ________ [幾秒] per question.",
                    "clue": "金色證書目標每題秒數",
                    "answer": "15-20 seconds"
                },
                {
                    "prompt": "Seeing 'will _____ verb', immediately choose an ________ [詞性].",
                    "clue": "詞性，夾心位置",
                    "answer": "Adverb (-ly)"
                },
                {
                    "prompt": "In Part 7, always pay close attention to ________ [星號小字與附註].",
                    "clue": "陷阱常出沒處",
                    "answer": "Fine print / footnotes (*Note)"
                },
                {
                    "prompt": "The golden milestone score: ________ [幾分以上] points.",
                    "clue": "金色證書門檻",
                    "answer": "860+"
                }
            ],
            "spaced_traps": [
                {
                    "id": 1,
                    "question": "Employees who show exceptional dedication are ________ for leadership advancements.",
                    "options": {
                        "A": "eligible",
                        "B": "compatible",
                        "C": "accustomed",
                        "D": "resistant"
                    },
                    "answer": "A",
                    "trap_point": "eligible for（符合…資格）。",
                    "analysis": "後方接介系詞 for，秒選 eligible。compatible 接 with；accustomed 接 to；resistant 接 to。",
                    "translation": "表現出卓越奉獻精神的員工符合晉升領導職務的資格。"
                },
                {
                    "id": 2,
                    "question": "Management decided to ________ the marketing campaign until market conditions improve.",
                    "options": {
                        "A": "hold off on",
                        "B": "step down",
                        "C": "take over",
                        "D": "back down"
                    },
                    "answer": "A",
                    "trap_point": "hold off on（暫緩推遲）。",
                    "analysis": "依句意知管理層決定『暫緩』行銷活動直到市況好轉，故選 (A) hold off on。"
                }
            ],
            "part7": {
                "text_type": "Final Motivational Briefing (教練考前終極祝福與叮嚀)",
                "title": "Your Golden Certificate Journey: Day 25 Final Message",
                "content": "Dear Fighter,\n\nOver the past 25 days, you have systematically dismantled every grammatical trap, conquered your priority error bank, mastered over 150 business chunks, and sharpened your detail radar for Part 7. You are no longer answering questions by vague intuition; you are navigating the test with laser-sharp visual anchors.\n\nTomorrow, maintain your composure. Keep your Part 5 rhythm at 15-20 seconds per question. In Part 7, trust your scanning instincts and always double-check the footnotes. You have earned every bit of that 860+ Golden Certificate. Go seize it!",
                "questions": [
                    {
                        "question": "What is the recommended approach for Part 5 tomorrow?",
                        "options": {
                            "A": "Spend at least 60 seconds analyzing complex sentences.",
                            "B": "Maintain a rapid rhythm of 15-20 seconds per question.",
                            "C": "Skip all preposition questions until the end.",
                            "D": "Translate every sentence into Chinese before answering."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：配速心法 'Keep your Part 5 rhythm at 15-20 seconds per question'！",
                        "analysis": "內文明確提醒：Part 5 保持每題 15-20 秒的高速節奏，故選 (B)。"
                    },
                    {
                        "question": "What key mindset should you carry into the exam room tomorrow?",
                        "options": {
                            "A": "Rely strictly on guessing when encountering long words.",
                            "B": "Maintain composure and trust your trained visual anchors.",
                            "C": "Finish the entire reading test in under 40 minutes.",
                            "D": "Focus exclusively on vocabulary rather than context."
                        },
                        "answer": "B",
                        "radar": "🔍 防漏看雷達：心態金句 'maintain your composure... trust your trained instincts... laser-sharp visual anchors'！",
                        "analysis": "文中叮嚀保持沉著冷靜並信任訓練出來的視覺錨點，故選 (B)。"
                    }
                ]
            }
        }
    }
}

DAYS_DATA.update(ADDITIONAL_DAYS)
DAYS_DATA.update(DAYS_15_TO_25)

# Write out master_curriculum.py
with open("master_curriculum.py", "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""\nMaster 25-Day TOEIC Golden Certificate (860+) Curriculum\n"""\n\n')
    f.write("DAYS_DATA = " + repr(DAYS_DATA) + "\n")

print(f"Master curriculum created successfully! Total days: {len(DAYS_DATA)}")
