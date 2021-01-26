from flask import Blueprint, session
from flask import render_template, url_for, request, redirect, flash, make_response
import pdfkit
from flaskapp import db
from .forms import LoginForm, LogoutForm, InvoiceForm, CreateUserForm
from .models import Users
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user
import os
from base64 import b64encode
from uuid import uuid4


main = Blueprint('main', __name__, url_prefix='')
KazuyaIki = Blueprint('KazuyaIki', __name__, url_prefix='/0123456789')
template_user = Blueprint('template_user', __name__, url_prefix='/template_template_template')
guestuser = Blueprint('guestuser', __name__, url_prefix='/d6e5c00c-056c-4bcb-8dc7-c8413518eecb')
guest2 = Blueprint('guest2', __name__, url_prefix='/4485d2f6-29dd-41fb-980c-c5d1bb29e38a')



@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        user = Users.select_user_by_email(email)
        if user:
            username = user.username
            if user.password == password:
                login_user(user, remember=True)
                flash('You logged in successfully', 'success')
                return redirect(url_for(f'{username}.invoice_input'))
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
        return redirect(url_for('main.login'))
    return render_template('main/logout.html', form=form)

@main.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    form = CreateUserForm(request.form)
    if current_user.is_admin:
        if request.method == 'POST' and form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            url_prefix = str(uuid4())
            created_at = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            new_user = Users(username, email, password, url_prefix, created_at)
            new_user.create_new_user()
            flash('NEW USER CREATED')
            return render_template('main/update_program.html', username=username, url_prefix=url_prefix)
        return render_template('main/create_user.html', form=form)
    return redirect(url_for('login'))

@main.route('/invoice_input', methods=['GET', 'POST'])
@login_required
def invoice_input():
    user_id = current_user.get_id()
    user = Users.select_user_by_id(user_id)
    username = user.username
    form = InvoiceForm(request.form)
    if request.method == 'POST' and form.validate():
        session['invoice_to'] = form.invoice_to.data
        session['invoice_no'] = form.invoice_no.data
        session['date_issued'] =form.date_issued.data
        session['date_issued_quotation'] =form.date_issued_quotation.data
        session['date_issued_delivery'] =form.date_issued_delivery.data
        session['date_issued_receipt'] =form.date_issued_receipt.data
        session['p1_name'] = form.p1_name.data
        session['p1_quantity'] = int(form.p1_quantity.data)
        session['p1_unit_price'] = int(form.p1_unit_price.data)
        session['p2_name'] = form.p2_name.data
        session['p2_quantity'] = int(form.p2_quantity.data)
        session['p2_unit_price'] = int(form.p2_unit_price.data)
        session['p3_name'] = form.p3_name.data
        session['p3_quantity'] = int(form.p3_quantity.data)
        session['p3_unit_price'] = int(form.p3_unit_price.data)
        session['p4_name'] = form.p4_name.data
        session['p4_quantity'] = int(form.p4_quantity.data)
        session['p4_unit_price'] = int(form.p4_unit_price.data)
        session['p5_name'] = form.p5_name.data
        session['p5_quantity'] = int(form.p5_quantity.data)
        session['p5_unit_price'] = int(form.p5_unit_price.data)
        session['p6_name'] = form.p6_name.data
        session['p6_quantity'] = int(form.p6_quantity.data)
        session['p6_unit_price'] = int(form.p6_unit_price.data)
        session['p1_total_price'] = session['p1_unit_price'] * session['p1_quantity']
        session['p2_total_price'] = session['p2_unit_price'] * session['p2_quantity']
        session['p3_total_price'] = session['p3_unit_price'] * session['p3_quantity']
        session['p4_total_price'] = session['p4_unit_price'] * session['p4_quantity']
        session['p5_total_price'] = session['p5_unit_price'] * session['p5_quantity']
        session['p6_total_price'] = session['p6_unit_price'] * session['p6_quantity']
        session['total_price'] = session['p1_total_price'] + session['p2_total_price'] + session['p3_total_price'] + session['p4_total_price'] + session['p5_total_price'] + session['p6_total_price']
        today = datetime.today()
        timestamp = str( f'{today:%y%m%d}')
        session['quo'] = request.form.get('quotation', '')
        session['deli'] = request.form.get('delivery', '')
        session['inv'] = request.form.get('invoice', '')
        session['rec'] = request.form.get('receipt', '')
        return render_template(f'{username}/invoice_template.html', timestamp=timestamp)
    return render_template('main/input_invoice.html', form=form)

