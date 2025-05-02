from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



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
    lost_items = conn.execute('SELECT * FROM items WHERE is_approved = 0').fetchall()
    found_items = conn.execute('SELECT * FROM found_items WHERE is_approved = 0').fetchall()
    conn.close()
    return render_template('admin_dashboard.html', items=lost_items, found_items=found_items, language=session.get('language', 'ar'))


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
        image = request.files.get('image')
        image_path = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
        username = session['username']
        conn = sqlite3.connect('lost_found.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO items (name, description, contact, lost_time, lost_place, image_path, username)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, contact, lost_time, lost_place, image_path, username))
        conn.commit()
        conn.close()
        return redirect('/account')
    return render_template('report.html', language=session.get('language', 'ar'))

@app.route('/user/delete/<int:item_id>', methods=['POST'])
def user_delete_lost_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('account'))


@app.route('/admin/delete/<int:item_id>', methods=['POST'])
def admin_delete_lost_item(item_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('account'))

@app.route('/admin/delete_found/<int:item_id>', methods=['POST'])
def admin_delete_found_item(item_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM found_items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))



@app.route('/chatbot_page')
def chatbot_page():
    return render_template('chatbot_page.html', language=session.get('language', 'ar'))

@app.route('/found_report', methods=['GET', 'POST'])
def found_report():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        contact = request.form['contact']
        found_time = request.form['found_time']
        found_place = request.form['found_place']
        image = request.files.get('image')
        image_path = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
        username = session['username']
        conn = get_db_connection()
        conn.execute('INSERT INTO found_items (name, description, contact, found_time, found_place, image_path, username) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (name, description, contact, found_time, found_place, image_path, username))
        conn.commit()
        conn.close()
        return redirect('/account')
    return render_template('found_report.html', language=session.get('language', 'ar'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

