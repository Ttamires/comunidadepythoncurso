import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '29cecf8afd6176f06bb3f55472d490d1')
app.config['DEBUG'] = False 

# CORREÇÃO PARA POSTGRESQL NO RAILWAY
database_url = os.getenv('DATABASE_URL')
if database_url:
    # Railway usa 'postgres://' mas SQLAlchemy precisa de 'postgresql://'
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print("Usando PostgreSQL do Railway")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
    print("Usando SQLite local")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.errorhandler(500)
def internal_error(error):
    return str(error), 500

print("Inicializando extensões...")
try:
    database = SQLAlchemy(app)
    print("SQLAlchemy inicializado")
except Exception as e:
    print(f"Erro no SQLAlchemy: {e}")

try:
    bcrypt = Bcrypt(app)
    print("Bcrypt inicializado")
except Exception as e:
    print(f"Erro no Bcrypt: {e}")

try:
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'alert-info'
    print("LoginManager inicializado")
except Exception as e:
    print(f"Erro no LoginManager: {e}")

# Testar conexão com o banco
try:
    with app.app_context():
        database.engine.connect()
        print("✅ Conexão com o banco estabelecida com sucesso")
except Exception as e:
    print(f"❌ Erro na conexão com o banco: {e}")

print("Importando rotas...")
try:
    from comunidadeimpressionadora import routes
    print("Rotas importadas com sucesso")
except Exception as e:
    print(f"Erro ao importar rotas: {e}")

print("Aplicação inicializada")
