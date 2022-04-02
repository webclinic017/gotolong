from django import forms

from django_gotolong.uploaddoc.models import UploadDocModel


class UploadDocForm(forms.ModelForm):
    class Meta:
        model = UploadDocModel
        fields = ('uploaddoc_scope', 'uploaddoc_type', 'uploaddoc_year', 'uploaddoc_fpath')
