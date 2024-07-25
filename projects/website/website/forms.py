"""
This module defines a Django form for inputting date ranges and market choices
for gap detection.

Classes:
    DateForm: A form for inputting start date, end date, specific date, and market choice.
"""

from django import forms

class DateForm(forms.Form):
    """
    A form for inputting date ranges and market choices for gap detection.

    Attributes:
        start_date (forms.DateField): The start date for the date range.
        end_date (forms.DateField): The end date for the date range.
        specific_date (forms.DateField): A specific date within the date range.
        market (forms.ChoiceField): The market choice, one of 'USA', 'Denmark', or 'Sweden'.
    """

    start_date: forms.DateField = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date: forms.DateField = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    specific_date: forms.DateField = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    market: forms.ChoiceField = forms.ChoiceField(choices=[('USA', 'USA'),
                                                           ('Denmark', 'Denmark'),
                                                           ('Sweden', 'Sweden')])

