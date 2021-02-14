from django.contrib.auth.models import User

from django.http.response import HttpResponseRedirect

from django.shortcuts import render

from django.urls import reverse

from django.core.files.storage import FileSystemStorage

from django.conf import settings

from .forms import PostForm

from .models import Post, PostImage, PostLike

from datetime import date

"""
Primero se suben las imagenes
Luego se sube toda la info adicional del post
"""

#Renderizamos el formulario para crear el post
def render_post_form(request):
    if request.user.is_authenticated:
        return render(request, "accounts/create_post.html", {
            "form" : PostForm
        })
    
    return HttpResponseRedirect(reverse('signin'))

def create_post(request):
    try:
        if request.method == "POST":
            
            username = request.user.username
            user = request.user
            dir = f"{settings.MEDIA_ROOT}{username}/posts/"  
            storage = FileSystemStorage(location=dir)
            files = request.FILES.getlist('files') 
            current_date = date.today()
            today = current_date.strftime("%Y-%m-%d")

            post = Post.objects.create(user=user, description=request.POST['description'], date=today)

            if post:
                for file in files:
                    storage.save(file.name, file)
                    PostImage.objects.create(post=post, file=file)

                PostLike.objects.create(post=post, likes=0)

                return render(request, "accounts/create_post.html", {
                    "form" : PostForm,
                    "msg" : "Publicacion creada!"
                })

            else:
                raise Exception
        
        else:
            raise Exception

    except Exception as e:

        form = PostForm(request.POST)
        
        return render(request, "accounts/create_post.html", {
            "form" : form,
            "msg"  : str(e) 
        })
            