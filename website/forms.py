from django import forms

class MovieForm(forms.Form):
    name = forms.CharField(label='NAME', max_length=100)
    year = forms.IntegerField(label='YEAR')
    date = forms.DateField(label='DATE', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    rating = forms.DecimalField(label='MY RATING', max_digits=3, decimal_places=1)
    comments = forms.CharField(label='COMMENTS', max_length=500, required=False)
    password = forms.CharField(label='PASSWORD', max_length=100, widget=forms.PasswordInput)
