from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager() 

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados (use o URI do seu banco de dados)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta'

    # Habilitar CORS para todas as rotas
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    
    db.init_app(app)
    migrate.init_app(app, db)

    # Inicializar o JWTManager com o app Flask
    jwt.init_app(app)


    # Registrar blueprints e rotas
    from .routes import main
    app.register_blueprint(main)

    return app
