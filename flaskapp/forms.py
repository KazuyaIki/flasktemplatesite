from wtforms import Form, IntegerField, StringField, TextAreaField, PasswordField, SubmitField, BooleanField, DateField, HiddenField, RadioField, SelectField, validators, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from flaskapp.models import User, Product

class RegistrationForm(Form):
    username = StringField('User Name :', validators=[DataRequired(), Length(min=6, max=32, message='length must be between 6 to 32')])
    email = StringField('Email :', validators=[DataRequired(), Email('not recognized as email-address')])
    email_confirm = StringField('Email(confirmation): ', validators=[DataRequired(), EqualTo('email', message="Email doesn't match")])
    submit = SubmitField('Register')


class SetPasswordForm(Form):
    password = PasswordField('Password: ', validators=[DataRequired(),Length(min=8, max=32, message='length must be between 8 to 32')])
    password_confirm = PasswordField('Password confirm: ', validators=[DataRequired(), EqualTo('password', message="Password doesn't match")])
    submit = SubmitField('Submit')

class LoginForm(Form):
    email = StringField('Email address :', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ',validators=[DataRequired()])
    submit = SubmitField('Login')

class LogoutForm(Form):
    submit = SubmitField('Logout')

class WordCloudForm(Form):
    text = TextAreaField('Text :', validators=[DataRequired(), Length(min=500, message='the number of letters must be over 500')])
    submit = SubmitField('Show Wordcloud')

class JanomeForm(Form):
    text = TextAreaField('Text :', validators=[DataRequired(), Length(min=500, message='the number of letters must be over 500')])
    parts_of_speech = RadioField('Select a part of speech :', validators=[DataRequired('Please select a part of speech')], choices=[('名詞','Noun'), ('動詞','Verb'), ('形容詞','Adjective'), ('副詞','Adverb')], default='')
    submit = SubmitField('Show Result')

class TweetSearchForm(Form):
    keyword_1 = StringField('Keyword_1 :', validators=[DataRequired(), Length(min=1, max=10)])
    keyword_3 = StringField('Keyword_3 :', validators=[Length(min=0, max=10)], default='')
    keyword_2 = StringField('Keyword_2 :', validators=[Length(min=0, max=10)], default='')
    keyword_4 = StringField('Keyword_4 :', validators=[Length(min=0, max=10)], default='')
    keyword_5 = StringField('Keyword_5 :', validators=[Length(min=0, max=10)], default='')
    count = IntegerField('the number of tweets you need :', validators=[DataRequired(), NumberRange(1,100)])
    submit = SubmitField('Show Tweets')

class SeleniumBsForm(Form):
    keywords = StringField('Keywords :', validators=[DataRequired(), Length(min=1, max=10)])
    submit = SubmitField('Show Result')

class AddcartForm(Form):
    product_id = HiddenField()
    submit = SubmitField('Add Cart')

class AddProductForm(Form):
    product_name = StringField('Product Name :', validators=[DataRequired()])
    price = IntegerField('Price :', validators=[DataRequired()])
    stock = IntegerField('Stock :', validators=[DataRequired()])
    comment = StringField('Comment :')
    image_path = StringField('Image Path :')
    submit = SubmitField('Add New Product')

    def validate_product_name(self, field):
        if Product.select_product_by_name(field.data):
            raise ValidationError('The item is already listed')

class ProductEditForm(Form):
    product_name = StringField('Product Name :', validators=[DataRequired()])
    price = IntegerField('Price :', validators=[DataRequired()])
    stock = IntegerField('Stock :', validators=[DataRequired()])
    comment = StringField('Comment :')
    image_path = StringField('Image Path :')
    submit = SubmitField('Edit Product')
