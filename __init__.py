from flask import Flask
from flask import Bcrypt
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)

from app import routes
