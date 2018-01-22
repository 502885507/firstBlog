

from django.urls import path, re_path
# from blog.views import index
from blog import views

app_name = 'blog'
urlpatterns = [
    path('',views.IndexView.as_view(), name='index'),
    re_path('post/(?P<pk>[0-9]+)/', views.PostDetailView.as_view(), name='detail'),
    re_path('arctives/(?P<year>[0-9]{4})/(?P<month>[0-12]{1,2})',views.Archives.as_view(), name='archives'),
    re_path('category/(?P<pk>[0-9])', views.Category.as_view(), name='category'),
    re_path('tag/(?P<pk>[0-9])', views.TagView.as_view(), name = 'tag')
]