from django import forms

class PointsForm(forms.Form):
    amount = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={'cols': 1, 'placeholder': '0.00'}
        ),
        label='Enter Amount Here',
        help_text='You must Enter a Number',
        )
        
class CSVForm(forms.Form):
    file = forms.FileField(label='')