from django import forms
from django.core.validators import RegexValidator
from .models import KokamaHistory

class AddNewHistory(forms.Form):
    
    history_title = forms.CharField(
        label='history_title',
        error_messages={'required': 'Preencha este campo.'}
    )
    
    history_text = forms.CharField(
        label='history_text',
        error_messages={'required': 'Preencha este campo.'}
    )
    
