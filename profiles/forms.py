from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import UserProfile


# Форма реєстрації
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Перевірка на співпадіння паролів
        if password != confirm_password:
            raise ValidationError("Паролі не співпадають.")

        # Перевірка унікальності імені користувача та email
        if User.objects.filter(username=cleaned_data.get("username")).exists():
            raise ValidationError("Це ім'я користувача вже зайняте.")

        if User.objects.filter(email=cleaned_data.get("email")).exists():
            raise ValidationError("Ця електронна пошта вже зареєстрована.")

        return cleaned_data


# Форма редагування профілю
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'birth_date', 'location']


# Форма зміни паролю
class PasswordChangeFormCustom(PasswordChangeForm):
    confirm_new_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password1")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        # Перевірка на співпадіння нового паролю з підтвердженням
        if new_password != confirm_new_password:
            raise ValidationError("Нова пароль не співпадає з підтвердженням.")

        return cleaned_data


