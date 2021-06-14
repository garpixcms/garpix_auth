from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super(LoginForm, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = User.objects.filter(username=username).first()

        if not user:
            raise forms.ValidationError('User is not found')

        if user and not user.is_active:
            raise forms.ValidationError('User is inactive. You must confirm the registration email address at registration.')

        valid = user.check_password(password)
        if not valid:
            raise forms.ValidationError('Invalid: username / password')
        return valid
