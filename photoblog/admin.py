from django.contrib import admin
from .models import Post, PostImage, Comment


class PostImageInline(admin.TabularInline):
    model = PostImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'post', 'created_at')
    search_fields = ('name', 'email', 'content')


admin.site.register(PostImage)
