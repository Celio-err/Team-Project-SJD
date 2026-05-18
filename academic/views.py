from urllib import request
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from academic.models import Disiplina, Klase, AlokasiMateria
from users.models import Professor, Estudante
from django.contrib import messages

# 1. View untuk membuat Disiplina Baru
def disiplina_create_view(request):
    if request.method == 'POST':
        naran = request.POST.get('naran_disiplina')
        kodigu = request.POST.get('kodigu')
        departamentu = request.POST.get('departamentu')

        # Validasi Naran
        if Disiplina.objects.filter(naran_disiplina=naran).exists():
            messages.error(request, f"Erru: Naran disiplina '{naran}' eziste ona!")
            return render(request, 'academic/disiplina_form.html', {
                'naran_disiplina': naran, 'kodigu': kodigu, 'departamentu': departamentu
            })
        
        # Validasi Kodigu
        if Disiplina.objects.filter(kodigu=kodigu).exists():
            messages.error(request, f"Erru: Kodigu '{kodigu}' eziste ona!")
            return render(request, 'academic/disiplina_form.html', {
                'naran_disiplina': naran, 'kodigu': kodigu, 'departamentu': departamentu
            })
        
        try:
            Disiplina.objects.create(
                naran_disiplina=naran,
                kodigu=kodigu,
                departamentu=departamentu
            )
            messages.success(request, "Disiplina rejistu ho susesu!")
            return redirect('disiplina_list')
        except Exception as e:
            messages.error(request, f"Erru tekniku: {e}")
            
    return render(request, 'academic/disiplina_form.html')

def disiplina_list_view(request):
    # Mengambil semua disiplina dan mengurutkan berdasarkan departemen
    disciplinas = Disiplina.objects.all().order_by('departamentu', 'naran_disiplina')
    return render(request, 'academic/lista_disiplina.html', {'disciplinas': disciplinas})

def hamoos_disiplina(request, pk):
    disiplina = get_object_or_404(Disiplina, id=pk) #Ambil data disiplina berdasarkan ID, jika tidak ada muncul 404
    if request.method == 'POST':
        disiplina.delete()
        return redirect('disiplina_list')
    return render(request, 'academic/konfirm_delete_disiplina.html', {'disiplina': disiplina})

def edit_disiplina(request, pk):
    disiplina = get_object_or_404(Disiplina, id=pk)
    if request.method == 'POST':
        naran = request.POST.get('naran_disiplina')
        kodigu = request.POST.get('kodigu')
        dept = request.POST.get('departamentu')

        if Disiplina.objects.filter(naran_disiplina=naran).exclude(id=pk).exists():
            messages.error(request, f"Erru: Naran '{naran}' kuseda iha ona!")
            return render(request, 'academic/disiplina_form.html', {'disiplina': disiplina})

        if Disiplina.objects.filter(kodigu=kodigu).exclude(id=pk).exists():
            messages.error(request, f"Erru: Kodigu '{kodigu}' kuseda iha ona!")
            return render(request, 'academic/disiplina_form.html', {'disiplina': disiplina})

        disiplina.naran_disiplina = naran
        disiplina.kodigu = kodigu
        disiplina.departamentu = dept
        disiplina.save()
        messages.success(request, "Dadus atualiza ho susesu!")
        return redirect('disiplina_list')

    return render(request, 'academic/disiplina_form.html', {'disiplina': disiplina})

# 2. View Utama Alokasaun (Modu Tabel / Admin Power)
def alokasaun_create(request):
    if request.method == 'POST':
        disiplina_id = request.POST.get('disiplina')
        klase_id = request.POST.get('klase')
        professor_id = request.POST.get('professor')

        # Simpan tanpa tinan_akademiku
        AlokasiMateria.objects.create(
            disiplina_id=disiplina_id,
            klase_id=klase_id,
            professor_id=professor_id,
        )
        
        messages.success(request, "Alokasaun foun kria ho susesu!")
        return redirect('alokasaun_list')

    context = {
        'disiplinas': Disiplina.objects.all(),
        'klases': Klase.objects.all(),
        'profesores': Professor.objects.all(),
    }
    return render(request, 'academic/konfig_alokasaun.html', context)

