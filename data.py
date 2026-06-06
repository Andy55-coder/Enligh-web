import firebase_admin
from firebase_admin import credentials, firestore
import os

# 1. 讀取金鑰連線
base_dir = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(base_dir, "serviceAccountKey.json")
cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. 準備「百大」多益必考單字庫 (與原版相同，保留結構)
vocabulary_data = [
    # --- 核心商業與管理 ---
    {"word": "implement", "part": "v.", "meaning": "實施、執行", "example": "The company will implement a new policy next month."},
    {"word": "evaluate", "part": "v.", "meaning": "評估", "example": "We need to evaluate the results of the marketing campaign."},
    {"word": "negotiate", "part": "v.", "meaning": "談判、協商", "example": "They are trying to negotiate a new contract with the supplier."},
    {"word": "collaborate", "part": "v.", "meaning": "合作", "example": "The two departments will collaborate on the new project."},
    {"word": "allocate", "part": "v.", "meaning": "撥出、分配", "example": "The manager allocated tasks to each team member."},
    {"word": "facilitate", "part": "v.", "meaning": "促進、使便利", "example": "The new software will facilitate the workflow."},
    {"word": "authorize", "part": "v.", "meaning": "授權、批准", "example": "Only the manager is authorized to sign this document."},
    {"word": "coordinate", "part": "v.", "meaning": "協調", "example": "She will coordinate the schedule for the upcoming conference."},
    {"word": "delegate", "part": "v.", "meaning": "委派(工作)", "example": "A good manager knows how to delegate tasks effectively."},
    {"word": "scrutinize", "part": "v.", "meaning": "詳細審查", "example": "The auditor will scrutinize the financial records."},
    # --- 財務與業績 ---
    {"word": "revenue", "part": "n.", "meaning": "營收、收益", "example": "The company's revenue increased by 20% this quarter."},
    {"word": "fluctuate", "part": "v.", "meaning": "波動、變動", "example": "Stock prices tend to fluctuate depending on the market."},
    {"word": "lucrative", "part": "adj.", "meaning": "有利可圖的、賺錢的", "example": "She has a very lucrative consulting business."},
    {"word": "deficit", "part": "n.", "meaning": "赤字、虧損", "example": "The government is facing a huge budget deficit."},
    {"word": "reimburse", "part": "v.", "meaning": "核銷、退還款項", "example": "The company will reimburse your travel expenses."},
    {"word": "deduct", "part": "v.", "meaning": "扣除", "example": "Taxes will be automatically deducted from your salary."},
    {"word": "yield", "part": "v.", "meaning": "產生(收益)、出產", "example": "The investment is expected to yield a high return."},
    {"word": "overhead", "part": "n.", "meaning": "經常性開支、營運成本", "example": "We need to reduce our overhead costs to increase profit."},
    {"word": "audit", "part": "n.", "meaning": "審計、查帳", "example": "The annual tax audit will begin next week."},
    {"word": "appraisal", "part": "n.", "meaning": "估價、評價", "example": "The bank requires an appraisal of the property."},
    # --- 辦公與會議 ---
    {"word": "mandatory", "part": "adj.", "meaning": "強制的、義務的", "example": "Attendance at the safety meeting is mandatory."},
    {"word": "tentative", "part": "adj.", "meaning": "暫定的", "example": "We have made a tentative agreement, pending final approval."},
    {"word": "consensus", "part": "n.", "meaning": "共識", "example": "The committee finally reached a consensus on the issue."},
    {"word": "preliminary", "part": "adj.", "meaning": "初步的、預備的", "example": "The preliminary results of the survey are very positive."},
    {"word": "unanimous", "part": "adj.", "meaning": "全體一致的", "example": "The board made a unanimous decision to promote him."},
    {"word": "postpone", "part": "v.", "meaning": "延期", "example": "The meeting has been postponed until next Friday."},
    {"word": "agenda", "part": "n.", "meaning": "議程", "example": "What is the first item on today's agenda?"},
    {"word": "minutes", "part": "n.", "meaning": "會議記錄", "example": "Please send the meeting minutes to all attendees."},
    {"word": "adjourn", "part": "v.", "meaning": "休會、暫停", "example": "The meeting was adjourned at 5:00 PM."},
    {"word": "briefing", "part": "n.", "meaning": "簡報", "example": "We will have a short briefing before the client arrives."},
    # --- 契約與法規 ---
    {"word": "compliance", "part": "n.", "meaning": "遵守、合規", "example": "The company acts in compliance with environmental laws."},
    {"word": "obligation", "part": "n.", "meaning": "義務、責任", "example": "Employers have an obligation to protect their employees."},
    {"word": "valid", "part": "adj.", "meaning": "有效的、合法的", "example": "This coupon is valid for one month."},
    {"word": "terminate", "part": "v.", "meaning": "終止、結束", "example": "The contract was terminated due to a breach of terms."},
    {"word": "exempt", "part": "adj.", "meaning": "免除的、豁免的", "example": "Non-profit organizations are exempt from paying certain taxes."},
    {"word": "breach", "part": "n.", "meaning": "違反、違約", "example": "They sued the supplier for a breach of contract."},
    {"word": "stipulate", "part": "v.", "meaning": "規定、約定", "example": "The lease stipulates that pets are not allowed."},
    {"word": "liable", "part": "adj.", "meaning": "負有法律責任的", "example": "The airline is not liable for lost baggage."},
    {"word": "nullify", "part": "v.", "meaning": "使無效、取消", "example": "The judge nullified the contract."},
    {"word": "amend", "part": "v.", "meaning": "修改、修訂", "example": "We need to amend the policy to reflect the new laws."},
    # --- 招募與人事 ---
    {"word": "eligible", "part": "adj.", "meaning": "有資格的", "example": "Only full-time employees are eligible for the bonus."},
    {"word": "compensate", "part": "v.", "meaning": "補償、賠償", "example": "The company will compensate workers for overtime."},
    {"word": "prospective", "part": "adj.", "meaning": "預期的、未來的", "example": "We are interviewing three prospective candidates today."},
    {"word": "prerequisite", "part": "n.", "meaning": "先決條件", "example": "A bachelor's degree is a prerequisite for this position."},
    {"word": "incentive", "part": "n.", "meaning": "激勵、獎金", "example": "The sales team was offered a cash incentive for hitting the target."},
    {"word": "probation", "part": "n.", "meaning": "試用期", "example": "New employees are subject to a three-month probation period."},
    {"word": "apprentice", "part": "n.", "meaning": "學徒、見習生", "example": "He started his career as an electrician's apprentice."},
    {"word": "credential", "part": "n.", "meaning": "資歷、證書", "example": "Please submit your academic credentials with your application."},
    {"word": "versatile", "part": "adj.", "meaning": "多才多藝的、多功能的", "example": "We are looking for a versatile employee who can handle multiple tasks."},
    {"word": "layoff", "part": "n.", "meaning": "裁員", "example": "The company announced massive layoffs due to the recession."},
    # --- 採購與供應鏈 ---
    {"word": "inventory", "part": "n.", "meaning": "庫存、存貨", "example": "We need to conduct a full inventory check this weekend."},
    {"word": "surplus", "part": "n.", "meaning": "剩餘、過剩", "example": "We will sell the surplus equipment at a discount."},
    {"word": "shortage", "part": "n.", "meaning": "短缺", "example": "There is a global shortage of computer chips."},
    {"word": "vendor", "part": "n.", "meaning": "供應商、小販", "example": "We are currently evaluating several software vendors."},
    {"word": "procurement", "part": "n.", "meaning": "採購", "example": "She is the director of the procurement department."},
    {"word": "freight", "part": "n.", "meaning": "貨物、運費", "example": "The freight train is carrying tons of coal."},
    {"word": "fragile", "part": "adj.", "meaning": "易碎的", "example": "Please handle these fragile items with care."},
    {"word": "invoice", "part": "n.", "meaning": "發票、請款單", "example": "The invoice must be paid within 30 days."},
    {"word": "rebate", "part": "n.", "meaning": "折扣、退款", "example": "Customers can get a $50 rebate on this printer."},
    {"word": "warranty", "part": "n.", "meaning": "保固", "example": "This laptop comes with a two-year warranty."},
    # --- 日常營運與品質 ---
    {"word": "accommodate", "part": "v.", "meaning": "容納、提供住宿", "example": "The hotel can accommodate up to 500 guests."},
    {"word": "alternative", "part": "n.", "meaning": "替代方案", "example": "We need to find an alternative to this problem."},
    {"word": "comprehensive", "part": "adj.", "meaning": "全面的、廣泛的", "example": "The report provides a comprehensive overview of the market."},
    {"word": "equivalent", "part": "adj.", "meaning": "相等的、等值的", "example": "His silence is equivalent to an admission of guilt."},
    {"word": "consecutive", "part": "adj.", "meaning": "連續的", "example": "It has rained for five consecutive days."},
    {"word": "unprecedented", "part": "adj.", "meaning": "史無前例的", "example": "The event was an unprecedented success."},
    {"word": "specify", "part": "v.", "meaning": "具體指出、詳細說明", "example": "Please specify the time and place of the meeting."},
    {"word": "verify", "part": "v.", "meaning": "證明、核實", "example": "Please verify your email address to activate your account."},
    {"word": "compile", "part": "v.", "meaning": "收集、編纂", "example": "She was asked to compile a list of potential clients."},
    {"word": "feasible", "part": "adj.", "meaning": "可行的", "example": "It's not feasible to complete the project by tomorrow."},
    # --- 溝通與客服 ---
    {"word": "inquiry", "part": "n.", "meaning": "詢問、打聽", "example": "We received numerous inquiries about the new product."},
    {"word": "prompt", "part": "adj.", "meaning": "迅速的、即時的", "example": "Thank you for your prompt reply."},
    {"word": "courteous", "part": "adj.", "meaning": "有禮貌的", "example": "Customer service representatives must always be courteous."},
    {"word": "resolve", "part": "v.", "meaning": "解決", "example": "The technician resolved the network issue quickly."},
    {"word": "apologize", "part": "v.", "meaning": "道歉", "example": "We sincerely apologize for the inconvenience."},
    {"word": "assure", "part": "v.", "meaning": "向...保證", "example": "I assure you that the mistake will not happen again."},
    {"word": "clarify", "part": "v.", "meaning": "澄清、說明", "example": "Could you clarify what you mean by 'extra fees'?"},
    {"word": "feedback", "part": "n.", "meaning": "回饋意見", "example": "We welcome customer feedback to improve our services."},
    {"word": "notify", "part": "v.", "meaning": "通知", "example": "You will be notified via email when your package ships."},
    {"word": "pertain", "part": "v.", "meaning": "關於、有關", "example": "This rule does not pertain to part-time workers."},
    # --- 行銷與企劃 ---
    {"word": "campaign", "part": "n.", "meaning": "宣傳活動", "example": "The advertising campaign was highly successful."},
    {"word": "sponsor", "part": "n.", "meaning": "贊助商", "example": "We are looking for sponsors for the annual charity run."},
    {"word": "endorse", "part": "v.", "meaning": "代言、背書", "example": "The famous athlete endorsed the new sports drink."},
    {"word": "innovative", "part": "adj.", "meaning": "創新的", "example": "The company is known for its innovative designs."},
    {"word": "niche", "part": "n.", "meaning": "利基市場、小眾市場", "example": "They found a profitable niche in organic cosmetics."},
    {"word": "penetrate", "part": "v.", "meaning": "打入、滲透(市場)", "example": "It is difficult to penetrate the European market."},
    {"word": "prominent", "part": "adj.", "meaning": "著名的、顯著的", "example": "The logo should be placed in a prominent position."},
    {"word": "rival", "part": "n.", "meaning": "競爭對手", "example": "Our main rival has just released a similar product."},
    {"word": "survey", "part": "n.", "meaning": "調查", "example": "According to a recent survey, 80% of customers are satisfied."},
    {"word": "target", "part": "v.", "meaning": "以...為目標", "example": "The ad is targeted at teenagers."},
    # --- 旅遊與交通 ---
    {"word": "itinerary", "part": "n.", "meaning": "行程表", "example": "I will send you a copy of the travel itinerary."},
    {"word": "commute", "part": "v.", "meaning": "通勤", "example": "She commutes to Taipei by high-speed rail every day."},
    {"word": "delay", "part": "v.", "meaning": "延遲", "example": "The flight was delayed due to heavy fog."},
    {"word": "destination", "part": "n.", "meaning": "目的地", "example": "We reached our destination after a ten-hour drive."},
    {"word": "fare", "part": "n.", "meaning": "票價", "example": "Train fares are expected to increase next year."},
    {"word": "baggage", "part": "n.", "meaning": "行李", "example": "Please do not leave your baggage unattended."},
    {"word": "customs", "part": "n.", "meaning": "海關", "example": "It took us an hour to get through customs."},
    {"word": "layover", "part": "n.", "meaning": "轉機等待時間", "example": "We have a three-hour layover in Tokyo."},
    {"word": "shuttle", "part": "n.", "meaning": "接駁車", "example": "There is a free shuttle bus from the hotel to the airport."},
    {"word": "transit", "part": "n.", "meaning": "運輸、過境", "example": "The goods were damaged in transit."}
]

