import os
import json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

# ==========================================
# 1. 直接在同一層尋找 frontend 資料夾
# ==========================================
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'frontend')

app = Flask(__name__, template_folder=template_dir)
CORS(app) 

# ==========================================
# 2. 讀取金鑰 (支援 Vercel 與本地端)
# ==========================================
firebase_credentials = os.environ.get('FIREBASE_SERVICE_ACCOUNT')

if firebase_credentials:
    cred_dict = json.loads(firebase_credentials)
    cred = credentials.Certificate(cred_dict)
else:
    # 現在金鑰也跟 app.py 放在同一層了
    key_path = os.path.join(base_dir, "serviceAccountKey.json")
    cred = credentials.Certificate(key_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ...(下面保留你所有的 @app.route 首頁和 API)...
# ==========================================
# 3. 網頁畫面路由設定 (控制哪個網址顯示哪個 HTML)
# ==========================================
@app.route('/')
def home():
    # 網站一進來就是登入畫面
    return render_template('login.html')

@app.route('/index')
def index_page():
    return render_template('index.html')

@app.route('/vocabulary')
def vocabulary_page():
    return render_template('vocabulary.html')

@app.route('/add_vocabulary')
def add_vocabulary_page():
    return render_template('add_vocabulary.html')

# ==========================================
# 以下是你原本寫好的 API 系統，原封不動保留
# ==========================================

# --- 使用者註冊系統 ---
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
            
        user_ref.set({
            "password": password,
            "exp": 0,
            "completedChapters": [],
            "completedHardMode": [],
            "activeProgress": {}  
        })
        return jsonify({"success": True, "msg": "帳號註冊成功！請進行登入。"}), 201
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

# --- 使用者登入系統 ---
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

# --- 讀取與儲存雲端進度 API ---
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
        "completedHardMode": user_data.get('completedHardMode', []),
        "activeProgress": user_data.get('activeProgress', {}) 
    }), 200

@app.route('/api/save_progress', methods=['POST'])
def save_progress():
    try:
        data = request.json
        username = data.get('username', '').strip()
        
        user_ref = db.collection("users").document(username)
        if not user_ref.get().exists:
            return jsonify({"success": False, "msg": "使用者未註冊"}), 404
            
        user_ref.update({
            "exp": data.get('exp', 0),
            "completedChapters": data.get('completedChapters', []),
            "completedHardMode": data.get('completedHardMode', []),
            "activeProgress": data.get('activeProgress', {}) 
        })
        return jsonify({"success": True, "msg": "雲端進度同步成功"}), 200
    except Exception as e:
        return jsonify({"success": False, "msg": str(e)}), 500

# --- API：取得文法章節與對答案系統 ---
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

# --- API：取得單字卡資料 (全域百大 + 個人專屬) ---
@app.route('/api/vocabulary', methods=['GET'])
def get_vocabulary():
    try:
        username = request.args.get('username')
        words = []
        
        # 1. 取得全域百大單字
        docs = db.collection("vocabulary").stream()
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            data['type'] = 'global'
            words.append(data)
            
        # 2. 取得使用者專屬單字 (子集合)
        if username:
            user_words_ref = db.collection("users").document(username).collection("my_words").stream()
            for doc in user_words_ref:
                data = doc.to_dict()
                data['id'] = doc.id
                data['type'] = 'private'
                words.append(data)

        return jsonify(words), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- API：儲存自訂單字卡 (存入個人的子集合) ---
@app.route('/api/vocabulary', methods=['POST'])
def add_vocabulary():
    try:
        data = request.json
        username = data.get('username', '').strip()
        word = data.get('word', '').strip()
        part = data.get('part', '').strip()
        meaning = data.get('meaning', '').strip()
        example = data.get('example', '').strip()

        if not username:
            return jsonify({"error": "未登入，無法新增專屬單字"}), 401
        if not word or not meaning:
            return jsonify({"error": "欄位必填"}), 400

        new_vocab = {
            "word": word, 
            "part": part if part else "n.", 
            "meaning": meaning, 
            "example": example if example else ""
        }
        
        # 存入 users -> {username} -> my_words
        db.collection("users").document(username).collection("my_words").document().set(new_vocab)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)