from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, AnyOf


class LoginAuthencation(FlaskForm):
    username = StringField(
        'username',
        validators=[
            DataRequired(message="Silahkan isi username"),
            Length(min=4, message="Username minimal 4 karakter")
        ],
        render_kw={"placeholder": "username"}
    )

    password = PasswordField(
        'password',
        validators=(
            DataRequired(message='Silahkan isi password'),
            Length(min=4, message='Password minimal 4 karakter')
        ),
        render_kw={"placeholder": "password"}
    )
