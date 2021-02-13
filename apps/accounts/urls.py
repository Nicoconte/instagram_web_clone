from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.render_user_profile, name="profile"),
]