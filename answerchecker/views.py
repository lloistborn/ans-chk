from django.shortcuts import render, redirect, Http404, HttpResponse

from .forms import SigninForm

from .models import Siswa, Soal, Hasil

from multiprocessing import Process, Queue, Lock

from .preprocess import Preprocess
from .rabinkarpparallel import RabinKarpParallel
from .rabinkarpparallel import Shingle

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
		request.session['pk'] = siswa.pk

		print(request.session['pk'])

		return redirect('memulai')
	except Siswa.DoesNotExist:
		return HttpResponse('Siswa tidak terdaftar')

def logout(request):
	try:
		del request.session['pk']
	except KeyError:
		pass	
	return HttpResponse('Logged out')

def memulai(request):
	title_page = 'Simulasi soal'
	pk = request.session['pk']

	try:
		soal = Soal.objects.all()
	except Soal.DoesNotExist:
		return HttpResponse('Soal tidak tersedia')

	return render(
		request, 
		'answerchecker/mulai.html', {
			'title_page'	: title_page,
			'id_siswa'		: pk,
			'soal'			: soal,
			'nama_siswa'	: Siswa.objects.get(id=request.session['pk']),
		})

def get_skor(request):
	pp = Preprocess()
	shl = Shingle()
	prk = RabinKarpParallel()

	if request.method == 'POST':
		soal = Soal.objects.all()

		# result_prk = []
		k = 3
		processes = []
		R = Queue()
		L = Lock()
		similarity = 0

		for i, s in enumerate(soal):
			# jawaban asli
			txt = s.jawaban
			txt = txt.replace('\n', ' ').replace('\r', '')
			txt = pp.prep_text(txt)

			# jawaban dari siswa
			pattern = request.POST['jawaban%d' % (i+1)]
			pattern = pattern.replace('\n', ' ').replace('\r', '')
			pattern = pp.prep_text(pattern)		
			
			print('soal ', s.soal)
			print('jawaban asli -> ', txt)
			print('jawaban siswa -> ', pattern)

			patlen = len(pattern)

			d = int((patlen - 5 + 1) / k + 1)

			pattern = shl.wordshingling(pattern)
			print("pattern first")
			print(pattern)

			for j in range(k - 1):
				print('[%d][%d]' %(int(d * j), int((j + 1) * d) + 5 - 1))
				p = Process(target=prk.sim_measure, args=(int(d * j), int((j+1) * d) + 5 - 1, pattern, txt, R, L, )) 
				processes.append(p)
				p.start()

			print('[%d][%d]' %(int(d * (k-1)), patlen))
			p = Process(target=prk.sim_measure, args=(int(d * (k-1)), patlen, pattern, txt, R, L,)) 
			processes.append(p)
			p.start()

			for pr in processes:
				pr.join()

			while not R.empty():
				similarity += R.get()
				print(similarity)

			similarity = round(similarity * 100)
						
			# result_prk.append((fileOri, i, int(similarity), time_consumed))
			# print('sim = ', similarity)

			Hasil.objects.create(
				siswa 		= Siswa.objects.get(id=request.session['pk']), # harus diambil dari tabel Siswa karena foreign key
				soal 		= Soal.objects.get(id=s.id), # harus diambil dari tabel Soal karena foreign key
				jawaban 	= request.POST['jawaban%d' % (i+1)],
				skor		= similarity,
			)

			similarity = 0
			# print(i)



	return render(request, 'answerchecker/hasil.html', {
		'hasil'			: Hasil.objects.filter(siswa = Siswa.objects.get(id=request.session['pk'])),
		'id_siswa'		: request.session['pk'],
		'nama_siswa'	: Siswa.objects.get(id=request.session['pk']),
	})