# coding: utf-8
from django import forms
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Row, Div, Column, Fieldset, Submit, Field, HTML


class NewListForm(forms.Form):
    title = forms.CharField(label='Title', max_length=80)
    description = forms.CharField(
        label='Description', required=False, widget=forms.Textarea())
    ordered = forms.BooleanField(label='ordered', required=False)
    private = forms.BooleanField(label='private', required=False)

    def __init__(self, link_pk, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'createlistform'
        self.helper.form_action = reverse('ajax-create-list', args=(link_pk,))

        self.helper.layout = Layout(
            Fieldset(
                u'Create a list',
                Row(
                    Column(
                        Field('title'), css_class='large-12'
                    ),
                ),
                Row(
                    Column(
                        Field('description'), css_class='large-12'
                    ),
                ),
                Row(
                    Column(
                        Field('ordered'), css_class='large-4'
                    ),
                    Column(
                        Field('private'), css_class='large-4'
                    ),
                ),
            ),
            Row(
                Column(
                    HTML('<a id="createlist" class="small button">Create</a><a id="createclose" class="small secondary button" style="display:none">Close</a>'), css_class='large-12'
                ),
            ),
        )
        super(NewListForm, self).__init__(*args, **kwargs)
