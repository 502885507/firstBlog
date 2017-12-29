from django.db import models

# Create your models here.
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    url = models.URLField(blank=True)
    text = models.TextField()
    # 使用创建时间当做creat_time
    creat_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('blog.Post', on_delete=True)

