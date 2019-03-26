from django import forms
from .model import Desk


class DeskModelForm(forms.ModelForm):
    class Meta:
        model = Desk
        fields = [
            'description',
            'name'
        ]
