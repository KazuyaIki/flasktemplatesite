from wtforms import Form, IntegerField, StringField, PasswordField, SubmitField, validators, ValidationError, BooleanField, DateField
from wtforms.validators import DataRequired, Email
from flaskapp.models import Users

class LoginForm(Form):
    email = StringField('Email address :', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ',validators=[DataRequired()])
    submit = SubmitField('Login')

class LogoutForm(Form):
    submit = SubmitField('Logout')

class CreateUserForm(Form):
    username = StringField('username: ', validators=[DataRequired()])
    email = StringField('email: ', validators=[DataRequired()])
    password = PasswordField('password: ', validators=[DataRequired()])
    submit = SubmitField('ユーザー作成')

class InvoiceForm(Form):
    invoice_no = StringField('整理番号 :', validators=[DataRequired()], default='00-0000')
    invoice_to = StringField('宛先（御中/様を含めて） :', validators=[DataRequired()])
    date_issued = StringField('請求書発行日 :', validators=[DataRequired()], default='令和　年　月　日')
    date_issued_quotation = StringField('見積書発行日 :', validators=[DataRequired()], default='令和　年　月　日')
    date_issued_delivery = StringField('納品書発行日 :', validators=[DataRequired()], default='令和　年　月　日')
    date_issued_receipt = StringField('領収書発行日 :', validators=[DataRequired()], default='令和　年　月　日')
    p1_name = StringField('品名（備考）_1 :',validators=[DataRequired()])
    p1_quantity = IntegerField('数量 _1 :',validators=[DataRequired()], default=1)
    p1_unit_price = IntegerField('単価（税込）_1 :',validators=[DataRequired()])
    p2_name = StringField('品名（備考）_2 :')
    p2_quantity = IntegerField('数量_2 :', default=0)
    p2_unit_price = IntegerField('単価（税込）_2 :', default=0)
    p3_name = StringField('品名（備考）_3 :')
    p3_quantity = IntegerField('数量_3 :', default=0)
    p3_unit_price = IntegerField('単価（税込）_3 :', default=0)
    p4_name = StringField('品名（備考） _4:')
    p4_quantity = IntegerField('数量_4 :', default=0)
    p4_unit_price = IntegerField('単価（税込） _4 :', default=0)
    p5_name = StringField('品名（備考）_5 :')
    p5_quantity = IntegerField('数量_5 :', default=0)
    p5_unit_price = IntegerField('単価（税込）_5 :', default=0)
    p6_name = StringField('品名（備考）_6 :')
    p6_quantity = IntegerField('数量_6 :', default=0)
    p6_unit_price = IntegerField('単価（税込）_6 :', default=0)

    submit = SubmitField('選択・入力した書類を表示')
