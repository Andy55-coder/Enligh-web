import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import os

# 1. 自動讀取金鑰，連線至 Firestore
base_dir = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(base_dir, "serviceAccountKey.json")
cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. 讀取同資料夾下的 Excel 檔案
excel_file = os.path.join(base_dir, "toeic_high_frequency_words.xlsx")
print(f"正在讀取檔案: {excel_file}...")

try:
    # 將 Excel 轉換成 DataFrame
    df = pd.read_excel(excel_file)
    
    # 處理空值(NaN)，轉為空字串，避免 Firebase 報錯
    df = df.fillna("") 
    
    # 將資料轉為字典清單格式
    words_data = df.to_dict(orient='records')
    total_words = len(words_data)
    print(f"✅ 成功讀取 {total_words} 個單字，準備開始上傳...")
    
except Exception as e:
    print(f"❌ 讀取 Excel 失敗，請確認檔案名稱是否正確。錯誤訊息：{e}")
    exit()

# 3. 使用 Firebase 的批次處理 (Batch) 功能上傳
# Firebase 規定一個 Batch 最多只能裝 500 筆資料，所以我們要做分批上傳
batch_size = 400
batches_count = 0
current_batch = db.batch()

for idx, item in enumerate(words_data):
    # 建立文件 ID (例如 word_0001, word_0002)
    doc_id = f"word_{str(idx+1).zfill(4)}" 
    doc_ref = db.collection("vocabulary").document(doc_id)
    
    # 將這筆資料加入目前的 Batch 購物車
    current_batch.set(doc_ref, item)
    
    # 如果購物車裝滿 400 筆，就結帳送出一次，然後重新拿一個新的購物車
    if (idx + 1) % batch_size == 0:
        current_batch.commit()
        batches_count += 1
        print(f"🚀 已成功上傳 {idx + 1} / {total_words} 筆單字...")
        current_batch = db.batch() 

# 把最後一次還沒滿 400 筆的剩餘資料送出
if (total_words % batch_size) != 0:
    current_batch.commit()
    print(f"🚀 已成功上傳 {total_words} / {total_words} 筆單字...")

print("🎉 恭喜！所有單字已全數匯入 Firebase 雲端資料庫！")