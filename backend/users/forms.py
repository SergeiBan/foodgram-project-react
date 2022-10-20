from django import forms
from django.contrib.auth import get_user_model


class AdminForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username', 'password', 'email', 'first_name', 'last_name')