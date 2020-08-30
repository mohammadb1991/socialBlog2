from django import forms
from .models import post ,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ('body',)

class AddCommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('body',)
        widgets={
            'body': forms.Textarea(attrs={'class':'form-control'})
        }

        help_texts={
            'body':'max 400 char'
        }


        error_messages = {
            'body':{
                'required': 'این فیلد اجباری است',
            }
        }