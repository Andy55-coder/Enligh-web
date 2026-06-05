from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
CORS(app) 

# 1. 讀取金鑰，連線至 Firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ==========================================
# [新增] 使用者註冊系統
# ==========================================
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({"success": False, "msg": "帳號密碼不可為空"}), 400
            
        user_ref = db.collection("users").document(username)
        if user_ref.get().exists:
            return jsonify({"success": False, "msg": "此使用者帳號已被註冊"}), 400
            
        # 建立使用者核心紀錄與初始零進度結構
        user_ref.set({
            "password": password,
            "exp": 0,
            "completedChapters": [],
            "completedHardMode": []
        })
        return jsonify({"success": True, "msg": "帳號註冊成功！請進行登入。"}), 201
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

# ==========================================
# [新增] 使用者登入系統
# ==========================================
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        user_ref = db.collection("users").document(username)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            return jsonify({"success": False, "msg": "此帳號不存在"}), 404
            
        user_data = user_doc.to_dict()
        if user_data.get('password') != password:
            return jsonify({"success": False, "msg": "密碼輸入錯誤"}), 401
            
        return jsonify({"success": True, "msg": "登入成功！歡迎回來。"}), 200
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

# ==========================================
# [新增] 讀取雲端進度 API
# ==========================================
@app.route('/api/get_progress', methods=['POST'])
def get_progress():
    data = request.json
    username = data.get('username', '').strip()
    
    user_ref = db.collection("users").document(username)
    user_doc = user_ref.get()
    if not user_doc.exists:
        return jsonify({"error": "找不到該使用者"}), 404
        
    user_data = user_doc.to_dict()
    return jsonify({
        "exp": user_data.get('exp', 0),
        "completedChapters": user_data.get('completedChapters', []),
        "completedHardMode": user_data.get('completedHardMode', [])
    }), 200

# ==========================================
# [新增] 儲存進度同步 API
# ==========================================
@app.route('/api/save_progress', methods=['POST'])
def save_progress():
    try:
        data = request.json
        username = data.get('username', '').strip()
        
        user_ref = db.collection("users").document(username)
        if not user_ref.get().exists:
            return jsonify({"success": False, "msg": "使用者未註冊"}), 404
            
        # 將前端最新計算完成的數據複寫回雲端專屬文件
        user_ref.update({
            "exp": data.get('exp', 0),
            "completedChapters": data.get('completedChapters', []),
            "completedHardMode": data.get('completedHardMode', [])
        })
        return jsonify({"success": True, "msg": "雲端進度儲存成功"}), 200
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

# ==========================================
# API：取得文法章節
# ==========================================
@app.route('/api/lessons', methods=['GET'])
def get_lessons():
    try:
        docs = db.collection("grammar_lessons").order_by("order").stream()
        lessons = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            if 'questions' in data and isinstance(data['questions'], list):
                for q in data['questions']:
                    q.pop('ans', None)
            if 'hard_questions' in data and isinstance(data['hard_questions'], list):
                for q in data['hard_questions']:
                    q.pop('ans', None)
            lessons.append(data)
        return jsonify(lessons), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# API：對答案系統
# ==========================================
@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    ch_id = data.get('id')
    q_idx = data.get('questionIndex', 0)
    user_selected_text = data.get('text')
    mode = data.get('mode', 'basic')

    doc_ref = db.collection("grammar_lessons").document(ch_id)
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({"correct": False, "msg": "找不到該章節"}), 404

    db_data = doc.to_dict()
    questions = db_data.get('hard_questions', []) if mode == 'hard' else db_data.get('questions', [])

    if q_idx < 0 or q_idx >= len(questions):
        return jsonify({"correct": False, "msg": "題目索引超出範圍"}), 400

    current_q = questions[q_idx]
    correct_ans_letter = current_q.get('ans')
    options = current_q.get('options', [])
    
    correct_full_str = next((opt for opt in options if opt.startswith(correct_ans_letter)), "")
    correct_text = correct_full_str[3:].strip() if len(correct_full_str) > 3 else ""

    if user_selected_text and user_selected_text.strip() == correct_text:
        return jsonify({"correct": True, "msg": "答案正確！"}), 200
    else:
        return jsonify({"correct": False, "msg": "答錯囉！"}), 200

# ==========================================
# API：取得單字卡資料
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
        return jsonify(words), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# API：儲存自訂單字卡
# ==========================================
@app.route('/api/vocabulary', methods=['POST'])
def add_vocabulary():
    try:
        data = request.json
        word = data.get('word', '').strip()
        part = data.get('part', '').strip()
        meaning = data.get('meaning', '').strip()
        example = data.get('example', '').strip()

        if not word or not meaning:
            return jsonify({"error": "欄位必填"}), 400

        new_vocab = {
            "word": word, "part": part if part else "n.", "meaning": meaning, "example": example if example else ""
        }
        doc_ref = db.collection("vocabulary").document()
        doc_ref.set(new_vocab)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)