from django import forms
from .models import CommentPost


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '8',
    }))

    class Meta:
        model = CommentPost
        fields = ('text', 'author',)
