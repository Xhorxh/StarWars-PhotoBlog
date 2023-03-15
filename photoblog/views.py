from django.views.generic import ListView, DetailView
from .models import Post


class PostListView(ListView):
    model = Post
    queryset = Post.objects.all().order_by('-created_at')
    paginate_by = 6  # 6 posts per page
    context_object_name = 'posts'
    template_name = 'index.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        return context
