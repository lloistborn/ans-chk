from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import SigninForm

from .models import Siswa, Soal, Hasil

def login_view(request):
	title_page = 'Login user'

	form = SigninForm()

	return render(request, 'answerchecker/login.html', {
				'title_page'	: title_page,
				'form'			: form						
		})

def login(request):
	# create logic here when user loging in

# def memulai(request):
	