# coding: utf-8

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Fieldset, Submit, Field, ButtonHolder, HTML


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
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(  # FIXME : css classes here and form_class
            Field('title', css_class='asdf'),
            Field('url', css_class='asdf'),
            Field('tags'),
            Submit('submit', 'Add'),
        )
        super(NewLinkForm, self).__init__(*args, **kwargs)
