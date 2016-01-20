from django import forms

from .models import Siswa

class SigninForm(forms.ModelForm):
	class Meta:
		model = Siswa
		fields = ('nomor_induk',)