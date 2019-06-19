from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import User



# форма редактирования
class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    about_me = TextAreaField('О себе', validators=[Length(min=0, max=300)], id="area")
    submit = SubmitField('Изменить', id='submit')
    
    def __init__(self, original_name, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
        
    def validate_username(self, username):
        if username.data != self.original_name:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("Это имя уже занято, введите другое")
    
    

# форма отправки поста
class PostForm(FlaskForm):
    post = TextAreaField('Напишите о своих мыслях', validators=[
        DataRequired(), Length(min=1, max=300)], id='post_field')
    submit = SubmitField('Опубликовать', id='post_submit')