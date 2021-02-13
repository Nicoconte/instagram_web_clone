from django.urls import path

from . import views

urlpatterns = [
    path('signin/', views.render_login, name="signin"),
    path('register/', views.user_register, name="register"),
    path('signup/', views.render_register, name='signup'),
    path('auth/', views.user_login, name="auth"),
    path('signout', views.user_logout, name="signout"),
    path('home/', views.render_home, name="home")
]