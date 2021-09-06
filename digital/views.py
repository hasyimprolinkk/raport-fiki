from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from .decorators import tolakhalaman_ini, ijinkan_pengguna, pilihan_login

# Create your views here.
@login_required(login_url='login')
def pdf_report_create(request,pk, semester):
    siswa = Siswa.objects.get(id=pk)

    if semester == 'ganjil':
        nilai = Nilai.objects.filter(siswa=siswa.id, semester="GANJIL")
    else :
        nilai = Nilai.objects.filter(siswa=siswa.id, semester="GENAP")

    if nilai.first() is None:
        messages.error(request, f"Nilai siswa tersebut masih belum ada")
        return redirect('cetakraport')

    template_path = 'data/export_raport.html'
    context = {
        'siswa': siswa,
        'nilai': nilai,
        'detail': nilai.first()
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@tolakhalaman_ini
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cocokan = authenticate(request, username=username, password=password )
        if cocokan is not None:
            login(request, cocokan)
            return redirect('beranda')
        else:
            messages.error(request, f'Username/password salah')
            return redirect('login')
    context = {
        'page': 'Halaman Login',
        'menu': 'login',
    }
    return render(request, 'data/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@pilihan_login 
@ijinkan_pengguna(yang_diizinkan=['admin'])
def beranda(request):
    list_guru = Guru.objects.all()
    list_mapel = Mapel.objects.all()
    list_siswa = Siswa.objects.all()
    totalguru = list_guru.count()
    totalmapel = list_mapel.count()
    totalsiswa = list_siswa.count()
    context = {
        'menu' : 'beranda',
        'page' : 'Selamat datang di raport digital',
        'siswa' : totalsiswa,
        'guru' : totalguru,
        'mapel' : totalmapel
    }
    return render(request, 'data/beranda.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def guru(request):
    data = Guru.objects.order_by('-id')
    context ={
        "menu" : 'Form Guru',
        "page" : 'Form Karyawan',
        'dataguru' : data
    }
    return render(request, 'data/formguru.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def inputGuru(request):
    form = GuruForm()
    formguru = GuruForm(request.POST)
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username = username).first():
            messages.success(request, 'Username sudah ada.')
            return redirect('inputguru')

        if password1 != password2:
            messages.success(request, 'Password Tidak sama')
            return redirect('inputguru')
        # user
        if formguru.is_valid:
            user = User.objects.create_user(username=username)
            user.set_password(password1)
            user.is_active = True
            user.save()
            # user

            # Group
            akses_guru = Group.objects.get(name='guru')
            user.groups.add(akses_guru)
            # Group

            # Guru
            formsimpanguru = formguru.save()
            formsimpanguru.user = user
            formsimpanguru.save()
            # Guru
        
        return redirect('guru')

    context ={
        "menu" : 'Input guru',
        "page" : 'Halaman input guru',
        "formguru" : form
        
    }
    return render(request,'data/inputguru.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def updateGuru(request, pk):
    guruupdate = Guru.objects.get(id=pk)
    formguru = GuruForm(instance=guruupdate)
    if request.method == 'POST':
        form = GuruForm(data=request.POST, instance=guruupdate)
        update = form.save()
        # update.user = request.user
        # update.save()
        return redirect ('guru')

    context = {
        "menu" : 'edit guru',
        "page" : 'Halaman edit guru',
        "formguru" : formguru
        
    }
    return render(request, 'data/inputguru.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def deleteGuru(request, pk):
    guruhapus = Guru.objects.get(id=pk)
    if request.method == 'POST':
        guruhapus.delete()
        return redirect ('guru')
    context = {
        'menu':'delete guru',
        'page':'halaman delete guru',
        'formhapusguru': guruhapus
    }
    return render(request, 'data/delete_guru.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def mapel(request):
    data = Mapel.objects.order_by('-id')
    context ={
        "menu" : 'Form Mapel',
        "page" : 'Halaman mapel',
        'datamapel' : data
    }
    return render(request, 'data/formmapel.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def inputMapel(request):
    formmapel = MapelForm()
    if request.method =='POST':
        formsimpan = MapelForm(request.POST)
        if formsimpan.is_valid:
            formsimpan.save()
            return redirect('mapel')
    context = {
        'menu' : 'input mapel',
        'page' : 'Halaman input mapel',
        'form': formmapel
    }
    return render(request,'data/inputmapel.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def updateMapel(request, pk):
	mapelupdate = Mapel.objects.get(id=pk)
	formmapel = MapelForm(instance=mapelupdate)
	if request.method == 'POST':
		formedit = MapelForm(request.POST, instance=mapelupdate)
		if formedit.is_valid:
			formedit.save()
			return redirect('mapel')
	context = {
		'menu': 'Edit santri',
        'page': 'Halaman update santri',
		'form': formmapel
	}
	return render(request, 'data/inputmapel.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def deleteMapel(request, pk):
    mapelhapus = Mapel.objects.get(id=pk)
    if request.method == 'POST':
        mapelhapus.delete()
        return redirect ('mapel')
    context = {
        'menu':'delete mapel',
        'page':'halaman delete santri',
        'formhapusmapel': mapelhapus
    }
    return render(request, 'data/delete_mapel.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def rinciannilai(request):
    data = RincianNilai.objects.order_by('-id')
    context ={
        "menu" : 'Form Rincian Nilai',
        "page" : 'halaman rincian nilai',
        'datarinciannilai' : data
    }
    return render(request, 'data/formrinciannilai.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def inputRincianNilai(request):
    formrinciannilai = RincianNilaiForm()
    if request.method =='POST':
        formsimpan = RincianNilaiForm(request.POST)
        if formsimpan.is_valid:
            formsimpan.save()
            return redirect('rinciannilai')
    context = {
        'menu' : 'input rincian nilai',
        'page' : 'Halaman rincian nilai',
        'form': formrinciannilai
    }
    return render(request,'data/inputrinciannilai.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def updateRincianNilai(request, pk):
	rinciannilaiupdate = RincianNilai.objects.get(id=pk)
	formrinciannilai = RincianNilaiForm(instance=rinciannilaiupdate)
	if request.method == 'POST':
		formedit = RincianNilaiForm(request.POST, instance=rinciannilaiupdate)
		if formedit.is_valid:
			formedit.save()
			return redirect('rinciannilai')
	context = {
		'menu': 'Edit rincian nilai',
        'page': 'Halaman update rincian nilai',
		'form': formrinciannilai
	}
	return render(request, 'data/inputrinciannilai.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def deleteRincianNilai(request, pk):
    rinciannilaihapus = RincianNilai.objects.get(id=pk)
    if request.method == 'POST':
        rinciannilaihapus.delete()
        return redirect ('rinciannilai')
    context = {
        'menu':'delete rincian nilai',
        'page':'halaman delete rincian nilai',
        'formhapusrinciannilai': rinciannilaihapus
    }
    return render(request, 'data/delete_rinciannilai.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def siswa(request):
    data = Siswa.objects.order_by('-id')
    context ={
        "menu" : 'Form siswa',
        "page" : 'halaman siswa',
        'datasiswa' : data
    }
    return render(request, 'data/formsiswa.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def inputSiswa(request):
    form = SiswaForm()
    formsiswa = SiswaForm(request.POST)
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username = username).first():
            messages.success(request, 'Username sudah ada.')
            return redirect('inputsiswa')

        if password1 != password2:
            messages.success(request, 'Password Tidak sama')
            return redirect('inputsiswa')
        # user
        user = User.objects.create_user(username=username)
        user.set_password(password1)
        user.is_active = True
        user.save()
        # user


        # Group
        akses_siswa = Group.objects.get(name='siswa')
        user.groups.add(akses_siswa)
        # Group

        # Guru
        formsimpansiswa = formsiswa.save()
        formsimpansiswa.user = user
        formsimpansiswa.save()
        # Guru
        
        return redirect('siswa')

    context ={
        "menu" : 'Input Siswa',
        "page" : 'Halaman input siswa',
        "formsiswa" : form
        
    }
    return render(request,'data/inputsiswa.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def updateSiswa(request, pk):
    siswaupdate = Siswa.objects.get(id=pk)
    formsiswa = SiswaForm(instance=siswaupdate)
    if request.method == 'POST':
        form = SiswaForm(data=request.POST, instance=siswaupdate)
        form.save()
#         update.user = request.user
#         update.save()
        return redirect ('siswa')

    context = {
        "menu" : 'edit siswa',
        "page" : 'Halaman edit siswa',
        "formsiswa" : formsiswa
        
    }
    return render(request, 'data/inputsiswa.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def deleteSiswa(request, pk):
    siswahapus = Siswa.objects.get(id=pk)
    if request.method == 'POST':
        siswahapus.delete()
        return redirect ('siswa')
    context = {
        'menu':'delete siswa',
        'page':'halaman delete siswa',
        'formhapussiswa': siswahapus
    }
    return render(request, 'data/delete_siswa.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['guru']) 
def nilai(request):
    data = Nilai.objects.order_by('-id')
    context ={
        "menu" : 'Form Nilai',
        "page" : 'halaman nilai',
        'datanilai' : data
    }
    return render(request, 'data/formnilai.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['guru']) 
def inputNilai(request):
    formnilai = NilaiForm()
    formmapel = Mapel.objects.all()
    formrinci = RincianNilai.objects.all()
    if request.method =='POST':
        n_siswa = Siswa.objects.get(id=request.POST.get('siswa'))
        cek = Nilai.objects.filter(siswa=n_siswa,semester=request.POST.get('semester'), tahun_ajaran=request.POST.get('tahun_ajaran'))
        if cek.first() is not None:
            messages.error(request, f'Nilai dari siswa "{n_siswa}" pada semester {request.POST.get("semester")}, tahun ajaran {request.POST.get("tahun_ajaran")} tersebut sudah di inputkan')
            return redirect('tambahnilai')

        formsimpan = NilaiForm(request.POST)
        if formsimpan.is_valid:

            for i in range(1, int(formmapel.count())+1):
                nilai = Nilai.objects.create(
                    siswa_id=request.POST.get('siswa'),
                    kelompok=request.POST.get('kelompok'),
                    semester=request.POST.get('semester'),
                    tahun_ajaran=request.POST.get('tahun_ajaran'),
                    rincian_nilai_id=request.POST.get('rincian_nilai_' + str(i))
                    )
            
            return redirect('nilai')
    context = {
        'menu' : 'input nilai',
        'page' : 'Halaman input nilai',
        'form': formnilai,
        'mapel' : formmapel,
        'nilai' : formrinci
    }
    return render(request,'data/inputnilai.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['guru']) 
def deleteNilai(request, pk):
    nilaihapus = Nilai.objects.get(id=pk)
    if request.method == 'POST':
        nilaihapus.delete()
        return redirect ('nilai')
    context = {
        'menu':'delete nilai',
        'page':'halaman delete nilai',
        'formhapusnilai': nilaihapus
    }
    return render(request, 'data/delete_nilai.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['guru']) 
def cetakRaport(request):
    data = Siswa.objects.order_by('-id')
    context ={
        "menu" : 'Form cetak raport siswa',
        "page" : 'halaman cetak raport siswa',
        'datasiswa' : data
    }
    return render(request, 'data/cetakraport.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['siswa']) 
def cetakRaportSaya(request):
    data = Siswa.objects.filter(user=request.user)
    context ={
        "menu" : 'Form cetak raport siswa',
        "page" : 'halaman cetak raport siswa',
        'datasiswa' : data
    }
    return render(request, 'data/cetakraport.html', context)

# @login_required(login_url='login')
# def profile(request):

#     data = Siswa.objects.order_by('-id')
#     context ={
#         "menu" : 'Form Nilai',
#         "page" : 'halaman nilai',
#         'datanilai' : data
#     }
#     return render(request, 'data/formnilai.html', context)
