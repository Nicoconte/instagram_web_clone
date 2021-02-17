from django.contrib import admin

from .models import Post, PostImage, PostLike, PostComment, PostCommentAnswer, SavedPost

admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(PostLike)
admin.site.register(PostComment)
admin.site.register(PostCommentAnswer)
admin.site.register(SavedPost)


# Register your models here.
