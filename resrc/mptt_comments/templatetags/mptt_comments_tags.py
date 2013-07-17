from django.contrib import comments
from django.contrib.comments.templatetags.comments import BaseCommentNode, CommentListNode
from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_unicode
from django.db.models import Max, Count

register = template.Library()

class BaseMpttCommentNode(BaseCommentNode):
    
    def __init__(self, ctype=None, object_pk_expr=None, object_expr=None, as_varname=None, root_only=False, with_parent=None, reverse=False, flat=False, comment=None, **kwargs):
        super(BaseMpttCommentNode, self). __init__(ctype=ctype, object_pk_expr=object_pk_expr, object_expr=object_expr, as_varname=as_varname, comment=comment)
        self.with_parent = with_parent
        self.root_only = root_only
        self.reverse = reverse
        self.flat = flat
        if self.reverse and not self.root_only:
            raise template.TemplateSyntaxError("'reverse' option is only available with root-only ('comments-more' link at toplevel expects normal order)")
            
    def handle_token(cls, parser, token):
        """
            Class method to parse get_comment_list/count/form and return a Node.

            Forked from django.contrib.comments.templatetags. with_parent, 
            root-only concepts borrowed from django-threadedcomments.
        """
        tokens = token.contents.split()
        
        with_parent = None
        extra_kw = {}
        extra_possible_kw = ('root_only', 'flat', 'reverse', 'sort=mostcommented', 'sort=mostrecentreplies')
        for dummy in extra_possible_kw:
            if tokens[-1] in extra_possible_kw:
                split = str(tokens.pop()).split('=')
                key = split[0]
                extra_kw[key] = len(split) > 1 and split[1] or True

        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        # {% get_whatever for obj as varname %}
        # {% get_whatever for obj as varname with parent %}
        if len(tokens) == 5 or len(tokens) == 7:
            if tokens[3] != 'as':
                raise template.TemplateSyntaxError("Third argument in %r must be 'as'" % tokens[0])
            if len(tokens) == 7:
                if tokens[5] != 'with':
                    raise template.TemplateSyntaxError("When 6 arguments are given, fifth argument in %r must be 'with' followed by the parent commment wanted" % tokens[0])
                with_parent = tokens[6]
            return cls(
                object_expr = parser.compile_filter(tokens[2]),
                as_varname = tokens[4],
                with_parent = with_parent,
                **extra_kw
            )

        # {% get_whatever for app.model pk as varname %}
        # {% get_whatever for app.model pk as varname with parent %}
        elif len(tokens) == 6 or len(tokens) == 8:
            if tokens[4] != 'as':
                raise template.TemplateSyntaxError("Fourth argument in %r must be 'as'" % tokens[0])
            if len(tokens) == 8:
                if tokens[6] != 'with':
                    raise template.TemplateSyntaxError("When 6 arguments are given, fifth argument in %r must be 'with' followed by the parent commment wanted" % tokens[0])
                with_parent = tokens[7]
            return cls(
                ctype = BaseCommentNode.lookup_content_type(tokens[2], tokens[0]),
                object_pk_expr = parser.compile_filter(tokens[3]),
                as_varname = tokens[5],
                with_parent = with_parent,
                **extra_kw
            )

        else:
            raise template.TemplateSyntaxError("%r tag requires 4, 5, 6 or 7 arguments" % tokens[0])

    handle_token = classmethod(handle_token)
        
