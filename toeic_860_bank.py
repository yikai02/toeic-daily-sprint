# -*- coding: utf-8 -*-
"""
Builds the complete 860+ Knowledge Base expansion from `860_antigravity.md`:
1. Parses all 97 vocabulary items + 8 confusion table pairs from `860_antigravity.md`.
2. Deduplicates against existing curriculum chunks so identical words are never repeated.
3. Adds all new vocabulary & distractors to the Traditional Chinese POS/Meaning/Usage Lexicon.
4. Generates high-complexity Part 3 (Vocabulary & Grammar Multiple Choice), Part 4 (12-Question Cloze Multiple Choice),
   and Part 2 (Detailed Grammar Modules covering all 4 major grammar rule sets in `860_antigravity.md`).
"""

import json
import re
from pathlib import Path

# Additional Lexicon entries for all 97 words & distractors from 860_antigravity.md
EXTRA_860_LEXICON = {
    "prominent": ("形容詞 (adj.)", "顯著的；傑出的；著名的", "修飾人物或地位（a prominent figure / economist）"),
    "prominently": ("副詞 (adv.)", "顯著地；醒目地", "修飾動詞或過去分詞（prominently displayed）"),
    "prominence": ("不可數名詞 (n.)", "卓越；顯著；聲望", "作主詞或受詞"),
    "complimentary": ("形容詞 (adj.)", "免費贈送的；讚美的", "多益必考 complimentary breakfast / shuttle（免費早餐／接駁車），注意勿與 complementary（互補的）混淆"),
    "complementary": ("形容詞 (adj.)", "互補的；相輔相成的", "指兩事物互相補足（complementary skills），非免費贈送"),
    "compliment": ("名詞 / 動詞 (n./v.)", "稱讚；恭維", "作名詞或及物動詞"),
    "deficient": ("形容詞 (adj.)", "缺乏的；不足的；有缺陷的", "常搭配 in（be deficient in），反義詞為 sufficient"),
    "deficiency": ("名詞 (n.)", "缺乏；不足；缺陷", "指營養或資金制度上的短缺"),
    "deficit": ("可數名詞 (n.)", "赤字；虧損；逆差", "常用於 budget / trade deficit（預算赤字／貿易逆差）"),
    "ascertain": ("及物動詞 (v.)", "查明；弄清；確定", "高分正式動詞，後接名詞或 whether/what 子句（ascertain the cause）"),
    "ascertained": ("過去式 / 過去分詞 (v./V-ed)", "被查明的；已確定的", "常用於假設語氣被動 be ascertained"),
    "ascertaining": ("動名詞 / 現在分詞 (V-ing)", "查明；確認", "後接名詞受詞"),
    "be ascertained": ("原形被動語態 (v.)", "被查明（用於重要性假設語氣 that S + (should) + be ascertained）", "觸發自 It is imperative that..."),
    "discrete": ("形容詞 (adj.)", "個別分開的；互不相連的；離散的", "⚠️ 形近字陷阱：discrete 指「分開獨立的（six discrete stages）」，勿與 discreet（謹慎保密的）混淆"),
    "discreet": ("形容詞 (adj.)", "言行謹慎的；守口如瓶的；低調的", "⚠️ 形近字陷阱：discreet 指「謹慎保密的」，勿與 discrete（個別分開的）混淆"),
    "accumulative": ("形容詞 (adj.)", "累積的；積聚的", "修飾效應或利息"),
    "accumulate": ("動詞 (v.)", "累積；積聚；積攢", "常用於 accumulate vacation days / wealth"),
    "accumulation": ("不可數名詞 (n.)", "累積；積聚物", "作主詞或受詞"),
    "pervasive": ("形容詞 (adj.)", "無處不在的；遍布的；普遍深入的", "修飾科技、影響力或風氣（pervasive influence）"),
    "pervasively": ("副詞 (adv.)", "普遍地；無所不在地", "修飾動詞或形容詞"),
    "pervade": ("及物動詞 (v.)", "瀰漫；遍及；滲透", "後接名詞受詞"),
    "conscientiously": ("副詞 (adv.)", "認真負責地；盡責地；一絲不苟地", "修飾工作態度動詞（work / perform conscientiously）"),
    "conscientious": ("形容詞 (adj.)", "勤勉認真的；盡責的", "修飾員工或工作表現（a conscientious employee）"),
    "conscience": ("名詞 (n.)", "良心；道德心", "指內心道德感"),
    "neglect": ("及物動詞 / 不可數名詞 (v./n.)", "疏忽；忽視；漏做", "常用於 neglect to V 或 neglect one's duties"),
    "negligence": ("不可數名詞 (n.)", "疏忽；過失；失職", "法律與品管高頻詞（gross negligence 重大過失）"),
    "negligent": ("形容詞 (adj.)", "疏忽的；粗心大意的", "常用於 be negligent in"),
    "negligently": ("副詞 (adv.)", "疏忽地；粗心地", "修飾動詞"),
    "subsequently": ("副詞 (adv.)", "隨後；後來；接著（等於 afterward）", "連接時間先後順序的副詞"),
    "succession": ("名詞 (n.)", "連續；接替；繼任", "必考片語 in succession（連續不斷地）或 leadership succession（領導層交班）"),
    "successive": ("形容詞 (adj.)", "連續的；接連的", "常用於 for three successive quarters（連續三個季度）"),
    "successor": ("可數名詞 (n.)", "繼任者；接班人；後續產品", "指接替職位的人或新一代機種"),
    "exposure": ("不可數名詞 (n.)", "曝光度；接觸；暴露（風險）", "必考搭配 exposure to + N（media exposure 媒體曝光／exposure to foreign markets）"),
    "expose": ("及物動詞 (v.)", "使接觸；揭露；使暴露於", "常用於 expose A to B"),
    "venue": ("可數名詞 (n.)", "（會議、展覽、音樂會之）舉辦會場；場地", "多益活動與會議最高頻地點名詞（conference venue）"),
    "unveil": ("及物動詞 (v.)", "首次推出；揭幕；公布（新產品或計畫）", "同義於 launch / reveal / introduce"),
    "unveiled": ("過去式 / 過去分詞 (v./V-ed)", "正式發表；揭幕", "常用於 unveiled its latest prototype"),
    "autonomous": ("形容詞 (adj.)", "自主獨立的；自動駕駛的；自治的", "常用於 autonomous vehicles / divisions"),
    "autonomously": ("副詞 (adv.)", "自主地；獨立運作地", "修飾動詞 operate / function"),
    "autonomy": ("不可數名詞 (n.)", "自主權；自治", "作受詞或主詞"),
    "namely": ("副詞 (adv.)", "也就是說；即（等於 that is to say）", "用於具體列舉或補充說明前文提到的名詞"),
    "thereby": ("副詞 (adv.)", "藉此；從而；因此", "多益必考句構：逗號後接 thereby + V-ing（如 thereby reducing costs）表結果"),
    "nonetheless": ("連接副詞 (adv.)", "然而；儘管如此（等於 nevertheless）", "轉折副詞，不可直接連接兩個無分號之獨立子句"),
    "somewhat": ("程度副詞 (adv.)", "有點；稍微（等於 slightly / rather）", "修飾形容詞、副詞或比較級（somewhat higher）"),
    "termination": ("名詞 (n.)", "終止（合約）；解僱；結束", "常用於 contract termination / termination clause"),
    "terminate": ("及物 / 不及物動詞 (v.)", "終止（契約）；解僱；結束", "後接 contract / employment 作受詞"),
    "clause": ("可數名詞 (n.)", "（法律合約之）條款；文法子句", "常用於 confidentiality clause（保密條款）／ penalty clause"),
    "though": ("從屬連接詞 / 副詞 (conj./adv.)", "雖然；儘管（置句首或句中連接子句） ／ 然而；不過（置句尾作副詞）", "注意雙重詞性用法"),
    "discrimination": ("不可數名詞 (n.)", "歧視；區別對待；鑑賞力", "常用於 workplace discrimination"),
    "discriminate": ("不及物動詞 (v.)", "歧視（against）；區分（between）", "不及物動詞"),
    "persistent": ("形容詞 (adj.)", "持續不斷的；堅持不懈的；固執的", "修飾努力或問題（persistent efforts / inflation）"),
    "persistence": ("不可數名詞 (n.)", "堅持不懈；毅力；持續存在", "作主詞或受詞"),
    "as far as": ("連接詞 / 介系詞片語 (conj./prep.)", "就……範圍而言；遠至……", "必考搭配 as far as I know / as far as the budget is concerned，注意勿與條件詞 provided that 混淆"),
    "in order that": ("從屬連接詞 (conj.)", "為了……；以便……（等於 so that）", "後接完整目的副詞子句（子句常含 can / could / may / will）"),
    "collateral": ("不可數名詞 (n.)", "抵押品；擔保物", "金融借貸必考字（pledge real estate as collateral）"),
    "fluctuation": ("可數 / 不可數名詞 (n.)", "波動；起伏；漲落", "常用於 currency / price fluctuations（匯率／價格波動）"),
    "fluctuate": ("不及物動詞 (v.)", "波動；起伏不定", "搭配 between A and B 或 with"),
    "resent": ("及物動詞 (v.)", "對……感到憤慨；不滿；怨恨", "後接名詞或動名詞（V-ing）作受詞"),
    "resentment": ("不可數名詞 (n.)", "憤慨；怨恨；不滿情緒", "作主詞或受詞"),
    "confine": ("及物動詞 (v.)", "限制；侷限；禁閉", "必考片語 confine A to B（將 A 限制在 B 範圍內）"),
    "confined": ("形容詞 / 過去分詞 (adj./V-ed)", "受限的；狹窄封閉的", "常用於 be confined to 或 confined spaces（密閉空間）"),
    "abstain": ("不及物動詞 (v.)", "棄權（不投票）；戒絕；自我克制", "必考搭配 abstain from + N/V-ing（abstain from voting 投票棄權）"),
    "abstention": ("名詞 (n.)", "棄權；節制", "指議會或董事會投票棄權"),
    "inclusive": ("形容詞 (adj.)", "包含……在內的；全包的；具包容性的", "必考片語 inclusive of taxes and shipping（含稅及運費），反義為 exclusive of"),
    "takeout": ("名詞 / 形容詞 (n./adj.)", "外帶餐點；外帶的", "餐飲情境高頻詞（takeout orders）"),
    "courier": ("可數名詞 (n.)", "快遞員；快遞公司；專差", "常用於 by express courier（透過快遞專遞）"),
    "repaving": ("動名詞 / 不可數名詞 (n./V-ing)", "道路重新鋪設工程", "市政交通改道通知高頻字（road repaving project）"),
    "repave": ("及物動詞 (v.)", "重新鋪設（路面）", "後接道路或停車場作受詞"),
    "pedestrians": ("複數可數名詞 (n.)", "行人；步行者", "常用於 pedestrian walkway / accessible only to pedestrians"),
    "pedestrian": ("可數名詞 / 形容詞 (n./adj.)", "行人 ／ 行人專用的", "常用於 pedestrian zone（行人徒步區）"),
    "stroll down": ("動詞片語 (phr.)", "沿著……漫步；散步", "Part 1 圖片題與旅遊文案高頻片語（stroll down the boardwalk）"),
    "task": ("可數名詞 / 及物動詞 (n./v.)", "任務；工作 ／ 指派任務（be tasked with）", "注意作動詞時常用被動 be tasked with + N/V-ing（被指派負責……）"),
    "garment": ("可數名詞 (n.)", "（一件）衣服；成衣；服裝", "多益常作 clothes 的正式替換詞（garment manufacturing 成衣製造）"),
    "scatter": ("動詞 (v.)", "使散落；分散；散佈", "常用被動 be scattered across the desk/floor（散落於桌面／地面）"),
    "scattered": ("過去分詞 / 形容詞 (V-ed/adj.)", "散落的；零星分佈的", "常用於 papers scattered across the table"),
    "along the coast": ("介系詞片語 (prep. phr.)", "沿著海岸線；在沿海地區", "地理位置與旅遊運輸高頻片語"),
    "complex": ("可數名詞 / 形容詞 (n./adj.)", "複合建築群；園區；綜合大樓 ／ 複雜的", "⚠️ 多益必考名詞熟詞偏義：an industrial / office / sports complex（工業園區／辦公大樓群）"),
    "stapler": ("可數名詞 (n.)", "訂書機", "辦公室文具與 Part 1 圖片題字彙"),
    "spare": ("形容詞 / 及物動詞 (adj./v.)", "備用的；多餘的 ／ 抽出（時間）；免除", "常用於 spare parts（備用零件）或 spare no effort（不遺餘力）"),
    "circular economy": ("專有名詞 (n.)", "循環經濟（資源再生與零廢棄經濟模式）", "ESG 永續商業閱讀高頻概念"),
    "circular": ("形容詞 / 可數名詞 (adj./n.)", "圓形的；循環的 ／ 傳單；通告函", "作名詞時指發給全體員工或顧客的「通告信／宣傳單」"),
    "alternative": ("可數名詞 / 形容詞 (n./adj.)", "替代方案；取捨 ／ 替代的；另類的", "常用於 a viable alternative to...（……的可行替代方案）"),
    "alternatively": ("連接副詞 (adv.)", "或者；作為另一種選擇", "用於提供第二種方案"),
    "inclement": ("形容詞 (adj.)", "（天氣）惡劣的；嚴酷的；狂風暴雨的", "多益極高頻搭配 inclement weather（惡劣天候，常接在 owing to / due to 之後）"),
    "collision": ("可數 / 不可數名詞 (n.)", "碰撞事故；相撞；衝突", "衍生自動詞 collide（collision avoidance system 防撞系統）"),
    "collide": ("不及物動詞 (v.)", "相撞；碰撞；衝突", "搭配 with"),
    "temps": ("複數可數名詞 (n.)", "臨時雇員；短期約聘人員（等於 temporary workers）", "人資招募情境口語與通知常用字（hire seasonal temps）"),
    "incentive": ("可數 / 不可數名詞 (n.)", "誘因；激勵措施；獎勵金", "常用於 financial incentives（財務獎勵）或 tax incentives（稅務優惠）"),
    "rehearsal": ("可數 / 不可數名詞 (n.)", "排練；彩排；預演", "常用於 dress rehearsal（總彩排）"),
    "rehearse": ("動詞 (v.)", "排練；預演", "演講或表演前之排練"),
    "urgent": ("形容詞 (adj.)", "緊急的；迫切的；刻不容緩的", "修飾名詞（urgent attention / matter）"),
    "urgently": ("副詞 (adv.)", "緊急地；迫切地", "修飾動詞"),
    "saturated": ("形容詞 / 過去分詞 (adj./V-ed)", "飽和的；充滿的；濕透的", "商務必考 a highly saturated market（高度飽和的市場）"),
    "saturate": ("及物動詞 (v.)", "使飽和；使充滿", "後接市場或液體作受詞"),
    "editorial": ("可數名詞 / 形容詞 (n./adj.)", "社論；主編評論 ／ 編輯上的", "新聞出版業高頻詞（editorial board 編輯委員會）"),
    "quote": ("可數名詞 / 動詞 (n./v.)", "報價（單）；估價（等於 quotation） ／ 報價；引述", "商務採購必考 request a price quote（索取報價）"),
    "quotation": ("可數名詞 (n.)", "正式報價單；引文", "常用於 submit a written quotation"),
    "dedication": ("不可數名詞 (n.)", "奉獻；敬業精神；專注致力", "必考搭配 dedication to + N/V-ing（對……的無私奉獻，to 為介系詞）"),
    "dedicated": ("形容詞 (adj.)", "敬業的；專用的；專屬的", "常用於 be dedicated to + N/V-ing"),
    "scrutinize": ("及物動詞 (v.)", "仔細審查；徹底檢驗；細看", "等同於 examine thoroughly（scrutinize financial statements）"),
    "scrutiny": ("不可數名詞 (n.)", "仔細審查；嚴密監督", "常用於 come under close scrutiny"),
    "testament": ("可數名詞 (n.)", "明證；鐵證；確鑿證明", "必考片語 a testament to + N（是某人能力或努力的最佳證明）"),
    "perseverance": ("不可數名詞 (n.)", "堅毅；百折不撓；堅持不懈", "表揚員工克服難關的核心名詞"),
    "persevere": ("不及物動詞 (v.)", "堅持不懈；鍥而不捨", "常搭配 in / with"),
    "devastating": ("形容詞 (adj.)", "毀滅性的；造成重創的；極具破壞力的", "修飾經濟衝擊或災害（a devastating impact on tourism）"),
    "devastate": ("及物動詞 (v.)", "摧毀；重創", "後接名詞受詞"),
    "distinguish": ("動詞 (v.)", "區別；辨別；使傑出", "常用於 distinguish between A and B 或 distinguish A from B"),
    "distinguished": ("形容詞 (adj.)", "卓越的；傑出的；受人尊崇的", "修飾學者、嘉賓或職涯（a distinguished career / speaker）"),
    "template": ("可數名詞 (n.)", "範本；模板；樣板", "常用於 standard invoice template（標準發票範本）"),
    "alteration": ("可數 / 不可數名詞 (n.)", "修改；變更；衣服修改", "⚠️ 形近字陷阱：alteration 指「修改、變動（alterations to the schedule）」，勿與 alternation（輪流交替）混淆"),
    "alternation": ("不可數名詞 (n.)", "交替；輪流；間隔出現", "⚠️ 形近字陷阱：衍生自 alternate（輪流），與「修改（alteration）」完全不同"),
    "culinary": ("形容詞 (adj.)", "烹飪的；廚房的；餐飲的", "常用於 culinary arts / academy / delights（烹飪藝術／餐飲學院）"),
    "literature": ("不可數名詞 (n.)", "產品宣傳品；說明手冊；文獻資料", "⚠️ 多益熟詞偏義：商務情境中 promotional / product literature 專指「產品宣傳冊、型錄文宣」！"),
    "monumental": ("形容詞 (adj.)", "重大的；具里程碑意義的；不朽的", "修飾成就或工程（a monumental achievement / task）"),
    "narrate": ("及物 / 不及物動詞 (v.)", "擔任旁白；敘述；講述", "常用於 narrate a training video（為培訓影片配音旁白）"),
    "narrator": ("可數名詞 (n.)", "旁白員；敘述者", "指紀錄片或有聲書的旁白人員"),
    "manifestation": ("可數 / 不可數名詞 (n.)", "具體展現；表徵；顯現", "常用於 a clear manifestation of...（……的明確展現）"),
    "manifest": ("及物動詞 / 形容詞 / 名詞 (v./adj./n.)", "表明；顯現 ／ 明顯的 ／ 貨運艙單", "注意多益海空運亦常考 cargo manifest（貨運艙單）"),
    "resourceful": ("形容詞 (adj.)", "足智多謀的；善於隨機應變解決問題的", "人資考評高頻讚美詞（a resourceful project coordinator）"),
    "resourcefulness": ("不可數名詞 (n.)", "足智多謀；應變能力", "作受詞或主詞"),
    "prohibit": ("及物動詞 (v.)", "明令禁止；阻止", "必考句型 prohibit A from V-ing（禁止 A 做某事）"),
    "prohibition": ("名詞 (n.)", "禁令；禁止", "作主詞或受詞"),
    "relinquish": ("及物動詞 (v.)", "正式放棄（職位、控制權、權利）；交出", "常用於 relinquish control / one's chairmanship（交出控制權／卸下主席職務）"),
    "concede": ("及物 / 不及物動詞 (v.)", "承認（失敗或疏失）；退讓；讓步", "常用於 concede defeat 或 concede that...（承認……事實）"),
    "concession": ("可數 / 不可數名詞 (n.)", "讓步；妥協；特許經營權", "常用於 make concessions（做出讓步）"),
    "discharge": ("及物動詞 / 名詞 (v./n.)", "履行（職責）；解僱；准許出院；排放（廢水）", "多益一詞多義霸主：discharge one's duties（履行職責）／ discharge a patient（准許病患出院）"),
    "stringent": ("形容詞 (adj.)", "（法規、標準、品管）極為嚴格的；嚴苛的；緊縮的", "必考搭配 stringent safety standards / quality controls"),
    "stringently": ("副詞 (adv.)", "嚴格地；嚴苛地", "修飾動詞或分詞"),
    "critical": ("形容詞 (adj.)", "批判的；挑剔的 ／ 至關重要的；關鍵的", "必考微觀訊號：be critical of + N（對……持批評態度）"),
    "criticize": ("及物動詞 (v.)", "批評；指責", "及物動詞直接接名詞受詞（criticize the decision），後方絕不可加 of"),
    "criticism": ("不可數 / 可數名詞 (n.)", "批評；指責；評論", "作主詞或受詞"),
    "against": ("介系詞 (prep.)", "反對；切勿；防範；緊靠", "必考微觀訊號：caution / warn sb against V-ing（告誡某人切勿做某事）"),
    "whose": ("關係代名詞所有格 (pron.)", "……的（代替先行詞之所有格，後方名詞前不可有 the）", "公式：先行詞 + whose + 無冠詞名詞"),
    "of which": ("介系詞 + 關係代名詞 (phr.)", "其中……的（後方接 the + 名詞，構成 of which the + N）", "公式：先行詞, of which + the + 名詞"),
    "which": ("關係代名詞 (pron.)", "先行詞為物之主格或受格關係代名詞", "後接不完整子句，不可直接修飾無冠詞名詞"),
    "submissions": ("複數可數名詞 (n.)", "提交之作品；投件；呈報文件", "複數可數名詞，搭配 All / Several photo submissions"),
    "submission": ("單數 / 不可數名詞 (n.)", "提交；呈遞；投件作品", "單數可數時不可直接接在 All / Several 後作複數主詞"),
    "permitting": ("現在分詞 (V-ing)", "允許（用於獨立分詞構句 Weather permitting / Time permitting）", "無連接詞時，主詞與 permit 為主動關係，必用現在分詞 permitting"),
    "permits": ("第三人稱單數動詞 / 複數名詞 (v./n.)", "允許（真動詞） ／ 許可證", "一山不容二虎：逗號前若無連接詞 if，絕不可填真動詞 permits"),
    "permitted": ("過去式 / 過去分詞 (v./V-ed)", "被允許的", "被動分詞"),
    "permit": ("動詞 / 可數名詞 (v./n.)", "允許 ／ 許可證；通行證", "作原形動詞或單數名詞"),
    "the remainder": ("名詞片語 (n.)", "其餘的人或物；剩餘部分（等於 the rest）", "常用於 the remainder of the fiscal year / contract balance"),
    "remains": ("複數名詞 / 第三人稱單數動詞 (n./v.)", "遺蹟；遺體；殘餘物 ／ 保持（連綴動詞）", "⚠️ 陷阱：作名詞時指「古蹟遺址、殘骸或吃剩殘渣」，不可指會議剩餘時間或尾款"),
    "remaining": ("形容詞 (adj.)", "剩餘的；剩下的", "前置修飾名詞（the remaining balance），不可單獨接在定冠詞後作 the remaining of"),
    "remain": ("連綴動詞 / 不及物動詞 (v.)", "保持；依然是；留下", "原形動詞"),
    "within reach": ("介系詞片語 (phr.)", "觸手可及；指日可待；在能力所及範圍內", "常用於 within reach of our annual target"),
    "out of reach": ("介系詞片語 (phr.)", "遙不可及；力所不及；放在兒童拿不到的地方", "與 within reach 語意相反"),
    "a combined total of": ("數量修飾片語 (phr.)", "總計共達……（固定搭配 + 金額或數量）", "商務財報固定結構"),
    "alike": ("副詞 / 敘述形容詞 (adv./adj.)", "兩者皆然；同樣地 ／ 相似的", "必考結構：A and B alike（A 與 B 兩者皆然，置於兩個對等名詞之後）"),
    "like": ("介系詞 (prep.)", "像……一樣（置於名詞之前）", "不可放在 A and B 之後表「兩者皆然」"),
    "likely": ("形容詞 / 副詞 (adj./adv.)", "很可能的（be likely to V）", "表機率可能性"),
    "likeness": ("名詞 (n.)", "相似處；肖像", "名詞"),
    "left behind": ("過去分詞片語 (phr.)", "被遺留下的（簡化關係子句，省略 which were）", "一山不容二虎：主句已有真動詞時，用過去分詞片語修飾名詞 Items left behind"),
    "are left behind": ("現在簡單式被動真動詞 (v.)", "被留下（有限動詞）", "若無關係代名詞 which/that，不可直接放入主詞與主要動詞之間"),
    "have been left behind": ("現在完成式被動真動詞 (v.)", "已經被留下（有限動詞）", "無連接詞或關代時會造成雙真動詞錯誤"),
    "leaving behind": ("現在分詞片語 (phr.)", "主動留下……（後方須有受詞）", "物品本身是被乘客留下，不可用主動"),
    "complacent": ("形容詞 (adj.)", "自滿的；沾沾自喜的", "形近字干擾項，與建築園區 complex 無關"),
    "whom": ("受格關係代名詞 (pron.)", "先行詞為人時之受格代名詞", "先行詞為公司或物品時不可單獨用 whom 表所有格"),
    "editorials": ("複數可數名詞 (n.)", "報紙社論；主編評論文章", "媒體出版字彙，與臨時雇員 temps 無關"),
    "was ascertained": ("過去式被動真動詞 (v.)", "被查明了（一般過去式）", "在重要性假設語氣 It is imperative that 後必須用原形 be ascertained，不可用 was ascertained"),
    "is ascertained": ("現在式被動真動詞 (v.)", "被查明（一般現在式）", "在重要性假設語氣 It is imperative that 後必須用原形 be ascertained，不可用 is ascertained"),
    "to ascertain": ("不定詞 (to-V)", "去查明", "that 名詞子句主詞後需要原形動詞 ascertain，不可填不定詞 to ascertain"),
    "are left": ("現在簡單式被動真動詞 (v.)", "被留下（有限真動詞）", "一山不容二虎：主句已有真動詞且無關代連接時，不可再選真動詞 are left"),
    "have been left": ("現在完成式被動真動詞 (v.)", "已經被留下（有限真動詞）", "一山不容二虎：無關代連接時會造成雙真動詞錯誤"),
    "left": ("過去分詞 / 過去式 (V-ed)", "被留下的（簡化關係子句，省略 which are）", "一山不容二虎：用過去分詞片語 left behind 後位修飾被遺留的物品"),
    "leaving": ("現在分詞 (V-ing)", "主動留下（後方須有受詞）", "物品是被乘客遺留，不可用主動分詞 leaving behind"),
    "quoted": ("過去式 / 過去分詞 (v./V-ed)", "報價；被引述的", "動詞過去式或被動分詞，不可作 All valuation... 的複數名詞主詞"),
    "quoting": ("現在分詞 / 動名詞 (V-ing)", "報價；引述", "分詞或動名詞"),
    "quotes": ("複數可數名詞 (n.)", "報價單；估價單（quote 的複數）", "搭配量詞 All valuation quotes 作複數主詞"),
    "complimented": ("過去式 / 過去分詞 (v./V-ed)", "稱讚；讚美", "動詞分詞，非「免費贈送的（complimentary）」"),
    "in succession": ("介系詞片語 (phr.)", "連續不斷地；接連地", "表時間連續，與業績目標「觸手可及（within reach）」語意不同"),
    "at length": ("介系詞片語 (phr.)", "詳盡地；長篇大論地；終於", "多修飾發言討論（discuss at length）"),
    "to permit": ("不定詞 (to-V)", "為了允許", "獨立分詞構句 Weather permitting 表示「若天氣允許」，不用不定詞"),
    "literacy": ("不可數名詞 (n.)", "識字能力；讀寫素養（如 financial literacy）", "⚠️ 陷阱：與「產品宣傳文宣（product literature）」完全不同"),
    "literal": ("形容詞 (adj.)", "字面上的；逐字的", "形容詞，不可作名詞受詞"),
    "literally": ("副詞 (adv.)", "照字面地；確實地", "副詞，不可作名詞受詞"),
    "garments": ("複數可數名詞 (n.)", "成衣；服裝（garment 的複數）", "指衣服商品，非臨時人員 temps"),
    "staplers": ("複數可數名詞 (n.)", "訂書機（stapler 的複數）", "辦公文具，非臨時人員 temps"),
    "about": ("介系詞 (prep.)", "關於；大約", "caution / warn sb against V-ing 表「告誡切勿做某事」固定用 against，不用 about"),
    "while": ("從屬連接詞 (conj.)", "當……的時候；雖然（後接完整子句或 V-ing）", "不可引導「名詞 + 過去分詞（prices predicted...）」之附帶狀況"),
    "criticized": ("過去式 / 過去分詞 (v./V-ed)", "批評；被批評", "及物動詞 criticize 後不可接 of；were openly critical of 必須用形容詞 critical"),
    "alternate": ("動詞 / 形容詞 (v./adj.)", "輪流；交替 ／ 間隔的；候補的", "不可作 an ___ to their itinerary 的名詞受詞（修改行程應選名詞 alteration）"),
    "into": ("介系詞 (prep.)", "進入……之內；轉變成", "caution sb against V-ing 固定搭配 against"),
    "complexity": ("不可數名詞 (n.)", "複雜性；錯綜複雜", "抽象名詞，不可指「生技研究園區（a biotech complex）」"),
    "where": ("關係副詞 (adv.)", "在……的地方（後接完整子句，不接 of which the 結構）", "後方主詞 the flagship treatments 為事物所屬關係，應選 of which"),
}


