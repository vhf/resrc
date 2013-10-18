# -*- coding: utf-8 -*-:
from django.db import models
from django.contrib.auth.models import User
from django.core import urlresolvers
from resrc.utils import slugify


class Profile(models.Model):

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    user = models.ForeignKey(User, unique=True, verbose_name='user')

    slug = models.SlugField(max_length=255)

    about = models.TextField('about', blank=True)

    from resrc.language.models import Language
    languages = models.ManyToManyField(Language)

    # karma = models.IntegerField('karma', null=True, blank=True)

    show_email = models.BooleanField('show_email', default=False)

    # favs = models.ManyToManyField(Link)

    def save(self, *args, **kwargs):
        self.do_unique_slug()
        super(Profile, self).save(*args, **kwargs)

    def do_unique_slug(self):
        """
        Ensures that the slug is always unique for this post
        """
        if not self.id:
            # make sure we have a slug first
            if not len(self.slug.strip()):
                self.slug = slugify(self.user.username)

            self.slug = self.get_unique_slug(self.slug)
            return True

        return False

    def get_unique_slug(self, slug):
        """
        Iterates until a unique slug is found
        """
        orig_slug = slug
        counter = 1

        while True:
            profiles = Profile.objects.filter(slug=slug)
            if not profiles.exists():
                return slug

            slug = '%s-%s' % (orig_slug, counter)
            counter += 1

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return urlresolvers.reverse("user-url", args=(self.slug, ))

    # Links
    def get_links(self):
        from resrc.link.models import Link
        return Link.objects.all().filter(owner__pk=self.user.pk)

    def get_link_count(self):
        return self.get_links().count()

    # Lists
    def get_lists(self):
        from resrc.list.models import List
        return List.objects.filter(owner__pk=self.user.pk)

    def get_list_count(self):
        return self.get_lists().count()

    def get_public_lists(self):
        return self.get_lists().filter(is_public=True)

    def get_private_lists(self):
        return self.get_tutorials().filter(is_public=False)

    # karma
    def get_karma(self):
        user = self.user
        karma = 0
        from resrc.link.models import Link
        links = Link.objects.filter(author=user)
        for link in links:
            karma = karma + link.get_votes()
            karma = karma + link.get_comment_count()

        from resrc.list.models import List
        lists = List.objects.filter(owner=user)
        for alist in lists:
            karma = karma + alist.get_votes()
            karma = karma + alist.get_comment_count()
        print karma
