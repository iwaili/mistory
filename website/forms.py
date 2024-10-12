from django import forms

class MovieForm(forms.Form):
    name = forms.CharField(label='Movie Name', max_length=100)
    year = forms.IntegerField(label='Year', required=False)
    rating = forms.DecimalField(label='My Rating', max_digits=3, decimal_places=1)
    comments = forms.CharField(label='Comments', max_length=500, required=False, widget=forms.Textarea)
