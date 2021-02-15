from django.http import response
from django.http.response import HttpResponseRedirect

from django.shortcuts import render

from django.urls import reverse 

from django.contrib.auth.models import User

from apps.users.models import UserProfileImage

from apps.posts.views import *

#Retornar la cantidad de publicaciones, followers, following 
#y las publicaciones en si


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