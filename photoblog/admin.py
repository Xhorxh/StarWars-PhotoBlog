from django.contrib import admin
from .models import Post, PostImage, Comment


class PostImageInline(admin.TabularInline):
    model = PostImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')


admin.site.register(Comment, CommentAdmin)
admin.site.register(PostImage)
