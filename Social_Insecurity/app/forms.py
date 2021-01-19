from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FormField, TextAreaField, FileField, validators
from flask_wtf.file import FileAllowed, FileRequired
from flask_login import current_user
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from app import query_db, get_db, login
from werkzeug.security import generate_password_hash, check_password_hash

# defines all forms in the application, these will be instantiated by the template,
# and the routes.py will read the values of the fields

class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={'placeholder': 'Username'}, validators=[DataRequired()])
    password = PasswordField('Password', render_kw={'placeholder': 'Password'}, validators=[DataRequired()])
    secret_question = PasswordField('Secret Question',render_kw={'placeholder': 'Secret question, favoritt animal?'})
    remember_me = BooleanField('Remember me') # TODO: It would be nice to have this feature implemented, probably by using cookies
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', [validators.Length(min=1, max=25), validators.DataRequired()], render_kw={'placeholder': 'First Name'})
    last_name = StringField('Last Name', [validators.Length(min=1, max=25), validators.DataRequired()], render_kw={'placeholder': 'Last Name'})
    username = StringField('Username',[validators.Length(min=6, max=25), 
        validators.DataRequired(), 
        validators.Regexp('^\w+$', message="Username must contain only letters numbers or underscore")] ,
            render_kw={'placeholder': 'Username'})
    password = PasswordField('Password',[validators.Length(min=8, max=25), validators.DataRequired(), validators.Regexp('^\w+$', message="Username must contain only letters numbers or underscore")] , render_kw={'placeholder': 'Password'})
    confirm_password = PasswordField('Confirm Password',[validators.Length(min=4, max=25), validators.DataRequired(), validators.EqualTo('password', message='Passwords must match.')] ,render_kw={'placeholder': 'Confirm Password'})
    secret_question = StringField("Secret Question", [validators.Length(min=1, max=25), validators.DataRequired()],render_kw={'placeholder': 'The name of your favorite animal'})
    recap = RecaptchaField()
    submit = SubmitField('Sign Up') 

    def validate_username(self, username):
        user = query_db('SELECT * FROM Users WHERE username= ?;',[username.data], one=True)
        if user is not None:
            raise ValueError('Please use a different username')

    def validate_password(self, password):
        upper_count = 0
        letter_count = 0
        numb_count = 0

        for i in password.data:
            if i.isalpha():
                letter_count += 1
            if i.isdigit():
                numb_count += 1
            if i.isupper():
                upper_count += 1

        if numb_count > 2 and upper_count > 0:
            return True
        else:
            raise ValueError('The password must have at least three numbers and one upper case letter')

    def validate_secret_question(self, secret_question):
        for i in secret_question.data:
            if i.isdigit():
                raise ValueError('Your answer can not be a number')
            else:
                return True

class ChangePass(FlaskForm):
    username = StringField('Username',[validators.Length(min=1, max=25), validators.DataRequired()], render_kw={'placeholder': 'Username'})
    password = PasswordField('New Password',[validators.Length(min=1, max=25), validators.DataRequired()], render_kw={'placeholder': 'New Password'})
    confirm_password = PasswordField('Confirm New Password',[validators.Length(min=1, max=25), validators.DataRequired()], render_kw={'placeholder': 'Confirm New Password'})
    secret_question = StringField("Secret question",[validators.Length(min=1, max=25), validators.DataRequired()], render_kw={'placeholder': 'The name of your favorite animal'})
    submit = SubmitField('Change Password')

    def validate_password(self, password):
        upper_count = 0
        letter_count = 0
        numb_count = 0

        for i in password.data:
            if i.isalpha():
                letter_count += 1
            if i.isdigit():
                numb_count += 1
            if i.isupper():
                upper_count += 1

        if numb_count > 2 and upper_count > 0:
            return True
        else:
            raise ValueError('The password must have at least three numbers and one upper case letter')

class IndexForm(FlaskForm):
    login = FormField(LoginForm)
    register = FormField(RegisterForm)
    change_pass = FormField(ChangePass)

class PostForm(FlaskForm):
    content = TextAreaField('New Post', [validators.Regexp('[\w.]+'), validators.Length(min=1, max=140), validators.DataRequired()], render_kw={'placeholder': 'What are you thinking about?'})
    image = FileField('Image', validators =[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], message = 'You can only upload images, (jpg, png, gif or jpeg files)!')])
    submit = SubmitField('Post')



class CommentsForm(FlaskForm):
    comment = TextAreaField('New Comment',[validators.Length(min=1, max=70), validators.DataRequired()] , render_kw={'placeholder': 'What do you have to say?'})
    submit = SubmitField('Comment')

class FriendsForm(FlaskForm):
    username = StringField('Friend\'s username',[validators.Regexp('^\w+$', message="Usernames cant have special characters, accept underscore") , validators.DataRequired()], render_kw={'placeholder': 'Username'})
    submit = SubmitField('Add Friend')

class ProfileForm(FlaskForm):
    education = StringField('Education', [validators.Length(max=25)] ,render_kw={'placeholder': 'Highest education'})
    employment = StringField('Employment', [ validators.Length(max=25)] ,render_kw={'placeholder': 'Current employment'})
    music = StringField('Favorite song', [ validators.Length(max=25)], render_kw={'placeholder': 'Favorite song'})
    movie = StringField('Favorite movie',[ validators.Length(max=25)] ,render_kw={'placeholder': 'Favorite movie'})
    nationality = StringField('Nationality', [validators.Length(max=25)] ,render_kw={'placeholder': 'Your nationality'})
    birthday = DateField('Birthday', [validators.optional()])
    submit = SubmitField('Update Profile')
