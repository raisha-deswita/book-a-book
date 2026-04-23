from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomRegisterForm(UserCreationForm):
    # Tambahkan field email dan wajib diisi!
    email = forms.EmailField(required=True, label="Alamat Email")

    class Meta:
        model = User
        # Kasih tau Django urutan field yang mau ditampilin
        fields = ("username", "email")