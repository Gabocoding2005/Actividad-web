from flask import Flask, request, jsonify
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'tracker_db')

DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    description = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'description': self.description,
            'amount': self.amount,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S')
        }

class Habit(Base):
    __tablename__ = 'habits'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S')
        }

def init_db():
    Base.metadata.create_all(engine)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

@app.route('/api/transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    session = Session()
    
    try:
        transaction = Transaction(
            type=data.get('type'),
            description=data.get('description'),
            amount=float(data.get('amount')),
            date=datetime.now()
        )
        
        session.add(transaction)
        session.commit()
        
        result = transaction.to_dict()
        session.close()
        
        return jsonify({
            'success': True,
            'message': 'Transacción agregada exitosamente',
            'transaction': result
        }), 201
    except Exception as e:
        session.rollback()
        session.close()
        return jsonify({
            'success': False,
            'message': f'Error al agregar transacción: {str(e)}'
        }), 500

@app.route('/api/habit', methods=['POST'])
def add_habit():
    data = request.get_json()
    session = Session()
    
    try:
        habit = Habit(
            name=data.get('name'),
            date=datetime.now()
        )
        
        session.add(habit)
        session.commit()
        
        result = habit.to_dict()
        session.close()
        
        return jsonify({
            'success': True,
            'message': 'Hábito registrado exitosamente',
            'habit': result
        }), 201
    except Exception as e:
        session.rollback()
        session.close()
        return jsonify({
            'success': False,
            'message': f'Error al registrar hábito: {str(e)}'
        }), 500

@app.route('/api/summary', methods=['GET'])
def get_summary():
    session = Session()
    
    try:
        total_income = session.query(func.sum(Transaction.amount)).filter(
            Transaction.type == 'income'
        ).scalar() or 0
        
        total_expense = session.query(func.sum(Transaction.amount)).filter(
            Transaction.type == 'expense'
        ).scalar() or 0
        
        balance = total_income - total_expense
        
        total_transactions = session.query(Transaction).count()
        
        today = datetime.now().date()
        habits_today = session.query(Habit).filter(
            func.date(Habit.date) == today
        ).count()
        
        total_habits = session.query(Habit).count()
        
        recent_transactions = session.query(Transaction).order_by(
            Transaction.id.desc()
        ).limit(5).all()
        
        recent_habits = session.query(Habit).order_by(
            Habit.id.desc()
        ).limit(5).all()
        
        result = {
            'success': True,
            'summary': {
                'total_income': float(total_income),
                'total_expense': float(total_expense),
                'balance': float(balance),
                'total_transactions': total_transactions,
                'habits_today': habits_today,
                'total_habits': total_habits
            },
            'recent_transactions': [t.to_dict() for t in recent_transactions],
            'recent_habits': [h.to_dict() for h in recent_habits]
        }
        
        session.close()
        return jsonify(result), 200
    except Exception as e:
        session.close()
        return jsonify({
            'success': False,
            'message': f'Error al obtener resumen: {str(e)}'
        }), 500

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

if __name__ == '__main__':
    init_db()
    print('Servidor iniciado en http://localhost:5000')
    print(f'Conectado a MySQL: {DB_HOST}:{DB_PORT}/{DB_NAME}')
    print('Base de datos inicializada con SQLAlchemy')
    print('Modelos: Transaction, Habit')
    app.run(debug=True, port=5000)
