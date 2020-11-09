from django import forms

from uploaddoc.models import UploadDoc


class UploadDocForm(forms.ModelForm):
    class Meta:
        model = UploadDoc
        fields = ('uploaddoc_scope', 'uploaddoc_type', 'uploaddoc_year', 'uploaddoc_fpath')
