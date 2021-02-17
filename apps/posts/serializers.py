
from .models import PostComment, PostLike

from apps.users.models import UserProfileImage

def postCommentSerializer(post : PostComment) -> dict:
    user = post.user
    profile = UserProfileImage.objects.get(user=user)

    comment = {
        "user_id" : user.id,
        "username" : user.username,
        "profile" : profile.file.url,
        "comment" : post.comment
    }

    return comment


def postLikeSerializer(post : PostLike) -> dict:
    return {}