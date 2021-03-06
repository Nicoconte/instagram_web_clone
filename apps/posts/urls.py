from django.urls import path

from . import views

urlpatterns = [
    path('post/', views.render_post_form, name="publish-post"),
    path('post/upload/', views.create_post, name="add-post"),
    path('post/modal/', views.get_post_for_modal, name="modal-post"),
    path('post/like/', views.toggle_like, name="like-post"),
    path('post/comment/', views.comment_a_post, name="comment-post"),
    path('post/save/', views.toggle_saved_post, name="save-post")
]