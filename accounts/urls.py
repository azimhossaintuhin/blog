from django import views
from django.urls import path
from accounts import views

urlpatterns = [
    path('login/' , views.loginuser, name='login'),
    path('registration', views.registretion , name = 'registretion'),
    path('userprofile',views.userprofile , name='profile' ),
    path('change_profile_picture' , views.change_profile_picture , name ="pro_picture"),
    path('logut',views.logoutuser , name = 'logout')
]
