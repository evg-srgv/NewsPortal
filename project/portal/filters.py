from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFromToRangeFilter 
from .models import *

from django.contrib.auth.models import User


class PostFilter(FilterSet):
    publicationDate = DateFromToRangeFilter(label='Dates From To Range')

    class Meta:
        model = Post
        fields = {
            'postTitle': ['icontains'],
            'author': ['exact'],
            'category': ['exact'],
        }