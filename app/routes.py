from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from .models import User, db
from app.models import User
from app import db

main = Blueprint('main', __name__)

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    user_name = data.get('user_name')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400
    
    if User.query.filter_by(user_name=user_name).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = User(email=email, password=password, first_name=first_name, last_name=last_name, user_name=user_name)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Verifique se o usuário existe
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Criar o token JWT
    access_token = create_access_token(identity={"id": user.id, "email": user.email})
    return jsonify(access_token=access_token), 200

@main.route('/users', methods=['GET'])
def list_users():
    try:
        users = User.query.all()
        print(users)  # Para ver os usuários no terminal
        users_list = [
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
            for user in users
        ]
        return jsonify(users_list), 200
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return jsonify({"error": "Erro ao listar usuários"}), 500
