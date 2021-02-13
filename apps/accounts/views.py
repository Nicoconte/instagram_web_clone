from django.http.response import HttpResponseRedirect

from django.shortcuts import render

from django.urls import reverse 

from django.contrib.auth.models import User


#Retornar la cantidad de publicaciones, followers, following 
#y las publicaciones en si
def render_user_profile(request):
    if request.user.is_authenticated:
        return render(request, "accounts/profile.html", {
            "username" : request.user.username,
            "real_name" : request.user.first_name
        })

    return HttpResponseRedirect(reverse())