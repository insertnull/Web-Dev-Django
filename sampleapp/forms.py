from django import forms
from .models import *

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'quantity']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Item.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("An item with this name already exists.")
        return name 