@main.app_errorhandler(404)
def page_not_found(e):
    flash('Redirected for Login Page', 'primary')
    return redirect(url_for('main.login'))

@main.route('/pdf/invoice/<timestamp>')
@login_required
def invoice_writer(timestamp):
    url = request.path
    basedir = os.path.abspath(os.path.dirname(__name__))
    user_id = current_user.get_id()
    user = Users.select_user_by_id(user_id)
    user_name = user.username
    stamp_path = os.path.join(basedir, f"flaskapp/static/{username}/stamp.png")
    # stamp_path_b64 = os.path.join(basedir, "flaskapp/static/{username}/stamp_b64.txt")
    with open(stamp_path, 'rb') as f:
        img_b = f.read()
    img_b64 = b64encode(img_b)
    img_b64_str = img_b64.decode()
    rendered = render_template(f'{username}/invoice_template.html', url=url, img_b64_str=img_b64_str)
    config = pdfkit.configuration(wkhtmltopdf='wkhtmltopdf.exe')
    options = {'enable-local-file-access': None}
    pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    return response

@KazuyaIki.route('/invoice_input', methods=['GET', 'POST'])
@login_required
def invoice_input():
    user_id = current_user.get_id()
    user = Users.select_user_by_id(user_id)
    username = user.username
    url_prefix = user.url_prefix
    form = InvoiceForm(request.form)
    if request.method == 'POST' and form.validate():
        session['invoice_to'] = form.invoice_to.data
        session['invoice_no'] = form.invoice_no.data
        session['date_issued'] =form.date_issued.data
        session['date_issued_quotation'] =form.date_issued_quotation.data
        session['date_issued_delivery'] =form.date_issued_delivery.data
        session['date_issued_receipt'] =form.date_issued_receipt.data
        session['p1_name'] = form.p1_name.data
        session['p1_quantity'] = int(form.p1_quantity.data)
        session['p1_unit_price'] = int(form.p1_unit_price.data)
        session['p2_name'] = form.p2_name.data
        session['p2_quantity'] = int(form.p2_quantity.data)
        session['p2_unit_price'] = int(form.p2_unit_price.data)
        session['p3_name'] = form.p3_name.data
        session['p3_quantity'] = int(form.p3_quantity.data)
        session['p3_unit_price'] = int(form.p3_unit_price.data)
        session['p4_name'] = form.p4_name.data
        session['p4_quantity'] = int(form.p4_quantity.data)
        session['p4_unit_price'] = int(form.p4_unit_price.data)
        session['p5_name'] = form.p5_name.data
        session['p5_quantity'] = int(form.p5_quantity.data)
        session['p5_unit_price'] = int(form.p5_unit_price.data)
        session['p6_name'] = form.p6_name.data
        session['p6_quantity'] = int(form.p6_quantity.data)
        session['p6_unit_price'] = int(form.p6_unit_price.data)
        session['p1_total_price'] = session['p1_unit_price'] * session['p1_quantity']
        session['p2_total_price'] = session['p2_unit_price'] * session['p2_quantity']
        session['p3_total_price'] = session['p3_unit_price'] * session['p3_quantity']
        session['p4_total_price'] = session['p4_unit_price'] * session['p4_quantity']
        session['p5_total_price'] = session['p5_unit_price'] * session['p5_quantity']
        session['p6_total_price'] = session['p6_unit_price'] * session['p6_quantity']
        session['total_price'] = session['p1_total_price'] + session['p2_total_price'] + session['p3_total_price'] + session['p4_total_price'] + session['p5_total_price'] + session['p6_total_price']
        today = datetime.today()
        timestamp = str( f'{today:%y%m%d}')
        session['quo'] = request.form.get('quotation', '')
        session['deli'] = request.form.get('delivery', '')
        session['inv'] = request.form.get('invoice', '')
        session['rec'] = request.form.get('receipt', '')
        return render_template(f'{username}/invoice_template.html', timestamp=timestamp, url_prefix=url_prefix)
    return render_template('main/input_invoice.html', form=form, username=username)

