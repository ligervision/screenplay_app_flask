from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'
# login.login_message = "Hey you can't do that!"
login.login_message_category = 'danger'

from app.blueprints.auth import bp as auth
app.register_blueprint(auth)

from app.blueprints.blog import bp as blog
app.register_blueprint(blog)

from . import routes, models
