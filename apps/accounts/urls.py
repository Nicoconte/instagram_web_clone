from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.render_user_profile, name="profile"),
    path('profile/<int:id>/', views.render_user_profile, name="see-another-profile"),
    path('profile/<int:id>/follow/', views.follow_user, name="follow-account"),
    path('profile/<int:id>/unfollow/', views.unfollow_user, name="unfollow-account")
]