from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, TextAreaField,
    URLField, IntegerField, DecimalField, SelectField,
    BooleanField, HiddenField, DateField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, Optional,
    URL, NumberRange, ValidationError
)
from models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please enter a valid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=8, message='Password must be at least 8 characters long.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password.'),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Create Account')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data.lower().strip()).first()
        if user:
            raise ValidationError('An account with this email already exists.')


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please enter a valid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.')
    ])
    submit = SubmitField('Sign In')


class ProfileEditForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required.'),
        Length(max=100)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required.'),
        Length(max=100)
    ])
    photo_url = URLField('Profile Photo URL', validators=[
        Optional(),
        URL(message='Please enter a valid URL for your photo.')
    ])
    personal_message = TextAreaField('Personal Message', validators=[
        Optional(),
        Length(max=1000, message='Personal message must be 1000 characters or fewer.')
    ])
    school_name = StringField('School / University', validators=[
        Optional(),
        Length(max=200)
    ])
    degree = StringField('Degree / Program', validators=[
        Optional(),
        Length(max=200)
    ])
    graduation_date = DateField('Graduation Date', validators=[Optional()])
    is_public = BooleanField('Make my page publicly visible')
    submit = SubmitField('Save Profile')


class PartyDetailsForm(FlaskForm):
    event_title = StringField('Event Title', validators=[
        Optional(),
        Length(max=200)
    ])
    event_date = DateField('Event Date', validators=[Optional()])
    event_time = StringField('Event Time (e.g. 2:00 PM)', validators=[
        Optional(),
        Length(max=50)
    ])
    location_name = StringField('Venue / Location Name', validators=[
        Optional(),
        Length(max=200)
    ])
    location_address = TextAreaField('Full Address', validators=[
        Optional(),
        Length(max=400)
    ])
    rsvp_instructions = TextAreaField('RSVP Instructions', validators=[
        Optional(),
        Length(max=1000)
    ])
    rsvp_deadline = DateField('RSVP Deadline', validators=[Optional()])
    additional_notes = TextAreaField('Additional Notes', validators=[
        Optional(),
        Length(max=2000)
    ])
    submit = SubmitField('Save Party Details')


class RegistryItemForm(FlaskForm):
    title = StringField('Item Name', validators=[
        DataRequired(message='Item name is required.'),
        Length(max=300)
    ])
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=2000)
    ])
    price = DecimalField('Price ($)', validators=[
        Optional(),
        NumberRange(min=0, message='Price must be a positive number.')
    ], places=2)
    quantity_needed = IntegerField('Quantity Needed', validators=[
        Optional(),
        NumberRange(min=1, max=999, message='Quantity must be between 1 and 999.')
    ], default=1)
    external_url = URLField('Product Link (any retailer)', validators=[
        Optional(),
        URL(message='Please enter a valid product URL.')
    ])
    image_url = URLField('Image URL (optional)', validators=[
        Optional(),
        URL(message='Please enter a valid image URL.')
    ])
    category = StringField('Category (optional)', validators=[
        Optional(),
        Length(max=100)
    ])
    priority = SelectField('Priority', choices=[
        ('high', 'High Priority'),
        ('medium', 'Medium Priority'),
        ('low', 'Low Priority')
    ], default='medium')
    submit = SubmitField('Save Item')


class ExternalRegistryForm(FlaskForm):
    name = StringField('Registry Name (e.g. Amazon Registry)', validators=[
        DataRequired(message='Registry name is required.'),
        Length(max=200)
    ])
    url = URLField('Registry URL', validators=[
        DataRequired(message='Registry URL is required.'),
        URL(message='Please enter a valid URL.')
    ])
    description = StringField('Short Description (optional)', validators=[
        Optional(),
        Length(max=400)
    ])
    submit = SubmitField('Add Registry Link')


class MarkPurchasedForm(FlaskForm):
    item_id = HiddenField('Item ID', validators=[DataRequired()])
    purchased_by_note = StringField('Your name (optional, so the graduate can thank you!)', validators=[
        Optional(),
        Length(max=200)
    ])
    submit = SubmitField('Mark as Purchased')


class SearchForm(FlaskForm):
    query = StringField('Search', validators=[
        Optional(),
        Length(max=200)
    ])
    school = StringField('School', validators=[
        Optional(),
        Length(max=200)
    ])
    year = IntegerField('Graduation Year', validators=[
        Optional(),
        NumberRange(min=2000, max=2100)
    ])
    submit = SubmitField('Search')


class AccountSettingsForm(FlaskForm):
    email = StringField('Email Address', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please enter a valid email address.')
    ])
    current_password = PasswordField('Current Password', validators=[
        Optional()
    ])
    new_password = PasswordField('New Password', validators=[
        Optional(),
        Length(min=8, message='New password must be at least 8 characters.')
    ])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        EqualTo('new_password', message='New passwords must match.')
    ])
    submit = SubmitField('Update Account')
