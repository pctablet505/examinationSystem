from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(help_text='Required. Inform a valid email address.')
    birth_date = forms.DateField(widget=forms.SelectDateWidget)
    account_type = forms.ChoiceField(choices=[('teacher', 'teacher'), ('student', 'student')])

    class Meta:
        model = User
        fields = (
        'first_name', 'last_name', 'email', 'birth_date', 'account_type', 'username', 'password1', 'password2')
