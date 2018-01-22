from django.contrib.syndication.views import Feed
from blog.models import Post

class AllPostsRssFeed(Feed):
    # 显示在聚合阅读器上的标题
    title = 'Stay'

    # 通过聚合阅读器跳转到网站的地址
    link = 'www.baidu.com'


    # 显示在聚合于阅读器的描述
    description = 'stay with me'

    # 需要显示的内容条目

    def items(self):
        return Post.objects.all()

    # 需要显示的内容条目

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    # 聚合器中显示的内容条目的描述

    def item_description(self, item):
        return item.body


