from flask import Flask, request, send_from_directory, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CODES_FILE = 'codes.txt'
USED_CODES_FILE = 'used_codes.json'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------- LOAD & SAVE --------------------

def load_codes():
    if not os.path.exists(CODES_FILE):
        return []
    with open(CODES_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def load_used_codes():
    if os.path.exists(USED_CODES_FILE):
        with open(USED_CODES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_used_codes(data):
    with open(USED_CODES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# -------------------- ROUTES --------------------

@app.route('/')
def home():
    return send_from_directory('.', 'admin.html')

@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

@app.route('/admin-data')
def admin_data():
    codes = load_codes()
    used = load_used_codes()
    result = []

    for code in codes:
        result.append({
            "code": code,
            "used": code in used,
            "date": used.get(code, "")
        })

    return jsonify(result)

@app.route('/add-code', methods=['POST'])
def add_code():
    data = request.get_json()
    new_code = data.get('code', '').strip()

    if not new_code:
        return "❌ كود غير صالح", 400

    codes = load_codes()
    if new_code in codes:
        return "⚠️ الكود موجود بالفعل"

    with open(CODES_FILE, 'a', encoding='utf-8') as f:
        f.write(new_code + '\n')

    return "✅ تمت إضافة الكود بنجاح"

@app.route('/delete-code', methods=['POST'])
def delete_code():
    data = request.get_json()
    code_to_delete = data.get('code', '').strip()

    codes = load_codes()
    if code_to_delete not in codes:
        return "❌ الكود غير موجود"

    updated_codes = [c for c in codes if c != code_to_delete]
    with open(CODES_FILE, 'w', encoding='utf-8') as f:
        for code in updated_codes:
            f.write(code + '\n')

    return "🗑️ تم حذف الكود"

# -------------------- RUN --------------------

if __name__ == '__main__':
    app.run(debug=True, port=5000)
