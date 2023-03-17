from django.urls import reverse
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect, render
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
        context['comment_form'] = CommentForm(initial={'comment': ''})
        context['user_comments'] = comments.filter(name=self.request.user)
        context['edit_comment_id'] = self.request.GET.get('edit_comment_id')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST, initial={'comment': ''})
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
    form = CommentForm(request.POST or None, initial={'content': comment.content})
    if request.method == 'POST':
        form = CommentForm(request.POST, initial={'content': comment.content})
        if form.is_valid():
            comment.content = form.cleaned_data['content']
            comment.save()
            messages.success(request, 'Comment edited successfully!')
            return redirect('post_detail', pk=comment.post.pk)
        else:
            messages.error(request, 'Error editing comment.')
    else:
        form = CommentForm(initial={'content': comment.content})

    context = {
        'comment': comment,
        'form': form
    }
    return render(request, 'edit_comment.html', context)


def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(request.user)
        messages.warning(request, 'You unliked this post!')
    else:
        post.likes.add(user)
        messages.success(request, 'Post liked successfully!')
    return redirect('post_detail', pk=post_id)
