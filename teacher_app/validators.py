from django import forms
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, URLValidator
from django.utils.deconstruct import deconstructible
from django.core.files.uploadedfile import File


class PasswordInfo(MinimumLengthValidator):
    def get_help_text(self):
        return ("Password need to have at least 1 letter, 1 digit, and 1 symbols.")


class UsernameValidator(MinimumLengthValidator):

    def get_help_text(self):
        return ("User name have to be min 3 character")


@deconstructible
class FileExtensionValidator:
    allowed_extensions = ['.doc', '.docx', '.pdf']

    def __call__(self, value):
        if not value.name:
            return
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in self.allowed_extensions:
            allowed_formats = ', '.join(self.allowed_extensions)
            raise ValidationError(f"Only {allowed_formats} files are allowed.")


@deconstructible
class MaxFileSizeValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        if isinstance(value, File) and value.size > self.max_size:
            raise ValidationError(f"File size should not exceed {self.max_size} bytes.")


def validate_profile_pic(value):
    if not value.name.lower().endswith('.jpg') and value != None:
        raise ValidationError('Profile picture must be a JPG image.')


def password_validation(password):
    letter = False
    digit = False
    special_char = False

    symbols = "!@#$%^&*()-_=+{}[]|\;:'\",.<>/?"

    for char in password:
        if char.isalpha():
            letter = True
        elif char.isdigit():
            digit = True
        elif char in symbols:
            special_char = True

    if not (letter and digit and special_char):
        raise ValidationError("Password need to have at least 1 letter, 1 digit, and 1 special character.")


def password_validator(value):
    if len(value) < 10:
        raise ValidationError("Password have to be 10 or more characters.")


def email_validation(email):
    try:
        validate_email(email)
    except ValidationError:
        raise forms.ValidationError("Invalid email format.")


def username_validation(username):
    if username.isdigit() or len(username) < 3:
        raise ValidationError('Username cant be numbers only and have to be 3 or more characters')


def description_validator(value):
    if len(value) < 3:
        raise ValidationError("Description have to be between 3 and 800 characters.")


def review_text_validator(value):
    if len(value) < 3:
        raise ValidationError("Review have to be between 3 and 300 characters.")


def user_comments_validator(value):
    if len(value) < 3:
        raise ValidationError("Comments have to be between 3 and 250 characters.")


def search_validator(value):
    if len(value) < 3:
        raise ValidationError("Search have to be between 3 and 250 characters.")


def title_validator(value):
    if len(value) < 3:
        raise ValidationError("Title have to be between 3 and 255 characters.")


def first_name_validator(value):
    if not value.isalpha():
        raise ValidationError("First name must contain only characters.")
    if len(value) < 3:
        raise ValidationError("First name have to be 3 or more characters.")


def last_name_validator(value):
    if not value.isalpha():
        raise ValidationError("Last name must contain only characters.")
    if len(value) < 3:
        raise ValidationError("Last name have to be 3 or more characters.")


def course_image_url_validator(value):
    url_validator = URLValidator()
    try:
        url_validator(value)
    except ValidationError:
        raise ValidationError('Invalid image URL.')