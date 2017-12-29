from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from comments.form import CommentForm
from .models import Post,Category
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import markdown

def index(request):
    # return HttpResponse("欢迎访问我的博客首页！")
    # return render(request, "blog/index.html", context={"title": "欢迎来到我的博客", "welcome": "欢迎访问我的博客首页"} )
    # return render_to_response("blog/index.html", {"title": "欢迎来到我的博客", "welcome": "欢迎访问我的博客首页"})
    post_list = Post.objects.all().order_by("-creat_time")
    return render_to_response("blog/index.html", {"post_list": post_list})


@csrf_exempt
def detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.body = markdown.markdown(post.body,extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    # 获取全部评论
    comment_list = post.comment_set.all()
    context = {'postM': post,
               'form': form,
               'comment_list': comment_list
               }

    # 将文章表单，以及以下评论l列表传入sigle.html,渲染数据

    return render(request, 'blog/single.html', context=context)


def archives(request, year, month):
    post = Post.objects.filter(creat_time__year=year,
                               creat_time__month=month).order_by("-creat_time")
    return render_to_response('blog/index.html',context={'post_list':post})

def category(request,pk):
    cate = get_object_or_404(Category, pk = pk)
    post_list = Post.objects.filter(category=cate).order_by('-creat_time')
    return render_to_response('blog/index.html', context={'post_list':post_list})





