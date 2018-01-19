from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from comments.form import CommentForm
from .models import Post,Category
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import markdown
from django.views.generic import ListView, DetailView

def index(request):
    # return HttpResponse("欢迎访问我的博客首页！")
    # return render(request, "blog/index.html", context={"title": "欢迎来到我的博客", "welcome": "欢迎访问我的博客首页"} )
    # return render_to_response("blog/index.html", {"title": "欢迎来到我的博客", "welcome": "欢迎访问我的博客首页"})
    post_list = Post.objects.all().order_by("-creat_time")
    return render_to_response("blog/index.html", {"post_list": post_list})


@csrf_exempt
def detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.increase_views()
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





class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 指定多少文章一页
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        在view中需要传递的模板变量获取在这个函数中获取
        """
        # 获取父类生成的传递给模板的变量
        context = super().get_context_data(**kwargs)

        # 父类生成的字典已经有paginator、page_obj、is_paginated三个模板变量
        # paginator 是 Paginator的一个实例
        # page_obj分页对象 Page的一个实例
        # is_paginated是一个bool值 是否分页

        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        is_paginator = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page=page_obj, is_paginated=is_paginator)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，不显示分页导航
            return {}
        # 当前页面左边的连续页码号，初始值为空
        left = []

        # 右边的连续页码号，初始值为空
        right = []

        # 第一页后需不需要显示省略号 默认为false

        left_has_more = False

        # 最后一页页码是否需要省略号
        right_has_more = False

        # 表示是否需要显示第一页的页码号
        # 如果当前页面前一页包含第一页的页码号 就不需要显示第一页
        # 其它情况都需要显示第一页的页码号
        # 初始值为false
        first = False

        # 最后一页的页码号
        last = False

        # 当前的页码号
        page_number = page.number
        # 分页后的总页数

        total_pages = paginator.num_pages

        # 获得整个分页页码列表。比如分四页[1,2,3,4]
        page_range = paginator.page_range

        if page_number == 1:

            right = page_range[page_number:page_number+2]
            # page_ragn 取   page_number+2>=i>page_number

            # 如果当前请求到的是第一个页面
            # 假如只显示当前页面后面两个页面

            if right[-1] < total_pages - 1:
                # 如果两页后的页码数小于总页码数-1
                # 说明还有其他页码 需要省略号
                right_has_more = True

            if right[-1]<total_pages:
                # 如果页码数小于总页码数，显示最后一页的页码数
                last=True
        elif page_number == total_pages:
            left = page_range[page_number-3 if page_number - 3 > 0 else 0:page_number-1]
            # 如果用户请求的是最后一页的页码数  就不需要 右边的页码 right=[]
            # 如果page_number-3 大于0 则[page_number-3: pagenumber-1] 中间的两项
            # 如果page_number-3<0 则取[0:pange_number-1]
            if left[0] > 2:
                left_has_more = True
                # 如果最左边的页码 比2还要大  说明  左边需要省略号
            if left[0] > 1:
                # 如果左边的页码 大于1 ,需要显示第一页
                first = True
        else:

            # 既不是第一页 又不是最右一页
            left = page_range[page_number-3 if page_number-3>0 else 0:page_number-1]
            right = page_number[page_number: page_number+2]

            #是否需要显示左边和右边的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                left = True
            if right[-1] < total_pages -1:
                right_has_more = True
            if right[-1] < total_pages:
                right = True

        data = {
            'left': left,
            'right': right,
            'left_has_more':left_has_more,
            'right_has_more': right_has_more,
            'first':first,
            'last':last
        }
        return data


class Archives(IndexView):
    def get_queryset(self):

        creatYear = self.kwargs.get('year')
        creatMonth = self.kwargs.get('month')
        super(Archives, self).get_queryset().filter(creat_time__year=creatYear, creat_time__month=creatMonth)




class Category(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    # 重写get_queryset 这个方法本来是获取w文章列表全部数据，
    def get_queryset(self):
        #在类试图中，从url捕获的命名组参数值保存在实例的kwargs中（这是一个字典）
        cate = self.kwargs.get('pk')
        return super(Category, self).get_queryset().filter(category = cate)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'postM'


    def get(self, request, *args, **kwargs):

     response = super(PostDetailView, self).get(request, *args, **kwargs)
     # 之所以先调用父类方法 只有调用了父类方法才能使用self.object,self.object为post实例
     # get的返回方法是一个httpresponse实例

    # 将文章阅读量加1
     self.object.increase_views()
     return response

    def get_object(self, queryset=None):

        post = super(PostDetailView, self).get_object(queryset=None)
        # 重写get_object是对post的body进行markdown渲染
        post.body = markdown.markdown(post.body,  extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):

        # 评论
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context










