from django.urls import path
from .views import *

from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', PostListView.as_view(), name='portal'),
    path('<int:pk>/',(PostDetailView.as_view()), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
]
