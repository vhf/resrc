# -*- coding: utf-8 -*-:
from django.contrib import admin

from resrc.vote.models import Vote

def vote_title(vote):
    if vote.link is not None and vote.alist is not None:
        return ("%s upvoted Link AND List : %s" % (vote.user, vote.link, vote.alist))
    elif vote.link is not None:
        return ("%s upvoted Link : %s" % (vote.user, vote.link))
    elif vote.alist is not None:
        return ("%s upvoted List : %s" % (vote.user, vote.alist))


class VoteAdmin(admin.ModelAdmin):
    list_display = (vote_title,)

    def get_form(self, request, obj=None):
        return super(VoteAdmin, self).get_form(request, obj)

admin.site.register(Vote, VoteAdmin)