@KazuyaIki.route('/pdf/<timestamp>')
@login_required
def invoice_writer(timestamp):
    url = request.path
    basedir = os.path.abspath(os.path.dirname(__name__))
    user_id = current_user.get_id()
    user = Users.select_user_by_id(user_id)
    username = user.username
    stamp_path = os.path.join(basedir, f"flaskapp/static/{username}/stamp.png")
    # stamp_path_b64 = os.path.join(basedir, "flaskapp/static/{username}/stamp_b64.txt")
    with open(stamp_path, 'rb') as f:
        img_b = f.read()
    img_b64 = b64encode(img_b)
    img_b64_str = img_b64.decode()
    rendered = render_template(f'{username}/invoice_template.html', url=url, img_b64_str=img_b64_str)
    config = pdfkit.configuration(wkhtmltopdf='wkhtmltopdf.exe')
    options = {'enable-local-file-access': None}
    pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    return response

@template_user.route('/invoice_input', methods=['GET', 'POST'])
@login_required
def invoice_input():
    user_id = current_user.get_id()
    user = Users.select_user_by_id(user_id)
    username = user.username
    url_prefix = user.url_prefix
    form = InvoiceForm(request.form)
    if request.method == 'POST' and form.validate():
        session['invoice_to'] = form.invoice_to.data
        session['invoice_no'] = form.invoice_no.data
        session['date_issued'] =form.date_issued.data
        session['date_issued_quotation'] =form.date_issued_quotation.data
        session['date_issued_delivery'] =form.date_issued_delivery.data
        session['date_issued_receipt'] =form.date_issued_receipt.data
        session['p1_name'] = form.p1_name.data
        session['p1_quantity'] = int(form.p1_quantity.data)
        session['p1_unit_price'] = int(form.p1_unit_price.data)
        session['p2_name'] = form.p2_name.data
        session['p2_quantity'] = int(form.p2_quantity.data)
        session['p2_unit_price'] = int(form.p2_unit_price.data)
        session['p3_name'] = form.p3_name.data
        session['p3_quantity'] = int(form.p3_quantity.data)
        session['p3_unit_price'] = int(form.p3_unit_price.data)
        session['p4_name'] = form.p4_name.data
        session['p4_quantity'] = int(form.p4_quantity.data)
        session['p4_unit_price'] = int(form.p4_unit_price.data)
        session['p5_name'] = form.p5_name.data
        session['p5_quantity'] = int(form.p5_quantity.data)
        session['p5_unit_price'] = int(form.p5_unit_price.data)
        session['p6_name'] = form.p6_name.data
        session['p6_quantity'] = int(form.p6_quantity.data)
        session['p6_unit_price'] = int(form.p6_unit_price.data)
        session['p1_total_price'] = session['p1_unit_price'] * session['p1_quantity']
        session['p2_total_price'] = session['p2_unit_price'] * session['p2_quantity']
        session['p3_total_price'] = session['p3_unit_price'] * session['p3_quantity']
        session['p4_total_price'] = session['p4_unit_price'] * session['p4_quantity']
        session['p5_total_price'] = session['p5_unit_price'] * session['p5_quantity']
        session['p6_total_price'] = session['p6_unit_price'] * session['p6_quantity']
        session['total_price'] = session['p1_total_price'] + session['p2_total_price'] + session['p3_total_price'] + session['p4_total_price'] + session['p5_total_price'] + session['p6_total_price']
        today = datetime.today()
        timestamp = str( f'{today:%y%m%d}')
        session['quo'] = request.form.get('quotation', '')
        session['deli'] = request.form.get('delivery', '')
        session['inv'] = request.form.get('invoice', '')
        session['rec'] = request.form.get('receipt', '')
        return render_template(f'{username}/invoice_template.html', timestamp=timestamp, url_prefix=url_prefix)
    return render_template('main/input_invoice.html', form=form, username=username)

