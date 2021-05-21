from django.contrib.auth.models import User
from django.db import models

# Create your models here.


def post_img_path(instance, filename):
    return 'post_pics/{0}/{1}'.format(instance.post_title, filename)


class Post(models.Model):

    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_img = models.ImageField(
        default='post_pic.jpg', upload_to=post_img_path)
    post_title = models.CharField(max_length=250)
    post_detail = models.TextField(max_length=1000)
    post_date = models.DateTimeField(auto_now_add=True)
    post_like = models.ManyToManyField(User, related_name='+', blank=True)

    def __str__(self):
        return f'{self.post_title } and id: { self.id }'


class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_detail = models.TextField(max_length=150)
    comment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.post_id.post_title} by {self.comment_author.username}'
