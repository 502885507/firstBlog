from blog.models import Post, Category
from django import template
from django.db.models.aggregates import Count
from blog.models import Category
from blog.models import Tag

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by("-creat_time")[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('creat_time', 'month', order='DESC')

@register.simple_tag
def get_category():

    # Count 计算分类下文章数量，接受的参数是需要计数的模型名称
    # num_posts__get = 0 是post的总数大于0的
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt = 0)

# 这个修饰器是注册为魔板标签 直接在模板中拿到返回的数据
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt = 0)





