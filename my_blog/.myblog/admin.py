from django.contrib import admin
from .models import BlogPost, Comment
from taggit.forms import TagWidget


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_at', 'active']
    list_filter = ['active', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'body']


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created_at']
    list_filter = ['created_at', 'owner', 'tags']
    search_fields = ['title', 'text']

    formfield_overrides = {
        'tags': {'widget': TagWidget},
    }


admin.site.register(BlogPost, BlogPostAdmin)
