from apps.accounts.views import get_suggested_accounts
from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect

from django.urls import reverse

from django.conf import settings

from .forms import UserRegisterForm, UserLoginForm

from .models import UserProfileImage

from apps.accounts.models import Account

import os

def render_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    return render(request, "accounts/login.html", {
        "form" : UserLoginForm
    })

def render_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    return render(request, "accounts/register.html", {
        "form" : UserRegisterForm
    })


def user_register(request):
    try:

        if request.method == "POST":
            form = UserRegisterForm(request.POST)

            user = User.objects.create_user(
                first_name=request.POST['name'],
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password']
            )

            if user:

                #Con esta cuenta vamos a identificar a todos los usuarios de la plataforma
                #Tambien sirve como auxiliar para el tema de los followers y following
                Account.objects.create(user=user)

                UserProfileImage.objects.create(user=user)

                #Creamos las carpetas en donde se almacena las imagenes del usuario
                #Con esto obtenemos una mejor gestion del contenido
                os.mkdir(f"{settings.MEDIA_ROOT}{user.username}" )
                os.mkdir(f"{settings.MEDIA_ROOT}{user.username}/profile" )
                os.mkdir(f"{settings.MEDIA_ROOT}{user.username}/posts" )

                return HttpResponseRedirect(reverse('signup'))
            
            else:
                return render(request, "accounts/register.html", {
                    "error_msg" : "Datos invalidos",
                    "form" : UserRegisterForm
                })

    except:
        return render(request, "accounts/register.html", {
            "error_msg" : "El usuario ya existe",
            "form" : form
        })



def user_login(request):
    try:
        if request.method == "POST":
            form = UserLoginForm(request.POST)

            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user:
                
                profile = UserProfileImage.objects.get(user=user)

                #https://docs.djangoproject.com/en/3.1/topics/http/sessions/
                request.session['user_image'] = profile.file.url

                login(request, user)
 
                return HttpResponseRedirect(reverse('home'))

            else:
                raise Exception
        
        else:
            raise Exception

    except Exception:
        return render(request, "accounts/login.html", {
            "error_msg" : "Credenciales invalidas",
            "form" : UserLoginForm
        })


def user_logout(request) -> HttpResponseRedirect:
    
    request.session['user_image'] = None

    logout(request)
    
    return HttpResponseRedirect(reverse('signin'))


def render_home(request):
    if request.user.is_authenticated:

        user = request.user

        return render(request, "accounts/home.html", {
            "username" : user.username,
            "real_name" : user.first_name,
            "suggested_accounts" : get_suggested_accounts(user)
        })
    else:
        return HttpResponseRedirect(reverse('signin'))