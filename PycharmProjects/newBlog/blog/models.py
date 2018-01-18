from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
from markdown import markdown
from django.utils.html import strip_tags

class Category(models.Model):
    """
      Django 要求模型必须继承 models.Model 类。
      Category 只需要一个简单的分类名 name 就可以了。
      CharField 指定了分类名 name 的数据类型，CharField 是字符型，
      CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
      当然 Django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
      Django 内置的全部类型可查看文档：
      https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
      """
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签 tag    继承model.Model类
    """
    mame = models.CharField(max_length=100)
    def __str__(self):
        return self.mame

@python_2_unicode_compatible
class Post(models.Model):

    # 文章数据库
    # 文章标题
    title = models.CharField(max_length=70)
    # 文章内容 对于比较短的储存用chartFiled 文章内容较多 使用textfield
    body = models.TextField()
    # 文章这个创建时间和最后修改时间
    creat_time = models.DateTimeField()
    modifi_time = models.DateTimeField()

    # 文章摘要，可以没有问斩个摘要
    # 指定chartFiled 的blank = false 就可以允许空值了
    excerpt = models.CharField(max_length=200, blank=True)
    #一对多的分类要使用Foreignkey() 一个分类下右多篇文章 ，而一篇文章只能对应一个分类
    category = models.ForeignKey(Category, on_delete=True)
    # 多对多要用ManyToMany（） 一个文章可以多个标签，一个标签也可以多个文章
    tag = models.ManyToManyField(Tag, blank=True)

    # 文章作者g
    # django.contrib.auth是django 内置的应用，处理注册 登录的流程User 是 Django 为我们已经写好的用户模型。
    # 文章和User关联起来
    author = models.ForeignKey(User, on_delete=True)
    # 评论数 默认为0
    # PositiveIntegerField只允许为正整数或者0
    views = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title

    # 自定义get_absolte方法
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    def increase_views(self):
        # 每一个阅读的人
        self.views += 1
        self.save(update_fields=['views'])

    # 重写save方法
    def save(self, *args, **kwargs):
        if not self.excerpt:
            # 实例化一个markdown类 用于渲染body文本
            md = markdown.Markdown(extensions=['markdown.extensions.extra', 'markdown.extensions.condehilite'])
            # 现将markdown文本渲染成html文本
            # strip_tags 去掉html 文本的全部Html标签
            self.excerpt = strip_tags(md.convert(self.body))[:54]
            # 调用父类额方法将数据保存在数据库中
            super(Post, self).save(*args, **kwargs)




# 评论数







