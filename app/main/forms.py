from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length, Email
from app.models import User
from flask_babel import _
from flask_babel import lazy_gettext as _l



# форма редактирования
class EditProfileForm(FlaskForm):
    username = StringField(_l('Имя пользователя'), validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    about_me = TextAreaField(_l('О себе'), validators=[Length(min=0, max=300)], id="area")
    submit = SubmitField(_l('Изменить'), id='submit')
    
    def __init__(self, original_name, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
        
    def validate_username(self, username):
        if username.data != self.original_name:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_("Это имя уже занято, введите другое"))
        user = User.query.filter_by(email=self.email.data).first()
        if user is not None:
            raise ValidationError(_("Этот e-mail уже занят, используйте другой"))

# форма отправки поста
class PostForm(FlaskForm):
    post = TextAreaField(_l('Напишите о своих мыслях'), validators=[
        DataRequired(), Length(min=1, max=300)], id='post_field')
    submit = SubmitField(_l('Опубликовать'), id='post_submit')