from django import forms
from django.forms import ValidationError
from .models import Post, Response
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
# from django.utils.translation import gettext as _


class PostForm(forms.ModelForm):
    post_title = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))
    post_content = forms.CharField(widget=SummernoteWidget())
    
    class Meta:
        model = Post

        fields = [
            'post_title',
            'post_content',
            'post_category',
            # 'author',
        ]
        labels = {
            # 'author': 'Автор',
            'post_category': 'Категория',
        }

        exclude = ('post_author',)

    def clean(self):
        cleaned = super().clean()
        content = cleaned.get('post_content')
        title = cleaned.get('post_title')
        if title == content:
            raise ValidationError('Название и контент не должны быть одинаковыми')
        return cleaned

class ResponseForm(forms.ModelForm):
    response_content = forms.CharField(label='Текст', widget=forms.Textarea(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Ваш текст',
            'rows': 4,
            'cols': 40
        }
    ))

    class Meta:
        model = Response

        fields = [
            'response_content',
        ]