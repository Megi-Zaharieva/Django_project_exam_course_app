from django import forms
from django.contrib.auth.models import User
from teacher_app.models import UserProfileInfo, CreateCourse, Comments, Review
from teacher_app.validators import password_validation, PasswordInfo, UsernameValidator, email_validation, \
    username_validation, search_validator, password_validator, first_name_validator, last_name_validator, \
    FileExtensionValidator, MaxFileSizeValidator, validate_profile_pic, title_validator, description_validator, \
    review_text_validator, user_comments_validator, course_image_url_validator


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(),
                               validators=[password_validation, password_validator],
                               help_text=PasswordInfo().get_help_text())

    username = forms.CharField(help_text=UsernameValidator().get_help_text(),
                               validators=[username_validation])

    email = forms.EmailField(validators=[email_validation])
    first_name = forms.CharField(validators=[first_name_validator], required=False)
    last_name = forms.CharField(validators=[last_name_validator], required=False)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

        for field_name in self.fields:
            field = self.fields[field_name]
            placeholder = field.label if field.label else field_name.capitalize()
            field.widget.attrs['placeholder'] = placeholder
            field.widget.attrs['class'] = 'form-control'
            field.label = ''

    class Meta():
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def as_div(self):
        return self._html_output(
            normal_row='<div class="form__row"><div class="form__controls">%(label)s%(field)s%(help_text)s</div></div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html='<p class="form__row--help-text">%s</p>',
            errors_on_separate_row=True,)


class UserProfileInfoForm(forms.ModelForm):
    profile_pic = forms.ImageField(validators=[validate_profile_pic], required=False)

    def __init__(self, *args, **kwargs):
        super(UserProfileInfoForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''

        for field_name in self.fields:
            field = self.fields[field_name]
            placeholder = field.label if field.label else field_name.capitalize()
            field.widget.attrs['placeholder'] = placeholder
            field.widget.attrs['class'] = 'form-control'
            field.label = False

        if 'type' in self.fields:
            self.fields['type'].choices = UserProfileInfo.CHOICES
            self.fields['type'].choices.insert(0, ('', 'Select a role'))
            self.fields['type'].initial = ''

    def as_div(self):
         return self._html_output(
            normal_row='<div class="form__row"><div class="form__controls">%(label)s%(field)s%(help_text)s</div></div>',
            error_row='%s',
            row_ender='</div>',
            help_text_html='<p class="form__row--help-text">%s</p>',
            errors_on_separate_row=True,
        )

    class Meta():
        model = UserProfileInfo
        fields = ['profile_pic', 'type']


class StudentProfileInfoForm(forms.ModelForm):
    profile_pic = forms.ImageField(validators=[validate_profile_pic], required=False)
    class Meta():
        model = UserProfileInfo
        fields = ['profile_pic', 'type']
        widgets = {
            'type': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class ProfileDetailsTeacherForm(forms.ModelForm):
    profile_pic = forms.ImageField(validators=[validate_profile_pic], required=False)
    file = forms.FileField(validators=[FileExtensionValidator(), MaxFileSizeValidator(5 * 1024 * 1024)], required=False)
    description = forms.CharField(validators=[description_validator], required=False)
    class Meta:
        model = UserProfileInfo
        fields = ['profile_pic', 'description', 'type', 'file']
        widgets = {
            'type': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class AddCourseForm(forms.ModelForm):
    description = forms.CharField(validators=[description_validator], required=False)
    title = forms.CharField(validators=[title_validator], required=True)
    course_image_url = forms.CharField(validators=[course_image_url_validator], required=False)
    class Meta:
        model = CreateCourse
        fields = ['title', 'video_url', 'course_image_url', 'date', 'type', 'description']
        date = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y'))


class CommentsForm(forms.ModelForm):
    user_comments = forms.CharField(validators=[user_comments_validator])
    class Meta:
        model = Comments
        fields = ['user_comments']


class ReviewForm(forms.ModelForm):
    review_text = forms.CharField(validators=[review_text_validator], required=False)
    class Meta:
        model = Review
        fields = ['review_text', 'rating']


class SearchForm(forms.Form):
    search_text = forms.CharField(label='Search', max_length=255, validators=[search_validator])


