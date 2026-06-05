from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
CORS(app) # 允許前端跨網域呼叫

# 1. 讀取金鑰，連線至 Firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ==========================================
# API 1：取得文法章節 (剔除陣列中每一題的正確答案防止作弊)
# ==========================================
@app.route('/api/lessons', methods=['GET'])
def get_lessons():
    try:
        docs = db.collection("grammar_lessons").order_by("order").stream()
        lessons = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            
            # 新版防作弊：遍歷 questions 陣列，把每一題的答案 (ans) 拿掉後再發送給前端
            if 'questions' in data and isinstance(data['questions'], list):
                for q in data['questions']:
                    q.pop('ans', None) # 移除個別題目的答案答案欄位
            
            lessons.append(data)
        return jsonify(lessons), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# API 2：對答案系統 (支援指定題號 index 審查)
# ==========================================
@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    ch_id = data.get('id')
    q_idx = data.get('questionIndex', 0)  # 接收前端傳來的題號索引 (0 ~ 19)
    user_selected_text = data.get('text')

    doc_ref = db.collection("grammar_lessons").document(ch_id)
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({"correct": False, "msg": "找不到該章節"}), 404

    db_data = doc.to_dict()
    questions = db_data.get('questions', [])

    # 安全檢查：確保前端傳來的索引值在陣列範圍內
    if q_idx < 0 or q_idx >= len(questions):
        return jsonify({"correct": False, "msg": "題目索引超出範圍"}), 400

    # 取得當前題目
    current_q = questions[q_idx]
    correct_ans_letter = current_q.get('ans')  # 例如 "C"
    options = current_q.get('options', [])
    
    # 根據正確字母 (如 "C")，在 options 陣列中尋找對應的完整字串 (如 "C) easier")
    correct_full_str = next((opt for opt in options if opt.startswith(correct_ans_letter)), "")
    
    # 去除開頭的 "C) " 提取純文字敘述進行比對
    correct_text = correct_full_str[3:].strip() if len(correct_full_str) > 3 else ""

    # 比對使用者去掉前後空白後的答案
    if user_selected_text and user_selected_text.strip() == correct_text:
        return jsonify({"correct": True, "msg": "答案正確！"}), 200
    else:
        return jsonify({"correct": False, "msg": "答錯囉！"}), 200

# ==========================================
# API 3：取得單字卡資料
# ==========================================
@app.route('/api/vocabulary', methods=['GET'])
def get_vocabulary():
    try:
        docs = db.collection("vocabulary").stream()
        words = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            words.append(data)
            
        # 若資料庫為空，先回傳假資料測試介面
        if not words:
            words = [
                {"word": "implement", "part": "v.", "meaning": "實施、執行", "example": "The company will implement a new policy."},
                {"word": "abandon", "part": "v.", "meaning": "放棄、拋棄", "example": "They had to abandon the project."}
            ]
        return jsonify(words), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 後端 API 伺服器啟動中...")
    app.run(port=5000, debug=True)