# api/index.py
import sys
import os

# 將上一層(專案根目錄)加入系統路徑，這樣 Vercel 才能找到您的 app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 引入您寫好的 app 實例
from app import app