GRAMMAR_MODULES_DB = [
    {
        "id": "G1-S1",
        "category": "微觀訊號秒殺法則",
        "title": "Signals 1：be critical of + N vs. criticize + O（形容詞與及物動詞之介系詞訊號）",
        "formula": "✅ be + critical + of + 名詞受詞  ｜  ✅ criticize + 名詞受詞（絕不可加 of）",
        "explanation": "看到空格位於 be 動詞（was / were / remain）之後，且空格後方緊接介系詞 of 時，必須秒選形容詞 critical（對……持批評態度的）。反之，若空格為主要動詞且後方直接接名詞受詞（無介系詞 of），才選及物動詞 criticize。",
        "correct_example": "The head of marketing was openly critical of the board's decision to reduce digital advertising expenditure. （行銷主管公開對董事會削減數位廣告支出的決定持批評態度。）",
        "wrong_trap": "❌ 常見陷阱：誤選 was criticized of（criticize 為及物動詞，被動語態應為 was criticized by/for，主動亦不可加 of）。"
    },
    {
        "id": "G1-S2",
        "category": "微觀訊號秒殺法則",
        "title": "Signals 2：caution / warn + 人 + against + V-ing（告誡切勿做某事）",
        "formula": "✅ caution / warn + 對象 (sb) + against + 動名詞 (V-ing) / 名詞  ｜  被動：be cautioned / warned + against + V-ing",
        "explanation": "及物動詞 caution 與 warn 表示「警告、告誡某人切勿做某事」時，固定搭配反對介系詞 against + V-ing（相當於 warn sb not to V）。在被動語態中，受詞「人」移至主詞位置，空格夾在 are cautioned 與 being / V-ing 之間，秒選 against。",
        "correct_example": "International travellers are strongly cautioned against leaving unattended baggage in the terminal concourse. （強烈告誡國際旅客切勿將無人看管的行李留在航廈大廳。）",
        "wrong_trap": "❌ 常見陷阱：誤用 about 或 from（prohibit / refrain 才接 from；caution / warn 表「切勿」時必接 against）。"
    },
    {
        "id": "G1-S3",
        "category": "微觀訊號秒殺法則",
        "title": "Signals 3：關係代名詞所有格陷阱（whose + N vs. of which + the + N）",
        "formula": "✅ 先行詞 + whose + 無冠詞名詞  ｜  ✅ 先行詞, of which + the + 名詞",
        "explanation": "關係代名詞所有格 whose 本身已取代所有格與冠詞，因此 whose 後方的名詞前「絕對不能有定冠詞 the」。反之，若題目空格後方的名詞前已經印出定冠詞「the + 名詞」，則絕對不可選 whose，必須改選介系詞片語「of which」（構成 of which the + N）。",
        "correct_example": "Remedica, of which the key pharmaceutical products have generated enormous revenues, will expand overseas next quarter. （主打藥品創造龐大營收的 Remedica 公司將於下季拓展海外市場。）",
        "wrong_trap": "❌ 常見陷阱：看到所有格語意就直接選 whose，卻漏看空格後面已經印有定冠詞 the（whose the key products 為嚴重文法錯誤）。"
    },
    {
        "id": "G1-S4",
        "category": "微觀訊號秒殺法則",
        "title": "Signals 4：單複數複合名詞陷阱（All / Several + 單數名詞修飾語 + 複數核心名詞）",
        "formula": "✅ All / Several / Numerous + [單數名詞修飾語] + [複數可數名詞主詞] + 動詞",
        "explanation": "量詞 All、Several、Many、Numerous 修飾可數名詞時，核心名詞必須為複數。若空格前方已印有一個單數可數名詞（如 photo、 safety、 customer），代表該單數名詞只是「形容詞化名詞修飾語（Noun Adjunct）」，空格本身才是真正的主詞中心語，必填複數名詞！",
        "correct_example": "All photo submissions received after the Friday deadline will be automatically returned to the senders. （所有在週五截止期限後收到的攝影投件作品都將自動退回給寄件人。）",
        "wrong_trap": "❌ 常見陷阱：誤以為前方的 photo 已經是主詞而選動詞或單數名詞 submission（All photo 語法不成立，必須是 All photo submissions）。"
    },
    {
        "id": "G2-R1",
        "category": "真動詞 vs. 分詞結構（一山不容二虎法則）",
        "title": "Rule 1：獨立分詞構句（Weather permitting / Time permitting）",
        "formula": "✅ 獨立主詞 (Weather / Time) + 現在分詞 V-ing (permitting), 主句 S + V...",
        "explanation": "英語句子遵循「一山不容二虎」原則：在沒有連接詞（如 if / because / as）的情況下，逗號前的附屬結構絕不可填入真動詞（有限動詞）。Weather permitting（若天氣允許的話，原為 If weather permits）中，因省略了連接詞 If，主詞 weather 與主動動詞 permit 必須轉為現在分詞 permitting。",
        "correct_example": "Weather permitting, the annual charity awards banquet will be held on the rooftop terrace overlooking the harbor. （若天氣允許的話，年度慈善頒獎晚宴將於俯瞰海港的頂樓露台舉行。）",
        "wrong_trap": "❌ 常見陷阱：看到單數名詞 Weather 就反射性選第三人稱單數真動詞 permits，造成無連接詞卻有兩個真動詞的致命錯誤。"
    },
    {
        "id": "G2-R2",
        "category": "真動詞 vs. 分詞結構（一山不容二虎法則）",
        "title": "Rule 2：附帶狀況結構（With + 受詞 + V-ing 主動 / p.p. 被動）",
        "formula": "✅ With + 名詞受詞 + 過去分詞 p.p.（被動） / 現在分詞 V-ing（主動）, 主句 S + V...",
        "explanation": "當句首逗號前為「名詞 + 分詞片語（如 gas prices predicted to drop...）」而非「主詞 + 有限真動詞」時，因為沒有真動詞，句首絕對不能填從屬連接詞（While / Although / Since / Because），必須填入介系詞 With 構成附帶狀況結構（With + O + OC）。",
        "correct_example": "With global fuel prices predicted to drop steadily next month, maritime shipping companies are reconsidering freight surcharges. （隨著全球燃油價格預計將於下月穩定回落，海運公司正重新考量貨運附加費。）",
        "wrong_trap": "❌ 常見陷阱：把過去分詞 predicted 誤看成過去式真動詞而誤選從屬連接詞 Since 或 Because（油價是『被預測』，predicted to drop 為分詞補語而非真動詞）。"
    },
    {
        "id": "G2-R3",
        "category": "真動詞 vs. 分詞結構（一山不容二虎法則）",
        "title": "Rule 3：簡化關係子句（主句已有真動詞，無關代時必選分詞）",
        "formula": "✅ 主詞 + [過去分詞 p.p. / 現在分詞 V-ing 後位修飾片語] + 主句主要真動詞",
        "explanation": "解題時務必先掃描整句找出「主句真動詞」（如 will be retained）。若主詞後方沒有關係代名詞（which / that / who），則主詞與主句真動詞之間的空格只能填入「分詞（V-ing 表主動 / p.p. 表被動）」，絕不可再填入 are left 或 have been left 等真動詞！",
        "correct_example": "Personal items left behind by passengers on commuter trains will be retained at the central lost-and-found office for 30 days. （乘客遺留在通勤列車上的個人物品將於中央失物招領處保留三十天。）",
        "wrong_trap": "❌ 常見陷阱：沒看到句尾的真動詞 will be retained，誤將空格當作主句動詞而選 are left behind 或 have been left behind。"
    },
    {
        "id": "G3-R1",
        "category": "重要性假設語氣與條件句辨析",
        "title": "Rule 1：重要性形容詞之虛擬語氣（It is imperative / vital / mandatory that + S + 原形動詞）",
        "formula": "✅ It is + imperative / essential / vital / mandatory / urgent + that + S + (should) + 原形動詞 V / be + p.p.",
        "explanation": "當主句出現表「極重要、強制、必要」的形容詞（imperative, essential, vital, mandatory, crucial）或要求建議動詞（mandate, insist, recommend）時，後方 that 子句中的助動詞 should 恆被省略，不論子句主詞為單數或過去語境，動詞一律使用「原形動詞」；若為被動語態則使用「be + 過去分詞（如 be ascertained）」。",
        "correct_example": "It is imperative that the root cause of the wire transfer delay be ascertained no later than five o'clock this afternoon. （務必在今天下午五點前查明電匯延誤的根本原因，這點至關重要。）",
        "wrong_trap": "❌ 常見陷阱：看到單數主詞 the cause 就誤選 is ascertained 或 was ascertained，忽略了 imperative 觸發省略 should 的原形被動 be ascertained。"
    },
    {
        "id": "G3-R2",
        "category": "重要性假設語氣與條件句辨析",
        "title": "Rule 2：條件連接詞（provided that / as long as）vs. 範圍界定詞（as far as）",
        "formula": "✅ provided that / providing that / as long as + S + V（只要……／在……條件下）  ｜  ✅ as far as + S + know / be concerned（就……範圍而言）",
        "explanation": "多益常將 provided that / as long as（表條件：只要……）與 as far as（表範圍程度：就……而言）放在同一組選項中。若句意為「只要滿足某項前提條件，即可執行某事」，必選 provided that 或 as long as；若句尾為 is concerned 或 I know，才選 as far as。",
        "correct_example": "Full tuition reimbursement can be approved provided that both the department supervisor and human resources sign the authorization form. （只要部門主管與人資部雙方皆簽署授權表單，即可核准全額學費補助。）",
        "wrong_trap": "❌ 常見陷阱：中文都翻成「只要／就……」，誤用 as far as 引導條件子句。"
    },
    {
        "id": "G4-R1",
        "category": "易混淆字詞、片語與商務固定搭配",
        "title": "形近字與商務偏義秒殺：discreet vs. discrete ／ alteration vs. alternation ／ the remainder vs. remains",
        "formula": "✅ discreet（謹慎保密的）vs. discrete（個別分開的） ｜ ✅ alteration（修改更動）vs. alternation（輪流交替） ｜ ✅ the remainder（其餘部分）vs. remains（遺蹟殘骸）",
        "explanation": "多益 860+ 最愛考核拼字極度相似但語意天差地別的雙胞胎字：(1) discreet 兩個 e 連在一起代表『守口如瓶、謹慎低調』，discrete 的 t 把 e 分開代表『各自獨立分開的階段』；(2) alteration to the contract 為『合約修改』，alternation 為『日夜或班次交替』；(3) the remainder of the payment 指『剩餘尾款』，remains 指『歷史遺址或殘骸』。",
        "correct_example": "Any alteration to the architectural blueprint must be approved in writing before the remainder of the construction budget is disbursed. （在撥付剩餘的工程預算之前，建築藍圖的任何修改都必須獲得書面核准。）",
        "wrong_trap": "❌ 常見陷阱：拼字視覺混淆誤選 alternation 或 remains，或將 literature（產品文宣手冊）與 complex（建築園區）誤解為一般字義。"
    },
]


