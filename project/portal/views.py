from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models.signals import ModelSignal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from django.core.paginator import Paginator 
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse_lazy
from .models import Author, Category, Post, PostCategory, Comment
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef
from django.core.cache import cache





class PostListView(ListView):
    model = Post 
    template_name = 'post/post_list.html'
    context_object_name = 'post_list'
    ordering = ['-publicationDate']
    queryset = Post.objects.order_by('-publicationDate')
    form_class = PostForm
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['news_list'] = Post.objects.all()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return queryset.order_by('id', '-publicationDate')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)
    
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'Post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'Post-{self.kwargs["pk"]}', obj)
        return obj


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/post_details.html'
    queryset = Post.objects.all()


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = PostCategory
    form_class = PostForm
    template_name = 'post/post_create.html'
    context_object_name = 'post_create'
    raise_exception = True
    permission_required = ('portal.add_post')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Добавить статью"
        return context


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'post/post_update.html'
    form_class = PostForm
    raise_exception = True
    permission_required = ('portal.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
    
    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Редактировать статью"
        return context

    def form_valid(self, form):
        self.object = form.save()  
        cat = Category.objects.get(pk=self.request.POST['postCategory'])
        self.object.postCategory.add(cat)  
        return super().form_valid(form)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post/post_delete.html'
    permission_required = ('portal.delete_post',)
    queryset = Post.objects.all()
    success_url = '/portal/'


class PostSearchView(ListView):
    model = Post 
    template_name = 'post/post_search.html'
    context_object_name = 'post_search'
    paginate_by = 10
    form_class = PostForm

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = PostCategory.objects.all()
        context['form'] = PostForm()
        return context


