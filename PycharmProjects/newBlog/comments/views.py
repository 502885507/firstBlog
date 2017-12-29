from django.shortcuts import render, get_object_or_404,redirect, render_to_response
from blog.models import Post
from comments.models import Comment
from comments.form import CommentForm

# Create your views here.


def post_commnet(request, post_pk):
    # 现获取被评论的文章，后面需要把评论和被评论的文章关联起来
    # 这里使用 django提供的一个快捷函数
    # get_object_or_404 有Post时候获取 没有的话 返回404

    post = get_object_or_404(Post, pk=post_pk)
    # 一般提供表单的都是post请求
    # 只有当用户请求为post的时候，才需要处理表单数据

    if request.method == 'POST':
        # 用数据构造了commentform 这样就创建一个django 的form就生成了
        form = CommentForm(request.POST)
        # 调用is_valid的时候 django会自动帮我们检查  这个form是否符合我们要求
        if form.is_valid():
            # 检查到数据是合法的  就保存起来
            # commit = false 作用仅仅利用表单的数据生成，但是不爆粗到数据库
            comment = form.save(commit=False)
            # 将评论和被评论的文章关联起来
            comment.post = post

            # 最终评论保存到数据库中
            comment.save()
            # 然后重定向到post的详情页
            # 当redirect函数接受一个模型实例的时候，会调用这个模型的get_absolute_url方法
           #然后重定向到get_absolute_url返回的url
            return redirect(post)

        else:
            #数据不合法时候，重启渲染详情页，并渲染form
            # 穿了三个数据给single.html
            # 一个是文章 一个是评论的列表 一个表单的form
            #post.comment_set.all() 类似于post.object.all方法 获取 文章的所有评论
            comment_list = post.comment_set.all()
            return render_to_response('blog/single.html',context= {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       })

    # 不是post请求，说明用户没有提交评论
    return redirect(post)





