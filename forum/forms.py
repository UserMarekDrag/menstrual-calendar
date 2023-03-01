from django import forms
from .models import ForumCommentPost, ForumPost


class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumCommentPost
        fields = ('body',)


class AddPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ('title',
                  'body',)
