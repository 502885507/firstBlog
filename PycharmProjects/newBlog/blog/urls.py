

from django.urls import path, re_path
# from blog.views import index
from blog import views

app_name = 'blog'
urlpatterns = [
    path('',views.index, name='index'),
    re_path('post/(?P<pk>[0-9]+)/', views.detail, name='detail'),
    re_path('arctives/(?P<year>[0-9]{4})/(?P<month>[0-12]{1,2})',views.archives, name='archives'),
    re_path('category/(?P<pk>[0-9])', views.category, name='category')

]