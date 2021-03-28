from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    #path('success', views.success),
    path('addquote', views.addquote),
    path('myaccount/<int:user_id>', views.account),
    path('edit', views.edit),
    path('user/<int:user_id>', views.userquotes),
    path('quotes',views.quotes),
    path('like/<int:quote_id>', views.likequote),
    path('logout', views.logout)
]