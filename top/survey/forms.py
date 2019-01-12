from django import forms
from django.contrib.auth.models import User

from .models import Client, Query, Person


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
    sort_by = forms.ChoiceField(choices=(('-open_query', u'Сначала открытые запросы'),
                                         ('-id', u'От новых к старым'),
                                         ('id', u'От старых к новым'),
                                         ('name', u'По алфавиту')), required=False, initial='-id')


class QuerySortingForm(forms.Form):

    search = forms.CharField(required=False)
    sort_by = forms.ChoiceField(choices=(('-id', u'От новых к старым'),
                                         ('id', u'От старых к новым')), required=False, initial='-id')
    only_open = forms.BooleanField(initial=False, required=False)


class ClientInfoForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ['type', 'sanctions', 'crimea', 'imp']


class QueryForm(forms.ModelForm):

    class Meta:
        model = Query
        fields = ['product_type', 'form_factor', 'type', 'upgrade', 'survey_comments']


class AddClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ['form', 'name', 'inn']


class AddContactForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['last_name', 'first_name', 'father_name', 'phone_number', 'phone_number2', 'email', 'position']


class DeclineForm(forms.Form):

    decline_reason = forms.CharField(widget=forms.Textarea, label=u'Причина отказа', required=True)

class CommentaryForm(forms.Form):

    comments = forms.CharField(widget=forms.Textarea, max_length=400)
