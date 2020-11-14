from flaskapp import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class Registration(db.Model):
    
    __tablename__ = 'registration'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    token = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime)
    valid_until = db.Column(db.DateTime)
    registered = db.Column(db.Boolean, nullable=False, unique=False, default=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    @classmethod
    def select_user_by_username(cls, name):
        return cls.query.filter_by(username=name).first()

    def create_new_record(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()



class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, unique=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, unique=False, default=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def admin_approval(self):
        self.is_admin = True # okokokokookkokookoko

    @classmethod
    def select_user_by_username(cls, name):
        return cls.query.filter_by(username=name).first()

    @classmethod
    def select_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def select_user_by_password(cls, password):
        return cls.query.filter_by(password=password).first()

    def create_new_user(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

class Product(db.Model):

    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(32), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False, unique=False)
    stock = db.Column(db.Integer, nullable=False, unique=False)
    comment = db.Column(db.String(64), nullable=True)
    image_path = db.Column(db.String(64), nullable=True)

    def __init__(self, product_name, price, stock, comment='', image_path=''):
        self.product_name = product_name
        self.price = price
        self. stock = stock
        self.comment = comment
        self.image_path = image_path

    @classmethod
    def select_product_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def select_product_by_name(cls, product_name):
        return cls.query.filter_by(product_name=product_name).first()

    def add_new_product(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

    @classmethod
    def product_update(cls, id, product_name, price, stock, comment='', image_path=''):
        cls.query.filter_by(id=id).update({'product_name':product_name, 'price':price, 'stock':stock, 'comment':comment, 'image_path':image_path})
        db.session.commit()

    @classmethod
    def product_delete(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()

class Cart(db.Model):

    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    added_at = db.Column(db.DateTime, nullable=False)
    still_in_cart = db.Column(db.Boolean, default=True)

    def __init__(self, customer_id, product_id, added_at):
        self.customer_id = customer_id
        self.product_id = product_id
        self.added_at = added_at

    def adding_cart(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

    @classmethod
    def select_items_in_cart(cls, user_id):
        return cls.query.filter_by(customer_id=user_id).all()

    def delete_from_cart(self):
        with db.session.begin(subtransactions=True):
            db.session.delete(self)
        db.session.commit()




