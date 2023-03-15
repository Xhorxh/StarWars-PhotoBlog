from django.shortcuts import get_object_or_404, redirect
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
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.name = request.user.username
            comment.save()
            return redirect('post_detail', pk=self.object.pk)
        else:
            context = self.get_context_data(**kwargs)
            context['comment_form'] = form
            return self.render_to_response(context)
