from django.contrib import admin
from main_app.models import Author, Post, Comment, Like


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'date_joined']
    search_fields = ['name', 'email']
    search_help_text = 'Search by author name or email'
    fieldsets = [
        ['Main info',
            {'fields': ['name', 'email', 'date_joined']}],
        ['Additional info',
            {'classes': ['collapse'],
             'fields': ['bio']
             }],
    ]
    readonly_fields = ['date_joined']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_date', 'is_published']
    list_filter = ['is_published']
    search_fields = ['title', 'author__name']
    search_help_text = 'Search by title or author name'
    fieldsets = [
        ['Main info',
         {'fields': ['title', 'author', 'is_published']}],
        ['Additional info',
         {'classes': ['collapse'],
          'fields': ['content']
          }],
    ]
    readonly_fields = ['publication_date']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'text', 'publication_date']
    search_fields = ['post__title', 'author__name']
    search_help_text = 'Search by post title or author name'
    fieldsets = [
        ['Main info',
         {'fields': ['post', 'author']}],
        ['Additional info',
         {'classes': ['collapse'],
          'fields': ['text']
          }],
    ]
    readonly_fields = ['publication_date']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'comment', 'date_liked']
    search_fields = ['author__name', 'post__title', 'comment__text']
    search_help_text = 'Search by author name, post title, or comment text'
    fieldsets = [
        ['Main info',
         {'fields': ['author', 'post', 'comment', 'date_liked']}],
    ]
    readonly_fields = ['date_liked']
