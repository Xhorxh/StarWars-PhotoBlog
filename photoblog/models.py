from django.db import models
import cloudinary
from cloudinary.models import CloudinaryField


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images')
    image = CloudinaryField('image')

    def __str__(self):
        return self.post.title