def hamoos_alokasaun(request, pk):
    # Jika ID 19 tidak ada di tabel AlokasiMateria, baris ini akan melempar 404
    objek = get_object_or_404(AlokasiMateria, id=pk)
    
    objek.delete()
    messages.success(request, "Dadus hamos ona!")
    return redirect('alokasaun_materia')

def alokasi_list(request):
    # 1. Ambil data asli dengan filter Anda
    alokasaun_query = AlokasiMateria.objects.filter(
        professor__isnull=False, 
        klase__isnull=False
    ).order_by('-id')
    
    paginator = Paginator(alokasaun_query, 10) 
    page_number = request.GET.get('page')
    alokasaun_data = paginator.get_page(page_number)
    
    return render(request, 'academic/alokasaun_list.html', {
        'alokasaun_data': alokasaun_data 
    })
# Halaman FORM saat nama disiplina diklik
def konfig_alokasaun(request, pk):
    alokasaun = get_object_or_404(AlokasiMateria, id=pk)
    
    if request.method == 'POST':
        alokasaun.klase_id = request.POST.get('klase')
        alokasaun.professor_id = request.POST.get('professor')
        alokasaun.disiplina_id = request.POST.get('disiplina')
        alokasaun.save()
        
        messages.success(request, "Alokasaun atualiza ho susesu!")
        return redirect('alokasaun_list')

    context = {
        'alokasaun': alokasaun,
        'disiplinas': Disiplina.objects.all(),
        'klases': Klase.objects.all(),
        'profesores': Professor.objects.all(),
        # Variable d_val dkk ini untuk 'selected' di template form
        'd_val': str(alokasaun.disiplina.id),
        'k_val': str(alokasaun.klase.id),
        'p_val': str(alokasaun.professor.id),
    }
    return render(request, 'academic/konfig_alokasaun.html', context)

#Views ba Klase
def klase_list_view(request):
    klases = Klase.objects.all().order_by('nivel', 'departamentu', 'turma')
    return render(request, 'academic/lista_klase.html', {'klases': klases})

def klase_create(request):
    if request.method == 'POST':
        nivel = request.POST.get('nivel')
        departamentu = request.POST.get('departamentu')
        turma = request.POST.get('turma')
        # Simpan ke database
        Klase.objects.create(
            nivel=nivel,
            departamentu=departamentu,
            turma=turma
        )
        return redirect('list_klase')
    # Ambil choices dari model Klase untuk ditampilkan di dropdown
    context = {
        'nivel_choices': Klase.NIVEL_CHOICES,
        'dept_choices': Klase.DEPARTAMENTU_CHOICES,
    }
    return render(request, 'academic/klase_form.html', context)

def hamoos_klase(request, pk):
    klase = get_object_or_404(Klase, id=pk)
    if request.method == 'POST':
        klase.delete()
    return redirect('list_klase')

def edit_klase(request, pk):
    klase = get_object_or_404(Klase, id=pk)

    if request.method == 'POST':
        klase.nivel = request.POST.get('nivel')
        klase.departamentu = request.POST.get('departamentu')
        klase.turma = request.POST.get('turma')
        klase.save()
        return redirect('list_klase')

    return render(request, 'academic/klase_form.html', {
        'klase': klase,
        'nivel_choices': Klase.NIVEL_CHOICES,
        'dept_choices': Klase.DEPARTAMENTU_CHOICES,
    })

def assign_professor(request, pk):
    alokasi = get_object_or_404(AlokasiMateria, id=pk)
    
    if request.method == 'POST':
        professor_id = request.POST.get('professor')
        alokasi.professor_id = professor_id
        alokasi.save()
        # Kembali ke detail kelas tersebut
        return redirect('klase_detail', pk=alokasi.klase.id)

    professores = Professor.objects.all()
    return render(request, 'academic/konfig_alokasaun.html', {
        'alokasi': alokasi,
        'professores': professores
    })

#views ba lista klase
def estudante_kada_klase(request, klase_id):
    klase = get_object_or_404(Klase, id=klase_id)
    estudantes = Estudante.objects.filter(klase=klase).order_by('naran_kompletu')
   
    context = {
        'klase': klase,
        'estudantes': estudantes
    }
    return render(request, 'academic/lista_prezensa.html', context)