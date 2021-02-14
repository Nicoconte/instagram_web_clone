from django.contrib import admin

from .models import Post, PostImage, PostLike, PostComment, PostCommentAnswer

admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(PostLike)
admin.site.register(PostComment)
admin.site.register(PostCommentAnswer)


# Register your models here.
