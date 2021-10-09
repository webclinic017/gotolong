from django.forms import ModelForm, Form
from .models import Othinv


class OthinvForm(ModelForm):
    class Meta:
        model = Othinv
        exclude = ('othinv_user',)