# 3. 文法資料 (10 章，每章 20 題)
lessons_data = [
    {
        "order": 1,
        "title": "第一章：詞類（Parts of Speech）",
        "grammar": "英文包含八大詞類：<br><b>名詞 Noun</b>: student, Taiwan<br><b>代名詞 Pronoun</b>: I/me, He/him<br><b>動詞 Verb</b>: 表示動作或狀態<br><b>形容詞 Adjective</b>: 修飾名詞<br><b>副詞 Adverb</b>: 修飾動詞或形容詞<br><b>介系詞 Preposition</b>: in, on, at<br><b>連接詞 Conjunction</b>: and, but, because<br><b>感嘆詞 Interjection</b>: Wow!, Oh!",
        "questions": [
            {"q": "請問單字 'beautiful' 在句中通常屬於哪一種詞類？", "options": ["A) 名詞 Noun", "B) 動詞 Verb", "C) 形容詞 Adjective", "D) 副詞 Adverb"], "ans": "C"},
            {"q": "The manager speaks 'quickly'. 句中的 quickly 是什麼詞？", "options": ["A) 名詞 Noun", "B) 動詞 Verb", "C) 形容詞 Adjective", "D) 副詞 Adverb"], "ans": "D"},
            {"q": "單字 'happiness' 屬於哪一種詞類？", "options": ["A) 名詞 Noun", "B) 動詞 Verb", "C) 形容詞 Adjective", "D) 介系詞 Preposition"], "ans": "A"},
            {"q": "We put the box 'under' the table. 句中的 under 是什麼詞？", "options": ["A) 介系詞 Preposition", "B) 動詞 Verb", "C) 副詞 Adverb", "D) 連接詞 Conjunction"], "ans": "A"},
            {"q": "I stayed at home 'because' it rained. 句中的 because 是什麼詞？", "options": ["A) 副詞 Adverb", "B) 介系詞 Preposition", "C) 連接詞 Conjunction", "D) 代名詞 Pronoun"], "ans": "C"},
            {"q": "'He' is my best friend. 句中的 He 是什麼詞？", "options": ["A) 介系詞 Preposition", "B) 連接詞 Conjunction", "C) 動詞 Verb", "D) 代名詞 Pronoun"], "ans": "D"},
            {"q": "'Wow!' That is amazing! 句中的 Wow 是什麼詞？", "options": ["A) 感嘆詞 Interjection", "B) 名詞 Noun", "C) 動詞 Verb", "D) 形容詞 Adjective"], "ans": "A"},
            {"q": "I usually 'run' in the park. 句中的 run 是什麼詞？", "options": ["A) 動詞 Verb", "B) 名詞 Noun", "C) 形容詞 Adjective", "D) 介系詞 Preposition"], "ans": "A"},
            {"q": "'The' apple is red. 句中的 The 屬於廣義的哪種詞類？", "options": ["A) 動詞 Verb", "B) 形容詞 Adjective (冠詞)", "C) 介系詞 Preposition", "D) 連接詞 Conjunction"], "ans": "B"},
            {"q": "She is 'always' late for work. 句中的 always 是什麼詞？", "options": ["A) 副詞 Adverb", "B) 動詞 Verb", "C) 名詞 Noun", "D) 形容詞 Adjective"], "ans": "A"},
            {"q": "They need more 'information'. 句中的 information 是什麼詞？", "options": ["A) 名詞 Noun", "B) 副詞 Adverb", "C) 介系詞 Preposition", "D) 動詞 Verb"], "ans": "A"},
            {"q": "He is a 'creative' designer. 句中的 creative 是什麼詞？", "options": ["A) 名詞 Noun", "B) 形容詞 Adjective", "C) 副詞 Adverb", "D) 動詞 Verb"], "ans": "B"},
            {"q": "Please 'create' a new file. 句中的 create 是什麼詞？", "options": ["A) 動詞 Verb", "B) 名詞 Noun", "C) 形容詞 Adjective", "D) 副詞 Adverb"], "ans": "A"},
            {"q": "'Creativity' is important in marketing. 句中的 Creativity 是？", "options": ["A) 動詞 Verb", "B) 形容詞 Adjective", "C) 介系詞 Preposition", "D) 名詞 Noun"], "ans": "D"},
            {"q": "She thought 'creatively' to solve the problem. creatively 是？", "options": ["A) 名詞 Noun", "B) 形容詞 Adjective", "C) 副詞 Adverb", "D) 介系詞 Preposition"], "ans": "C"},
            {"q": "We went out 'although' it was raining. although 是什麼詞？", "options": ["A) 連接詞 Conjunction", "B) 介系詞 Preposition", "C) 副詞 Adverb", "D) 代名詞 Pronoun"], "ans": "A"},
            {"q": "He walked 'through' the door. through 是什麼詞？", "options": ["A) 連接詞 Conjunction", "B) 介系詞 Preposition", "C) 動詞 Verb", "D) 名詞 Noun"], "ans": "B"},
            {"q": "They did the work by 'themselves'. themselves 是什麼詞？", "options": ["A) 動詞 Verb", "B) 名詞 Noun", "C) 代名詞 Pronoun", "D) 形容詞 Adjective"], "ans": "C"},
            {"q": "'Ouch!' That hurts. Ouch 是什麼詞？", "options": ["A) 代名詞 Pronoun", "B) 感嘆詞 Interjection", "C) 動詞 Verb", "D) 連接詞 Conjunction"], "ans": "B"},
            {"q": "We must 'analyze' the data carefully. analyze 是什麼詞？", "options": ["A) 副詞 Adverb", "B) 形容詞 Adjective", "C) 動詞 Verb", "D) 名詞 Noun"], "ans": "C"}
        ]
    },
    {
        "order": 2,
        "title": "第二章：句子結構",
        "grammar": "英文有五大基本句型：<br>1. <b>S + V</b> (Birds fly.)<br>2. <b>S + V + O</b> (I eat apples.)<br>3. <b>S + V + C</b> (She is happy.)<br>4. <b>S + V + O + O</b> (My father gave me a gift.)<br>5. <b>S + V + O + C</b> (We call him Tom.)",
        "questions": [
            {"q": "在句子 'We call him Tom.' 中，單字 'Tom' 扮演什麼角色？", "options": ["A) S (主詞)", "B) V (動詞)", "C) O (受詞)", "D) C (受詞補語)"], "ans": "D"},
            {"q": "句子 'She sleeps.' 屬於哪種句型？", "options": ["A) S + V", "B) S + V + O", "C) S + V + C", "D) S + V + O + C"], "ans": "A"},
            {"q": "在句子 'He bought a car.' 中，'car' 扮演什麼角色？", "options": ["A) S (主詞)", "B) V (動詞)", "C) O (受詞)", "D) C (補語)"], "ans": "C"},
            {"q": "句子 'They made me happy.' 屬於哪種句型？", "options": ["A) S + V + O", "B) S + V + C", "C) S + V + O + O", "D) S + V + O + C"], "ans": "D"},
            {"q": "在 'I gave her a book.' 中，'her' 是什麼？", "options": ["A) 主詞 S", "B) 間接受詞 IO", "C) 直接受詞 DO", "D) 補語 C"], "ans": "B"},
            {"q": "在 'I gave her a book.' 中，'a book' 是什麼？", "options": ["A) 主詞 S", "B) 間接受詞 IO", "C) 直接受詞 DO", "D) 補語 C"], "ans": "C"},
            {"q": "句子 'The sky is blue.' 屬於哪種句型？", "options": ["A) S + V", "B) S + V + O", "C) S + V + C", "D) S + V + O + O"], "ans": "C"},
            {"q": "在 'Dogs bark.' 中，'bark' 扮演什麼角色？", "options": ["A) 主詞 S", "B) 動詞 V", "C) 受詞 O", "D) 補語 C"], "ans": "B"},
            {"q": "在 'She seems tired.' 中，'tired' 是什麼？", "options": ["A) 受詞 O", "B) 主詞補語 SC", "C) 動詞 V", "D) 間接受詞 IO"], "ans": "B"},
            {"q": "句子 'He painted the door green.' 屬於哪種句型？", "options": ["A) S + V + O", "B) S + V + C", "C) S + V + O + O", "D) S + V + O + C"], "ans": "D"},
            {"q": "在 'I consider him a genius.' 中，'a genius' 扮演什麼角色？", "options": ["A) 直接受詞 DO", "B) 間接受詞 IO", "C) 受詞補語 OC", "D) 主詞補語 SC"], "ans": "C"},
            {"q": "在 'My mother cooked dinner.' 中，'dinner' 是什麼？", "options": ["A) 受詞 O", "B) 補語 C", "C) 主詞 S", "D) 動詞 V"], "ans": "A"},
            {"q": "句子 'The baby is crying.' 屬於哪一種基本句型？", "options": ["A) S + V", "B) S + V + O", "C) S + V + C", "D) S + V + O + C"], "ans": "A"},
            {"q": "在 'We elected him president.' 中，'president' 是？", "options": ["A) 直接受詞 DO", "B) 受詞補語 OC", "C) 間接受詞 IO", "D) 主詞補語 SC"], "ans": "B"},
            {"q": "句子 'She handed me a letter.' 屬於哪種句型？", "options": ["A) S + V + O", "B) S + V + C", "C) S + V + O + O", "D) S + V + O + C"], "ans": "C"},
            {"q": "在 'The flowers smell sweet.' 中，'sweet' 扮演什麼角色？", "options": ["A) 受詞 O", "B) 副詞 Adv", "C) 主詞補語 SC", "D) 動詞 V"], "ans": "C"},
            {"q": "在 'John became a doctor.' 中，'a doctor' 是什麼？", "options": ["A) 主詞 S", "B) 受詞 O", "C) 主詞補語 SC", "D) 受詞補語 OC"], "ans": "C"},
            {"q": "句子 'They found the test difficult.' 中的 'difficult' 是什麼？", "options": ["A) 受詞補語 OC", "B) 直接受詞 DO", "C) 間接受詞 IO", "D) 主詞補語 SC"], "ans": "A"},
            {"q": "在 'I enjoy reading.' 中，'reading' 是什麼？", "options": ["A) 補語 C", "B) 動詞 V", "C) 受詞 O", "D) 介系詞 Prep"], "ans": "C"},
            {"q": "句子 'The sun rises.' 屬於什麼句型？", "options": ["A) S + V + O", "B) S + V", "C) S + V + C", "D) S + V + O + C"], "ans": "B"}
        ]
    },
    {
        "order": 3,
        "title": "第三章：英文十二時態",
        "grammar": "核心時態公式：<br><b>現在簡單式：</b> S + V(s/es)<br><b>現在進行式：</b> S + am/is/are + Ving<br><b>現在完成式：</b> S + have/has + p.p.<br><b>過去簡單式：</b> S + V2<br><b>過去進行式：</b> S + was/were + Ving<br><b>過去完成式：</b> S + had + p.p.<br><b>未來簡單式：</b> S + will + V",
        "questions": [
            {"q": "I _______ basketball yesterday.", "options": ["A) play", "B) played", "C) am playing", "D) have played"], "ans": "B"},
            {"q": "Please be quiet. The baby _______ now.", "options": ["A) sleeps", "B) slept", "C) is sleeping", "D) has slept"], "ans": "C"},
            {"q": "She _______ in Taipei since 2010.", "options": ["A) lived", "B) lives", "C) is living", "D) has lived"], "ans": "D"},
            {"q": "We _______ to Japan next month.", "options": ["A) go", "B) went", "C) have gone", "D) will go"], "ans": "D"},
            {"q": "When I arrived at the station, the train _______.", "options": ["A) left", "B) leaves", "C) had left", "D) is leaving"], "ans": "C"},
            {"q": "He usually _______ up at 7 AM.", "options": ["A) wake", "B) wakes", "C) woke", "D) is waking"], "ans": "B"},
            {"q": "While I _______ TV, the phone rang.", "options": ["A) watch", "B) watched", "C) was watching", "D) have watched"], "ans": "C"},
            {"q": "By the end of next year, I _______ my degree.", "options": ["A) will finish", "B) finish", "C) will have finished", "D) had finished"], "ans": "C"},
            {"q": "I _______ very busy lately.", "options": ["A) am", "B) was", "C) will be", "D) have been"], "ans": "D"},
            {"q": "They _______ a great movie two days ago.", "options": ["A) see", "B) saw", "C) have seen", "D) will see"], "ans": "B"},
            {"q": "Look! The bus _______.", "options": ["A) comes", "B) came", "C) is coming", "D) has come"], "ans": "C"},
            {"q": "It often _______ in Seattle.", "options": ["A) rain", "B) rains", "C) is raining", "D) rained"], "ans": "B"},
            {"q": "We _______ have a meeting tomorrow morning.", "options": ["A) are going to", "B) go to", "C) went to", "D) have gone to"], "ans": "A"},
            {"q": "He _______ English for three hours.", "options": ["A) studied", "B) studies", "C) has been studying", "D) is studying"], "ans": "C"},
            {"q": "Before she came, we _______ dinner.", "options": ["A) eat", "B) ate", "C) have eaten", "D) had already eaten"], "ans": "D"},
            {"q": "At 8 PM yesterday, we _______ dinner.", "options": ["A) had", "B) were having", "C) have had", "D) had had"], "ans": "B"},
            {"q": "She _______ her grandparents every weekend.", "options": ["A) visit", "B) visits", "C) visited", "D) has visited"], "ans": "B"},
            {"q": "His English _______ a lot recently.", "options": ["A) improves", "B) improved", "C) has improved", "D) will improve"], "ans": "C"},
            {"q": "In 2050, cars _______ flying.", "options": ["A) are", "B) were", "C) will be", "D) have been"], "ans": "C"},
            {"q": "I will call you as soon as he _______.", "options": ["A) arrive", "B) arrives", "C) arrived", "D) will arrive"], "ans": "B"}
        ]
    },
    {
        "order": 4,
        "title": "第四章：被動語態",
        "grammar": "被動語態公式：<b>Be + p.p. (過去分詞)</b><br><br><b>主動：</b>Tom wrote the letter.<br><b>被動：</b>The letter <b>was written</b> by Tom.",
        "questions": [
            {"q": "The window _______ by the boy yesterday.", "options": ["A) break", "B) broke", "C) is broken", "D) was broken"], "ans": "D"},
            {"q": "English _______ all over the world.", "options": ["A) speaks", "B) is speaking", "C) is spoken", "D) was spoken"], "ans": "C"},
            {"q": "The final report _______ tomorrow.", "options": ["A) will finish", "B) is finished", "C) will be finished", "D) finished"], "ans": "C"},
            {"q": "My car _______ right now.", "options": ["A) repairs", "B) is repaired", "C) is being repaired", "D) has repaired"], "ans": "C"},
            {"q": "The letter _______ already.", "options": ["A) sent", "B) was sending", "C) has been sent", "D) is sent"], "ans": "C"},
            {"q": "This house _______ in 1990.", "options": ["A) builds", "B) built", "C) is built", "D) was built"], "ans": "D"},
            {"q": "A new shopping mall _______ next year.", "options": ["A) will build", "B) builds", "C) is going to be built", "D) built"], "ans": "C"},
            {"q": "The cake _______ by the dog before I got home.", "options": ["A) had eaten", "B) was eating", "C) had been eaten", "D) ate"], "ans": "C"},
            {"q": "This problem must _______ immediately.", "options": ["A) solve", "B) be solved", "C) solving", "D) to solve"], "ans": "B"},
            {"q": "The thief _______ by the police last night.", "options": ["A) caught", "B) is caught", "C) was caught", "D) has caught"], "ans": "C"},
            {"q": "Harry Potter _______ by J.K. Rowling.", "options": ["A) wrote", "B) was written", "C) is writing", "D) has written"], "ans": "B"},
            {"q": "These shoes _______ of genuine leather.", "options": ["A) make", "B) made", "C) are making", "D) are made"], "ans": "D"},
            {"q": "The room _______ when I arrived.", "options": ["A) was cleaned", "B) was being cleaned", "C) is cleaned", "D) cleans"], "ans": "B"},
            {"q": "The lost keys _______ by someone.", "options": ["A) have been found", "B) have found", "C) found", "D) are finding"], "ans": "A"},
            {"q": "Tickets can _______ online.", "options": ["A) buy", "B) buying", "C) be bought", "D) bought"], "ans": "C"},
            {"q": "Mistakes _______ during the project.", "options": ["A) make", "B) made", "C) were made", "D) have made"], "ans": "C"},
            {"q": "The meeting _______ due to the storm.", "options": ["A) canceled", "B) has been canceled", "C) is canceling", "D) has canceled"], "ans": "B"},
            {"q": "She _______ a prize for her excellent work.", "options": ["A) gave", "B) was given", "C) gives", "D) has given"], "ans": "B"},
            {"q": "The facts _______ to everyone in the office.", "options": ["A) know", "B) knew", "C) are known", "D) are knowing"], "ans": "C"},
            {"q": "The project should _______ by Friday.", "options": ["A) complete", "B) completed", "C) be completed", "D) completing"], "ans": "C"}
        ]
    },
    {
        "order": 5,
        "title": "第五章：助動詞",
        "grammar": "常見助動詞：<br>can (能夠), could (過去能夠), may (可能), must (必須), should (應該), will (將會)。<br><br>💡 <b>重要規則：</b>助動詞後面的動詞必須是「原形動詞」。",
        "questions": [
            {"q": "You must _______ your homework before watching TV.", "options": ["A) finish", "B) finishes", "C) finishing", "D) finished"], "ans": "A"},
            {"q": "She can _______ four languages fluently.", "options": ["A) speaks", "B) spoke", "C) speaking", "D) speak"], "ans": "D"},
            {"q": "You should _______ to a doctor if you feel sick.", "options": ["A) go", "B) going", "C) gone", "D) goes"], "ans": "A"},
            {"q": "Take an umbrella. It may _______ later.", "options": ["A) rain", "B) rains", "C) raining", "D) rained"], "ans": "A"},
            {"q": "He might _______ late for the meeting.", "options": ["A) is", "B) be", "C) being", "D) been"], "ans": "B"},
            {"q": "I could _______ when I was five years old.", "options": ["A) swim", "B) swims", "C) swimming", "D) swam"], "ans": "A"},
            {"q": "I will _______ you with your project.", "options": ["A) helping", "B) helped", "C) help", "D) helps"], "ans": "C"},
            {"q": "I would _______ a cup of coffee, please.", "options": ["A) likes", "B) like", "C) liking", "D) liked"], "ans": "B"},
            {"q": "We have to _______ early tomorrow.", "options": ["A) leave", "B) leaves", "C) left", "D) leaving"], "ans": "A"},
            {"q": "You ought to _______ for your mistake.", "options": ["A) apologize", "B) apologizing", "C) apologized", "D) apologizes"], "ans": "A"},
            {"q": "You had better _______ there alone at night.", "options": ["A) not go", "B) don't go", "C) not going", "D) to not go"], "ans": "A"},
            {"q": "He dare not _______ the truth to his boss.", "options": ["A) tells", "B) told", "C) telling", "D) speak"], "ans": "D"},
            {"q": "He used to _______ a lot, but he quit last year.", "options": ["A) smoke", "B) smoking", "C) smoked", "D) smokes"], "ans": "A"},
            {"q": "You need not _______ about me.", "options": ["A) worries", "B) to worry", "C) worry", "D) worrying"], "ans": "C"},
            {"q": "I could have _______ it, but I decided not to.", "options": ["A) do", "B) did", "C) done", "D) doing"], "ans": "C"},
            {"q": "He must have _______ his keys at home.", "options": ["A) forget", "B) forgets", "C) forgot", "D) forgotten"], "ans": "D"},
            {"q": "You failed the test. You should have _______ harder.", "options": ["A) study", "B) studied", "C) studying", "D) studies"], "ans": "B"},
            {"q": "She may have _______ the train. Let's wait.", "options": ["A) miss", "B) misses", "C) missed", "D) missing"], "ans": "C"},
            {"q": "That cannot _______ true! I don't believe it.", "options": ["A) be", "B) is", "C) being", "D) was"], "ans": "A"},
            {"q": "_______ we dance?", "options": ["A) Shall", "B) May", "C) Ought", "D) Must"], "ans": "A"}
        ]
    },
    {
        "order": 6,
        "title": "第六章：假設語氣",
        "grammar": "1. <b>第一類條件句</b> (可能發生)：If it rains, I will stay home.<br>2. <b>第二類條件句</b> (與現在事實相反)：If I were rich, I would buy a Ferrari.<br>3. <b>第三類條件句</b> (與過去事實相反)：If I had studied harder, I would have passed.",
        "questions": [
            {"q": "If I _______ a bird, I would fly in the sky.", "options": ["A) am", "B) was", "C) were", "D) have been"], "ans": "C"},
            {"q": "If it rains tomorrow, I _______ at home.", "options": ["A) will stay", "B) stay", "C) would stay", "D) stayed"], "ans": "A"},
            {"q": "If I had known you were in hospital, I _______ you.", "options": ["A) would visit", "B) will visit", "C) visited", "D) would have visited"], "ans": "D"},
            {"q": "If she _______ hard, she will pass the exam.", "options": ["A) study", "B) studies", "C) studied", "D) had studied"], "ans": "B"},
            {"q": "If I _______ a million dollars, I would buy a big house.", "options": ["A) have", "B) has", "C) had", "D) had had"], "ans": "C"},
            {"q": "If you heat ice, it _______.", "options": ["A) melt", "B) melts", "C) melted", "D) will melt"], "ans": "B"},
            {"q": "If he had driven carefully, he _______ crashed.", "options": ["A) wouldn't", "B) wouldn't have", "C) didn't", "D) won't have"], "ans": "B"},
            {"q": "If I _______ you, I would apologize to her.", "options": ["A) am", "B) was", "C) were", "D) be"], "ans": "C"},
            {"q": "If we leave now, we _______ catch the bus.", "options": ["A) can", "B) could", "C) might have", "D) would"], "ans": "A"},
            {"q": "If they _______ me, I would have attended the party.", "options": ["A) invited", "B) invite", "C) had invited", "D) will invite"], "ans": "C"},
            {"q": "I would travel the world if I _______ the lottery.", "options": ["A) win", "B) won", "C) had won", "D) will win"], "ans": "B"},
            {"q": "If she calls, _______ her I'm busy.", "options": ["A) tell", "B) telling", "C) told", "D) tells"], "ans": "A"},
            {"q": "If I had seen him, I _______ hello.", "options": ["A) would say", "B) said", "C) would have said", "D) will say"], "ans": "C"},
            {"q": "If he _______ hurry, he will miss the train.", "options": ["A) isn't", "B) doesn't", "C) didn't", "D) won't"], "ans": "B"},
            {"q": "If it _______ tomorrow, we would make a snowman.", "options": ["A) snows", "B) snowed", "C) had snowed", "D) will snow"], "ans": "B"},
            {"q": "Had I known about the problem, I _______ helped.", "options": ["A) will have", "B) would have", "C) would", "D) had"], "ans": "B"},
            {"q": "If you mix red and blue, you _______ purple.", "options": ["A) got", "B) will get", "C) get", "D) would get"], "ans": "C"},
            {"q": "If she _______ my boss, I would quit my job.", "options": ["A) is", "B) was", "C) were", "D) had been"], "ans": "C"},
            {"q": "If they _______ more, they would have won the game.", "options": ["A) practiced", "B) had practiced", "C) practice", "D) practicing"], "ans": "B"},
            {"q": "Unless you _______, you will fail the test.", "options": ["A) study", "B) don't study", "C) studied", "D) will study"], "ans": "A"}
        ]
    },
    {
        "order": 7,
        "title": "第七章：關係代名詞",
        "grammar": "關係代名詞用途：<br><b>who</b> (代替人)<br><b>whom</b> (代替人/受格)<br><b>whose</b> (代替所有格)<br><b>which</b> (代替物)<br><b>that</b> (代替人或物)<br><br>例句：The man <b>who</b> helped me is my teacher.",
        "questions": [
            {"q": "This is the book _______ I bought yesterday.", "options": ["A) who", "B) which", "C) whom", "D) whose"], "ans": "B"},
            {"q": "The man _______ helped me is my uncle.", "options": ["A) which", "B) who", "C) whom", "D) whose"], "ans": "B"},
            {"q": "The girl _______ father is a doctor is my classmate.", "options": ["A) who", "B) whom", "C) whose", "D) which"], "ans": "C"},
            {"q": "The person _______ I met yesterday was very polite.", "options": ["A) who", "B) which", "C) whom", "D) whose"], "ans": "C"},
            {"q": "Where is the car _______ was parked here?", "options": ["A) who", "B) that", "C) whom", "D) whose"], "ans": "B"},
            {"q": "This is the house _______ I was born.", "options": ["A) which", "B) where", "C) when", "D) that"], "ans": "B"},
            {"q": "Tell me the reason _______ you left early.", "options": ["A) which", "B) why", "C) when", "D) where"], "ans": "B"},
            {"q": "I still remember the day _______ we first met.", "options": ["A) which", "B) where", "C) when", "D) who"], "ans": "C"},
            {"q": "Anyone _______ knows the answer, please raise your hand.", "options": ["A) which", "B) whom", "C) whose", "D) who"], "ans": "D"},
            {"q": "The dog _______ bit me belongs to my neighbor.", "options": ["A) who", "B) whom", "C) which", "D) whose"], "ans": "C"},
            {"q": "The woman _______ bag was stolen went to the police.", "options": ["A) who", "B) whom", "C) whose", "D) which"], "ans": "C"},
            {"q": "She believed everything _______ he said.", "options": ["A) who", "B) which", "C) that", "D) whom"], "ans": "C"},
            {"q": "He is the teacher _______ we all respect.", "options": ["A) who", "B) whom", "C) which", "D) whose"], "ans": "B"},
            {"q": "Paris, _______ is the capital of France, is beautiful.", "options": ["A) that", "B) where", "C) which", "D) who"], "ans": "C"},
            {"q": "The students _______ are studying in the library are very quiet.", "options": ["A) which", "B) whom", "C) whose", "D) who"], "ans": "D"},
            {"q": "We went to the restaurant _______ they serve great pasta.", "options": ["A) which", "B) where", "C) when", "D) that"], "ans": "B"},
            {"q": "The artist _______ paintings are famous is visiting Taiwan.", "options": ["A) who", "B) whom", "C) whose", "D) which"], "ans": "C"},
            {"q": "That was the moment _______ I realized my mistake.", "options": ["A) where", "B) which", "C) when", "D) why"], "ans": "C"},
            {"q": "There is nothing _______ I can do to help.", "options": ["A) what", "B) who", "C) which", "D) that"], "ans": "D"},
            {"q": "The team _______ won the game celebrated all night.", "options": ["A) who", "B) which", "C) whom", "D) whose"], "ans": "B"}
        ]
    },
    {
        "order": 8,
        "title": "第八章：介系詞",
        "grammar": "常見時間介系詞用法：<br><b>at</b> (特定時刻)：at 7 o'clock<br><b>on</b> (特定日子)：on Monday, on October 10th<br><b>in</b> (月份/年份/長時間)：in 2026, in October<br><br>空間：on (在...上面), in (在...裡面)",
        "questions": [
            {"q": "My birthday is _______ October 10th.", "options": ["A) in", "B) on", "C) at", "D) to"], "ans": "B"},
            {"q": "I will graduate _______ 2026.", "options": ["A) in", "B) on", "C) at", "D) for"], "ans": "A"},
            {"q": "The meeting starts _______ 7 o'clock.", "options": ["A) in", "B) on", "C) at", "D) with"], "ans": "C"},
            {"q": "We don't go to school _______ Sundays.", "options": ["A) in", "B) on", "C) at", "D) by"], "ans": "B"},
            {"q": "He is very good _______ playing tennis.", "options": ["A) in", "B) on", "C) at", "D) for"], "ans": "C"},
            {"q": "I am interested _______ learning Spanish.", "options": ["A) at", "B) in", "C) on", "D) with"], "ans": "B"},
            {"q": "It depends _______ the weather.", "options": ["A) at", "B) in", "C) on", "D) to"], "ans": "C"},
            {"q": "She is afraid _______ spiders.", "options": ["A) with", "B) of", "C) at", "D) to"], "ans": "B"},
            {"q": "I look forward _______ hearing from you.", "options": ["A) to", "B) for", "C) at", "D) in"], "ans": "A"},
            {"q": "He apologized _______ his bad behavior.", "options": ["A) to", "B) for", "C) at", "D) with"], "ans": "B"},
            {"q": "Please listen _______ the teacher carefully.", "options": ["A) at", "B) in", "C) to", "D) with"], "ans": "C"},
            {"q": "I have been waiting _______ the bus for 30 minutes.", "options": ["A) to", "B) for", "C) at", "D) in"], "ans": "B"},
            {"q": "This book belongs _______ me.", "options": ["A) for", "B) with", "C) to", "D) at"], "ans": "C"},
            {"q": "I completely agree _______ you.", "options": ["A) to", "B) on", "C) with", "D) at"], "ans": "C"},
            {"q": "They arrived _______ the train station at 5 PM.", "options": ["A) in", "B) at", "C) on", "D) to"], "ans": "B"},
            {"q": "We arrived _______ Tokyo yesterday morning.", "options": ["A) in", "B) at", "C) on", "D) to"], "ans": "A"},
            {"q": "Taiwan is famous _______ its street food.", "options": ["A) with", "B) to", "C) for", "D) at"], "ans": "C"},
            {"q": "The manager is responsible _______ the sales team.", "options": ["A) for", "B) with", "C) to", "D) at"], "ans": "A"},
            {"q": "Your phone is similar _______ mine.", "options": ["A) with", "B) as", "C) to", "D) for"], "ans": "C"},
            {"q": "I will drink tea instead _______ coffee.", "options": ["A) to", "B) of", "C) for", "D) with"], "ans": "B"}
        ]
    },
    {
        "order": 9,
        "title": "第九章：比較級與最高級",
        "grammar": "<b>比較級：</b>A + be + 比較級 + than + B<br>(Tom is taller than John.)<br><br><b>最高級：</b>A + be + the + 最高級<br>(Tom is the tallest student.)",
        "questions": [
            {"q": "This test is _______ than the previous one.", "options": ["A) easy", "B) easily", "C) easier", "D) the easiest"], "ans": "C"},
            {"q": "He is the _______ boy in his class.", "options": ["A) tall", "B) taller", "C) tallest", "D) most tall"], "ans": "C"},
            {"q": "This dress is _______ beautiful than that one.", "options": ["A) more", "B) most", "C) much", "D) very"], "ans": "A"},
            {"q": "My car runs as _______ as yours.", "options": ["A) faster", "B) fast", "C) fastest", "D) more fast"], "ans": "B"},
            {"q": "That was the _______ interesting book I have ever read.", "options": ["A) more", "B) very", "C) most", "D) much"], "ans": "C"},
            {"q": "I feel much _______ today than yesterday.", "options": ["A) good", "B) well", "C) best", "D) better"], "ans": "D"},
            {"q": "This is the _______ day of my life!", "options": ["A) bad", "B) worse", "C) worst", "D) worser"], "ans": "C"},
            {"q": "A bicycle is _______ expensive than a car.", "options": ["A) least", "B) less", "C) little", "D) fewer"], "ans": "B"},
            {"q": "It is the _______ important issue to consider right now.", "options": ["A) less", "B) least", "C) fewer", "D) little"], "ans": "B"},
            {"q": "She is two years older _______ her sister.", "options": ["A) then", "B) than", "C) as", "D) from"], "ans": "B"},
            {"q": "Russia is the _______ country in the world.", "options": ["A) big", "B) bigger", "C) biggest", "D) most big"], "ans": "C"},
            {"q": "You need to drive more _______ in the rain.", "options": ["A) careful", "B) carefully", "C) care", "D) most carefully"], "ans": "B"},
            {"q": "The hospital is _______ than I thought.", "options": ["A) far", "B) further", "C) furthest", "D) farthest"], "ans": "B"},
            {"q": "His performance was not as _______ as we expected.", "options": ["A) good", "B) better", "C) best", "D) well"], "ans": "A"},
            {"q": "Einstein was one of the _______ scientists in history.", "options": ["A) smart", "B) smarter", "C) smartest", "D) most smart"], "ans": "C"},
            {"q": "Chinese is _______ difficult to learn than English for many Europeans.", "options": ["A) very", "B) more", "C) most", "D) much"], "ans": "B"},
            {"q": "This hotel is the _______ expensive in the city.", "options": ["A) more", "B) much", "C) most", "D) very"], "ans": "C"},
            {"q": "I am _______ now than I was a year ago.", "options": ["A) happy", "B) happiest", "C) happier", "D) more happy"], "ans": "C"},
            {"q": "The weather today is _______ than yesterday.", "options": ["A) bad", "B) worst", "C) worse", "D) worser"], "ans": "C"},
            {"q": "This is the _______ pizza I have ever tasted!", "options": ["A) good", "B) better", "C) best", "D) most good"], "ans": "C"}
        ]
    },
    {
        "order": 10,
        "title": "第十章：綜合實戰挑戰",
        "grammar": "恭喜你完成了前面的九大基礎章節！回顧一下：<br>1. 詞類與句型是地基。<br>2. 時態、被動語態與助動詞是核心骨架。<br>3. 假設語氣、關代與比較級是進階裝飾。<br><br>準備好接受最終測驗，驗證你的學習成果了嗎？",
        "questions": [
            {"q": "The company _______ a new policy next month.", "options": ["A) implements", "B) will implement", "C) implemented", "D) has implemented"], "ans": "B"},
            {"q": "If I _______ the manager, I would change the rules.", "options": ["A) am", "B) was", "C) were", "D) have been"], "ans": "C"},
            {"q": "The man _______ briefcase was stolen is reporting to the police.", "options": ["A) who", "B) whom", "C) whose", "D) which"], "ans": "C"},
            {"q": "Our boss is very interested _______ launching a new product.", "options": ["A) at", "B) in", "C) on", "D) for"], "ans": "B"},
            {"q": "The monthly report _______ by the sales team yesterday.", "options": ["A) writes", "B) wrote", "C) was written", "D) is written"], "ans": "C"},
            {"q": "All employees must _______ their expense reports by Friday.", "options": ["A) submit", "B) submitting", "C) submitted", "D) to submit"], "ans": "A"},
            {"q": "This is the _______ lucrative contract we have ever signed.", "options": ["A) more", "B) most", "C) very", "D) much"], "ans": "B"},
            {"q": "We need to carefully _______ the results of the campaign.", "options": ["A) evaluate", "B) evaluation", "C) evaluator", "D) evaluating"], "ans": "A"},
            {"q": "His excellent presentation made the clients _______.", "options": ["A) happily", "B) happy", "C) happiness", "D) to happy"], "ans": "B"},
            {"q": "By the time the client arrives, we _______ the preparations.", "options": ["A) finish", "B) finished", "C) are finishing", "D) will have finished"], "ans": "D"},
            {"q": "Unless it _______ tomorrow, the outdoor event will proceed as planned.", "options": ["A) rain", "B) rains", "C) rained", "D) will rain"], "ans": "B"},
            {"q": "The supplier _______ we contacted last week has agreed to a discount.", "options": ["A) which", "B) whom", "C) whose", "D) what"], "ans": "B"},
            {"q": "The success of the project depends heavily _______ teamwork.", "options": ["A) in", "B) on", "C) at", "D) with"], "ans": "B"},
            {"q": "The elevator _______ right now, so please use the stairs.", "options": ["A) repairs", "B) is repairing", "C) is being repaired", "D) has repaired"], "ans": "C"},
            {"q": "You _______ me earlier! I could have helped you.", "options": ["A) should tell", "B) should have told", "C) must tell", "D) might tell"], "ans": "B"},
            {"q": "The new software is not as _______ as the old one.", "options": ["A) efficient", "B) more efficient", "C) most efficient", "D) efficiently"], "ans": "A"},
            {"q": "Reducing _______ costs is our priority for this quarter.", "options": ["A) overhead", "B) overhear", "C) overdue", "D) overcoat"], "ans": "A"},
            {"q": "The board members elected her _______ of the committee.", "options": ["A) president", "B) presently", "C) preside", "D) presidency"], "ans": "A"},
            {"q": "He is neither experienced _______ qualified for the position.", "options": ["A) or", "B) and", "C) nor", "D) but"], "ans": "C"},
            {"q": "[進階綜合題] If the report _______ earlier, we could have avoided the mistake.", "options": ["A) was submitted", "B) had been submitted", "C) is submitted", "D) has submitted"], "ans": "B"}
        ]
    }
]

print("開始匯入龐大資料至 Firebase...")

# 匯入 100 個單字
for idx, vocab in enumerate(vocabulary_data):
    doc_id = f"word_{str(idx+1).zfill(3)}" # 產生 word_001 ~ word_100
    db.collection("vocabulary").document(doc_id).set(vocab)
print("✅ 100 個多益精選單字庫匯入完成！")

# 匯入 10 章文法 (現已擴充為每章 20 題)
for lesson in lessons_data:
    doc_id = f"ch_{str(lesson['order']).zfill(2)}" # 產生 ch_01 ~ ch_10
    db.collection("grammar_lessons").document(doc_id).set(lesson)
print("✅ 10 章文法資料（共 200 題）匯入完成！")

print("🎉 恭喜！百大單字與豐富的文法題庫已成功上傳至雲端！")