from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def get_db_connection():
    conn = sqlite3.connect('lost_found.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('account'))
    return redirect(url_for('login'))

@app.route('/set_language/<lang>')
def set_language(lang):
    session['language'] = lang
    return redirect(request.referrer or '/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)
        conn = get_db_connection()
        is_admin = 1 if username == 'msh' else 0
        try:
            conn.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', (username, hashed_password, is_admin))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('signup.html', error="اسم المستخدم مستخدم من قبل", language=session.get('language', 'ar'))
        conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html', language=session.get('language', 'ar'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and verify_password(password, user['password']):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            return redirect(url_for('account'))
        else:
            error = "اسم المستخدم أو كلمة المرور خاطئة"
    return render_template('login.html', error=error, language=session.get('language', 'ar'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items WHERE username = ?', (session['username'],)).fetchall()
    conn.close()
    return render_template('account.html', username=session['username'], items=items, is_admin=session.get('is_admin', 0), language=session.get('language', 'ar'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('account'))
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items WHERE is_approved = 0').fetchall()
    conn.close()
    return render_template('admin_dashboard.html', items=items, language=session.get('language', 'ar'))

@app.route('/approve/<int:item_id>', methods=['POST'])
def approve_item(item_id):
    if not session.get('is_admin'):
        return redirect(url_for('account'))
    conn = get_db_connection()
    conn.execute('UPDATE items SET is_approved = 1 WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/reject/<int:item_id>', methods=['POST'])
def reject_item(item_id):
    if not session.get('is_admin'):
        return redirect(url_for('account'))
    conn = get_db_connection()
    conn.execute('UPDATE items SET is_approved = -1 WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/report', methods=['GET', 'POST'])
def report():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        contact = request.form['contact']
        lost_time = request.form['lost_time']
        lost_place = request.form['lost_place']
        username = session['username']

        conn = sqlite3.connect('lost_found.db')
        c = conn.cursor()
        c.execute('INSERT INTO items (name, description, contact, lost_time, lost_place, username) VALUES (?, ?, ?, ?, ?, ?)',
                  (name, description, contact, lost_time, lost_place, username))
        conn.commit()
        conn.close()
        return redirect('/account')

    return render_template('report.html', language=session.get('language', 'ar'))

@app.route('/search_report', methods=['GET', 'POST'])
def search_report():
    result = None
    if request.method == 'POST':
        item_id = request.form['item_id']
        conn = get_db_connection()
        item = conn.execute('SELECT * FROM items WHERE id = ? AND user_id = ?', (item_id, session.get('user_id'))).fetchone()
        conn.close()
        if item:
            if item['is_approved'] == 1:
                result = "✅ تم قبول البلاغ"
            elif item['is_approved'] == 0:
                result = "🕒 البلاغ قيد المراجعة"
            elif item['is_approved'] == -1:
                result = "❌ تم رفض البلاغ"
        else:
            result = "❌ لا يوجد بلاغ بهذا الرقم خاص بك."
    return render_template('search_report.html', result=result, language=session.get('language', 'ar'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()

    if not item:
        conn.close()
        return redirect(url_for('account'))

    if session.get('is_admin') or item['user_id'] == session['user_id']:
        conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
        conn.commit()

    conn.close()
    if session.get('is_admin'):
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('account'))

@app.route('/chatbot_page')
def chatbot_page():
    return render_template('chatbot_page.html', language=session.get('language', 'ar'))


if __name__ == "__main__":
    app.run()

