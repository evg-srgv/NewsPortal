from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)



class PostAdmin(admin.ModelAdmin):

    list_display = [field.name for field in Post._meta.get_fields()]
    list_filter = ('price', 'quantity', 'name')
    search_fields = ('name', 'category__name')