QUESTIONS_860_BANK = [
    # --- Grammar Rules from 860_antigravity.md ---
    {
        "question": "During the emergency shareholders' meeting, several institutional investors were openly ________ of the executive board's decision to delay the dividend payout.",
        "options": {"A": "critical", "B": "criticize", "C": "criticism", "D": "criticized"},
        "answer": "A",
        "rule_ref": "微觀訊號第 1 條 (Signals 1)：be critical of + N vs. criticize + O",
        "trap_point": "微觀訊號秒殺：空格前有 be 動詞 were + 副詞 openly，後方緊接介系詞 of，必選形容詞 critical！",
        "analysis": "【句構拆解與定位】主句主詞為 several institutional investors，動詞為連綴動詞 were，後接副詞 openly 與介系詞 of，空格需填入形容詞作主詞補語。【核心考點與正解理由】觸發微觀訊號第 1 條：be critical of + N（對……持批評態度），故秒選形容詞 (A) critical。【常見陷阱提醒】及物動詞 criticize 後方直接接名詞受詞，絕不可加 of；過去分詞 criticized 若構成被動 were criticized 表示「投資人被批評」，與語意相反且不接 of。",
        "translation": "在緊急股東大會期間，數家機構投資人公開對執行董事會延後發放股利的決定持批評態度。"
    },
    {
        "question": "All international passengers transiting through the northern terminal are strongly cautioned ________ leaving their carry-on luggage unattended near the boarding gates.",
        "options": {"A": "against", "B": "about", "C": "from", "D": "with"},
        "answer": "A",
        "rule_ref": "微觀訊號第 2 條 (Signals 2)：caution / warn + 人 + against + V-ing",
        "trap_point": "微觀訊號秒殺：be cautioned + [against] + V-ing（被告誡切勿做某事）！",
        "analysis": "【句構拆解與定位】主句主詞為 All international passengers（現在分詞片語 transiting... 後位修飾），動詞為被動語態 are strongly cautioned，後方接動名詞片語 leaving their carry-on luggage unattended。【核心考點與正解理由】觸發微觀訊號第 2 條：caution / warn sb against V-ing（告誡某人切勿做某事），故選介系詞 (A) against。【常見陷阱提醒】prohibit / refrain 才搭配 from；caution / warn 後接動名詞表「禁止、切勿」時固定搭配 against。",
        "translation": "強烈告誡所有經由北側航廈轉機的國際旅客，切勿將手提行李留在登機門附近無人看管。"
    },
    {
        "question": "Remedica BioLabs, ________ the flagship oncology treatments have generated record-breaking export revenues, plans to open a research complex in Zurich.",
        "options": {"A": "of which", "B": "whose", "C": "which", "D": "where"},
        "answer": "A",
        "rule_ref": "微觀訊號第 3 條 (Signals 3)：whose + N vs. of which + the + N",
        "trap_point": "微觀訊號秒殺：空格後方已印有定冠詞 the（the flagship oncology treatments），絕對不可選 whose，必選 of which！",
        "analysis": "【句構拆解與定位】逗號中間為非限定關係子句修飾先行詞 Remedica BioLabs，子句主詞為 the flagship oncology treatments（前方已有定冠詞 the）。【核心考點與正解理由】觸發微觀訊號第 3 條：關係代名詞所有格 whose 後方的名詞前「絕對不能有 the」；當名詞前已存在定冠詞 the 時，必須使用「of which + the + N」，故選 (A) of which。【常見陷阱提醒】90% 考生一看到所有格關係就秒選 whose，卻忽略了後面的定冠詞 the！",
        "translation": "旗下主打腫瘤治療藥物創下破紀錄出口營收的 Remedica BioLabs 公司，計畫在蘇黎世設立一座研究園區。"
    },
    {
        "question": "All architectural blueprint ________ received after the five o'clock municipal filing deadline will be returned unopened to the engineering firms.",
        "options": {"A": "submissions", "B": "submission", "C": "submit", "D": "submitted"},
        "answer": "A",
        "rule_ref": "微觀訊號第 4 條 (Signals 4)：單複數複合名詞陷阱 All + [單數名詞修飾語] + [複數核心名詞]",
        "trap_point": "微觀訊號秒殺：量詞 All 後方雖印有單數名詞 blueprint，但 blueprint 為名詞修飾語，空格必須填複數核心名詞 submissions！",
        "analysis": "【句構拆解與定位】主句主要動詞為後半句的 will be returned（過去分詞片語 received after... 後位修飾主詞），故句首 All architectural blueprint ________ 為完整主詞片語。【核心考點與正解理由】觸發微觀訊號第 4 條：量詞 All 後接可數名詞必須用複數；前方的單數名詞 blueprint 作形容詞化修飾語，空格核心主詞必填複數可數名詞 (A) submissions（提交之文件／作品）。【常見陷阱提醒】單數 submission 無法搭配量詞 All。",
        "translation": "所有在下午五點市政申報截止期限之後收到的建築藍圖投件，都將原封不動退回給各工程事務所。"
    },
    {
        "question": "Weather ________, the unveiling ceremony for the autonomous electric ferry will take place on the outdoor pier along the coast this Saturday.",
        "options": {"A": "permitting", "B": "permits", "C": "permitted", "D": "permit"},
        "answer": "A",
        "rule_ref": "一山不容二虎 Rule 1：獨立分詞構句 Weather permitting / Time permitting",
        "trap_point": "一山不容二虎法則：逗號前沒有連接詞 if，主句已有真動詞 will take place，故絕對不可選真動詞 permits，必選現在分詞 permitting！",
        "analysis": "【句構拆解與定位】主句 the unveiling ceremony... will take place 已具備完整主詞與主要真動詞，句首 Weather ________, 後僅以逗號隔開且無任何連接詞。【核心考點與正解理由】觸發一山不容二虎 Rule 1：獨立分詞構句 Weather permitting（若天氣允許的話，原為 If weather permits），weather 與主動動詞 permit 轉為現在分詞 (A) permitting。【常見陷阱提醒】若誤選真動詞 permits，會造成無連接詞連接兩個子句的 Comma Splice 錯誤。",
        "translation": "若天氣允許的話，自動駕駛電動渡輪的揭幕典禮將於本週六在沿海戶外碼頭舉行。"
    },
    {
        "question": "________ international wholesale coffee prices predicted to fluctuate sharply next quarter, several beverage chains have locked in long-term supply contracts.",
        "options": {"A": "With", "B": "While", "C": "Although", "D": "Since"},
        "answer": "A",
        "rule_ref": "一山不容二虎 Rule 2：附帶狀況結構 With + 受詞 + 分詞 (V-ing / p.p.)",
        "trap_point": "一山不容二虎法則：逗號前 prices predicted to fluctuate 為「名詞 + 過去分詞片語」而非完整子句，無真動詞必選介系詞 With！",
        "analysis": "【句構拆解與定位】句首逗號前結構為 ________ + 名詞受詞 (international wholesale coffee prices) + 過去分詞受詞補語 (predicted to fluctuate...)，整段並無有限真動詞（is/are/were）。【核心考點與正解理由】觸發一山不容二虎 Rule 2：附帶狀況結構 With + O + p.p.（隨著咖啡批發價格被預測將劇烈波動），故選介系詞 (A) With。【常見陷阱提醒】(B) While、(C) Although、(D) Since 均為從屬連接詞，後方必須接含有限真動詞的完整子句。",
        "translation": "隨著國際咖啡批發價格預計將於下季劇烈波動，數家連鎖飲品企業已提前鎖定長期供應合約。"
    },
    {
        "question": "Personal electronic devices ________ behind by conference delegates in the main auditorium will be stored at the security desk for fourteen days.",
        "options": {"A": "left", "B": "are left", "C": "have been left", "D": "leaving"},
        "answer": "A",
        "rule_ref": "一山不容二虎 Rule 3：簡化關係子句（主句已有真動詞，無關代時必選分詞）",
        "trap_point": "一山不容二虎法則：全句已有主要真動詞 will be stored，且無關係代名詞 which/that，空格只能填過去分詞 left！",
        "analysis": "【句構拆解與定位】主句主詞為 Personal electronic devices，主要真動詞為後半句的 will be stored！中間沒有關係代名詞 which 或 that，故空格至 auditorium 為後位修飾主詞的簡化關係子句（分詞片語）。【核心考點與正解理由】觸發一山不容二虎 Rule 3：電子設備是「被與會代表遺留下的」，省略 which are 後保留過去分詞 (A) left（left behind by...）。【常見陷阱提醒】(B) are left 與 (C) have been left 皆為真動詞，填入會導致一句雙動詞錯誤。",
        "translation": "與會代表遺留在主禮堂的個人電子設備，將於安全櫃檯保管十四天。"
    },
    {
        "question": "It is imperative that the exact cause of the chemical leakage in the storage tank ________ before the assembly complex resumes operation.",
        "options": {"A": "be ascertained", "B": "is ascertained", "C": "was ascertained", "D": "ascertaining"},
        "answer": "A",
        "rule_ref": "重要性假設語氣 Rule 1：It is imperative that + S + (should) + 原形動詞 / be p.p.",
        "trap_point": "重要性形容詞 imperative 觸發假設語氣：that 子句省略 should，被動語態必須維持原形 be ascertained！",
        "analysis": "【句構拆解與定位】句首 It is imperative that... 為重要性虛擬語氣句型，that 子句主詞為 the exact cause of the chemical leakage，與動詞 ascertain（查明）為被動關係。【核心考點與正解理由】觸發重要性假設語氣 Rule 1：that 子句中助動詞 should 被省略，動詞必須還原為原形 be 動詞 + 過去分詞，故選 (A) be ascertained（被查明）。【常見陷阱提醒】切勿因主詞 the exact cause 為單數而誤選現在式 is ascertained 或過去式 was ascertained。",
        "translation": "在組裝園區恢復運轉之前，務必先查明儲槽化學洩漏的確切原因，這點至關重要。"
    },
    {
        "question": "Full-time research fellows may apply for an additional travel grant ________ their research paper is accepted for presentation at an international venue.",
        "options": {"A": "provided that", "B": "as far as", "C": "in spite of", "D": "regardless of"},
        "answer": "A",
        "rule_ref": "條件句辨析 Rule 2：條件連接詞 provided that vs. 範圍詞 as far as",
        "trap_point": "條件連接詞 vs. 範圍詞辨析：後方為完整條件子句「只要論文獲准發表」，必選 provided that，不可選範圍詞 as far as！",
        "analysis": "【句構拆解與定位】主句說明研究員可申請額外差旅補助，空格後為完整子句 their research paper is accepted...，表獲得補助的「前提條件」。【核心考點與正解理由】觸發條件句辨析 Rule 2：(A) provided that 意為「只要……、以……為條件」，引導條件副詞子句。【常見陷阱提醒】(B) as far as 表範圍程度「就……而言（如 as far as I know）」，不可用來引導一般條件句；(C)(D) 為介系詞片語不可接子句。",
        "translation": "只要研究論文獲准於國際會場發表，全職研究員即可申請額外的差旅補助金。"
    },
    # --- Confusion Pairs & High-Frequency 860 Vocabulary ---
    {
        "question": "Because the corporate acquisition talks were highly sensitive, the chief legal officer conducted a ________ inquiry into the target firm's patent portfolio.",
        "options": {"A": "discreet", "B": "discrete", "C": "discretion", "D": "discrepancy"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #07 & 易混淆表：discreet (謹慎保密的) vs. discrete (個別分開的)",
        "trap_point": "雙胞胎形近字陷阱：併購談判高度敏感，需進行「謹慎低調保密的（discreet）」調查，勿誤選 discrete（個別分離的）！",
        "analysis": "【句構拆解與定位】Because 子句指出企業併購談判高度敏感，主句冠詞 a 與名詞 inquiry（調查）之間需填入形容詞。【核心考點與正解理由】觸發 860 弱點庫 #07：(A) discreet（兩個 e 緊挨在一起）意為「言行謹慎的、低調保密的」，完全契合敏感併購情境。【常見陷阱提醒】(B) discrete（t 把兩個 e 分開）意為「個別獨立的、不連續的」；(C) discretion 與 (D) discrepancy 為名詞。",
        "translation": "由於企業併購談判高度敏感，法務長對目標公司的專利組合進行了謹慎低調的調查。"
    },
    {
        "question": "The semiconductor manufacturing process is divided into six ________ stages, each of which undergoes stringent quality scrutiny inside the cleanroom.",
        "options": {"A": "discrete", "B": "discreet", "C": "discretion", "D": "discreetly"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #07 & 易混淆表：discrete (個別分開的) vs. discreet (謹慎保密的)",
        "trap_point": "雙胞胎形近字陷阱：製程分為六個「各自獨立分開的（discrete）」階段，勿誤選 discreet（謹慎低調的）！",
        "analysis": "【句構拆解與定位】主句被動動詞 is divided into 後接數量詞 six 與複數名詞 stages（階段），空格需填入表「彼此獨立區隔」的形容詞。【核心考點與正解理由】觸發 860 弱點庫 #07 對照：(A) discrete 意為「個別分開的、互不連續的」，six discrete stages 指「六個獨立階段」。【常見陷阱提醒】(B) discreet 指「言行謹慎守密的」，不能用來形容工廠製程的階段劃分。",
        "translation": "半導體製造流程分為六個各自獨立的階段，每個階段在無塵室內皆須接受嚴格的品質審查。"
    },
    {
        "question": "Passengers requesting an ________ to their confirmed international flight itinerary within twenty-four hours of departure will be charged a processing fee.",
        "options": {"A": "alteration", "B": "alternation", "C": "alternative", "D": "alternate"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #84 & 易混淆表：alteration (修改更動) vs. alternation (輪流交替)",
        "trap_point": "形近字陷阱：對已確認航班行程提出「修改／變更（alteration）」，切勿誤選 alternation（輪流交替）！",
        "analysis": "【句構拆解與定位】現在分詞片語 requesting an ________ to their confirmed international flight itinerary 中，不定冠詞 an 後需接母音開頭的單數名詞，且搭配介系詞 to 表示「對行程的變更」。【核心考點與正解理由】觸發 860 弱點庫 #84：(A) alteration 意為「修改、更動、變更」，an alteration to the itinerary / schedule 為必考搭配。【常見陷阱提醒】(B) alternation 指「輪流、交替（如日夜交替）」；(C) alternative 指「替代方案（兩者擇一）」。",
        "translation": "在起飛前二十四小時內要求修改已確認國際航班行程的旅客，將被收取一筆手續費。"
    },
    {
        "question": "While thirty percent of the consulting fee must be paid upon signing the contract, ________ is due within fifteen days of project completion.",
        "options": {"A": "the remainder", "B": "remains", "C": "remaining", "D": "remain"},
        "answer": "A",
        "rule_ref": "860 易混淆對照表：the remainder (其餘款項／時間) vs. remains (遺體／歷史遺蹟)",
        "trap_point": "其餘 vs. 遺骸陷阱：前文付了 30% 顧問費，後文主詞指「剩餘的 70% 尾款」，必選 the remainder，絕不可選 remains！",
        "analysis": "【句構拆解與定位】While 從屬子句提及簽約時須支付 30% 費用，主句動詞為單數 is due（到期應付），空格作主句主詞指「其餘款項」。【核心考點與正解理由】觸發 860 易混淆對照表：(A) the remainder（等於 the rest）專指「其餘的人事物、剩餘款項或時間」，作單數主詞搭配 is due。【常見陷阱提醒】(B) remains 作名詞時指「古蹟遺址、遺體或殘羹剩飯」；(C) remaining 為形容詞，必須接名詞（the remaining balance）才可作主詞。",
        "translation": "雖然百分之三十的顧問費必須於簽約時支付，但其餘尾款則於專案完成後十五天內到期應付。"
    },
    {
        "question": "Thanks to the persistent dedication of our regional sales representatives, our ambitious annual revenue target is finally ________.",
        "options": {"A": "within reach", "B": "out of reach", "C": "at length", "D": "in succession"},
        "answer": "A",
        "rule_ref": "860 易混淆對照表：within reach (指日可待／觸手可及) vs. out of reach (遙不可及)",
        "trap_point": "正反語意秒殺：句首 Thanks to（多虧了業務代表的堅持奉獻），年度營收目標終於「指日可待（within reach）」！",
        "analysis": "【句構拆解與定位】句首 Thanks to... 表正面原因，主句主詞為 our ambitious annual revenue target，連綴動詞 is finally 後需接介系詞片語作主詞補語。【核心考點與正解理由】觸發 860 易混淆對照表：(A) within reach 意為「觸手可及、指日可待、即將達成」，完全呼應正面語境。【常見陷阱提醒】(B) out of reach 意為「遙不可及、無法達成」，與 Thanks to 的正面因果完全矛盾。",
        "translation": "多虧了我們區域業務代表堅持不懈的投入與奉獻，我們遠大的年度營收目標終於指日可待。"
    },
    {
        "question": "The newly unveiled cloud bookkeeping template has been praised by seasoned certified accountants and small-business proprietors ________.",
        "options": {"A": "alike", "B": "like", "C": "likely", "D": "likeness"},
        "answer": "A",
        "rule_ref": "860 易混淆對照表：A and B alike（A 與 B 兩者皆然）",
        "trap_point": "固定位置秒殺：置於兩個對等名詞片語 A and B 之後表「兩者皆然、一視同仁」，必選副詞 alike！",
        "analysis": "【句構拆解與定位】介系詞 by 後接兩個對等人物族群 seasoned certified accountants and small-business proprietors，句尾空格修飾此對等結構。【核心考點與正解理由】觸發 860 易混淆對照表：A and B alike 為多益必考結構，意為「A 與 B 兩者皆然、同樣地受到雙方讚賞」，故選 (A) alike。【常見陷阱提醒】介系詞 like 必須放在名詞前面（like A and B），絕不可放在 A and B 的句尾。",
        "translation": "新發表的雲端記帳範本同時獲得了資深合格會計師與小型企業主的雙雙讚賞。"
    },
    {
        "question": "Visitors stopping by our exhibition booth at the convention venue will receive complimentary product ________ detailing our circular economy initiatives.",
        "options": {"A": "literature", "B": "literacy", "C": "literal", "D": "literally"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #86：literature 多益熟詞偏義（產品宣傳品、說明手冊）",
        "trap_point": "多益熟詞偏義：展場攤位發送的 product literature 指「產品宣傳手冊、型錄文宣」，並非文學作品！",
        "analysis": "【句構拆解與定位】及物動詞 will receive 後接形容詞 complimentary 與名詞修飾語 product，空格需填入不可數名詞作受詞，且後接現在分詞片語 detailing...。【核心考點與正解理由】觸發 860 弱點庫 #86：(A) literature 在商務多益中極常考「產品文宣、印刷宣傳冊、說明手冊（product / promotional literature）」。【常見陷阱提醒】(B) literacy 指「識字能力、素養（如 financial literacy）」，與攤位發放的文宣品無關。",
        "translation": "在會議展覽會場造訪我們展位之訪客，都將獲贈免費的產品宣傳手冊，內含我們循環經濟計畫的詳細說明。"
    },
    {
        "question": "The municipal government approved the construction of a sprawling biotech ________ that will house twelve autonomous research laboratories and a conference center.",
        "options": {"A": "complex", "B": "complexity", "C": "complacent", "D": "complementary"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #57：complex 多益熟詞偏義（複合建築群、園區）",
        "trap_point": "多益熟詞偏義：不定冠詞 a + sprawling biotech + [單數可數建築名詞 complex（生技園區／複合建築群）]！",
        "analysis": "【句構拆解與定位】介系詞 of 後接不定冠詞 a、形容詞 sprawling 與名詞修飾語 biotech，且後方關係子句 that will house twelve...（將容納十二座實驗室）說明此名詞為大型建築場所。【核心考點與正解理由】觸發 860 弱點庫 #57：(A) complex 作可數名詞時意為「複合建築群、工業園區、綜合大樓（biotech / office / sports complex）」。【常見陷阱提醒】complexity 為抽象名詞「複雜性」，無法容納（house）十二座實驗室。",
        "translation": "市政府批准興建一座大型生技園區，內部將容納十二座自主研究實驗室與一間會議中心。"
    },
    {
        "question": "Hotel guests attending the culinary symposium are entitled to a ________ continental breakfast and high-speed wireless internet throughout their stay.",
        "options": {"A": "complimentary", "B": "complementary", "C": "compliment", "D": "complimented"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #03：complimentary（免費贈送的）vs. complementary（互補的）",
        "trap_point": "高頻雙胞胎陷阱：飯店提供的「免費（complimentary，中間是 i）」早餐，切勿誤選「互補的（complementary，中間是 e）」！",
        "analysis": "【句構拆解與定位】空格夾在不定冠詞 a 與名詞片語 continental breakfast 之間，需填入形容詞修飾早餐。【核心考點與正解理由】觸發 860 弱點庫 #03：(A) complimentary（拼字含 i）意為「免費贈送的、招待的」，complimentary breakfast 為多益聽力與閱讀最高頻搭配。【常見陷阱提醒】(B) complementary（拼字含 e，源自 complement 補充）意為「互補的」，不指免費招待。",
        "translation": "參加餐飲研討會的飯店房客在住宿期間，皆有權享有免費的歐陸式早餐與高速無線網路。"
    },
    {
        "question": "By automating customs tariff calculations across all regional hubs, the courier company eliminated manual clerical errors, ________ reducing operational costs by fifteen percent.",
        "options": {"A": "thereby", "B": "nonetheless", "C": "whereas", "D": "namely"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #20：thereby + V-ing（藉此／因而……，引導結果分詞構句）",
        "trap_point": "文法結構秒殺：逗號後緊接現在分詞 reducing 表「前句行動所帶來的自然結果」，必選副詞 thereby！",
        "analysis": "【句構拆解與定位】主句 the courier company eliminated manual clerical errors 已完整，逗號後為現在分詞片語 ________ reducing operational costs，表因果推進關係。【核心考點與正解理由】觸發 860 弱點庫 #20：(A) thereby（藉此、因而）最常置於逗號後搭配 V-ing（, thereby V-ing），說明前項措施達成的成果。【常見陷阱提醒】(B) nonetheless 表讓步轉折；(C) whereas 為連接詞須接完整 S+V 子句；(D) namely 用於列舉特定名稱。",
        "translation": "藉由將所有區域中心的關稅計算自動化，該快遞公司消除了人工文書錯誤，進而將營運成本降低了百分之十五。"
    },
    {
        "question": "Factory safety regulations strictly ________ unauthorized personnel from entering the high-voltage testing zone while machinery is in operation.",
        "options": {"A": "prohibit", "B": "confine", "C": "abstain", "D": "relinquish"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #91：prohibit A from B-ing（明令禁止 A 做某事）",
        "trap_point": "動詞 + 受詞 + 介系詞搭配：prohibit + 人 + from V-ing（禁止某人進入），confine 搭配 to，abstain 為不及物！",
        "analysis": "【句構拆解與定位】主詞為複數名詞 regulations，空格為主要及物動詞，後接名詞受詞 unauthorized personnel 與介系詞片語 from entering...。【核心考點與正解理由】觸發 860 弱點庫 #91：(A) prohibit 構成固定句型 prohibit A from V-ing（禁止 A 做某事）。【常見陷阱提醒】(B) confine 搭配 to（confine A to B 將 A 限制在 B 範圍）；(C) abstain 為不及物動詞（abstain from voting），不可直接接人物受詞；(D) relinquish 指放棄職權。",
        "translation": "工廠安全法規嚴格禁止未經授權的人員在機器運轉期間進入高壓測試區。"
    },
    {
        "question": "To prevent potential conflicts of interest, board members who hold equity in competing firms must ________ from voting on the vendor selection resolution.",
        "options": {"A": "abstain", "B": "prohibit", "C": "resent", "D": "concede"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #44：abstain from voting（於投票中棄權／迴避）",
        "trap_point": "不及物動詞搭配秒殺：must + [abstain] + from voting（棄權不參與投票）！",
        "analysis": "【句構拆解與定位】主詞為 board members（關係子句 who hold... 修飾），情態助動詞 must 後接原形不及物動詞，並直接搭配介系詞片語 from voting。【核心考點與正解理由】觸發 860 弱點庫 #44：(A) abstain 為不及物動詞，固定搭配 from（abstain from voting 投票棄權／利益迴避）。【常見陷阱提醒】(B) prohibit 為及物動詞，若無受詞不可直接接 from voting（須用被動 be prohibited from voting）。",
        "translation": "為防止潛在的利益衝突，持有競爭公司股權的董事會成員在供應商遴選決議中必須棄權迴避投票。"
    },
    {
        "question": "Following three successive quarters of declining export margins, the founder agreed to ________ operational control of the garment enterprise to an experienced chief executive.",
        "options": {"A": "relinquish", "B": "scrutinize", "C": "unveil", "D": "ascertain"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #92：relinquish control / position / rights（放棄／交出控制權或職位）",
        "trap_point": "高階商務動詞搭配：relinquish operational control to sb（將營運控制權交出／讓渡給某人）！",
        "analysis": "【句構拆解與定位】不定詞 agreed to 後接原形及物動詞，受詞為 operational control（營運控制權），後接轉移對象介系詞片語 to an experienced chief executive。【核心考點與正解理由】觸發 860 弱點庫 #92：(A) relinquish 意為「正式放棄、交出（控制權、職位或權利）」，relinquish control to sb 為高分必考搭配。【常見陷阱提醒】(B) scrutinize 指仔細審查；(C) unveil 指揭幕發表；(D) ascertain 指查明真相。",
        "translation": "在出口利潤率連續三個季度下滑之後，創辦人同意將成衣企業的營運控制權交給一位經驗豐富的執行長。"
    },
    {
        "question": "The rapid completion of the transcontinental railway tunnel ahead of schedule stands as a remarkable ________ to the perseverance and ingenuity of our structural engineers.",
        "options": {"A": "testament", "B": "manifestation", "C": "succession", "D": "collateral"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #78：a testament to + N（對某人能力或毅力的最佳明證／鐵證）",
        "trap_point": "固定片語搭配：stands as a remarkable [testament] to...（作為對……的最佳證明）！",
        "analysis": "【句構拆解與定位】動詞片語 stands as a remarkable ________ to the perseverance... 中，空格後固定搭配介系詞 to，表示「作為對工程師堅毅精神的明證」。【核心考點與正解理由】觸發 860 弱點庫 #78：(A) testament 搭配介系詞 to（a testament to...），意為「……的確鑿證明、明證」。【常見陷阱提醒】(B) manifestation（表徵、展現）固定搭配介系詞 of（a manifestation of），不搭配 to。",
        "translation": "跨洲鐵路隧道能提前迅速竣工，正是我們結構工程師堅毅精神與卓越巧思的最佳明證。"
    },
    {
        "question": "Before approving the commercial mortgage, the regional bank required the borrower to pledge two downtown retail properties as loan ________.",
        "options": {"A": "collateral", "B": "incentive", "C": "quote", "D": "deficit"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #39：collateral（金融貸款之抵押品、擔保物）",
        "trap_point": "金融貸款情境核心字：pledge properties as loan [collateral]（將房產質押作為貸款抵押品）！",
        "analysis": "【句構拆解與定位】句首 Before approving the commercial mortgage 點出商業貸款情境，不定詞 to pledge two downtown retail properties as loan ________ 表示將兩處店面作為「貸款抵押擔保品」。【核心考點與正解理由】觸發 860 弱點庫 #39：(A) collateral 為不可數名詞「抵押品、擔保物」，loan collateral 為銀行融資必考術語。【常見陷阱提醒】(B) incentive 為激勵獎金；(C) quote 為報價單；(D) deficit 為赤字虧損。",
        "translation": "在核准該筆商業房貸之前，區域銀行要求借款人將兩處市中心零售房產質押作為貸款抵押品。"
    },
    {
        "question": "The compliance committee commended Ms. Vance for ________ discharging her auditing duties despite facing severe staffing shortages during the merger.",
        "options": {"A": "conscientiously", "B": "conscientious", "C": "conscience", "D": "subsequently"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #10 & #94：conscientiously（認真盡責地）+ discharge duties（履行職責）",
        "trap_point": "介系詞 for + [副詞 conscientiously] + 動名詞 discharging her duties：修飾動名詞 discharging 必用副詞！",
        "analysis": "【句構拆解與定位】介系詞 for 後接動名詞片語 discharging her auditing duties（此處 discharge 為一詞多義「履行職責」），空格位於動名詞前修飾其執行態度，必須填入副詞。【核心考點與正解理由】觸發 860 弱點庫 #10 與 #94：(A) conscientiously 為副詞「認真負責地、盡責地」，修飾動名詞 discharging。【常見陷阱提醒】動名詞 V-ing 仍具動詞性質，前方修飾語須用副詞 conscientiously 而非形容詞 conscientious。",
        "translation": "合規委員會表揚 Vance 女士在併購期間儘管面臨嚴重的人力短缺，依然認真盡責地履行其稽核職責。"
    },
]


CLOZE_PASSAGES_BANK = [
    {
        "title": "MEMORANDUM: Downtown Office Complex Relocation & Temporary Transit Guidelines",
        "text_type": "Corporate Facility Notice (Part 6 段落填空)",
        "content": (
            "To: All Full-Time Personnel and Seasonal Temps\n"
            "From: Facilities Management Committee\n"
            "Subject: Relocation to the Harborview Office Complex\n\n"
            "Please be advised that our headquarters will officially relocate to the newly constructed Harborview Office Complex next Monday. "
            "Because municipal crews are currently conducting a road ___[1]___ project along Main Street, vehicular access to the main entrance will be restricted throughout the week. "
            "___[2]___, employees commuting by private car are strongly encouraged to use the underground garage entrance on Fourth Avenue, which remains accessible to staff and visitors alike.\n\n"
            "Furthermore, personal office items ___[3]___ behind in the old building after Friday at 5:00 P.M. will be donated to local charities. "
            "It is imperative that every department coordinator ___[4]___ whether all confidential client files have been securely packed into encrypted crates prior to Friday noon."
        ),
        "questions": [
            {
                "blank_num": 1,
                "question": "Select the best word for Blank [1]: '...municipal crews are currently conducting a road ___[1]___ project along Main Street...'",
                "options": {"A": "repaving", "B": "rehearsal", "C": "quote", "D": "garment"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #49：repaving（道路重新鋪設工程）",
                "analysis": "【前後文脈絡定位】前文提及 municipal crews（市政施工團隊）與 along Main Street，後文提到車輛通行受限（vehicular access will be restricted），故空格需填入與道路工程相關之名詞修飾 project。【正解確認】(A) repaving 指「道路重新鋪設」，road repaving project 為多益交通改道公告最高頻搭配。",
                "translation": "由於市政工程團隊目前正在主街進行道路重新鋪設工程，本週將限制車輛由正門進出。"
            },
            {
                "blank_num": 2,
                "question": "Select the best transition word for Blank [2]: '___[2]___, employees commuting by private car are strongly encouraged to use the underground garage...'",
                "options": {"A": "Consequently", "B": "Whereas", "C": "Regardless of", "D": "As if"},
                "answer": "A",
                "rule_ref": "860 轉折與因果副詞辨析：獨立子句句首 + 逗號 -> 選連接副詞",
                "analysis": "【前後文脈絡定位】前句說明正門因鋪路而限制通行，本句提出「因此建議開車員工改走四號大道地下車庫」，前後為因果關係，且空格後有逗號並接完整獨立子句。【正解確認】(A) Consequently（因此、結果）為連接副詞，置於句首搭配逗號完全正確。(B)(D) 為從屬連接詞不可單獨配逗號而不接從屬子句；(C) 為介系詞片語。",
                "translation": "因此，強烈建議開車通勤的員工改用四號大道的地下停車場入口，該入口對員工與訪客一視同仁開放。"
            },
            {
                "blank_num": 3,
                "question": "Select the best verb/participle form for Blank [3]: '...personal office items ___[3]___ behind in the old building after Friday at 5:00 P.M. will be donated...'",
                "options": {"A": "left", "B": "are left", "C": "have been left", "D": "leaving"},
                "answer": "A",
                "rule_ref": "一山不容二虎 Rule 3：簡化關係子句（主句已有真動詞 will be donated，無關代必選過去分詞 left）",
                "analysis": "【前後文脈絡定位】本句主詞為 personal office items，主要真動詞為後半句的 will be donated！中間沒有關係代名詞 which/that，故空格必須填入分詞作後位修飾。【正解確認】物品是「被遺留下的」，故選過去分詞 (A) left（left behind）。(B)(C) 皆為真動詞，會觸犯一山不容二虎原則。",
                "translation": "此外，週五下午五點後遺留在舊大樓內的個人辦公物品，將全數捐贈予當地慈善機構。"
            },
            {
                "blank_num": 4,
                "question": "Select the best verb form for Blank [4]: 'It is imperative that every department coordinator ___[4]___ whether all confidential client files have been securely packed...'",
                "options": {"A": "ascertain", "B": "ascertained", "C": "ascertaining", "D": "to ascertain"},
                "answer": "A",
                "rule_ref": "重要性假設語氣 Rule 1 & 單字 #06：It is imperative that + S + (should) + 原形動詞 ascertain（查明）",
                "analysis": "【前後文脈絡定位】句首 It is imperative that... 觸發重要性假設語氣，that 子句主詞為單數名詞 every department coordinator，後接省略 should 的「原形動詞」。【正解確認】(A) ascertain 為原形及物動詞「查明、確定（是否所有機密檔案皆已裝箱）」，完全符合虛擬語氣規則。",
                "translation": "務必請每位部門協調員於週五中午前查明是否所有客戶機密檔案皆已安全裝入加密貨箱，這點至關重要。"
            },
        ],
    },
    {
        "title": "EMAIL: Confidential Merger Inquiry & Financial Audit Protocol",
        "text_type": "Executive Legal Email (Part 6 段落填空)",
        "content": (
            "To: Senior Audit Partners\n"
            "From: Helena Vance, Chief Legal Counsel\n"
            "Subject: Due Diligence for the Apex Robotics Acquisition\n\n"
            "As we enter the final stage of negotiating the ___[1]___ of Apex Robotics, all members of the auditing committee are reminded to maintain strict confidentiality. "
            "Please be extremely ___[2]___ when discussing financial valuations in public venues, and refrain from leaving printed spreadsheets on conference tables.\n\n"
            "During yesterday's preliminary review, our analysts noticed a minor ___[3]___ between the vendor's tax filings and their warehouse collateral records. "
            "We have asked their accounting team to submit the missing documentation ___ [4]___ our legal advisors can finalize the termination and liability clauses before Monday."
        ),
        "questions": [
            {
                "blank_num": 1,
                "question": "Select the best noun for Blank [1]: 'As we enter the final stage of negotiating the ___[1]___ of Apex Robotics...'",
                "options": {"A": "acquisition", "B": "alternation", "C": "rehearsal", "D": "collision"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #81：acquisition（企業併購、收購案）",
                "analysis": "【前後文脈絡定位】主旨與內文提及對 Apex Robotics 進行盡職調查（Due Diligence）與財務估值，定冠詞 the 與 of Apex Robotics 之間需填入表「企業收購案」的名詞。【正解確認】(A) acquisition 意為「企業併購、收購」，為 M&A 商務情境核心字。",
                "translation": "隨著我們進入談判收購 Apex Robotics 的最後階段，謹提醒稽核委員會所有成員維持嚴格保密。"
            },
            {
                "blank_num": 2,
                "question": "Select the best adjective for Blank [2]: 'Please be extremely ___[2]___ when discussing financial valuations in public venues...'",
                "options": {"A": "discreet", "B": "discrete", "C": "deficient", "D": "devastating"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #07 & 易混淆表：discreet（言行謹慎保密的）vs. discrete（個別分開的）",
                "analysis": "【前後文脈絡定位】前句強調維持嚴格保密（maintain strict confidentiality），本句提醒在公共場所討論財務估值時務必「言行謹慎、守口如瓶」。【正解確認】(A) discreet（兩個 e 緊連）指「謹慎低調保密的」；(B) discrete 指「分開獨立的」，切勿混淆！",
                "translation": "在公共場所討論財務估值時請務必極度謹慎低調，並切勿將列印出的試算表留在會議桌上。"
            },
            {
                "blank_num": 3,
                "question": "Select the best noun for Blank [3]: '...our analysts noticed a minor ___[3]___ between the vendor's tax filings and their warehouse collateral records.'",
                "options": {"A": "discrepancy", "B": "discrimination", "C": "dedication", "D": "perseverance"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #33：discrepancy between A and B（帳目／紀錄之間的不一致與出入）",
                "analysis": "【前後文脈絡定位】空格後接介系詞片語 between the vendor's tax filings and their warehouse collateral records（報稅申報與倉庫抵押品紀錄之間），財務對帳發現的「不一致、出入」必選 discrepancy。【正解確認】(A) discrepancy 完美搭配 between A and B。",
                "translation": "在昨日的初步審查中，我們的分析師發現該廠商的報稅資料與其倉庫抵押品紀錄之間存在微幅出入。"
            },
            {
                "blank_num": 4,
                "question": "Select the best conjunction for Blank [4]: 'We have asked their accounting team to submit the missing documentation ___[4]___ our legal advisors can finalize...'",
                "options": {"A": "in order that", "B": "regardless of", "C": "as far as", "D": "nonetheless"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #37：in order that + S + can/may + V（為了、以便……，引導目的副詞子句）",
                "analysis": "【前後文脈絡定位】空格後為含情態助動詞 can 的完整子句 our legal advisors can finalize...，說明要求補交文件的「目的」。【正解確認】(A) in order that 為從屬連接詞「為了、以便」，後接含 can/may/could 的完整子句。(B) 為介系詞；(C) 表範圍；(D) 為副詞不可連接子句。",
                "translation": "我們已要求其會計團隊補交缺漏的文件，以便我們的法律顧問能在週一前敲定終止與責任條款。"
            },
        ],
    },
    {
        "title": "ANNOUNCEMENT: Annual Culinary & Sustainable Packaging Expo",
        "text_type": "Trade Show Announcement (Part 6 段落填空)",
        "content": (
            "The Nordic Hospitality Association is delighted to ___[1]___ the schedule for this year's Culinary & Sustainable Packaging Expo, which will be held at the Grand Harbor Venue from November 18 to 20. "
            "With biodegradable takeout containers becoming increasingly ___[2]___ across the food-service industry, this year's keynote panels will focus on transitioning toward a circular economy.\n\n"
            "All exhibitor booth applications and promotional ___[3]___ must be uploaded to the organizer portal by Friday. "
            "Complimentary shuttle buses will operate every twenty minutes between the central train station and the exhibition hall, ___[4]___ eliminating parking congestion along the coast."
        ),
        "questions": [
            {
                "blank_num": 1,
                "question": "Select the best verb for Blank [1]: 'The Nordic Hospitality Association is delighted to ___[1]___ the schedule for this year's Expo...'",
                "options": {"A": "unveil", "B": "relinquish", "C": "abstain", "D": "resent"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #17：unveil（首次公布、揭幕、發表）",
                "analysis": "【前後文脈絡定位】不定詞 is delighted to 後接及物動詞原形與受詞 the schedule for this year's Expo（今年博覽會的日程表）。【正解確認】(A) unveil 意為「公布、揭曉、發表（新計畫或日程）」，同義於 reveal / announce。",
                "translation": "北歐餐旅協會欣然公布今年餐飲與永續包裝博覽會的日程表，活動將於 11 月 18 日至 20 日在海港大展館舉行。"
            },
            {
                "blank_num": 2,
                "question": "Select the best adjective for Blank [2]: 'With biodegradable takeout containers becoming increasingly ___[2]___ across the food-service industry...'",
                "options": {"A": "pervasive", "B": "deficient", "C": "negligent", "D": "inclement"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #09：pervasive（無處不在的、普遍深入的）",
                "analysis": "【前後文脈絡定位】附帶狀況 With... becoming increasingly ________ across the food-service industry 描述可生物降解外帶容器在餐飲業變得「越來越普及、無處不在」。【正解確認】(A) pervasive 意為「遍布的、普遍盛行的」，搭配 across the industry 語意最精準。",
                "translation": "隨著可生物降解外帶容器在餐飲服務業日益普及，今年的專題座談將聚焦於邁向循環經濟的轉型。"
            },
            {
                "blank_num": 3,
                "question": "Select the best noun for Blank [3]: 'All exhibitor booth applications and promotional ___[3]___ must be uploaded to the organizer portal...'",
                "options": {"A": "literature", "B": "collateral", "C": "succession", "D": "perseverance"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #86：literature 多益熟詞偏義（產品宣傳品、文宣手冊）",
                "analysis": "【前後文脈絡定位】與 exhibitor booth applications（參展攤位申請書）並列，且受形容詞 promotional（宣傳促銷的）修飾，指參展商的「宣傳文宣、產品型錄手冊」。【正解確認】(A) promotional literature 為多益必考熟詞偏義「宣傳文宣品」。",
                "translation": "所有參展商攤位申請書與宣傳文宣手冊皆須於週五前上傳至主辦單位入口網站。"
            },
            {
                "blank_num": 4,
                "question": "Select the best adverb for Blank [4]: '...between the central train station and the exhibition hall, ___[4]___ eliminating parking congestion along the coast.'",
                "options": {"A": "thereby", "B": "however", "C": "whereas", "D": "as far as"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #20：, thereby + V-ing（藉此／從而達成某結果）",
                "analysis": "【前後文脈絡定位】前句說明免費接駁巴士每二十分鐘往返火車站與展館，逗號後緊接現在分詞 eliminating parking congestion（消除沿海停車壅塞），表前項措施帶來的正面結果。【正解確認】(A) thereby + V-ing 為標準結果分詞構句。",
                "translation": "免費接駁巴士將每二十分鐘往返於中央火車站與展覽館之間，藉此消除沿海地區的停車壅塞。"
            },
        ],
    },
    {
        "title": "POLICY UPDATE: Stringent Quality Scrutiny & Supplier Compliance",
        "text_type": "Manufacturing Quality Directive (Part 6 段落填空)",
        "content": (
            "Effective December 1, Helios Medical Devices, ___[1]___ the surgical laser systems are distributed to hospitals worldwide, will enforce more stringent quality standards across all component suppliers. "
            "Recent inspections revealed that a small batch of optical lenses was ___[2]___ in anti-reflective coating thickness.\n\n"
            "To prevent future product recalls, quality assurance engineers will thoroughly ___[3]___ every incoming shipment before signing the courier receipt. "
            "Suppliers are also cautioned ___[4]___ making any unauthorized alteration to approved raw-material specifications without prior written consent."
        ),
        "questions": [
            {
                "blank_num": 1,
                "question": "Select the best relative phrase for Blank [1]: 'Helios Medical Devices, ___[1]___ the surgical laser systems are distributed to hospitals worldwide, will enforce...'",
                "options": {"A": "of which", "B": "whose", "C": "which", "D": "whom"},
                "answer": "A",
                "rule_ref": "微觀訊號第 3 條 (Signals 3)：先行詞, of which + the + N（後方已有定冠詞 the，必選 of which）",
                "analysis": "【前後文脈絡定位】先行詞為 Helios Medical Devices，逗號後關係子句主詞為 the surgical laser systems（注意前方已印有定冠詞 the！）。【正解確認】觸發微觀訊號第 3 條：whose 後不可加 the；當名詞前已有 the 時，必須選 (A) of which。",
                "translation": "自 12 月 1 日起，旗下手術雷射系統銷往全球醫院的 Helios 醫療器材公司，將對所有零組件供應商實施更嚴格的品質標準。"
            },
            {
                "blank_num": 2,
                "question": "Select the best adjective for Blank [2]: '...revealed that a small batch of optical lenses was ___[2]___ in anti-reflective coating thickness.'",
                "options": {"A": "deficient", "B": "prominent", "C": "autonomous", "D": "unanimous"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #04：be deficient in + N（在……方面不足／有缺陷）",
                "analysis": "【前後文脈絡定位】前文提及需要實施更嚴格品質標準，因為檢查發現一小批光學鏡片在防反射塗層厚度上「不足／有缺陷」，且後方搭配介系詞 in。【正解確認】(A) deficient 固定搭配 in（be deficient in 在……方面缺乏或有瑕疵）。",
                "translation": "近期檢驗顯示，有一小批光學鏡片在抗反射塗層厚度上存在缺陷與不足。"
            },
            {
                "blank_num": 3,
                "question": "Select the best verb for Blank [3]: '...quality assurance engineers will thoroughly ___[3]___ every incoming shipment before signing the courier receipt.'",
                "options": {"A": "scrutinize", "B": "concede", "C": "narrate", "D": "scatter"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #77：scrutinize（仔細審查、澈底檢驗）",
                "analysis": "【前後文脈絡定位】為防止產品召回，品保工程師在簽收快遞收據前將會徹底「仔細審查、檢驗」每一批進貨。【正解確認】(A) scrutinize 意為「仔細檢查、徹底審視」，與副詞 thoroughly 及品管情境完美契合。",
                "translation": "為防止未來發生產品召回，品保工程師在簽收快遞收據前將徹底檢驗每一批進貨。"
            },
            {
                "blank_num": 4,
                "question": "Select the best preposition for Blank [4]: 'Suppliers are also cautioned ___[4]___ making any unauthorized alteration to approved raw-material specifications...'",
                "options": {"A": "against", "B": "for", "C": "with", "D": "into"},
                "answer": "A",
                "rule_ref": "微觀訊號第 2 條 (Signals 2) & 單字 #84：be cautioned against + V-ing（告誡切勿做某事）",
                "analysis": "【前後文脈絡定位】被動語態 Suppliers are also cautioned 後接動名詞片語 making any unauthorized alteration（進行任何未經授權的修改），表「警告切勿擅自更改規格」。【正解確認】觸發微觀訊號第 2 條：caution sb against V-ing，秒選 (A) against。",
                "translation": "同時亦告誡供應商，在未獲事前書面同意前，切勿對已核准的原物料規格進行任何未經授權的修改。"
            },
        ],
    },
    {
        "title": "INTERNAL MEMO: Executive Succession & Board Voting Procedures",
        "text_type": "Board Governance Memo (Part 6 段落填空)",
        "content": (
            "Following twelve years of distinguished service, Chairman Arthur Pendelton has announced his intention to ___[1]___ his executive role at the end of the fourth quarter. "
            "His unwavering ___[2]___ to technological innovation has transformed our firm from a regional courier into a prominent global logistics enterprise.\n\n"
            "The corporate governance committee will convene next Tuesday to vote on the leadership ___[3]___ plan. "
            "In accordance with our charter, any board director who has a personal financial relationship with a nominated candidate must ___[4]___ from voting during the ballot."
        ),
        "questions": [
            {
                "blank_num": 1,
                "question": "Select the best verb for Blank [1]: '...Chairman Arthur Pendelton has announced his intention to ___[1]___ his executive role at the end of the fourth quarter.'",
                "options": {"A": "relinquish", "B": "prohibit", "C": "confine", "D": "expose"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #92：relinquish one's role / position（正式卸下／放棄職位與職權）",
                "analysis": "【前後文脈絡定位】前文提及服務滿十二年後，董事長宣布打算在第四季末「卸下、交出」其執行職務，後段亦提到領導層交班（succession plan）。【正解確認】(A) relinquish 意為「正式放棄、交出（職位或控制權）」，搭配 his executive role 最精準。",
                "translation": "在卓越服務滿十二年後，Arthur Pendelton 董事長已宣布打算於第四季末卸下其執行職務。"
            },
            {
                "blank_num": 2,
                "question": "Select the best noun for Blank [2]: 'His unwavering ___[2]___ to technological innovation has transformed our firm...'",
                "options": {"A": "dedication", "B": "negligence", "C": "fluctuation", "D": "collision"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #76：dedication to + N（對……的無私奉獻與專注投入）",
                "analysis": "【前後文脈絡定位】形容詞 unwavering（堅定不移的）後接名詞，並搭配介系詞 to technological innovation，讚揚董事長對技術創新的「奉獻與投入」。【正解確認】(A) dedication 固定搭配介系詞 to，語意積極正面。",
                "translation": "他對技術創新堅定不移的奉獻投入，已將我們公司從一家區域快遞商轉型為傑出的全球物流企業。"
            },
            {
                "blank_num": 3,
                "question": "Select the best noun for Blank [3]: 'The corporate governance committee will convene next Tuesday to vote on the leadership ___[3]___ plan.'",
                "options": {"A": "succession", "B": "termination", "C": "discrimination", "D": "alteration"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #13：leadership succession plan（領導層繼任／交班計畫）",
                "analysis": "【前後文脈絡定位】前段說明董事長即將卸任，本段治理委員會開會投票表決的應為「領導層接班／繼任計畫」。【正解確認】(A) succession 指「繼任、接替」，leadership succession plan 為多益高階人資與董事會必考語塊。",
                "translation": "公司治理委員會將於下週二召開會議，就領導層繼任交班計畫進行投票表決。"
            },
            {
                "blank_num": 4,
                "question": "Select the best verb for Blank [4]: '...any board director who has a personal financial relationship with a nominated candidate must ___[4]___ from voting...'",
                "options": {"A": "abstain", "B": "resent", "C": "concede", "D": "unveil"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #44：abstain from voting（於投票中棄權迴避）",
                "analysis": "【前後文脈絡定位】與被提名人有私人財務關係的董事，在投票表決時必須「棄權迴避」，空格後搭配介系詞片語 from voting。【正解確認】(A) abstain from voting 為多益必考固定片語。",
                "translation": "依據本公司章程，任何與被提名候選人有私人財務關係的董事，在無記名投票期間皆必須棄權迴避。"
            },
        ],
    },
    {
        "title": "CUSTOMER NOTICE: Outdoor Concert Venue & Inclement Weather Policy",
        "text_type": "Event Operations Notice (Part 6 段落填空)",
        "content": (
            "Thank you for purchasing tickets to the Starlight Symphony performance at the Bayside Amphitheater. "
            "Weather ___[1]___, the orchestra will perform the entire two-hour program on the open-air stage overlooking the marina, followed by areception for VIP pass holders.\n\n"
            "___[2]___ severe inclement weather or coastal gale warnings on the evening of the concert, the performance will be relocated to the indoor Philharmonic Hall two blocks east. "
            "Should a schedule or venue change occur, ticket holders will be notified via text message; ___[3]___, the remainder of the weekend festival itinerary will proceed as planned. "
            "Please note that all ticket prices are ___[4]___ of municipal entertainment taxes and shuttle service fees."
        ),
        "questions": [
            {
                "blank_num": 1,
                "question": "Select the best participle/verb for Blank [1]: 'Weather ___[1]___, the orchestra will perform the entire two-hour program on the open-air stage...'",
                "options": {"A": "permitting", "B": "permits", "C": "permitted", "D": "to permit"},
                "answer": "A",
                "rule_ref": "一山不容二虎 Rule 1：獨立分詞構句 Weather permitting（若天氣允許的話）",
                "analysis": "【前後文脈絡定位】逗號後為完整主句 the orchestra will perform...，逗號前僅有名詞 Weather 且無連接詞 if。【正解確認】觸發一山不容二虎 Rule 1：獨立分詞構句必用現在分詞 (A) permitting，絕不可選真動詞 permits。",
                "translation": "若天氣允許的話，交響樂團將在俯瞰遊艇碼頭的露天舞台演出完整兩小時節目。"
            },
            {
                "blank_num": 2,
                "question": "Select the best prepositional phrase for Blank [2]: '___[2]___ severe inclement weather or coastal gale warnings on the evening of the concert, the performance will be relocated...'",
                "options": {"A": "In the event of", "B": "In the event that", "C": "Provided that", "D": "Whereas"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #31 & #64：in the event of + 名詞片語 (inclement weather) vs. in the event that + 子句",
                "analysis": "【前後文脈絡定位】逗號前 severe inclement weather or coastal gale warnings 為純名詞片語（無任何動詞！），表示「萬一發生惡劣天氣」。【正解確認】(A) In the event of 為複合介系詞，後接名詞片語；(B)(C)(D) 均為從屬連接詞，後方必須接完整 S+V 子句。",
                "translation": "萬一音樂會當晚出現嚴重惡劣天氣或沿海強風警報，演出將移師至東側兩個街區外的室內愛樂廳舉行。"
            },
            {
                "blank_num": 3,
                "question": "Select the best transition adverb for Blank [3]: '...ticket holders will be notified via text message; ___[3]___, the remainder of the weekend festival itinerary will proceed as planned.'",
                "options": {"A": "nonetheless", "B": "thereby", "C": "namely", "D": "because"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #21 & 易混淆表：; nonetheless,（然而／儘管如此）+ the remainder（其餘部分）",
                "analysis": "【前後文脈絡定位】分號前說明若場地異動會發簡訊通知，分號後說明「儘管如此，週末音樂節其餘的行程（the remainder of the itinerary）仍將照常進行」，前後為讓步轉折，且夾在分號與逗號之間。【正解確認】(A) nonetheless（儘管如此、然而）語法與語意完全吻合。",
                "translation": "萬一時間或場地有所更動，持票人將收到簡訊通知；儘管如此，週末音樂節其餘的日程仍將按原定計畫進行。"
            },
            {
                "blank_num": 4,
                "question": "Select the best adjective for Blank [4]: 'Please note that all ticket prices are ___[4]___ of municipal entertainment taxes and shuttle service fees.'",
                "options": {"A": "inclusive", "B": "prominent", "C": "persistent", "D": "resourceful"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #46：be inclusive of + N（包含……費用／稅金在內）",
                "analysis": "【前後文脈絡定位】空格位於 are 與介系詞 of 之間，說明所有票價皆「包含」娛樂稅與接駁車費。【正解確認】(A) inclusive 固定搭配 of（inclusive of taxes 包含稅金在內）。",
                "translation": "請注意，所有門票價格皆已包含市政娛樂稅與接駁車服務費。"
            },
        ],
    },
]

CLOZE_PASSAGES_BANK.extend([
    {
        "title": "PRESS RELEASE: Autonomous Maritime Freight & Coastal Port Expansion",
        "text_type": "Corporate Press Release (Part 6 段落填空)",
        "content": (
            "OSLO — Vestergaard Maritime announced today that it has completed the ___[1]___ of two regional container terminals along the coast of southern Norway. "
            "With global shipping rates continuing to experience sharp ___[2]___, the company's autonomous cargo vessels offer exporters a reliable and cost-effective alternative.\n\n"
            "Each vessel is equipped with optical radar sensors designed to prevent ___[3]___ in congested harbor channels. "
            "___[4]___ the new fleet passes final maritime safety scrutiny next week, commercial operations will commence on December 15."
        ),
        "questions": [
            {
                "blank_num": 1,
                "question": "Select the best noun for Blank [1]: '...announced today that it has completed the ___[1]___ of two regional container terminals along the coast...'",
                "options": {"A": "acquisition", "B": "abstention", "C": "rehearsal", "D": "stapler"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #81：acquisition（企業併購、收購案）",
                "analysis": "【前後文脈絡定位】完成對挪威南部沿海兩座區域貨櫃碼頭的「收購案」，the + [名詞] + of 結構必選 acquisition。【正解確認】(A) acquisition 指企業或資產收購。",
                "translation": "Vestergaard 海運今日宣布，已完成對挪威南部沿海兩座區域貨櫃碼頭的收購案。"
            },
            {
                "blank_num": 2,
                "question": "Select the best noun for Blank [2]: 'With global shipping rates continuing to experience sharp ___[2]___, the company's autonomous cargo vessels offer...'",
                "options": {"A": "fluctuation", "B": "perseverance", "C": "literature", "D": "takeout"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #40：fluctuation（價格／匯率之劇烈波動與起伏）",
                "analysis": "【前後文脈絡定位】全球海運費率持續出現劇烈的「波動起伏（sharp fluctuation）」，故公司的自動駕駛貨輪提供了穩定且具成本效益的替代方案。【正解確認】(A) fluctuation 指價格或費率波動。",
                "translation": "隨著全球海運費率持續經歷劇烈波動，該公司的自動駕駛貨輪為出口商提供了可靠且具成本效益的替代方案。"
            },
            {
                "blank_num": 3,
                "question": "Select the best noun for Blank [3]: 'Each vessel is equipped with optical radar sensors designed to prevent ___[3]___ in congested harbor channels.'",
                "options": {"A": "collision", "B": "clause", "C": "venue", "D": "quote"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #66：collision（碰撞事故、相撞）",
                "analysis": "【前後文脈絡定位】配備光學雷達感測器的目的是為了在擁擠的港口航道中防止「船隻碰撞（collision）」。【正解確認】(A) collision 指碰撞事故。",
                "translation": "每艘船隻皆配備光學雷達感測器，旨在防止於擁擠的港口航道中發生碰撞事故。"
            },
            {
                "blank_num": 4,
                "question": "Select the best conjunction for Blank [4]: '___[4]___ the new fleet passes final maritime safety scrutiny next week, commercial operations will commence on December 15.'",
                "options": {"A": "Provided that", "B": "As far as", "C": "Regardless of", "D": "Nonetheless"},
                "answer": "A",
                "rule_ref": "條件句辨析 Rule 2：Provided that（只要……／以……為條件）vs. As far as（就……範圍而言）",
                "analysis": "【前後文脈絡定位】逗號前 the new fleet passes final maritime safety scrutiny next week 為完整條件子句（只要新船隊下週通過最終海事安全審查），主句便於 12/15 展開商業營運。【正解確認】(A) Provided that 引導條件副詞子句。",
                "translation": "只要新船隊於下週通過最終海事安全審查，商業營運將於 12 月 15 日正式展開。"
            },
        ],
    },
    {
        "title": "HR DIRECTIVE: Seasonal Temps Onboarding & Workplace Conduct",
        "text_type": "Human Resources Directive (Part 6 段落填空)",
        "content": (
            "To accommodate peak holiday order volume at our fulfillment premises, the warehouse committee has hired forty seasonal ___[1]___ for the November–December period. "
            "Department supervisors are tasked with ensuring that all new recruits receive a standardized training ___[2]___ and safety vest upon arrival.\n\n"
            "Our organization maintains a strict policy against any form of workplace ___[3]___ or safety negligence. "
            "Furthermore, because our domestic market is highly ___[4]___, employees who suggest workflow improvements that reduce packaging waste will receive a $300 cash incentive."
        ),
        "questions": [
            {
                "blank_num": 1,
                "question": "Select the best plural noun for Blank [1]: '...the warehouse committee has hired forty seasonal ___[1]___ for the November–December period.'",
                "options": {"A": "temps", "B": "staplers", "C": "garments", "D": "editorials"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #67：temps（臨時雇員、季節性約聘人員，等同於 temporary workers）",
                "analysis": "【前後文脈絡定位】為因應連假訂單高峰，倉庫委員會聘請了四十名季節性「臨時員工（seasonal temps）」。【正解確認】(A) temps 為多益人資情境必考口語／通知字彙。",
                "translation": "為因應我們出貨廠區的連假訂單高峰，倉庫委員會已針對十一至十二月期間聘請了四十名季節性臨時雇員。"
            },
            {
                "blank_num": 2,
                "question": "Select the best noun for Blank [2]: '...ensuring that all new recruits receive a standardized training ___[2]___ and safety vest upon arrival.'",
                "options": {"A": "brochure", "B": "collision", "C": "deficit", "D": "exposure"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #56：brochure（宣傳冊、培訓指引手冊，同義於 pamphlet）",
                "analysis": "【前後文脈絡定位】新進人員報到時會領取一份標準化「培訓手冊（training brochure）」與安全背心。【正解確認】(A) brochure 指小冊子、手冊。",
                "translation": "部門主管負責確保所有新進人員在報到時皆能領取一份標準化培訓手冊與安全背心。"
            },
            {
                "blank_num": 3,
                "question": "Select the best noun for Blank [3]: 'Our organization maintains a strict policy against any form of workplace ___[3]___ or safety negligence.'",
                "options": {"A": "discrimination", "B": "alteration", "C": "succession", "D": "rehearsal"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #34：workplace discrimination（職場歧視）",
                "analysis": "【前後文脈絡定位】本公司對任何形式的「職場歧視（workplace discrimination）」或安全疏失（negligence）採取嚴格禁止政策。【正解確認】(A) discrimination 搭配 workplace 最合乎人資規章。",
                "translation": "本機構對任何形式的職場歧視或安全疏失皆維持嚴格禁止政策。"
            },
            {
                "blank_num": 4,
                "question": "Select the best adjective for Blank [4]: 'Furthermore, because our domestic market is highly ___[4]___, employees who suggest workflow improvements...'",
                "options": {"A": "saturated", "B": "inclement", "C": "culinary", "D": "complimentary"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #73：saturated market（飽和的市場）",
                "analysis": "【前後文脈絡定位】形容國內市場已經高度「飽和（highly saturated）」，因此更需要透過改善流程減少包裝浪費來提升獲利。【正解確認】(A) saturated 為市場分析必考形容詞。",
                "translation": "此外，由於我們的國內市場已高度飽和，提出能減少包裝浪費之工作流程改善建議的員工，將獲得三百美元現金獎勵。"
            },
        ],
    },
    {
        "title": "CLIENT LETTER: Commercial Loan Collateral & Contract Clause Review",
        "text_type": "Banking Advisory Letter (Part 6 段落填空)",
        "content": (
            "Dear Mr. Lindqvist,\n\n"
            "Our credit committee has reviewed your application for a commercial expansion loan. "
            "While we were impressed by your firm's ___[1]___ revenue growth over the past three years, our underwriters were somewhat critical ___[2]___ the machinery appraisal report submitted last week.\n\n"
            "Specifically, all valuation ___[3]___ for industrial equipment pledged as collateral must be certified by an independent third-party assessor. "
            "Once the revised appraisal is received, we will prepare the final loan agreement, including a standard early-repayment ___[4]___."
        ),
        "questions": [
            {
                "blank_num": 1,
                "question": "Select the best adjective for Blank [1]: 'While we were impressed by your firm's ___[1]___ revenue growth over the past three years...'",
                "options": {"A": "monumental", "B": "deficient", "C": "negligent", "D": "scattered"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #87：monumental（重大的、具里程碑意義的、極為可觀的）",
                "analysis": "【前後文脈絡定位】動詞片語 were impressed by（對……印象深刻）表示正面肯定，修飾過去三年的營收成長應選正面形容詞。【正解確認】(A) monumental 指「重大的、驚人可觀的」。",
                "translation": "雖然我們對貴公司過去三年來重大的營收成長印象深刻，但我們的核貸人員對上週提交的機器鑑價報告持保留批評態度。"
            },
            {
                "blank_num": 2,
                "question": "Select the best preposition for Blank [2]: '...our underwriters were somewhat critical ___[2]___ the machinery appraisal report submitted last week.'",
                "options": {"A": "of", "B": "with", "C": "against", "D": "from"},
                "answer": "A",
                "rule_ref": "微觀訊號第 1 條 (Signals 1)：be critical of + N（對……持批評／挑剔態度）",
                "analysis": "【前後文脈絡定位】空格前為 were somewhat critical，後方接名詞受詞 the machinery appraisal report。【正解確認】觸發微觀訊號第 1 條：形容詞 critical 後固定接介系詞 (A) of。",
                "translation": "我們的核貸審查人員對上週提交的機械鑑價報告抱持些許批評與質疑。"
            },
            {
                "blank_num": 3,
                "question": "Select the best plural noun for Blank [3]: 'Specifically, all valuation ___[3]___ for industrial equipment pledged as collateral must be certified...'",
                "options": {"A": "quotes", "B": "quote", "C": "quoting", "D": "quoted"},
                "answer": "A",
                "rule_ref": "微觀訊號第 4 條 (Signals 4) & 單字 #75：All + [單數名詞修飾語 valuation] + [複數核心名詞 quotes]",
                "analysis": "【前後文脈絡定位】量詞 all 後方印有單數不可數名詞 valuation 作修飾語，故空格核心主詞必須填入複數可數名詞。【正解確認】(A) quotes（估價單、報價單）為複數可數名詞，符合微觀訊號第 4 條。",
                "translation": "具體而言，所有作為抵押品之工業設備的估價單，都必須經過獨立第三方估價師認證。"
            },
            {
                "blank_num": 4,
                "question": "Select the best noun for Blank [4]: '...we will prepare the final loan agreement, including a standard early-repayment ___[4]___.'",
                "options": {"A": "clause", "B": "venue", "C": "courier", "D": "garment"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #24：clause（合約條款，如 early-repayment clause 提前還款條款）",
                "analysis": "【前後文脈絡定位】最終貸款合約（final loan agreement）中包含一項標準的「提前還款條款（early-repayment clause）」。【正解確認】(A) clause 指法律合約中的條款。",
                "translation": "一旦收到修訂後的鑑價報告，我們將備妥最終貸款合約，其中包含標準的提前還款條款。"
            },
        ],
    },
])


# Additional 13 bespoke 860+ questions covering remaining vocabulary items from 860_antigravity.md
QUESTIONS_860_BANK.extend([
    {
        "question": "Because the newly acquired manufacturing ________ comprises twelve interconnected warehouses and an on-site customs clearance center, visitors must wear identification badges at all times.",
        "options": {"A": "complex", "B": "complexity", "C": "complexly", "D": "stapler"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #59：complex 作名詞之熟詞偏義（複合建築群、工業園區）",
        "analysis": "【秒殺錨點】冠詞與分詞形容詞 the newly acquired manufacturing 後接單數主詞（後方動詞為 comprises），且語意指由十二座相連倉庫組成的「製造業複合園區」。【正解確認】(A) complex 作可數名詞時指「建築群、綜合園區（manufacturing complex）」，為多益熟詞偏義代表題。",
        "translation": "由於新收購的製造園區包含十二座相連的倉庫與一座駐廠海關清關中心，訪客必須隨時配戴識別證。"
    },
    {
        "question": "To promote a sustainable ________ economy across its European supply chain, the footwear manufacturer now offers a 20 percent discount to customers who return worn-out shoes for recycling.",
        "options": {"A": "circular", "B": "scattered", "C": "inclement", "D": "complimentary"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #62：circular economy（循環經濟，ESG 永續商業核心概念）",
        "analysis": "【秒殺錨點】後方說明顧客退回舊鞋回收再生可享八折優惠，此商業模式即為「循環經濟」。【正解確認】(A) circular economy 為固定永續專有名詞。",
        "translation": "為了在其歐洲供應鏈推廣永續的循環經濟，該鞋業製造商現在針對退回舊鞋進行回收的顧客提供八折優惠。"
    },
    {
        "question": "Although the investigative journalist's Sunday ________ praised the city's public transit expansion, it raised serious questions about how the municipal bond deficit would be repaid.",
        "options": {"A": "editorial", "B": "rehearsal", "C": "takeout", "D": "courier"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #74：editorial 作可數名詞（報章雜誌之社論、主編評論文章）",
        "analysis": "【秒殺錨點】所有格 journalist's Sunday 後接可數名詞作主詞，且後方描述「讚揚大眾運輸擴建但質疑市政債券赤字如何償還」，屬於報紙評論文章。【正解確認】(A) editorial 作名詞指「社論、評論」。",
        "translation": "儘管該調查記者的週日社論讚揚了本市的大眾運輸擴建計畫，但文中也對市政債券赤字將如何償還提出了嚴肅質疑。"
    },
    {
        "question": "Before the symphony orchestra's opening night at the newly renovated ________, the conductor scheduled an extra three-hour dress rehearsal to test the hall's acoustics.",
        "options": {"A": "venue", "B": "clause", "C": "collateral", "D": "abstention"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #15 & #70：venue（表演或會議場地）+ dress rehearsal（總彩排）",
        "analysis": "【秒殺錨點】介系詞片語 at the newly renovated 後接表示「演出場地、音樂廳會場」的名詞，且後文提到測試大廳音響效果與總彩排（rehearsal）。【正解確認】(A) venue 指「舉辦場地、會場」。",
        "translation": "在交響樂團於新翻修完成的場地舉行開幕夜演出前，指揮家額外安排了一場三小時的總彩排以測試大廳的音響效果。"
    },
    {
        "question": "Several confidential blueprints were left ________ across the conference room table after the engineering committee adjourned its emergency briefing.",
        "options": {"A": "scattered", "B": "scattering", "C": "scatters", "D": "to scatter"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #57 & 一山不容二虎：leave + O + V-ed（blueprints were left scattered 被散落在桌面上）",
        "analysis": "【秒殺錨點】主詞 blueprints（藍圖文件）與動詞 scatter（使散落）之間為「被動狀態」關係，用於 be left + V-ed 結構作主詞補語。【正解確認】(A) scattered across the table 表示「散落於會議桌上」。",
        "translation": "在工程委員會結束緊急簡報會議後，有數份機密藍圖被散落在會議室桌面上。"
    },
    {
        "question": "While waiting for the harbor ferry to depart, tourists can ________ the historic cobblestone boardwalk and browse the artisan boutiques along the coast.",
        "options": {"A": "stroll down", "B": "abstain from", "C": "confine to", "D": "dispense with"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #52 & #58：stroll down（沿著……漫步）+ along the coast（沿著海岸）",
        "analysis": "【秒殺錨點】助動詞 can 後接原形動詞片語，受詞為 the historic cobblestone boardwalk（歷史悠久的鵝卵石木棧道），描述遊客候船時可「沿著木棧道漫步」。【正解確認】(A) stroll down 為旅遊與 Part 1/5 高頻片語。",
        "translation": "在等待港口渡輪出發的期間，遊客可以沿著歷史悠久的鵝卵石木棧道漫步，並逛逛海岸線旁的手工藝精品店。"
    },
    {
        "question": "Due to the ongoing asphalt ________ project on Maple Avenue, delivery trucks must use the northern service gate while the main entrance remains accessible only to pedestrians.",
        "options": {"A": "repaving", "B": "rehearsing", "C": "resenting", "D": "unveiling"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #50 & #51：asphalt repaving project（柏油道路重鋪工程）+ pedestrians（行人）",
        "analysis": "【秒殺錨點】名詞 asphalt（柏油路面）與 project（工程）之間需填表示「道路重新鋪設」的動名詞作複合名詞修飾語。【正解確認】(A) repaving（重新鋪設路面）完全吻合交通改道情境。",
        "translation": "由於楓樹大道正在進行柏油路面重鋪工程，送貨卡車必須改走北側服務大門，而正門目前僅供行人通行。"
    },
    {
        "question": "Every Delicate Silk ________ manufactured at our Milan facility undergoes a rigorous hand-inspection process to ensure that the stitching and dye quality meet luxury retail standards.",
        "options": {"A": "garment", "B": "courier", "C": "takeout", "D": "deficit"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #55：garment（一件成衣、服裝，常用作 clothes 的正式商業替換詞）",
        "analysis": "【秒殺錨點】限定詞 Every 後接單數可數名詞，且後文提到 silk（絲綢）、stitching（縫線）與 dye quality（染色品質）。【正解確認】(A) garment 指「（一件）成衣、服裝」。",
        "translation": "在我們米蘭廠製造的每一件精緻絲綢成衣，皆須經過嚴格的人工檢驗流程，以確保縫線與染色品質符合精品零售標準。"
    },
    {
        "question": "To reduce plastic waste from midday ________ orders, the corporate cafeteria now provides reusable stainless-steel containers to employees who dine at their desks.",
        "options": {"A": "takeout", "B": "collateral", "C": "succession", "D": "abstention"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #48：takeout orders（外帶訂餐）",
        "analysis": "【秒殺錨點】後文說明員工把餐點帶回辦公桌吃（dine at their desks），為減少這類午間「外帶餐點（takeout orders）」產生的塑膠垃圾，員工餐廳改提供不鏽鋼環保餐盒。【正解確認】(A) takeout 指「外帶餐點」。",
        "translation": "為了減少午間外帶餐點所產生的塑膠廢棄物，公司員工餐廳現在提供可重複使用的不鏽鋼餐盒給在辦公桌用餐的員工。"
    },
    {
        "question": "Because the regional distribution manager was ________ with coordinating the cross-border inventory transfer, she delegated the weekly sales meeting to her deputy.",
        "options": {"A": "tasked", "B": "scattered", "C": "saturated", "D": "resented"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #53：be tasked with + N/V-ing（被指派負責……任務）",
        "analysis": "【秒殺錨點】空格前為 was，後方接介系詞 with coordinating...，構成被動片語「被賦予／被指派協調跨國庫存調度之任務」。【正解確認】(A) tasked（be tasked with 為多益必考動詞片語）。",
        "translation": "由於區域物流經理被指派負責協調跨國庫存移轉作業，她將每週業務會議交由副手主持。"
    },
    {
        "question": "Always keep a ________ projector bulb and HDMI adapter in the podium cabinet in the event that the primary audiovisual equipment malfunctions during a keynote speech.",
        "options": {"A": "spare", "B": "pervasive", "C": "deficient", "D": "discrete"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #61 & #31：spare bulb/parts（備用燈泡／零件）+ in the event that（萬一）",
        "analysis": "【秒殺錨點】後文說明「萬一主視聽設備在主題演講期間故障」，因此講台櫃子裡應隨時準備一顆「備用的（spare）」投影機燈泡與轉接頭。【正解確認】(A) spare 作形容詞指「備用的、多餘的」。",
        "translation": "請務必在講台儲物櫃中隨時準備一顆備用投影機燈泡與 HDMI 轉接頭，以防主視聽設備在主題演講期間發生故障。"
    },
    {
        "question": "Under the terms of the commercial lease, any structural ________ to the interior partition walls requires prior written consent from the property management committee.",
        "options": {"A": "alteration", "B": "altercate", "C": "alternatively", "D": "allusion"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #63 & 易混淆表：alteration（局部修改、改建）vs. alternative（替代方案）",
        "analysis": "【秒殺錨點】形容詞 structural 後接名詞，且搭配介系詞 to the interior partition walls（對室內隔間牆進行結構上的改動／改建）。【正解確認】(A) alteration 指「變更、改建、修改」。",
        "translation": "根據商業租賃契約條款，對室內隔間牆進行任何結構上的改建，皆須事先取得物業管理委員會的書面同意。"
    },
    {
        "question": "The newly appointed chief financial officer has been praised for her ________ in restructuring the company's short-term debt without laying off a single factory worker.",
        "options": {"A": "resourcefulness", "B": "negligence", "C": "discrepancy", "D": "collision"},
        "answer": "A",
        "rule_ref": "860 弱點庫 #80：resourceful (adj.) / resourcefulness (n.)（足智多謀、善於隨機應變解決問題的能力）",
        "analysis": "【秒殺錨點】動詞片語 has been praised for her（因她的……而備受讚揚）後接正面能力名詞，指她在不裁撤任何工廠員工的情況下成功重組短期債務的「足智多謀與應變手腕」。【正解確認】(A) resourcefulness 為 resourceful 之名詞形。",
        "translation": "新上任的財務長因其在不裁撤任何一名工廠員工的情況下，足智多謀地完成公司短期債務重組而備受讚揚。"
    },
])

# Additional 4 Cloze Passages (16 questions) so CLOZE_PASSAGES_BANK has 12 passages (48 Cloze questions)
CLOZE_PASSAGES_BANK.extend([
    {
        "title": "MEMORANDUM: Culinary Innovation Lab & Complimentary Tasting Menu",
        "text_type": "Hospitality Operations Memo (Part 6 段落填空)",
        "content": (
            "To: All Kitchen & Dining Room Staff\n"
            "From: Chef Julian Vance, Culinary Director\n"
            "Subject: Autumn Tasting Menu Launch\n\n"
            "Beginning next Friday, our downtown restaurant will ___[1]___ its new autumn tasting menu featuring organic ingredients sourced from farms along the coast. "
            "To generate positive media ___[2]___ ahead of the holiday dining season, we have invited twelve prominent food critics to a private preview dinner on Wednesday evening.\n\n"
            "All guests attending the preview will receive a ___[3]___ glass of sparkling apple cider upon arrival. "
            "During tomorrow's full-staff service ___[4]___, please pay close attention to the allergy protocol for dishes containing tree nuts."
        ),
        "questions": [
            {
                "blank_num": 1,
                "question": "Select the best verb for Blank [1]: 'Beginning next Friday, our downtown restaurant will ___[1]___ its new autumn tasting menu...'",
                "options": {"A": "unveil", "B": "abstain", "C": "resent", "D": "collide"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #16：unveil（首次推出、揭幕、正式公布新菜單或產品）",
                "analysis": "【前後文脈絡定位】助動詞 will 後接原形及物動詞，受詞為 its new autumn tasting menu（全新秋季品嚐菜單）。【正解確認】(A) unveil 指「首次公開、隆重推出」。",
                "translation": "自下週五起，我們位於市中心的餐廳將正式推出採用沿海農場有機食材製作的全新秋季品嚐菜單。"
            },
            {
                "blank_num": 2,
                "question": "Select the best noun for Blank [2]: 'To generate positive media ___[2]___ ahead of the holiday dining season, we have invited twelve prominent food critics...'",
                "options": {"A": "exposure", "B": "deficit", "C": "negligence", "D": "clause"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #14 & #1：media exposure（媒體曝光度）+ prominent（著名的）",
                "analysis": "【前後文脈絡定位】邀請十二位知名美食評論家參加預覽晚宴的目的，是為了在連假餐飲旺季前創造正面的「媒體曝光度（media exposure）」。【正解確認】(A) exposure 為不可數名詞，固定搭配 media exposure。",
                "translation": "為了在連假餐飲旺季前創造正面的媒體曝光度，我們已邀請十二位知名美食評論家參加週三晚間的私人預覽晚宴。"
            },
            {
                "blank_num": 3,
                "question": "Select the best adjective for Blank [3]: 'All guests attending the preview will receive a ___[3]___ glass of sparkling apple cider upon arrival.'",
                "options": {"A": "complimentary", "B": "complementary", "C": "deficient", "D": "pervasive"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #2 & 易混淆表：complimentary（免費招待的）vs. complementary（互補的）",
                "analysis": "【前後文脈絡定位】出席預覽晚宴的貴賓在抵達時皆會獲贈一杯「免費招待的（complimentary）」氣泡蘋果酒。【正解確認】(A) complimentary（字母 i）指「免費贈送的」；(B) complementary（字母 e）指「互補的」。",
                "translation": "所有出席預覽晚宴的貴賓在抵達時，皆可獲贈一杯免費招待的氣泡蘋果酒。"
            },
            {
                "blank_num": 4,
                "question": "Select the best noun for Blank [4]: 'During tomorrow's full-staff service ___[4]___, please pay close attention to the allergy protocol...'",
                "options": {"A": "rehearsal", "B": "collision", "C": "collateral", "D": "stapler"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #70 & #89：service rehearsal（餐飲服務彩排／預演）+ culinary（餐飲烹飪的）",
                "analysis": "【前後文脈絡定位】在正式晚宴登場前，全體外場與廚房人員於明日進行的應為「服務流程彩排／預演（service rehearsal）」。【正解確認】(A) rehearsal 指彩排、預演。",
                "translation": "在明日的全體員工服務流程彩排期間，請特別留意含堅果菜餚的過敏原處理規範。"
            },
        ],
    },
    {
        "title": "INTERNAL AUDIT REPORT: Inventory Discrepancy & Record-Keeping Scrutiny",
        "text_type": "Compliance Audit Memo (Part 6 段落填空)",
        "content": (
            "During last month's quarterly inspection of the central pharmaceutical depot, external auditors discovered a significant ___[1]___ between the digital stock ledger and the physical warehouse count. "
            "It is imperative that the root cause of this variance ___[2]___ before the regulatory filing deadline on November 20.\n\n"
            "Preliminary findings suggest that several night-shift supervisors were ___[3]___ in logging temperature-sensitive shipments upon arrival. "
            "Effective immediately, access to the cold-storage vault will be ___[4]___ to certified pharmacists and senior compliance officers."
        ),
        "questions": [
            {
                "blank_num": 1,
                "question": "Select the best noun for Blank [1]: '...external auditors discovered a significant ___[1]___ between the digital stock ledger and the physical warehouse count.'",
                "options": {"A": "discrepancy", "B": "discretion", "C": "dedication", "D": "perseverance"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #32 & 易混淆表：discrepancy（帳目／數據差異、出入）vs. discretion（自行決定權）",
                "analysis": "【前後文脈絡定位】數位庫存分類帳與倉庫實際盤點數量之間出現重大的「數據出入／不一致（discrepancy between A and B）」。【正解確認】(A) discrepancy 指帳目或數據不符；(B) discretion 指自由裁量權。",
                "translation": "在上個月對中央藥品倉庫進行的季度檢查中，外部稽核員發現數位庫存分類帳與倉庫實際盤點數量之間存在重大差異。"
            },
            {
                "blank_num": 2,
                "question": "Select the best verb form for Blank [2]: 'It is imperative that the root cause of this variance ___[2]___ before the regulatory filing deadline...'",
                "options": {"A": "be ascertained", "B": "is ascertained", "C": "ascertained", "D": "ascertaining"},
                "answer": "A",
                "rule_ref": "重要性假設語氣 Rule 1 & 單字 #5：It is imperative that + S + (should) + be ascertained（原形被動）",
                "analysis": "【前後文脈絡定位】句首 It is imperative that 觸發重要性假設語氣，that 子句動詞須用「(should) + 原形動詞」，且主詞 the root cause 為「被查明（be ascertained）」。【正解確認】(A) be ascertained 為唯一合法之原形被動語態。",
                "translation": "務必在 11 月 20 日法規申報截止日前，徹底查明此項帳目差異的根本原因。"
            },
            {
                "blank_num": 3,
                "question": "Select the best adjective for Blank [3]: 'Preliminary findings suggest that several night-shift supervisors were ___[3]___ in logging temperature-sensitive shipments...'",
                "options": {"A": "negligent", "B": "prominent", "C": "conscientious", "D": "inclusive"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #10：be negligent in + V-ing（在……方面疏忽職守／粗心大意）",
                "analysis": "【前後文脈絡定位】造成庫存帳目差異的原因，是數名夜班主管在登錄溫控貨件時「疏忽大意（were negligent in logging...）」。【正解確認】(A) negligent 指「疏忽的、失職的」。",
                "translation": "初步調查結果顯示，數名夜班主管在溫控貨件抵達時疏於登錄紀錄。"
            },
            {
                "blank_num": 4,
                "question": "Select the best participle for Blank [4]: 'Effective immediately, access to the cold-storage vault will be ___[4]___ to certified pharmacists and senior compliance officers.'",
                "options": {"A": "confined", "B": "unveiled", "C": "scattered", "D": "resented"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #42：be confined to + N（僅限於……／被限制在……範圍內）",
                "analysis": "【前後文脈絡定位】為加強管控，即日起冷藏庫的進出權限將「僅限於（be confined to）」合格藥師與資深法遵官。【正解確認】(A) confined 搭配介系詞 to 表示「限制於……」。",
                "translation": "即日起，冷藏庫的進出權限將僅限於合格藥師與資深法規遵循主管。"
            },
        ],
    },
    {
        "title": "EMPLOYEE RECOGNITION: Monumental Engineering Achievement Award",
        "text_type": "Executive Commendation Announcement (Part 6 段落填空)",
        "content": (
            "It is my privilege to announce that Senior Systems Architect Dr. Elena Rostova has been selected to receive this year's Chairman's Excellence Medal. "
            "Over the past eighteen months, Dr. Rostova has worked ___[1]___ to redesign our cloud encryption architecture across six discrete regional data centers.\n\n"
            "The successful deployment of the zero-trust protocol last week stands as a ___[2]___ to her technical brilliance and unwavering ___[3]___ in the face of complex hardware constraints. "
            "Her resourceful leadership has saved the corporation an estimated $4.2 million, ___[4]___ positioning our cybersecurity division as an industry benchmark."
        ),
        "questions": [
            {
                "blank_num": 1,
                "question": "Select the best adverb for Blank [1]: 'Over the past eighteen months, Dr. Rostova has worked ___[1]___ to redesign our cloud encryption architecture...'",
                "options": {"A": "conscientiously", "B": "negligently", "C": "somewhat", "D": "namely"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #9：work conscientiously（認真盡責地、一絲不苟地工作）",
                "analysis": "【前後文脈絡定位】修飾動詞 has worked，表揚得獎者在過去十八個月來「一絲不苟、認真盡責地（conscientiously）」重新設計雲端加密架構。【正解確認】(A) conscientiously 為正面態度副詞。",
                "translation": "在過去十八個月裡，Rostova 博士一絲不苟地致力於重新設計我們橫跨六座獨立區域資料中心的雲端加密架構。"
            },
            {
                "blank_num": 2,
                "question": "Select the best noun for Blank [2]: 'The successful deployment of the zero-trust protocol last week stands as a ___[2]___ to her technical brilliance...'",
                "options": {"A": "testament", "B": "discrepancy", "C": "fluctuation", "D": "takeout"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #78：stand as a testament to + N（作為……的最佳明證／鐵證）",
                "analysis": "【前後文脈絡定位】零信任協定的成功部署，正是她卓越技術能力的「最佳證明（a testament to her technical brilliance）」。【正解確認】(A) testament 固定搭配介系詞 to。",
                "translation": "上週零信任協定的成功部署，正是她卓越技術才華的最佳明證。"
            },
            {
                "blank_num": 3,
                "question": "Select the best noun for Blank [3]: '...stands as a testament to her technical brilliance and unwavering ___[3]___ in the face of complex hardware constraints.'",
                "options": {"A": "perseverance", "B": "abstention", "C": "collision", "D": "brochure"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #79：unwavering perseverance（堅定不移的毅力／百折不撓的精神）",
                "analysis": "【前後文脈絡定位】面對複雜的硬體限制（in the face of complex hardware constraints），仍展現堅定不移的「毅力與百折不撓精神（perseverance）」。【正解確認】(A) perseverance 指「堅毅、堅持不懈」。",
                "translation": "上週零信任協定的成功部署，正是她卓越技術才華以及面對複雜硬體限制時百折不撓之毅力的最佳明證。"
            },
            {
                "blank_num": 4,
                "question": "Select the best adverb for Blank [4]: 'Her resourceful leadership has saved the corporation an estimated $4.2 million, ___[4]___ positioning our cybersecurity division as an industry benchmark.'",
                "options": {"A": "thereby", "B": "nonetheless", "C": "whereas", "D": "as far as"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #20 & 一山不容二虎：逗號 + thereby + V-ing（藉此／從而達成……結果）",
                "analysis": "【前後文脈絡定位】逗號後緊接現在分詞 positioning...，表示前句「省下 420 萬美元」進而帶來的正面結果。【正解確認】(A) thereby + V-ing（藉此使資安部門成為業界標竿）為多益 860+ 必考句型。",
                "translation": "她足智多謀的領導已為公司省下約四百二十萬美元，藉此使我們的網路安全部門成為業界標竿。"
            },
        ],
    },
    {
        "title": "CUSTOMER SERVICE POLICY: Courier Shipments & Price Quote Validity",
        "text_type": "Wholesale Terms & Conditions (Part 6 段落填空)",
        "content": (
            "All wholesale orders exceeding $2,500 are dispatched via express ___[1]___ at no additional charge to commercial accounts within the continental United States. "
            "Should a client request overnight air freight or weekend delivery, the ___[2]___ surcharges will be itemized on the final pro forma invoice.\n\n"
            "Please note that any written price ___[3]___ issued by our sales department remains valid for thirty calendar days, ___[4]___ raw material costs do not fluctuate by more than five percent during that interval."
        ),
        "questions": [
            {
                "blank_num": 1,
                "question": "Select the best noun for Blank [1]: 'All wholesale orders exceeding $2,500 are dispatched via express ___[1]___ at no additional charge...'",
                "options": {"A": "courier", "B": "pedestrian", "C": "garment", "D": "venue"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #49：via express courier（透過快遞專遞寄送）",
                "analysis": "【前後文脈絡定位】批發訂單透過「特快專遞／快遞公司（express courier）」寄出。【正解確認】(A) courier 指快遞服務或快遞員。",
                "translation": "所有超過 2,500 美元的批發訂單，針對美國本土境內的商業帳戶皆免費透過快遞專遞寄出。"
            },
            {
                "blank_num": 2,
                "question": "Select the best adjective for Blank [2]: 'Should a client request overnight air freight or weekend delivery, the ___[2]___ surcharges will be itemized...'",
                "options": {"A": "applicable", "B": "inclement", "C": "saturated", "D": "autonomous"},
                "answer": "A",
                "rule_ref": "多益高頻商務搭配：applicable surcharges / fees（相關適用的附加費）",
                "analysis": "【前後文脈絡定位】萬一客戶要求隔夜空運或週末配送，「相關適用的（applicable）」附加費用將會逐項列於形式發票上。【正解確認】(A) applicable 指「適用的、相關的」。",
                "translation": "萬一客戶要求隔夜空運或週末配送服務，相關適用的附加費用將逐項列載於最終形式發票上。"
            },
            {
                "blank_num": 3,
                "question": "Select the best noun for Blank [3]: 'Please note that any written price ___[3]___ issued by our sales department remains valid for thirty calendar days...'",
                "options": {"A": "quote", "B": "collision", "C": "rehearsal", "D": "complex"},
                "answer": "A",
                "rule_ref": "860 弱點庫 #75：written price quote（書面報價單，等同於 quotation）",
                "analysis": "【前後文脈絡定位】業務部門開立的任何「書面報價單（written price quote）」有效期限為三十個日曆天。【正解確認】(A) quote 作可數名詞指「報價、估價單」。",
                "translation": "請注意，由本業務部門開立之任何書面報價單，其有效期限皆為三十個日曆天。"
            },
            {
                "blank_num": 4,
                "question": "Select the best conjunction for Blank [4]: '...remains valid for thirty calendar days, ___[4]___ raw material costs do not fluctuate by more than five percent...'",
                "options": {"A": "provided that", "B": "as far as", "C": "in order to", "D": "despite"},
                "answer": "A",
                "rule_ref": "條件句辨析 Rule 2 & 單字 #40：provided that（只要……）+ fluctuate（波動）",
                "analysis": "【前後文脈絡定位】逗號後為完整條件子句 raw material costs do not fluctuate...（只要原物料成本波動不超過 5%），報價單即維持三十天有效。【正解確認】(A) provided that 引導條件子句。",
                "translation": "只要在該期間內原物料成本波動幅度不超過百分之五，業務部開立的書面報價單皆維持三十個日曆天有效。"
            },
        ],
    },
])


# Ensure all new distractors are in EXTRA_860_LEXICON
EXTRA_860_LEXICON.update({
    "complexity": ("不可數 / 可數名詞 (n.)", "複雜性；錯綜複雜的事物", "抽象名詞，指複雜程度，非建築園區"),
    "complexly": ("副詞 (adv.)", "複雜地", "修飾動詞或形容詞"),
    "scatters": ("第三人稱單數動詞 (v.)", "使散落；驅散", "主動語態真動詞"),
    "scattering": ("現在分詞 / 動名詞 (V-ing)", "散播；分散（主動動作）", "後須接名詞受詞"),
    "to scatter": ("不定詞 (to V)", "去散播；分散", "表目的或未來動作"),
    "abstain from": ("動詞片語 (phr.)", "戒絕；於投票中棄權（abstain from voting）", "不可用於沿著步道散步"),
    "confine to": ("動詞片語 (phr.)", "將……限制在……範圍內", "中間須先接受詞（confine A to B）"),
    "dispense with": ("動詞片語 (phr.)", "省卻；免除；不再需要", "指免除不必要之程序"),
    "rehearsing": ("動名詞 / 現在分詞 (V-ing)", "排練；彩排", "指演講或演出排練，不可修飾柏油道路工程"),
    "resenting": ("動名詞 / 現在分詞 (V-ing)", "對……感到憤慨；怨恨", "心理情緒動詞"),
    "unveiling": ("動名詞 / 現在分詞 (V-ing)", "揭幕；首次發表", "指新產品發表"),
    "tasked": ("過去分詞 (V-ed)", "被指派任務的（be tasked with + N/V-ing）", "多益必考被動片語"),
    "resented": ("過去式 / 過去分詞 (v./V-ed)", "對……感到憤慨；不滿", "不搭配 with coordinating"),
    "altercate": ("不及物動詞 (v.)", "爭吵；口角", "指激烈爭執"),
    "allusion": ("可數名詞 (n.)", "暗指；典故；間接提及（allusion to）", "勿與 alteration（改建）或 illusion（錯覺）混淆"),
    "resourcefulness": ("不可數名詞 (n.)", "足智多謀；隨機應變的能力", "衍生自形容詞 resourceful（足智多謀的）"),
    "discrepancy": ("可數名詞 (n.)", "差異；出入；不一致（discrepancy between A and B）", "多益財會稽核最高頻字彙，勿與 discretion 混淆"),
    "discretion": ("不可數名詞 (n.)", "自行決定權；自由裁量權；謹慎（at one's discretion）", "指由某人全權斟酌決定，非數據差異"),
    "applicable": ("形容詞 (adj.)", "適用的；相關的；合適的", "常用於 applicable fees / taxes / laws（相關適用費用或法規）"),
    "in order to": ("不定詞片語 (phr.)", "為了……（後接原形動詞 V，不可接完整 S+V 子句）", "注意與 in order that + S+V 子句區分"),
    "despite": ("介系詞 (prep.)", "儘管（後接名詞或 V-ing，不可接完整 S+V 子句）", "等同於 in spite of"),
    "although": ("從屬連接詞 (conj.)", "雖然；儘管（後須接完整 S+V 子句，不可接 O + V-ing 附帶狀況結構）", "連接讓步子句"),
    "as if": ("從屬連接詞 (conj.)", "彷彿；好像（後須接完整 S+V 子句）", "非附帶狀況介系詞"),
    "consequently": ("連接副詞 (adv.)", "因此；結果（置於獨立子句句首並加逗號，表示因果關係）", "等同於 therefore / as a result"),
    "in the event of": ("複合介系詞 (prep.)", "萬一發生……（後接純名詞片語，如 in the event of inclement weather）", "注意勿與連接詞 in the event that 混淆"),
    "in the event that": ("從屬連接詞 (conj.)", "萬一……；倘若……（後須接完整 S+V 子句）", "不可直接接純名詞片語"),
    "provided that": ("從屬連接詞 (conj.)", "只要……；以……為條件（後接完整條件子句，等同於 providing that / as long as）", "多益條件句最高頻連接詞"),
    "regardless of": ("複合介系詞 (prep.)", "無論；不管（後接名詞或 V-ing，不可接完整 S+V 子句）", "介系詞片語"),
    "since": ("從屬連接詞 / 介系詞 (conj./prep.)", "既然；因為 ／ 自從……以來", "連接完整原因子句或時間點，不用於附帶狀況 O + V-ing"),
    "whereas": ("從屬連接詞 (conj.)", "然而；鑑於；反之（後接完整 S+V 對比子句，不可單獨加逗號作連接副詞）", "連接前後對比之兩個子句"),
    "with": ("介系詞 (prep.)", "伴隨；隨著（構成附帶狀況結構 With + 受詞 + V-ing / p.p.）", "一山不容二虎 Rule 2 必考介系詞"),
    "acquisition": ("可數 / 不可數名詞 (n.)", "企業併購；收購案；獲得物（corporate acquisition）", "商務併購最高頻核心字"),
    "because": ("從屬連接詞 (conj.)", "因為（後接完整原因子句，不可夾在分號與逗號之間作轉折副詞）", "從屬連接詞"),
    "brochure": ("可數名詞 (n.)", "宣傳小冊子；培訓指引手冊（同義於 pamphlet / booklet）", "多益閱讀與填空高頻替換詞"),
    "discreetly": ("副詞 (adv.)", "謹慎地；低調保密地（衍生自 discreet）", "副詞不可修飾名詞 stages，且語意為保密地而非分開地"),
    "for": ("介系詞 (prep.)", "為了；長達（時間）；給", "不與 critical 搭配表批評"),
    "from": ("介系詞 (prep.)", "來自；從；免於（prevent / abstain from）", "不與 critical 或 advise（表切勿）搭配"),
    "however": ("連接副詞 / 複合關係副詞 (adv.)", "然而；不過（接逗號） ／ 無論多麼（however + adj./adv. + S + V）", "雙重用法必考詞"),
    "in spite of": ("複合介系詞 (prep.)", "儘管（後接名詞或 V-ing，不可接完整 S+V 子句）", "等同於 despite"),
    "of": ("介系詞 (prep.)", "……的；關於（固定搭配 be critical of / inclusive of / notify A of B）", "微觀訊號第 1 條必考介系詞"),
    "submit": ("及物動詞 (v.)", "提交；呈報（原形動詞）", "不可直接置於形容詞與單數名詞修飾語之後作複數主詞"),
    "submitted": ("過去式 / 過去分詞 (v./V-ed)", "已提交的；被呈報的", "過去分詞不可作句中核心複數名詞主詞"),
    "unanimous": ("形容詞 (adj.)", "全體一致同意的；無異議的（a unanimous vote / decision）", "董事會表決必考形容詞"),
})


def build_4option_details(q: dict, target_ans_letter: str = None) -> dict:
    """
    Deterministically rotate options so the correct answer is at `target_ans_letter` (if provided)
    and generate comprehensive Traditional Chinese `option_details` for (A)(B)(C)(D).
    """
    opts = dict(q.get("options", {}))
    orig_ans = q.get("answer", "A")
    if target_ans_letter and target_ans_letter in ("A", "B", "C", "D") and target_ans_letter != orig_ans:
        opts[orig_ans], opts[target_ans_letter] = opts[target_ans_letter], opts[orig_ans]
        q["options"] = opts
        q["answer"] = target_ans_letter

    ans = q.get("answer", "A")
    correct_word = opts.get(ans, "").strip()
    c_pos, c_zh, c_note = EXTRA_860_LEXICON.get(
        correct_word,
        EXTRA_860_LEXICON.get(correct_word.lower(), ("核心考點詞彙", "符合本題句構與商務語意之最佳解", "契合前後文語法槽位與搭配詞要求"))
    )

    details = {}
    for letter in ("A", "B", "C", "D"):
        w = opts.get(letter, "").strip()
        pos, zh, note = EXTRA_860_LEXICON.get(
            w,
            EXTRA_860_LEXICON.get(w.lower(), ("干擾選項", "詞性或語意不符本題上下文脈絡", "需注意句構槽位與固定搭配限制"))
        )
        if letter == ans:
            details[letter] = (
                f"【✓ 正確選項】詞性：{pos}｜字義：「{zh}」。"
                f"正確原因：{note}；完全契合本題「{q.get('rule_ref', '核心語法與搭配')}」之要求。"
            )
        else:
            details[letter] = (
                f"【✗ 錯誤干擾】詞性：{pos}｜字義：「{zh}」。"
                f"錯誤原因：{note}，代入本題空格後與正解「{correct_word}（{zh if letter == ans else c_zh}）」之語法功能或上下文語意衝突，故排除。"
            )
    q["option_details"] = details
    return q


# Pre-enrich all QUESTIONS_860_BANK and CLOZE_PASSAGES_BANK with balanced A/B/C/D keys and 4-option breakdowns
_LETTERS = ("A", "B", "C", "D")
for _idx, _q in enumerate(QUESTIONS_860_BANK):
    build_4option_details(_q, _LETTERS[_idx % 4])

for _p_idx, _pas in enumerate(CLOZE_PASSAGES_BANK):
    for _q_idx, _cq in enumerate(_pas["questions"]):
        build_4option_details(_cq, _LETTERS[(_p_idx * 4 + _q_idx) % 4])
