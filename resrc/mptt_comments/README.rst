====================
Django Mptt Comments
====================

Django Mptt Comments is a simple way to display threaded comments instead of the django contrib comments.

Installation
============

#. Get the required third party modules ::

    svn checkout http://django-mptt.googlecode.com/svn/trunk/mptt

    svn checkout http://django-template-utils.googlecode.com/svn/trunk/template_utils

#. Get Mptt Comments

    hg clone http://bitbucket.org/fivethreeo/django-mptt-comments/

#. Add the `resrc.mptt_comments` directory to your Python path.

#. Add the needed apps to `INSTALLED_APPS` ::

    'django.contrib.comments',
    'django.contrib.markup',
    'template_utils',
    'mptt',
    'resrc.mptt_comments'

#. Add `resrc.mptt_comments.urls` to your projects urlconf ::

    (r'^comments/', include('resrc.mptt_comments.urls')),

#. Add the required code to the objects detail page (see Usage)

#. Copy the templates to adapt them for your site

#. Style the forms using css

Usage
=====

In any detail template that wants to use `resrc.mptt_comments` ::

        {% block extrahead %}

        {% load resrc.mptt_comments_tags %}
        {% resrc.mptt_comments_media %}

        {% endblock extrahead %}

To display the toplevel tree in templates: ::

        {% load resrc.mptt_comments_tags %}

        {% display_comment_toplevel_for object %}


SETTINGS
========

MPTT_COMMENTS_OFFSET

    Number of comments displayed before 'read more' link appears

MPTT_COMMENTS_CUTOFF

    Depth of comments to be shown

MPTT_COMMENTS_SELECT_RELATED

    Additional related objects to be used in select_related call
    for example ['user__designer', 'user__designer__level']

    Use patch from ticket #7270 if you need reverse OneToOne lookups like in example above

TODO
====
- Make the more link work without javascript

Contributors
============
Михаил Сычёв (Mike)
