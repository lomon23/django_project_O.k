from .models import *
from django import forms

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'tags', 'status']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email','body']
class EmailForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    from_email = forms.EmailField()
    to_email = forms.EmailField()

