# events/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # カスタムUserモデルをインポート


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # カスタムUserモデルを指定
        fields = ("email", "name", "password1", "password2")
