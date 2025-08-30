import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '29cecf8afd6176f06bb3f55472d490d1')
app.config['DEBUG'] = False 
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    print("Usando DATABASE_URL do ambiente")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
    print("Usando SQLite local")

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

print("Importando rotas...")
try:
    from comunidadeimpressionadora import routes
    print("Rotas importadas com sucesso")
except Exception as e:
    print(f"Erro ao importar rotas: {e}")

print("Aplicação inicializada")
