from django import template
register = template.Library()

@register.filter(name='has_like_answ')
def has_like_answ(user, question_id):
    b_id = int(question_id)
    if user.is_authenticated:
        return user.profile.liked_by_answ.filter(id=b_id).count() > 0
    else: return False

@register.filter(name='has_dislike_answ')
def has_dislike_answ(user, question_id):
    b_id = int(question_id)
    if user.is_authenticated:
        return user.profile.disliked_by_answ.filter(id=b_id).count() > 0
    else:
        return False