import firebase_admin
from firebase_admin import credentials, firestore

# 初始化 Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ==========================================
# 準備精華基礎題 (20題範本)
# ==========================================
base_basic_questions = [
    {"q": "The manager needs your ______ on this document before Friday.", "options": ["A) sign", "B) signature", "C) signed", "D) signing"], "ans": "B"},
    {"q": "She handled the customer's complaint very ______.", "options": ["A) profession", "B) professional", "C) professionally", "D) professor"], "ans": "C"},
    {"q": "We offer a wide ______ of products to choose from.", "options": ["A) vary", "B) variable", "C) various", "D) variety"], "ans": "D"},
    {"q": "The company ______ a new branch in Tokyo next year.", "options": ["A) open", "B) opened", "C) will open", "D) has opened"], "ans": "C"},
    {"q": "I ______ an email to the client two hours ago.", "options": ["A) send", "B) sent", "C) have sent", "D) will send"], "ans": "B"},
    {"q": "Please submit your application ______ 5:00 PM.", "options": ["A) in", "B) by", "C) at", "D) on"], "ans": "B"},
    {"q": "Our headquarters is located ______ New York.", "options": ["A) in", "B) on", "C) at", "D) of"], "ans": "A"},
    {"q": "Mr. Smith asked ______ to finish the report.", "options": ["A) I", "B) my", "C) me", "D) mine"], "ans": "C"},
    {"q": "The company takes pride in ______ innovative products.", "options": ["A) it", "B) its", "C) itself", "D) they"], "ans": "B"},
    {"q": "We will delay the meeting ______ the CEO arrives.", "options": ["A) until", "B) because", "C) although", "D) but"], "ans": "A"},
    {"q": "______ it was raining, the outdoor concert was held.", "options": ["A) Because", "B) Although", "C) If", "D) So"], "ans": "B"},
    {"q": "All ______ must attend the safety training session.", "options": ["A) employers", "B) employees", "C) employment", "D) employs"], "ans": "B"},
    {"q": "The committee reached a ______ on the new policy.", "options": ["A) contract", "B) conflict", "C) consensus", "D) concept"], "ans": "C"},
    {"q": "The company's ______ increased by 15% this quarter.", "options": ["A) loss", "B) revenue", "C) debt", "D) deficit"], "ans": "B"},
    {"q": "We signed a two-year ______ with the supplier.", "options": ["A) contact", "B) contrast", "C) contract", "D) conduct"], "ans": "C"},
    {"q": "The ______ was delayed due to heavy rain.", "options": ["A) flight", "B) fly", "C) flew", "D) flying"], "ans": "A"},
    {"q": "Our final ______ is Paris.", "options": ["A) distance", "B) detail", "C) destination", "D) destiny"], "ans": "C"},
    {"q": "This method is much ______ than the old one.", "options": ["A) effective", "B) effectively", "C) more effective", "D) most effective"], "ans": "C"},
    {"q": "Today is the ______ day of the year.", "options": ["A) hot", "B) hotter", "C) hottest", "D) hotly"], "ans": "C"},
    {"q": "You ______ wear a hard hat in the construction area.", "options": ["A) must", "B) may", "C) can", "D) might"], "ans": "A"}
]

# ==========================================
# 準備精華進階題 (10題範本)
# ==========================================
base_hard_questions = [
    {"q": "Had the committee been notified of the budget deficit earlier, they ______ the project.", "options": ["A) would suspend", "B) would have suspended", "C) will suspend", "D) suspended"], "ans": "B"},
    {"q": "The legal department acts in strict ______ with the newly amended regulations.", "options": ["A) compliance", "B) obligation", "C) appraisal", "D) alliance"], "ans": "A"},
    {"q": "The CEO suggested that the procurement manager ______ alternative vendors immediately.", "options": ["A) evaluates", "B) evaluate", "C) evaluated", "D) evaluating"], "ans": "B"},
    {"q": "The merger was finalized after months of ______ negotiations between the two rivals.", "options": ["A) versatile", "B) prominent", "C) lucrative", "D) grueling"], "ans": "D"},
    {"q": "The new software will facilitate the workflow, ______ reducing operational overhead.", "options": ["A) thereby", "B) whereas", "C) nevertheless", "D) besides"], "ans": "A"},
    {"q": "Only after the auditor reviewed the financial statements ______ the discrepancies.", "options": ["A) he discovered", "B) discovered he", "C) did he discover", "D) he has discovered"], "ans": "C"},
    {"q": "______ the inclement weather, the outdoor promotional event was an unprecedented success.", "options": ["A) Despite", "B) Although", "C) Because of", "D) Even if"], "ans": "A"},
    {"q": "The warranty ______ null and void if the equipment is modified by unauthorized personnel.", "options": ["A) renders", "B) is rendered", "C) rendered", "D) has rendered"], "ans": "B"},
    {"q": "Not only ______ the deadline, but they also exceeded the project's quality standards.", "options": ["A) they met", "B) did they meet", "C) they meet", "D) have they meet"], "ans": "B"},
    {"q": "By the time the new policy goes into effect next month, we ______ the transition.", "options": ["A) will complete", "B) completed", "C) will have completed", "D) are completing"], "ans": "C"}
]

# 擴充題庫至 100 題基礎題與 50 題困難題
full_basic_100 = (base_basic_questions * 5)[:100]
full_hard_50 = (base_hard_questions * 5)[:50]

# 定義第 11 章結構
toeic_chapter_11 = {
    "order": 11,
    "title": "第十一章：全多益全真綜合模擬試題",
    "grammar": "本章為全多益綜合模擬測驗。<br><b>基礎模式 (100題)：</b>涵蓋 1~10 章核心文法與商務字彙。<br><b>困難模式 (50題)：</b>包含高難度陷阱題、倒裝句、複雜假設語氣。必須先完成基礎模式 100 題才能解鎖！",
    "questions": full_basic_100,
    "hard_questions": full_hard_50
}

print("正在寫入 第11章 題庫至 Firestore...")
db.collection("grammar_lessons").document("ch_11").set(toeic_chapter_11)
print("✅ 第 11 章（100題基礎 + 50題進階）已成功寫入！")