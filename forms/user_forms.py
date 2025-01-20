from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(message="メールアドレスを入力してください。"),
        Email(message="有効なメールアドレスを入力してください。")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(message="パスワードを入力してください。")
    ])
    password2 = PasswordField("Confirm Password", validators=[
        DataRequired(message="パスワード確認を入力してください。"),
        EqualTo('password', message="パスワードが一致しません。")
    ])
    submit = SubmitField("Login")

class Profile(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(message="ユーザー名を入力してください。"),
        Length(min=3, max=20, message="ユーザー名は3～20文字で入力してください。")
    ])
    email = StringField("Email", validators=[
        DataRequired(message="メールアドレスを入力してください。"),
        Email(message="有効なメールアドレスを入力してください。")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(message="パスワードを入力してください。"),
        Length(min=8, message="パスワードは8文字以上で入力してください。")
    ])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User')], validators=[DataRequired()], default='user')

    submit = SubmitField("Sign Up")
