from django import template

register = template.Library()

@register.filter(name='has_like')
def has_like(user, question_id):
    b_id = int(question_id)
    if user.is_authenticated:
        return user.profile.liked_by.filter(id=b_id).count() > 0
    return False

@register.filter(name='has_dislike')
def has_dislike(user, question_id):
    b_id = int(question_id)
    if user.is_authenticated:
        return user.profile.disliked_by.filter(id=b_id).count() > 0
    else: return False