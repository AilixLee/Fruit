from django import forms

from index.models import *


class LoginForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['uphone','upwd']
        labels = {
            'uphone':'手机号',
            'upwd':'密码',
        }
        widgets = {
            'uphone':forms.TextInput(
                attrs={
                    'class':'form-control',
                }
            ),
            'upwd':forms.PasswordInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'请6-20位输入密码',
                }
            )
        }