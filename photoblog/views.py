from django.views.generic import ListView, DetailView
from .models import Post, Comment
from .forms import CommentForm


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
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return self.render_to_response(context)

        context['comment_form'] = comment_form
        return self.render_to_response(context)
