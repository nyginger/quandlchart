from django.forms import ModelForm, TextInput
from .models import API_keys, Items_table

class ItemForm(ModelForm):
    class Meta:
        model=Items_table
        fields=['name']
        widgets={'name': TextInput(attrs={'class':'input', 'placeholder':'Search'})}