from django import forms
from core.models import ModelGroup
from django.forms import ModelForm
from dal import autocomplete

class GroupSearchForm(forms.ModelForm):
    class Meta:
        model = ModelGroup
        fields = ('number', )
        widgets = {
            'number': autocomplete.Select2(url='group-autocomplete')
        }

class SearchForm(forms.ModelForm):
    number = forms.ModelChoiceField(
        queryset=ModelGroup.objects.all(),
        widget=autocomplete.ModelSelect2(url='group-autocomplete')
    )

    class Meta:
        model = ModelGroup
        fields = ('number',)

def add_variable_to_context(request):
    return {
        'testme': GroupSearchForm()
    }