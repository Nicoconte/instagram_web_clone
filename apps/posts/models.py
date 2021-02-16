from django.db import models

from django.contrib.auth.models import User

# Create your models here.

def path(instance, filename) -> str:
    return "{0}/posts/{1}".format(instance.post.user.username, filename)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    date = models.DateField()

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.ImageField(upload_to=path, default='not-image.png')

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=200)

class PostCommentAnswer(models.Model):
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
