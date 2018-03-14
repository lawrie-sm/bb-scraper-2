from django import forms

class SPSearchForm(forms.Form):
    q = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter search term...'}))