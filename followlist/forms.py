from django import forms

from .models import SimpleUser
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .apps import user_registered
from .models import TypeList, SimpleUser, List, Goal
from django.contrib.auth.hashers import check_password


class CreateCheckListForm(forms.ModelForm):
    type = forms.ModelChoiceField(empty_label=None, queryset=TypeList.objects.all(), label='тип')
    class Meta:
        model = List
        fields = '__all__'
        labels = {'name_list': '', 'is_private': 'только для себя', 'type': 'тип'}
        widgets = {'user': forms.HiddenInput,
                   'original_id': forms.HiddenInput,
                   'name_list': forms.TextInput(attrs={'class': 'name-list-input', 'placeholder': 'название'})}


class CreateGoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = {'name_goal', 'user',}
        labels = {'name_goal': ''}
        widgets = {'user': forms.HiddenInput,
                   'name_goal': forms.TextInput(attrs={'class':'name-list-input', 'placeholder': 'цель'})}

class ChangeEmailUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='email')

    class Meta:
        model = SimpleUser
        fields = ('email',)


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'email', 'class': 'join-input'}), label="")
    username = forms.CharField(help_text=None, widget=forms.TextInput(attrs={'placeholder': 'логин', 'class': 'join-input'}), label="")
    password_first = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'пароль', 'class': 'join-input'}),
                                     help_text=None, label="")
    password_second = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'повторите пароль', 'class': 'join-input'}), label="")

    def clean_password_first(self):
        password_first = self.cleaned_data['password_first']
        try:
            password_validation.validate_password(password_first)
        except forms.ValidationError as error:
            self.add_error('password_first', error)
        return password_first

    def clean(self):
        super().clean()
        password_first = self.cleaned_data['password_first']
        password_second = self.cleaned_data['password_second']
        if password_first and password_second and password_first and password_first != password_second:
            errors = {'password_second': ValidationError('пароли не совпадают', code='password_first_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):

        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password_second'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, isinstance=user)
        return user

    class Meta:
        model = SimpleUser
        help_texts = None
        fields = ('username', 'email', 'password_first', 'password_second')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'логин', 'class': 'join-input'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'пароль', 'class': 'join-input'}))

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = SimpleUser.objects.filter(username=username)

        if user.exists() is True and SimpleUser.objects.get(username=username).is_activated is False:
            raise ValidationError('неподтвержденный пользователь')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise ValidationError('Неправильный логин или пароль')
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


