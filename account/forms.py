from django import forms
from .models import profilee
message={
'required':'تکمیل این فیلد اجباری می باشد',
'invalid':'لطفا ایمیل معتبر وارد کنید',
'max_length':'کارکتر وارد شده بیشتر از حد مجاز',
'min_length':'کاراکتر وارد شده کمتر از حد مجاز',
}
class UserLoginFrom(forms.Form):
    username=forms.CharField(error_messages=message ,max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    password=forms.CharField(error_messages=message ,max_length=40,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))


class UserRegisteritionForm(forms.Form):
    username=forms.CharField(error_messages=message ,max_length=30, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    email=forms.EmailField(error_messages=message ,max_length=50, widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}))
    password = forms.CharField(error_messages=message , max_length=40, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))



class EditProfileUser(forms.ModelForm):
    email=forms.EmailField()
    fname=forms.CharField(label='first name')
    lname=forms.CharField(label='last name')
    class Meta:
        model=profilee
        fields=('age','bio','phone')

class PhoneLoginForm(forms.Form):
    phone=forms.IntegerField()

    def clean_phone(self):
        phone=profilee.objects.filter(phone=self.cleaned_data['phone'])
        if not phone.exists():
            raise forms.ValidationError('this phone doesnt exist')
        return self.cleaned_data['phone']

class CodeLoginForm(forms.Form):
    code=forms.IntegerField()