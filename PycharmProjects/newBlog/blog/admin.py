from django.contrib import admin
from blog.models import Post, Category, Tag

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_filter = ('title',)
    search_fields = ('title',)



admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)


