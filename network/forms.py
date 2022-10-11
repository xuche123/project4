from .models import User, Post
from django.forms import ModelForm, Textarea

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            "content": Textarea(attrs={'class': "form-control", 'rows' : 5,  'placeholder': 'What\'s on your mind?'})
        }