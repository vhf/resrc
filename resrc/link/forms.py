# coding: utf-8

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Row, Column, Submit, Field


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
                    Submit('submit', 'Add', css_class='small button'),
                    css_class='large-12',
                ),
            )
        )
        super(NewLinkForm, self).__init__(*args, **kwargs)
