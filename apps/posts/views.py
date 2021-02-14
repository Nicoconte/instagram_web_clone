from django.http.response import HttpResponseRedirect

from django.shortcuts import render

from django.urls import reverse

from django.conf import settings

from .forms import PostForm

from .models import Post, PostComment, PostCommentAnswer, PostImage, PostLike

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
            
            user = request.user
            files = request.FILES.getlist('files') 
            current_date = date.today()
            today = current_date.strftime("%Y-%m-%d")

            post = Post.objects.create(user=user, description=request.POST['description'], date=today)

            if post:
                for file in files:
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


def post_amount(user) -> int:
    return Post.objects.filter(user=user).count()

#https://stackoverflow.com/questions/17846290/django-display-imagefield
def list_preview_user_posts(user) -> list:
    response = []
    posts = []
    user_posts = Post.objects.filter(user=user)

    for post in user_posts:
        post_likes = PostLike.objects.get(post=post)
        post_images = PostImage.objects.filter(post=post)

        post_comments = PostComment.objects.filter(post=post).count()
        post_answer = PostCommentAnswer.objects.filter(comment=post_comments).count()
        post_comment_len = post_comments + post_answer 
        

        posts.append([
            post_likes.likes, post_images[0].file.url, post_comment_len, post.id
        ])

        response = posts
    
    return response


#Obtener un registro por ID y ajax
def get_post(request, id):
    try:
        if request.user.is_authenticated:
            post = Post.objects.get(id=id, user=request.user)

            if post:
                return {
                    "description" : post.description
                }

            else:
                raise Exception

        else:
            raise Exception

    except Exception as e:
        return {
            "error" : str(e)
        }