from django import forms

class DateForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    specific_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    market = forms.ChoiceField(choices=[('USA', 'USA'), ('Denmark', 'Denmark'), ('Sweden', 'Sweden')])


