from django.forms import ModelForm, Form
from .models import Fratio


class FratioForm(ModelForm):
    class Meta:
        model = Fratio
        exclude = ('id',)
