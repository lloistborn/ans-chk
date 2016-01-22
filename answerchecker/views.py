from django.shortcuts import render, redirect, Http404, HttpResponse
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
	if request.method != 'POST':
		raise Http404('Not allowed')
	try:
		siswa = Siswa.objects.get(nomor_induk = request.POST['nomor_induk'])
		request.session['id_siswa'] = siswa.nomor_induk

		return redirect('memulai')
	except Siswa.DoesNotExist:
		return HttpResponse('Siswa tidak terdaftar')

def logout(request):
	try:
		del request.session['id_siswa']
	except KeyError:
		pass	
	return HttpResponse('Logged out')

def memulai(request):
	title_page = 'Simulasi soal'
	id_siswa = request.session['id_siswa']

	try:
		soal = Soal.objects.all()
	except Soal.DoesNotExist:
		return HttpResponse('Soal tidak tersedia')

	return render(
		request, 
		'answerchecker/mulai.html', {
			'title_page': title_page,
			'id_siswa': id_siswa,
			'soal': soal,
		})