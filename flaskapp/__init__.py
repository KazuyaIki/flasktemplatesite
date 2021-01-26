from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flaskapp.admin import MyAdminIndexView
from .config.settings import DevelopmentConfig


db = SQLAlchemy()
migrate = Migrate()
admin = Admin()

login_manager = LoginManager()
login_manager.login_view = 'main.login'

basedir = os.path.abspath(os.path.dirname(__name__))

config_class = {'development':DevelopmentConfig}


def create_app():
    	
	app = Flask(__name__)
	
	from flaskapp.views import main, KazuyaIki, template_user, guestuser, guest2
	app.register_blueprint(main)
	app.register_blueprint(KazuyaIki)
	app.register_blueprint(template_user)
	app.register_blueprint(guestuser)
	app.register_blueprint(guest2)
	
	admin.init_app(app, index_view=MyAdminIndexView())
	from flaskapp.models import Users
	admin.add_view(ModelView(Users, db.session))
	
	config_setting = config_class[os.getenv('ENVIRONMENT', 'development')]
	app.config.from_object(config_setting)
	# app.config['SECRET_KEY'] = 'secretkey'
	# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
	# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


	db.init_app(app)
	migrate.init_app(app, db)
	
	login_manager.init_app(app)
	

	return app
