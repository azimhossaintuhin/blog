from home import views
from django.urls import  path


urlpatterns = [
    path('', views.index , name = 'index'),
    path('post', views.blog , name = 'post'),
    path('blog/<str:slug>', views.blog_datails , name = 'blog_datails'),
    path('category_blog/<str:slug>', views.category_blog , name = 'category_blog'),
    path('tags_blog/<str:slug>', views.tags_blog , name = 'tags_blog'),
    path('add_reply/<int:comment_id>/<int:blog_id>' , views.Replay , name = 'replay' ),
    path('like/<int:pk>', views.like_blog , name = 'like_blog'), 
    path('search/', views.serch_blog , name = 'search'),
    path('my_blog', views.my_blog , name = 'my_blog'),
    path('add_blog', views.add_blog , name = 'add_blog'),
    path('update_blog/<str:slug>', views.update_blog , name = 'update_blog'),
]