from django.urls import path
from . import views


urlpatterns = [
    path('', views.reg_or_login),
    path('register', views.register),
    path('wall', views.wall),
    path('logout', views.logout),
    path('login', views.login),
    path('add_mesg', views.add_mesg),
    path('add_comment/<id>', views.add_comment)
]
