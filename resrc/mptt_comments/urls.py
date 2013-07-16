from django.conf.urls.defaults import *
from django.contrib.comments.urls import urlpatterns as contrib_comments_urlpatterns
from django.conf import settings

urlpatterns = patterns('resrc.mptt_comments.views',
                       url(r'^new/(\d+)/$',
                           'new_comment',
                           name='new-comment'
                           ),
                       url(r'^reply/(\d+)/$',
                           'new_comment',
                           name='comment-reply'
                           ),
                       url(r'^post/$',
                           'post_comment',
                           name='comments-post-comment'
                           ),
                       url(r'^posted-ajax/$',
                           'comment_done_ajax',
                           name='comments-comment-done-ajax'
                           ),
                       url(r'^more/(\d+)/$',
                           'comments_more',
                           name='comments-more'
                           ),
                       url(r'^replies/(\d+)/$',
                           'comments_subtree',
                           name='comments-subtree'
                           ),
                       url(r'^detail/(\d+)/$',
                           'comments_subtree',
                           name='comment-detail',
                           kwargs={
                               'include_self': True, 'include_ancestors': True}
                           )

                       )

urlpatterns += contrib_comments_urlpatterns
