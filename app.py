from flask import Flask, render_template, request, redirect, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'feedback.json'
ADMIN_PASSWORD = 'admin123'

# Load feedback entries
def load_feedback():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save feedback entries
def save_feedback(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Submit Feedback Page
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        new_feedback = {
            'member': request.form['member'],
            'project': request.form['project'],
            'task': request.form['task'],
            'difficulty': request.form['difficulty'],
            'comments': request.form['comments'],
            'email': request.form.get('email', ''),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        data = load_feedback()
        data.append(new_feedback)
        save_feedback(data)
        return render_template('thanks.html', name=new_feedback['member'])
    return render_template('submit.html')

# Admin Login and View
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password != ADMIN_PASSWORD:
            return render_template('admin.html', error='Incorrect password.')
        feedback = load_feedback()
        return render_template('admin.html', feedback=feedback, success=True)
    return render_template('admin.html')

# API: Get all feedback (JSON)
@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    return jsonify(load_feedback())

# API: Delete feedback entry by index
@app.route('/api/feedback/delete/<int:index>', methods=['POST'])
def delete_feedback(index):
    data = load_feedback()
    if 0 <= index < len(data):
        deleted = data.pop(index)
        save_feedback(data)
        return jsonify({'message': f'Deleted feedback from {deleted["member"]}'}), 200
    return jsonify({'error': 'Invalid index'}), 400

if __name__ == '__main__':
    app.run(debug=True)
