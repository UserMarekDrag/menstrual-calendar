from django import forms
from .models import ForumCommentPost


class ForumCommentForm(forms.ModelForm):

    class Meta:
        model = ForumCommentPost
        fields = ('body', )
