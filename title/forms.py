from django import forms
from .models import Title

class TitleForm(forms.ModelForm):
    
    class Meta:
        model = Title

        fields = ["title_name", "title_bound"]