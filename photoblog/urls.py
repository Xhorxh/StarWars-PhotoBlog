from django.urls import path
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('posts<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]