@template_user.route('/pdf/<timestamp>')
@login_required
def invoice_writer(timestamp):
    url = request.path
    basedir = os.path.abspath(os.path.dirname(__name__))
    user_id = current_user.get_id()
    user = Users.select_user_by_id(user_id)
    username = user.username
    stamp_path = os.path.join(basedir, f"flaskapp/static/{username}/stamp.png")
    # stamp_path_b64 = os.path.join(basedir, "flaskapp/static/{username}/stamp_b64.txt")
    with open(stamp_path, 'rb') as f:
        img_b = f.read()
    img_b64 = b64encode(img_b)
    img_b64_str = img_b64.decode()
    rendered = render_template(f'{username}/invoice_template.html', url=url, img_b64_str=img_b64_str)
    config = pdfkit.configuration(wkhtmltopdf='wkhtmltopdf.exe')
    options = {'enable-local-file-access': None}
    pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    return response

@guestuser.route('/invoice_input', methods=['GET', 'POST'])
@login_required
def invoice_input():
    user_id = current_user.get_id()
    user = Users.select_user_by_id(user_id)
    username = user.username
    url_prefix = user.url_prefix
    form = InvoiceForm(request.form)
    if request.method == 'POST' and form.validate():
        session['invoice_to'] = form.invoice_to.data
        session['invoice_no'] = form.invoice_no.data
        session['date_issued'] =form.date_issued.data
        session['date_issued_quotation'] =form.date_issued_quotation.data
        session['date_issued_delivery'] =form.date_issued_delivery.data
        session['date_issued_receipt'] =form.date_issued_receipt.data
        session['p1_name'] = form.p1_name.data
        session['p1_quantity'] = int(form.p1_quantity.data)
        session['p1_unit_price'] = int(form.p1_unit_price.data)
        session['p2_name'] = form.p2_name.data
        session['p2_quantity'] = int(form.p2_quantity.data)
        session['p2_unit_price'] = int(form.p2_unit_price.data)
        session['p3_name'] = form.p3_name.data
        session['p3_quantity'] = int(form.p3_quantity.data)
        session['p3_unit_price'] = int(form.p3_unit_price.data)
        session['p4_name'] = form.p4_name.data
        session['p4_quantity'] = int(form.p4_quantity.data)
        session['p4_unit_price'] = int(form.p4_unit_price.data)
        session['p5_name'] = form.p5_name.data
        session['p5_quantity'] = int(form.p5_quantity.data)
        session['p5_unit_price'] = int(form.p5_unit_price.data)
        session['p6_name'] = form.p6_name.data
        session['p6_quantity'] = int(form.p6_quantity.data)
        session['p6_unit_price'] = int(form.p6_unit_price.data)
        session['p1_total_price'] = session['p1_unit_price'] * session['p1_quantity']
        session['p2_total_price'] = session['p2_unit_price'] * session['p2_quantity']
        session['p3_total_price'] = session['p3_unit_price'] * session['p3_quantity']
        session['p4_total_price'] = session['p4_unit_price'] * session['p4_quantity']
        session['p5_total_price'] = session['p5_unit_price'] * session['p5_quantity']
        session['p6_total_price'] = session['p6_unit_price'] * session['p6_quantity']
        session['total_price'] = session['p1_total_price'] + session['p2_total_price'] + session['p3_total_price'] + session['p4_total_price'] + session['p5_total_price'] + session['p6_total_price']
        today = datetime.today()
        timestamp = str( f'{today:%y%m%d}')
        session['quo'] = request.form.get('quotation', '')
        session['deli'] = request.form.get('delivery', '')
        session['inv'] = request.form.get('invoice', '')
        session['rec'] = request.form.get('receipt', '')
        return render_template(f'{username}/invoice_template.html', timestamp=timestamp, url_prefix=url_prefix)
    return render_template('main/input_invoice.html', form=form, username=username)

@guestuser.route('/pdf/<timestamp>')
@login_required
def invoice_writer(timestamp):
    url = request.path
    basedir = os.path.abspath(os.path.dirname(__name__))
    user_id = current_user.get_id()
    user = Users.select_user_by_id(user_id)
    username = user.username
    stamp_path = os.path.join(basedir, f"flaskapp/static/{username}/stamp.png")
    # stamp_path_b64 = os.path.join(basedir, "flaskapp/static/{username}/stamp_b64.txt")
    with open(stamp_path, 'rb') as f:
        img_b = f.read()
    img_b64 = b64encode(img_b)
    img_b64_str = img_b64.decode()
    rendered = render_template(f'{username}/invoice_template.html', url=url, img_b64_str=img_b64_str)
    config = pdfkit.configuration(wkhtmltopdf='wkhtmltopdf.exe')
    options = {'enable-local-file-access': None}
    pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    return response


