from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
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
        comments = self.object.comments.all().order_by('-created_at')
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        context['user_comments'] = comments.filter(name=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.name = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', pk=self.object.pk)
        else:
            context = self.get_context_data(**kwargs)
            context['comment_form'] = form
            messages.error(request, 'Error adding comment.')
            return self.render_to_response(context)


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, name=request.user)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('post_detail', pk=comment.post.pk)
    else:
        messages.warning(request, 'Are you sure you want to delete this comment?')
        context = {'comment': comment}
        return redirect('post_detail', pk=comment.post.pk)


def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, name=request.user)
    form = CommentForm(request.POST or None, instance=comment)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment edited successfully!')
            return redirect('post_detail', pk=comment.post.pk)
        else:
            messages.error(request, 'Error editing comment.')
    return redirect('post_detail', pk=comment.post.pk)
