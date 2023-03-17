from django.db import models
import cloudinary
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = CloudinaryField('image', default='placeholder')
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images')
    image = CloudinaryField('image')

    def __str__(self):
        return self.post.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.post.id)])