from flaskapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Users.query.get(id)

class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, unique=False, default=False)
    url_prefix = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.String, nullable=False)

    def __init__(self, username, email, password, url_prefix, created_at):
        self.username = username
        self.email = email
        self.password = password
        self.url_prefix = url_prefix
        self.created_at = created_at

    @classmethod
    def select_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def select_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def select_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def select_user_by_password(cls, password):
        return cls.query.filter_by(password=password).first()
    
    @classmethod
    def select_user_by_url_prefix(cls, url_prefix):
        return cls.query.filter_by(url_prefix=url_prefix).first()

    def create_new_user(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

