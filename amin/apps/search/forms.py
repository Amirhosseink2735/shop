from django import forms

class SearchForm(forms.Form):
    search_field=forms.CharField(label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"جستجو"}))