from django import forms
from .models import Url
class HomeForm(forms.ModelForm):
	url = forms.URLField(max_length=1000, label=False, widget=forms.TextInput(
		attrs={'placeholder': 'Enter your url'}))
	slug = forms.CharField(max_length=10, required=False, label=False, widget=forms.TextInput(
		attrs={'placeholder': 'Enter your slug'}))
	class Meta:
		model = Url
		fields = ['url', 'slug']