@guest2.route('/invoice_input', methods=['GET', 'POST'])
@login_required
def invoice_input():
    user_id = current_user.get_id()
    user = Users.select_user_by_id(user_id)
    username = user.username
    url_prefix = user.url_prefix
    form = InvoiceForm(request.form)
    if request.method == 'POST' and form.validate():
        session['invoice_to'] = form.invoice_to.data
        session['invoice_no'] = form.invoice_no.data
        session['date_issued'] =form.date_issued.data
        session['date_issued_quotation'] =form.date_issued_quotation.data
        session['date_issued_delivery'] =form.date_issued_delivery.data
        session['date_issued_receipt'] =form.date_issued_receipt.data
        session['p1_name'] = form.p1_name.data
        session['p1_quantity'] = int(form.p1_quantity.data)
        session['p1_unit_price'] = int(form.p1_unit_price.data)
        session['p2_name'] = form.p2_name.data
        session['p2_quantity'] = int(form.p2_quantity.data)
        session['p2_unit_price'] = int(form.p2_unit_price.data)
        session['p3_name'] = form.p3_name.data
        session['p3_quantity'] = int(form.p3_quantity.data)
        session['p3_unit_price'] = int(form.p3_unit_price.data)
        session['p4_name'] = form.p4_name.data
        session['p4_quantity'] = int(form.p4_quantity.data)
        session['p4_unit_price'] = int(form.p4_unit_price.data)
        session['p5_name'] = form.p5_name.data
        session['p5_quantity'] = int(form.p5_quantity.data)
        session['p5_unit_price'] = int(form.p5_unit_price.data)
        session['p6_name'] = form.p6_name.data
        session['p6_quantity'] = int(form.p6_quantity.data)
        session['p6_unit_price'] = int(form.p6_unit_price.data)
        session['p1_total_price'] = session['p1_unit_price'] * session['p1_quantity']
        session['p2_total_price'] = session['p2_unit_price'] * session['p2_quantity']
        session['p3_total_price'] = session['p3_unit_price'] * session['p3_quantity']
        session['p4_total_price'] = session['p4_unit_price'] * session['p4_quantity']
        session['p5_total_price'] = session['p5_unit_price'] * session['p5_quantity']
        session['p6_total_price'] = session['p6_unit_price'] * session['p6_quantity']
        session['total_price'] = session['p1_total_price'] + session['p2_total_price'] + session['p3_total_price'] + session['p4_total_price'] + session['p5_total_price'] + session['p6_total_price']
        today = datetime.today()
        timestamp = str( f'{today:%y%m%d}')
        session['quo'] = request.form.get('quotation', '')
        session['deli'] = request.form.get('delivery', '')
        session['inv'] = request.form.get('invoice', '')
        session['rec'] = request.form.get('receipt', '')
        return render_template(f'{username}/invoice_template.html', timestamp=timestamp, url_prefix=url_prefix)
    return render_template('main/input_invoice.html', form=form, username=username)

@guest2.route('/pdf/<timestamp>')
@login_required
def invoice_writer(timestamp):
    url = request.path
    basedir = os.path.abspath(os.path.dirname(__name__))
    user_id = current_user.get_id()
    user = Users.select_user_by_id(user_id)
    username = user.username
    stamp_path = os.path.join(basedir, f"flaskapp/static/{username}/stamp.png")
    # stamp_path_b64 = os.path.join(basedir, "flaskapp/static/{username}/stamp_b64.txt")
    with open(stamp_path, 'rb') as f:
        img_b = f.read()
    img_b64 = b64encode(img_b)
    img_b64_str = img_b64.decode()
    rendered = render_template(f'{username}/invoice_template.html', url=url, img_b64_str=img_b64_str)
    config = pdfkit.configuration(wkhtmltopdf='wkhtmltopdf.exe')
    options = {'enable-local-file-access': None}
    pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    return response


