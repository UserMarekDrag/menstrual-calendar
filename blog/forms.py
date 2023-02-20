from django import forms
from .models import CommentPost


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '2',
    }))

    class Meta:
        model = CommentPost
        fields = ('author', 'text', )
