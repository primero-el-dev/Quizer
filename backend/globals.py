import os
from dotenv import load_dotenv
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

load_dotenv()

server = Flask(__name__, template_folder='../templates', static_folder='../static')
server.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
server.config['SESSION_TYPE'] = 'filesystem'
server.config['SECRET_KEY'] = os.urandom(24)
server.config['SECRET_KEY'] = 'asdff'
server.config['ENV'] = 'development'

db = SQLAlchemy(server, session_options={"autoflush": False})
hasher = Bcrypt(server)
sess = Session(server)
bootstrap = Bootstrap(server)