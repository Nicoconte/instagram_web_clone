from apps.users.models import UserProfileImage
from django.http.response import HttpResponse, HttpResponseRedirect

from django.shortcuts import render

from django.urls import reverse

from .forms import PostForm

from .models import Post, PostComment, PostCommentAnswer, PostImage, PostLike, SavedPost

from datetime import date, datetime

from django.contrib.auth.models import User

from .serializers import postCommentSerializer

from django.views.decorators.csrf import csrf_exempt

import json

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
            
            user = request.user
            files = request.FILES.getlist('files') 
            current_date = date.today()
            today = current_date.strftime("%Y-%m-%d")
            time = datetime.now()
            now = time.strftime("%H:%M:%S")

            post = Post.objects.create(user=user, description=request.POST['description'], date=today, time=now)

            if post:
                for file in files:
                    PostImage.objects.create(post=post, file=file)

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


def post_amount(user) -> int:
    return Post.objects.filter(user=user).count()

#https://stackoverflow.com/questions/17846290/django-display-imagefield
def list_preview_user_posts(user) -> list:
    response = []
    posts = []
    user_posts = Post.objects.filter(user=user).order_by("-time")

    for post in user_posts:
        post_likes = PostLike.objects.filter(post=post).count()
        post_images = PostImage.objects.filter(post=post)

        post_comments = PostComment.objects.filter(post=post).count()
        post_answer = PostCommentAnswer.objects.filter(comment=post_comments).count()
        post_comment_len = post_comments + post_answer 
        
        posts.append({
            "user_id" : user.id,
            "post_id" : post.id,
            "likes" : post_likes,
            "image" : post_images[0].file.url,
            "comments" : post_comment_len,
        })

        response = posts
    
    return response


def post_was_liked(post, user):
    return PostLike.objects.filter(post=post, user=user).exists()

#Obtener un registro por ID y ajax para mostrarlo en un modal
def get_post_for_modal(request):
    try:
        if request.method == "GET":
            
            id = request.GET['post_id']

            post = Post.objects.get(id=id)

            if post:

                user = post.user #Obtenemos los datos del usuario al que le pertenece la publicacion
                image = UserProfileImage.objects.get(user=user)

                post_likes = PostLike.objects.filter(post=post).count()
                post_images = PostImage.objects.filter(post=post)
                post_comments = PostComment.objects.filter(post=post)

                comments = []

                for post_comment in post_comments:
                    comments.append(postCommentSerializer(post_comment))
                
                
                response = {
                    "id" : post.id,
                    "user_id" : user.id,
                    "username" : user.username,
                    "user_profile_image" : image.file.url,
                    "publish_date" : post.date.strftime("%y-%m-%d"),
                    "description" : post.description,
                    "likes" : post_likes,
                    "was_liked" : post_was_liked(post, request.user), # Con esto vemos si NOSOTROS guardamos la publicacion o le dimos like 
                    "was_saved" : post_was_saved(post, request.user), # Lo mismo que arriba pero en lo guardados
                    "image" : post_images[0].file.url,
                    "comments" : comments
                }

                return HttpResponse(json.dumps(response))

            else:
                raise Exception

        else:
            raise Exception

    except Exception as e:
        return HttpResponse({
            "error" : str(e)
        })


@csrf_exempt
def toggle_like(request):
    try:
        
        if request.user.is_authenticated:
            id = request.POST['post_id']
        
            post = Post.objects.get(id=id)

            user = request.user

            #If the post was liked before -> English xd
            if post_was_liked(post, user):
                PostLike.objects.get(post=post, user=user).delete()
            
            else:
                PostLike.objects.create(post=post, user=user)
        
            return HttpResponse(json.dumps({
                "liked" : True
            }))
        
        else:
            raise Exception

    except Exception as e:
        return HttpResponse(json.dumps({
            "liked" : False,
            "error" : str(e)
        }))


@csrf_exempt
def comment_a_post(request):
    try:
        if request.user.is_authenticated:
            id = request.POST['post_id']

            comment = request.POST['comment']
            user = request.user
            post = Post.objects.get(id=id)

            post_comment = PostComment.objects.create(post=post, comment=comment, user=user)

            if post_comment:
                return HttpResponse(json.dumps({
                    "commented" : True
                }))

            else:
                raise Exception
        
        else:
            raise Exception

    except Exception as e:
        HttpResponse(json.dumps({
            "commented" : False,
            "error" : str(e)
        }))


def post_was_saved(post, user):
    return SavedPost.objects.filter(post=post, user=user).exists()

@csrf_exempt
def toggle_saved_post(request):
    try:

        if request.user.is_authenticated:
            id = request.POST['post_id']
            
            user = request.user
            post = Post.objects.get(id=id)

            if post_was_saved(post, user):
                SavedPost.objects.get(post=post, user=user).delete()
            else:
                SavedPost.objects.create(post=post, user=user)

            return HttpResponse(json.dumps({
                "saved" : True
            }))

        else:
            raise Exception

    except Exception as e:
        return HttpResponse(json.dumps({
            "saved" : False,
            "error" : str(e)
        }))