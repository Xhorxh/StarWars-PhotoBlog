from django.urls import path
from . import views
from .views import PostListView, PostDetailView, delete_comment, edit_comment, like_post

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
]
