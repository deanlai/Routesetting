from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import User

oneToFive = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
gradeOptions = [('Bonus', 'Bonus'), ('B', 'B'), ('1', '1'), ('2', '2'),
                ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
                ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'),
                ('11', '11'), ('12', '12'), ('13', '13')]
colorOptions = [('Red', 'Red'), ('Orange', 'Orange'), ('Yellow', 'Yellow'),
                ('Green', 'Green'), ('Blue', 'Blue'), ('Purple', 'Purple'),
                ('White', 'White'), ('Black', 'Black'), ('Pink', 'Pink'),
                ('Beige', 'Beige'), ('Brown', 'Brown')],


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class ProblemForm(FlaskForm):
    grade = SelectField(
        u'Grade',
        choices=gradeOptions, validators=[DataRequired()])
    color = SelectField(
        u'Color', choices=colorOptions, validators=[DataRequired()])
    risk = SelectField(
        u'Risk', choices=oneToFive, validators=[DataRequired()])
    intensity = SelectField(
        u'Intensity', choices=oneToFive, validators=[DataRequired()])
    complexity = SelectField(
        u'Complexity', choices=oneToFive, validators=[DataRequired()])
    submit = SubmitField('Submit')
