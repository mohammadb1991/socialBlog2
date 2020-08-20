from django import forms

class UserLoginFrom(forms.Form):
    username=forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    password=forms.CharField(max_length=40,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))


class UserRegisteritionForm(forms.Form):
    username=forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    email=forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}))
    password = forms.CharField(max_length=40, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))