from django.contrib import admin
from .models import *

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title')
    search_fields = ('id','content')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(Comments)


