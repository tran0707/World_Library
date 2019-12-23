from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from worldlibrary.models import User
from datetime import date


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RentForm(FlaskForm):

    startDate =DateField (
        label = 'Start date',
        # format='%m/%d/%Y',
        validators = [DataRequired()],
        # description = 'please select return date as form mm/dd/yyyy'
    )
    endDate =DateField (
        label = 'End date',
        # format='%m/%d/%Y',
        validators = [DataRequired()],
        # description = 'please select return date as form mm-dd-yyyy'
    )
    def validate_on_submit(self):
            result = super(RentForm, self).validate()
            re = False
            if (self.startDate.data and self.endDate.data):
                re = True
                if (self.startDate.data < date.today()):
                    self.startDate.errors.append("Start time should equal or greater than today date",)
                    re = False
                if ((self.startDate.data>= self.endDate.data) or (self.endDate.data< date.today())):
                    self.endDate.errors.append("End time should greater than start time and today date")
                    re = False 
            return re
    submit = SubmitField('Rent Now')

