
from django.conf.urls import url
from . import views
from django.urls import path, re_path
app_name = 'comments'
urlpatterns = [
    re_path("comment/post/(?P<post_pk>[0-9]+)", views.post_commnet, name='post_comment')
]