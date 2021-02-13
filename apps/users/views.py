from django.shortcuts import render

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from .forms import UserRegisterForm, UserLoginForm

def render_login(request):
    return render(request, "accounts/login.html", {
        "form" : UserLoginForm
    })

def render_register(request):
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
 
                return render(request, "accounts/login.html", {
                    "error_msg" : "Inicio de sesion",
                    "form" : form
                })

            else:
                raise Exception
        
        else:
            raise Exception

    except Exception:
        return render(request, "accounts/login.html", {
            "error_msg" : "Credenciales invalidas",
            "form" : UserLoginForm
        })