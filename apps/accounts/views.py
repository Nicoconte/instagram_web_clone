from django.http.response import HttpResponseRedirect

from django.shortcuts import render

from django.urls import reverse 

from django.contrib.auth.models import User

from apps.users.models import UserProfileImage

from apps.posts.views import *

from .models import Account, Follower

import random

#Retornar la cantidad de publicaciones, followers, following 
#y las publicaciones en si


#Yo como cuenta me siguen 3 usuarios
def get_followers(account):
    return Follower.objects.filter(account=account).count()

#Y yo como usuario sigo 2 cuentas
def get_following(user):
    return Follower.objects.filter(user=user).count()


def follow_user(request, id):
    try:
        #Cuenta y usuario actuales
        current_user = request.user

        #Cuenta y usuario del otro
        another_user = User.objects.get(id=id)
        another_account = Account.objects.get(user=another_user)

        follower = Follower.objects.create(account=another_account, user=current_user) #Sigo a la cuenta de otro usuario

        if follower:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #Volvemos a la pagina anterior

        else:
            raise Exception

    except Exception:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unfollow_user(request, id):
    try:
        #Cuenta y usuario actuales
        current_user = request.user

        #Cuenta y usuario del otro
        another_user = User.objects.get(id=id)
        another_account = Account.objects.get(user=another_user)

        Follower.objects.get(account=another_account, user=current_user).delete() #Sigo a la cuenta de otro usuario

        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #Volvemos a la pagina anterior

    except Exception:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_suggested_accounts(current_user) -> list:

    accounts_list = Account.objects.exclude(user=current_user)[3:8]

    accounts = []

    for account in accounts_list:

        image = UserProfileImage.objects.get(user=account.user)

        accounts.append({
            "user_id"  : account.user.id,
            "username" : account.user.username,
            "image"  : image.file.url,
            "is_already_follow" : Follower.objects.filter(account=account, user=current_user).exists()
        })

    return accounts

#Render de perfiles
def render_user_profile(request, id=None):
    if request.user.is_authenticated:

        user = None
        account = None
        image = None
        is_owner = None
        is_already_follow = None

        #Si nos envian un ID es porque nos piden renderizar el perfil de otro usuario
        if id != None:
            user = User.objects.get(id=id)
            account = Account.objects.get(user=user)
            image = UserProfileImage.objects.get(user=user)    
            is_already_follow = Follower.objects.filter(account=account, user=request.user).exists() #Verifico si ya lo habia seguido 
            is_owner = False if user != request.user else True 

        #De lo contrario renderizamos el nuestro
        else:
            user = request.user
            account = Account.objects.get(user=user)
            image = UserProfileImage.objects.get(user=user)
            is_owner = True


        return render(request, "accounts/profile.html", {
            "user_id" : user.id, 
            "username" : user.username,
            "real_name" : user.first_name,
            "user_profile_image" : image.file.url,
            "post_amount" : post_amount(user),
            "posts" : list_preview_user_posts(user),
            "followers" : get_followers(account),
            "following" : get_following(user),
            "is_owner" : is_owner,
            "is_already_follow" : is_already_follow
        })

    return HttpResponseRedirect(reverse('signin'))
