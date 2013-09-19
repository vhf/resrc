# coding: utf-8
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Row, Column, Submit, Field
from django.conf import settings

from resrc.tag.models import Language


LEVELS = ['beginner', 'intermediate', 'advanced']


class NewLinkForm(forms.Form):
    title = forms.CharField(
        label='Title',
        max_length=120
    )

    url = forms.URLField(label='URL')

    tags = forms.CharField(
        label='Tags',
        max_length=120,
        required=False
    )

    level = forms.ChoiceField(label='Level', choices=zip(LEVELS, LEVELS), required=False)

    #display a select with languages ordered by most used first
    from resrc.tag.models import Language
    from django.db.models import Count
    used_langs = Language.objects.all().annotate(c=Count('link')).order_by('-c').values_list()
    used_langs = [x[1] for x in used_langs]
    lang_choices = []
    for lang in used_langs:
        lang_choices += [x for x in settings.LANGUAGES if x[0] == lang]
    lang_choices += [x for x in settings.LANGUAGES if x not in lang_choices]

    language = forms.ChoiceField(label='Language', choices=lang_choices)

    def __init__(self, *args, **kwargs):
        from django.core.urlresolvers import reverse
        self.helper = FormHelper()
        self.helper.form_action = reverse("new-link")
        self.helper.form_class = ''
        self.helper.form_method = 'post'
        self.helper.form_id = 'create-link-form'

        self.helper.layout = Layout(
            Row(
                Column(
                    Field('url'),
                    css_class='large-12'
                ),
            ),
            Row(
                Column(
                    Field('title'),
                    css_class='large-12'
                ),
            ),
            Row(
                Column(
                    Field('tags'),
                    css_class='large-12'
                ),
            ),
            Row(
                Column(
                    Field('language'),
                    css_class='large-6'
                ),
                Column(
                    Field('level'),
                    css_class='large-6'
                ),
            ),
            Row(
                Column(
                    Submit('submit', 'Add', css_class='small button'),
                    css_class='large-12',
                ),
            )
        )
        super(NewLinkForm, self).__init__(*args, **kwargs)
