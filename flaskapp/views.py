from flask import Blueprint
from flask import render_template, url_for, request, redirect, flash, jsonify
from flaskapp import db
from .forms import RegistrationForm, SetPasswordForm, LoginForm, LogoutForm, WordCloudForm, JanomeForm, TweetSearchForm, SeleniumBsForm, AddcartForm, AddProductForm, ProductEditForm
from .models import Registration, User, Product, Cart
from datetime import datetime, timedelta
from uuid import uuid4
from flaskapp.send_email import send_email
from flask_login import login_user, login_required, logout_user, current_user
from flaskapp.applications.wordcloud import word_cloud
from flaskapp.applications.janome import jano_me
from flaskapp.applications.tweepy import tweet_search
from flaskapp.applications.selenium_bs import seleniumbs, seleniumbs_plt
from flask import send_file
import os
import numpy as np


main = Blueprint('main', __name__, url_prefix='')
applications = Blueprint('applications', __name__, url_prefix='/applications')

random_decimal = np.random.rand()

@main.route('/update_decimal', methods=['POST'])
def updatedecimal():
    random_decimal = np.random.rand()
    return jsonify('', render_template('main/random_decimal_model.html', x=random_decimal))

@main.route('/')
def home():
    return render_template('main/home.html', x=random_decimal)

@applications.route('/lists')
def lists():
    return render_template('applications/lists.html')

@main.route('/registration', methods=['GET', 'POST'])
def registration():
    logout_user()
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            new_record = Registration(username=form.username.data, email=form.email.data)
            new_record.token = str(uuid4())
            new_record.created_at = datetime.now()
            new_record.valid_until = datetime.now() + timedelta(days=1)
            url = f"setpassword/{form.username.data}/{new_record.token}"
            if User.select_user_by_username(new_record.username):
                flash('The username is already taken', 'danger')
            elif User.select_user_by_email(new_record.email):
                flash('The email is already registered', 'danger')
            else:
                new_record.create_new_record()
                flash('Check your email and set your password, please', 'success')

                send_email(new_record.email, url)
            return redirect(url_for('main.home'))
        except:
            flash('no internet connection')
            return redirect(url_for('main.registration'))
    return render_template('main/registration.html', form=form)

