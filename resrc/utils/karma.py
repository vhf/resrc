# -*- coding: utf-8 -*-:
from django.contrib.auth import get_user_model
from resrc.userprofile.models import Profile


def karma_rate(user_pk, diff):
    user = Profile.objects.get(user__pk=user_pk)
    if user.karma:
        user.karma += diff
    else:
        user.karma = diff
    user.save()
