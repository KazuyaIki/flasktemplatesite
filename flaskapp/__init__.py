from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flaskapp.admin import MyAdminIndexView


db = SQLAlchemy()
migrate = Migrate()
admin = Admin()


login_manager = LoginManager()
login_manager.login_view = 'main.login'

basedir = os.path.abspath(os.path.dirname(__name__))



def create_app():
    	
	app = Flask(__name__)
	
	from flaskapp.views import main, applications
	app.register_blueprint(applications)
	app.register_blueprint(main)
	
	admin.init_app(app, index_view=MyAdminIndexView())
	from flaskapp.models import User, Registration, Product, Cart
	admin.add_view(ModelView(User, db.session))
	admin.add_view(ModelView(Registration, db.session))
	admin.add_view(ModelView(Product, db.session))
	admin.add_view(ModelView(Cart, db.session))

	app.config['SECRET_KEY'] = 'secretkey'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	db.init_app(app)
	migrate.init_app(app, db)
	login_manager.init_app(app)
	

	return app
