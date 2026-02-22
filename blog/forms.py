from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "category", "tag", "summary", "img_url", "content", "visible")


class BlogEditor(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("content",)
