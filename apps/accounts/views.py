from django.http import response
from django.http.response import HttpResponseRedirect

from django.shortcuts import render

from django.urls import reverse 

from django.contrib.auth.models import User

from apps.posts.models import Post, PostImage, PostLike

#Retornar la cantidad de publicaciones, followers, following 
#y las publicaciones en si

def post_amount(user) -> int:
    return len(Post.objects.filter(user=user))

#https://stackoverflow.com/questions/17846290/django-display-imagefield
def list_preview_user_posts(user) -> list:
    response = []
    posts = []
    user_posts = Post.objects.filter(user=user)

    for post in user_posts:
        post_likes = PostLike.objects.get(post=post)
        post_images = PostImage.objects.filter(post=post)

        posts.append([
            post_likes.likes, post_images[0].file.url
        ])

        response = posts
    
    print(response)

    return response



def render_user_profile(request):
    if request.user.is_authenticated:
        
        user = request.user

        return render(request, "accounts/profile.html", {
            "username" : request.user.username,
            "real_name" : request.user.first_name,
            "post_amount" : post_amount(user),
            "posts" : list_preview_user_posts(user)
        })

    return HttpResponseRedirect(reverse('signin'))