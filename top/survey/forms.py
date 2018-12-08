from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField( max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Не задано имя пользователя')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('Не указан пароль')
        return password

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Неверное имя пользователя или пароль1')
        if not user.check_password(password):
            raise forms.ValidationError('Неверное имя пользователя или пароль2')


class ClientsSortingForm(forms.Form):

    search = forms.CharField(required=False)
    have_queries_first = forms.BooleanField(initial=True, required=False)
    sort_by = forms.ChoiceField(choices=(('-id', u'От новых к старым'),
                                         ('id', u'От старых к новым'),
                                         ('name', u'По алфавиту')),
                                          required=False, initial='-id')

