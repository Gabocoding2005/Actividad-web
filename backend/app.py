from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

@app.route('/api/transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    
    conn = get_db()
    cursor = conn.cursor()
    
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute(
        'INSERT INTO transactions (type, description, amount, date) VALUES (?, ?, ?, ?)',
        (data.get('type'), data.get('description'), float(data.get('amount')), date)
    )
    
    conn.commit()
    transaction_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'success': True,
        'message': 'Transacción agregada exitosamente',
        'transaction': {
            'id': transaction_id,
            'type': data.get('type'),
            'description': data.get('description'),
            'amount': float(data.get('amount')),
            'date': date
        }
    }), 201

@app.route('/api/habit', methods=['POST'])
def add_habit():
    data = request.get_json()
    
    conn = get_db()
    cursor = conn.cursor()
    
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute(
        'INSERT INTO habits (name, date) VALUES (?, ?)',
        (data.get('name'), date)
    )
    
    conn.commit()
    habit_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'success': True,
        'message': 'Hábito registrado exitosamente',
        'habit': {
            'id': habit_id,
            'name': data.get('name'),
            'date': date
        }
    }), 201

@app.route('/api/summary', methods=['GET'])
def get_summary():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
    total_income = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
    total_expense = cursor.fetchone()[0] or 0
    
    balance = total_income - total_expense
    
    cursor.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = cursor.fetchone()[0]
    
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) FROM habits WHERE date LIKE ?", (f'{today}%',))
    habits_today = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM habits")
    total_habits = cursor.fetchone()[0]
    
    cursor.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT 5")
    recent_transactions = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM habits ORDER BY id DESC LIMIT 5")
    recent_habits = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'success': True,
        'summary': {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'total_transactions': total_transactions,
            'habits_today': habits_today,
            'total_habits': total_habits
        },
        'recent_transactions': recent_transactions,
        'recent_habits': recent_habits
    }), 200

if __name__ == '__main__':
    init_db()
    print('Servidor iniciado en http://localhost:5000')
    print('Base de datos SQLite inicializada')
    app.run(debug=True, port=5000)
