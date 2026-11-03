# -*- coding: utf-8 -*-
"""
Expands Day 1 in master_curriculum.py:
- Morning: 10 Part 5 questions with individual explanations
- Afternoon: 4 Recall + 3 Traps + 3 Part 7 questions = 10 questions total
"""

import master_curriculum

day1 = master_curriculum.DAYS_DATA[1]

# 1. Expand Morning Part 5 to 10 questions
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
        "analysis": "空格後為 'the unexpected budget cuts'（純名詞片語），後面接逗號，完全沒有動詞，因此必須填入介系詞。(A) Although 與 (C) Even if 後方須接 S+V 子句；(D) Nevertheless 是轉折副詞，不可直接接名詞。",
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
        "analysis": "固定被動語態搭配：be exempted from + 名詞（被免除……職責/賦稅）。故選 (C) exempted。",
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
        "analysis": "空格後方出現介系詞 'with'，秒選 compatible with（與……相容）。compliant 搭配 with 表合規，但形容軟體系統相容性用 compatible；competitive 具競爭力的。",
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
        "analysis": "商務高頻片語：under the direction of + 人物（在某人的指導/領導之下）。形容詞 direct 後需接名詞 direction。director 指主任（人），不合語意。",
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
    }
]

# 2. Expand Afternoon to 10 questions total (4 Recall + 3 Traps + 3 Part 7)
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
        "trap_point": "名詞詞性與意義判斷：a minor + [名詞]。overseer 是監工（人），oversight 才是疏失（事物）。",
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
        "trap_point": "看空格後有沒有動詞！後方有 'worked'，不能選介系詞 (A), (C), (D)！",
        "analysis": "空格後為 'Mr. Henderson worked through the night'（主詞 + 動詞 worked），句意表轉折讓步，秒選從屬連接詞 (B) Although！"
    }
]

day1["afternoon"]["part7"]["questions"] = [
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
    },
    {
        "question": "Which item can be reimbursed under the corporate wellness program?",
        "options": {
            "A": "Standard home office stationery supplies.",
            "B": "Ergonomically certified home office furniture.",
            "C": "Public transport commuting passes.",
            "D": "Uncertified personal workout equipment."
        },
        "answer": "B",
        "radar": "🔍 防漏看雷達：內文具體名詞替換！'ergonomically approved home-office furniture' ＝ 'Ergonomically certified home office furniture'！",
        "analysis": "第一段第二句寫道：'This fund can be applied toward gym memberships or ergonomically approved home-office furniture'，故選 (B)。"
    }
]

# Write back to master_curriculum.py
with open("master_curriculum.py", "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""\nMaster 25-Day TOEIC Golden Certificate (860+) Curriculum\n"""\n\n')
    f.write("DAYS_DATA = " + repr(master_curriculum.DAYS_DATA) + "\n")

print("Day 1 updated with 10 Morning P5 questions and 10 Afternoon questions!")
