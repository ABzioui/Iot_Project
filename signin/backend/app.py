from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
import redis
from dotenv import load_dotenv
from models import db, User
from Config import Config
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)
load_dotenv()

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "fallback_secret_key")
jwt = JWTManager(app)

app.config.from_object(Config)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# Redis for session management
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({"message": "Missing data"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating user', 'error': str(e)}), 500

@app.route('/signin', methods=['POST'])
def signin():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Generate JWT Token
        access_token = create_access_token(identity=username)
        
        # Store session in Redis
        redis_client.set(f'session:{username}', access_token, ex=3600)  # 1 hour expiry
        
        return jsonify({
            "message": "Login successful", 
            "user": username, 
            "token": access_token
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    })

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    redis_client.delete(f'session:{current_user}')
    return jsonify({'message': 'Logged out successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)