class MpttCommentFormNode(BaseMpttCommentNode):
    """Insert a form for the comment model into the context."""
            
    def get_form(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if object_pk:
            return comments.get_form()(ctype.get_object_for_this_type(pk=object_pk), 
                                       parent_comment=None)
        else:
            return None

    def render(self, context):
        context[self.as_varname] = self.get_form(context)
        return ''
        
class MpttCommentTopLevelCountNode(BaseMpttCommentNode):

    """Insert a count of toplevel comments into the context."""

    def get_context_value_from_queryset(self, context, qs):
        return qs.filter(level=0).order_by().count()
        
class MpttCommentHiddenCountNode(BaseMpttCommentNode):

    """Insert a count of hidden comments into the context."""
    
    def get_query_set(self, context):
        # Copied from django.contrib.comments, but changing the is_public filter
        # Too bad you can't "unfilter" a queryset... :(
        
        ctype, object_pk = self.get_target_ctype_pk(context)
        if not object_pk:
            return self.comment_model.objects.none()

        qs = self.comment_model.objects.filter(
            content_type = ctype,
            object_pk    = smart_unicode(object_pk),
            site__pk     = settings.SITE_ID,
        )
        
        # The is_public and is_removed fields are implementation details of the
        # built-in comment model's spam filtering system, so they might not
        # be present on a custom comment model subclass. If they exist, we 
        # should filter on them.
        field_names = [f.name for f in self.comment_model._meta.fields]
        if 'is_public' in field_names:
            qs = qs.filter(is_public=False) # changed line is here
        if getattr(settings, 'COMMENTS_HIDE_REMOVED', True) and 'is_removed' in field_names:
            qs = qs.filter(is_removed=False)
        
        return qs
            
    def get_context_value_from_queryset(self, context, qs):
        return qs.count()
        
class MpttCommentListNode(BaseMpttCommentNode):

    offset = getattr(settings, 'MPTT_COMMENTS_OFFSET', 20)
    toplevel_offset = getattr(settings, 'MPTT_COMMENTS_TOPLEVEL_OFFSET', 20)
    cutoff_level = getattr(settings, 'MPTT_COMMENTS_CUTOFF', 3)
    bottom_level = 0 
    
    def get_query_set(self, context):
        qs = super(MpttCommentListNode, self).get_query_set(context)
        cutoff = self.cutoff_level
        
        if self.with_parent:
            if self.with_parent in context:
                parent = context[self.with_parent]
            else:
                try:
                    parent = int(self.with_parent)
                except ValueError:
                    raise template.TemplateSyntaxError("'%s' doesn't represent a known variable in the context or a tree_id" % self.with_parent)

            if isinstance(parent, int):
                # Interpret parent as a tree_id. 
                # Note: in this mode, we include the corresponding root-node too
                self.bottom_level = 0
                qs = qs.filter(tree_id=parent)
            else:
                # Interpret parent as a comment object
                qs = qs.filter(tree_id=parent.tree_id, lft__gt=parent.lft, rght__lt=parent.rght)
                self.bottom_level = parent.level + 1

        if self.flat:
            qs = qs.order_by('submit_date')
            return qs
        elif self.root_only:
            cutoff = 0
            
        if cutoff >= 0:
            qs = qs.filter(level__lte=cutoff)
        
        return qs
        
    def get_context_value_from_queryset(self, context, qs):
        if self.reverse:
            qs = qs.reverse()
        offset = self.get_offset()
        if offset > 0:
            return list(qs[:offset])
        # if offset <= 0, don't list(): the developer will use its own pagination system
        return qs 
        
    def get_offset(self):
        if self.root_only:
            return self.toplevel_offset
        else:
            return self.offset
        
    def render(self, context):
        qs = self.get_query_set(context)
        context[self.as_varname] = self.get_context_value_from_queryset(context, qs)
        
        # 'Remaining comments' : if offset is <= 0, we don't handle those
        if self.get_offset() > 0:
            comments_remaining = qs.count()
            comments_remaining = (comments_remaining - self.get_offset()) > 0 and comments_remaining - self.get_offset() or 0
            
            # If we have a parent, then we need to update the subcomments_remaining to paginate
            # each thread independantly.
            if self.with_parent:
                context['subcomments_remaining'] = comments_remaining
            else:
                context['subcomments_remaining'] = 0
                context['comments_remaining'] = comments_remaining
        else:
            context['comments_remaining'] = 0
            context['subcomments_remaining'] = 0
            
        context['collapse_levels_above'] = getattr(settings, 'MPTT_COMMENTS_COLLAPSE_ABOVE', 2)
        context['cutoff_level'] = self.cutoff_level
        context['bottom_level'] = self.bottom_level
        return ''
        
class MpttSpecialTreeListNode(MpttCommentListNode):

    def __init__(self, sort=None, **kwargs):
        super(MpttSpecialTreeListNode, self).__init__(**kwargs)
        self.sort = sort
        
        # Just to be sure, overwrite those, which shouldn't be used, they would
        # mess with our special queries
        self.with_parent = None
        self.flat = False
        self.root_only = False
   
    def get_query_set(self, context):
        qs = super(MpttSpecialTreeListNode, self).get_query_set(context)
        
        if self.sort == 'mostcommented':
            qs = qs.values_list('tree_id', flat=True).filter(level=0).order_by('-rght')                
        elif self.sort == 'mostrecentreplies':
            qs = qs.values_list('tree_id', flat=True).annotate(max_date=Max('submit_date')).order_by('-max_date')
        return qs

def get_mptt_comment_hidden_count(parser, token):
    """
    Gets the non public comment count for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.

    Syntax::

        {% get_mptt_comment_hidden_count for [object] as [varname]  %}
        {% get_mptt_comment_hidden_count for [app].[model] [object_id] as [varname]  %}

    """

    return MpttCommentHiddenCountNode.handle_token(parser, token)
        
def get_mptt_comment_toplevel_count(parser, token):
    """
    Gets the toplevel comment count for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.

    Syntax::

        {% get_mptt_comment_toplevel_count for [object] as [varname]  %}
        {% get_mptt_comment_toplevel_count for [app].[model] [object_id] as [varname]  %}

    """

    return MpttCommentTopLevelCountNode.handle_token(parser, token)
    
def get_mptt_comments_threads(parser, token):
    """
    Gets the list of threads for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.
    
    Note: This list just contains the tree_ids of each thread
    """
    return MpttSpecialTreeListNode.handle_token(parser, token)

        
def get_mptt_comment_list(parser, token):
    """
    Gets the list of comments for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.

    Syntax::

        {% get_comment_list for [object] as [varname]  %}
        {% get_comment_list for [app].[model] [object_id] as [varname]  %}

    Example usage::

        {% get_comment_list for event as comment_list %}
        {% for comment in comment_list %}
            ...
        {% endfor %}

    """
    return MpttCommentListNode.handle_token(parser, token)


def get_mptt_comment_form(parser, token):
    """
    Get a (new) form object to post a new comment.

    Syntax::

        {% get_comment_form for [object] as [varname] %}
        {% get_comment_form for [app].[model] [object_id] as [varname] %}
    """
    return MpttCommentFormNode.handle_token(parser, token)


def mptt_comment_form_target():
    """
    Get the target URL for the comment form.

    Example::

        <form action="{% comment_form_target %}" method="POST">
    """
    return comments.get_form_target()

def children_count(comment):
    return (comment.rght - comment.lft) / 2

def mptt_comments_media():

    return mark_safe( render_to_string( ('comments/comments_media.html',) , { }) )
    
def mptt_comments_media_css():

    return mark_safe( render_to_string( ('comments/comments_media_css.html',) , { }) )
    
def mptt_comments_media_js():

    return mark_safe( render_to_string( ('comments/comments_media_js.html',) , { }) )
    
def display_comment_toplevel_for(target):

    model = target.__class__
        
    template_list = [
        "comments/%s_%s_display_comments_toplevel.html" % tuple(str(model._meta).split(".")),
        "comments/%s_display_comments_toplevel.html" % model._meta.app_label,
        "comments/display_comments_toplevel.html"
    ]
    return render_to_string(
        template_list, {
            "object" : target
        } 
        # RequestContext(context['request'], {})
    )

class MpttCommentCollapseState(template.Node):
    def __init__(self, token):
        tokens = token.contents.split()
        
        if len(tokens) < 2:
            raise template.TemplateSyntaxError("%s takes one argument" % tokens[0])
        
        self.varname = tokens[1]

    def render(self, context):
        if not self.varname in context:
            raise template.TemplateSyntaxError("%s is an invalid context variable" % self.varname)
        
        comment = context[self.varname]
        collapse_levels_above = 'collapse_levels_above' in context and context['collapse_levels_above'] or 1e308
        collapse_levels_below = 'collapse_levels_below' in context and context['collapse_levels_below'] or -1e308        
        
        classname = ""
        
        if 'post_was_successful' in context:
            return "comment_expanded"
        else:
            if comment.level > collapse_levels_above or comment.level < collapse_levels_below:
                return "comment_collapsed"
            return "comment_expanded"

def mptt_comment_print_collapse_state(parser, token):

    return MpttCommentCollapseState(token)

register.filter(children_count)
register.tag(get_mptt_comment_form)
register.tag(mptt_comment_print_collapse_state)
register.simple_tag(mptt_comment_form_target)
register.simple_tag(mptt_comments_media)
register.simple_tag(mptt_comments_media_css)
register.simple_tag(mptt_comments_media_js)
register.tag(get_mptt_comment_list)
register.tag(get_mptt_comments_threads)
register.tag(get_mptt_comment_hidden_count)
register.tag(get_mptt_comment_toplevel_count)
register.simple_tag(display_comment_toplevel_for)
