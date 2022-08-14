from django.contrib import admin
from home.models import Category , Blog , Comment , Tag , replay

class Blogadmin(admin.ModelAdmin):
    list_display = ('title','category', 'created')
class Commentadmin(admin.ModelAdmin):
    list_display = ('user', 'blog' ,'text')

class Replayadmin(admin.ModelAdmin):
    list_display = ('user', 'comment' ,'text')

admin.site.register(Category)
admin.site.register(Blog , Blogadmin)
admin.site.register(Comment , Commentadmin)
admin.site.register(Tag)
admin.site.register(replay ,Replayadmin)
