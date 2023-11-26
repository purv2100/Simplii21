#
# Copyright 2023 Simplii from Group74 NCSU CSC510
#
# Licensed under the MIT/X11 License (http://opensource.org/licenses/MIT)
#

from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TimeField, ValidationError, SelectMultipleField, SelectField
# from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from apps import App

def end_time_after_start_time(form, field):
    start_time = form.start_time.data
    end_time = field.data

    if start_time and end_time:
        if start_time >= end_time:
            raise ValidationError("End time must be after the start time.")
            
def get_friends(session_email):
    app_object = App()
    mongo = app_object.mongo
    friends = mongo.db.friends.find({'sender': session_email}, {'receiver', 'accept'})
    friend_list = [("Please Select", "Please Select")]
    for friend in friends:
        if friend['accept']:
            friend_list.append((friend['receiver'], friend['receiver']))
    return friend_list


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        app_object = App()
        mongo = app_object.mongo

        temp = mongo.db.ath.find_one({'email': email.data}, {'email', 'pwd'})
        if temp:
            raise ValidationError('Email already exists!')


class TaskForm(FlaskForm):

    taskname = StringField('Task Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    category = SelectField('Category',
                           choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")])
    invitees = SelectMultipleField('Invitees')
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired(), end_time_after_start_time])
    description = StringField('Description',
                           validators=[DataRequired(), Length(min=2, max=500)])
    submit = SubmitField('Add Task')

    def __init__(self,session_email, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.invitees.choices = get_friends(session_email)


class UpdateForm(FlaskForm):
    taskname = StringField('Taskname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    category = SelectField('Category',
                           choices=[('physical', "physical"), ("intellectual", "intellectual")])
    startdate = DateField('Start Date', format='%Y-%m-%d')
    duedate = DateField('End Date', format='%Y-%m-%d')
    status = SelectField(
        'Status', choices=[
            ('In Progress', "In Progress"), ("Done", "Done"), ("Blocked", "Blocked")])
    hours = StringField('Hours',
                        validators=[DataRequired(), Length(min=1, max=20)])
    description = StringField('Description',
                           validators=[DataRequired(), Length(min=2, max=500)])
    submit = SubmitField('Update')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostingForm(FlaskForm):
    """name = StringField('Your Name: ',
                           validators=[DataRequired(), Length(min=2, max=20)])
    """
    designation = StringField(
        'Job Designation: ', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    job_title = StringField('Job Title: ',
                            validators=[DataRequired()])
    job_location = StringField('Job Location: ',
                               validators=[DataRequired()])
    job_description = StringField('Job Description: ',
                                  validators=[DataRequired()])
    skills = StringField('Skills Required: ',
                         validators=[DataRequired()])
    schedule = StringField('Schedule of the job (in hours): ',
                           validators=[DataRequired()])
    salary = StringField('Salary: ',
                         validators=[DataRequired(), Length(min=2, max=20)])
    rewards = StringField('Rewards / Benefits: ',
                          validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('POST')


class ApplyForm(FlaskForm):
    apply_name = StringField(
        'Name: ', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    apply_phone = StringField(
        'Phone Number: ', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    apply_address = StringField('Address: ',
                                validators=[DataRequired()])
    dob = StringField('Date of Birth: ',
                      validators=[DataRequired(), Length(min=2, max=20)])
    """position = StringField('Job Position applying for: ',
                           validators=[DataRequired(), Length(min=2, max=100)])
    """
    skills = StringField('Your Skills: ',
                         validators=[DataRequired()])
    availability = StringField('Availability (hours per day in a week): ',
                               validators=[DataRequired()])
    """resume = StringField('Upload Resume: *****',
                           validators=[DataRequired(), Length(min=2, max=50)])
    """
    signature = StringField('Signature (Full Name): ',
                            validators=[DataRequired(), Length(min=2, max=20)])
    schedule = StringField('Schedule: ',
                           validators=[DataRequired()])
    submit = SubmitField('APPLY')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')
