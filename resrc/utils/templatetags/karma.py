# -*- coding: utf-8 -*-:
from django import template

from resrc.userprofile.models import Profile

register = template.Library()


@register.filter('karma')
def karma(user):
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    return profile.karma or 0
