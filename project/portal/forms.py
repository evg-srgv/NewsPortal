from django import forms
from django.forms import ModelForm, BooleanField 
from .models import Post, Category, PostCategory
from django.core.exceptions import ValidationError


class PostForm(ModelForm):
    

    class Meta:
        model = Post
        fields = ['author', 'postTitle', 'category', 'postContent', 'categoryType',
                  ]