@main.route('/setpassword/<string:username>/<string:token>', methods=['GET', 'POST'])
def setpassword(username, token):
    logout_user()
    form = SetPasswordForm(request.form)
    user = Registration.select_user_by_username(username)
    email = user.email
    valid_until = user.valid_until
    if request.method == 'POST' and form.validate():
        if valid_until > datetime.now():
            if User.select_user_by_password(form.password.data):
                flash('the password is not available', 'danger')
            else:
                new_user = User(username, email, form.password.data)
                new_user.is_active = True
                new_user.created_at = datetime.now()
                new_user.updated_at = datetime.now()
                new_user.create_new_user()
                user.is_registered = True ###これが働かない
                flash('please login with your username and password', 'primary')
                return redirect(url_for('main.login'))
        else:
            flash('overtime, register again', 'danger')
            return redirect(url_for('main.registration'))
    return render_template('main/setpassword.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        user = User.select_user_by_email(email)
        if user:
            if user.password == password:
                login_user(user, remember=True)
                next = request.args.get('next')
                if not next:
                    next = url_for('main.home')
                flash('You logged in successfully', 'success')
                return redirect(next)
            else:
                flash("the password is wrong", 'danger')
        else:
            flash('the email is not registered', 'danger')
    return render_template('main/login.html', form=form)

@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    form = LogoutForm(request.form)
    if request.method == 'POST':
        logout_user()
        flash('You logged out', 'success')
        return redirect(url_for('main.home'))
    return render_template('main/logout.html', form=form)

@applications.route('/wordcloud', methods=['GET', 'POST'])
@login_required
def wordcloud():
    form = WordCloudForm(request.form)
    if request.method == 'POST' and form.validate():
        text = form.text.data
        path = word_cloud(text)
        form.text.data = ''
        return render_template('applications/wordcloud.html', form=form, path=path)
    return render_template('applications/wordcloud.html', form=form)

@applications.route('/download_wordcloud/images/wordcloud/<string:path>')
@login_required
def download_wordcloud(path):
    basedir = os.path.abspath(os.path.dirname(__name__))
    file_abs_path = os.path.join(basedir, f"flaskapp\\static\\images\\wordcloud\\{path}")
    name = file_abs_path[-18:]
    return send_file(file_abs_path, as_attachment=True, attachment_filename=name)


@applications.route('/janome', methods=['GET', 'POST'])
@login_required
def janome():
    form = JanomeForm(request.form)
    if request.method == 'POST' and form.validate():
        pos = form.parts_of_speech.data
        text = form.text.data
        word_dict = jano_me(pos, text)
        letter_counter = int(len(text))
        sum_of_words = 0
        for _, v in word_dict:
            sum_of_words += int(v)
        return render_template('applications/janome.html', form=form, word_dict=word_dict, pos=pos, sum_of_words=sum_of_words, letter_counter=letter_counter)
    return render_template('applications/janome.html', form=form)

@applications.route('/tweetsearch', methods=['GET', 'POST'])
@login_required
def tweetsearch():
    form = TweetSearchForm(request.form)
    if request.method == 'POST' and form.validate():
        k = [form.keyword_1.data, form.keyword_2.data, form.keyword_3.data, form.keyword_4.data, form.keyword_5.data]
        keywords = [i + ' -RT' for i in k if i]
        count = form.count.data
        tweet_list = tweet_search(keywords, count)
        return render_template('applications/tweetsearch.html', form=form, tweet_list=tweet_list)
    return render_template('applications/tweetsearch.html', form=form)

@applications.route('/selenium_bs', methods=['GET', 'POST'])
@login_required
def selenium_bs():
    form = SeleniumBsForm(request.form)
    if request.method == 'POST' and form.validate():
        keywords = form.keywords.data
        car_list = seleniumbs(keywords)
        time = seleniumbs_plt(car_list)
        filename = f'images/selenium_bs/{time}.jpeg'
        return render_template('applications/selenium_bs.html', form=form, car_list=car_list, filename=filename)
    return render_template('applications/selenium_bs.html', form=form)


@applications.route('/store_manage', methods=['GET', 'POST'])
@login_required
def storemanage():
    form = AddProductForm(request.form)
    products = Product.query.all()
    if request.method == 'POST' and form.validate():
        product_name = form.product_name.data
        price = form.price.data
        stock = form.stock.data
        comment = form.comment.data
        image_path = form.image_path.data
        new_product = Product(product_name, price, stock, comment, image_path)
        if not Product.select_product_by_name(product_name):
            new_product.add_new_product()
            return redirect(url_for('applications.storemanage',form= form, products=products))
    return render_template('applications/store_manage.html', form= form, products=products)

@applications.route('/product_edit/<string:product_name>', methods=['GET', 'POST'])
@login_required
def product_edit(product_name):
    form = ProductEditForm(request.form)
    product = Product.select_product_by_name(product_name)
    id = product.id
    if request.method == 'POST' and form.validate():
        editted_product_name = form.product_name.data
        editted_price = form.price.data
        editted_stock = form.stock.data
        editted_comment = form.comment.data
        editted_image_path = form.image_path.data
        if editted_product_name == product_name:
            Product.product_update(id, editted_product_name, editted_price, editted_stock, editted_comment, editted_image_path)
        elif Product.select_product_by_name(product_name=editted_product_name):
            flash(f'{editted_product_name} already exists. Please check list again', 'danger')
        else:
            Product.product_update(id, editted_product_name, editted_price, editted_stock, editted_comment, editted_image_path)
        return redirect(url_for('applications.storemanage'))
    return render_template('applications/product_edit.html', form= form, product_name=product_name, product=product)


@applications.route('/product_delete/<string:product_name>', methods=['GET', 'POST'])
@login_required
def productdelete(product_name):
    product = Product.select_product_by_name(product_name)
    id = product.id
    Product.product_delete(id)
    return redirect(url_for('applications.storemanage'))


@applications.route('/store', methods=['GET'])
@login_required
def store():
    form = AddcartForm(request.form)
    products = Product.query.all()
    # if request.method == 'POST' and form.validate():
    #     product_id = form.product_id.data
    #     addcart_product = Product.select_product_by_id(id=product_id)
    #     product_info = f'{addcart_product.product_name}({addcart_product.price}) is added in your cart'
    #     return render_template('applications/store.html', products=products, form=form, product_info=product_info)
    if request.args.get('addcart_id',''):
        product_id = request.args.get('addcart_id', '')
        addcart_product = Product.select_product_by_id(id=product_id)
        added_at = datetime.now()
        new_cart = Cart(current_user.id, product_id, added_at)
        new_cart.adding_cart()
    return render_template('applications/store.html', products=products, form=form)

@applications.route('my_cart/<string:user_name>', methods=['GET', 'POST'])
@login_required
def my_cart(user_name):
    if request.args.get('deletecart_id', ''):
        delete_cart_id = request.args.get('deletecart_id')
        delete_item = Cart.query.get(delete_cart_id)
        delete_item.delete_from_cart()
    customer = User.select_user_by_username(user_name)
    customer_id = customer.id
    items_in_cart = Cart.select_items_in_cart(customer_id)
    cart_ids = [i.id for i in items_in_cart]
    items_id = [i.product_id for i in items_in_cart]
    items =[]
    for i, j in zip(items_id, cart_ids):
        item = {}
        item['image_path'] = Product.query.get(i).image_path
        item['product_name'] = Product.query.get(i).product_name
        item['price'] = Product.query.get(i).price
        item['added_at'] = f'{Cart.query.get(j).added_at:%Y-%m-%d-%H:%M:%S}'
        item['cart_id'] = j
        items.append(item)
        print(item['added_at'])
    
    return render_template('applications/my_cart.html', items=items)



