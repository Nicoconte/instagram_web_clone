from django.shortcuts import render

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect

from django.urls import reverse

from .forms import UserRegisterForm, UserLoginForm

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
                return render(request, "accounts/register.html",{
                    "form" : UserRegisterForm
                })
            
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
    
    logout(request)
    
    return HttpResponseRedirect(reverse('signin'))

def render_home(request):
    if request.user.is_authenticated:
        return render(request, "accounts/home.html")
    else:
        return HttpResponseRedirect(reverse('signin'))