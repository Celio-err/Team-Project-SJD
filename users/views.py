from django.shortcuts import get_object_or_404, render, redirect
from .models import Estudante, Professor
from academic.models import Klase
from django.core.paginator import Paginator
from django.db.models import Q 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bemvindu mai iha Dashboard, {username}!")
                return redirect('dashboard') # Ganti ke nama URL dashboard Anda
            else:
                messages.error(request, "Username ka Password sala.")
        else:
            messages.error(request, "Username ka Password sala.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login_form.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Ita sai ona husi sistema.")
    return redirect('login')


def dashboard_view(request):
    # Data Siswa
    total_estudante = Estudante.objects.count()
    total_mane = Estudante.objects.filter(sexu='Mane').count()
    total_feto = Estudante.objects.filter(sexu='Feto').count()
    
    # Data Departementu
    total_cn = Estudante.objects.filter(klase__departamentu='CN').count()
    total_csh = Estudante.objects.filter(klase__departamentu='CSH').count()

    # Data Profesor (Asumsi Anda punya model Professor)
    total_professores = Professor.objects.count()
    prof_permanente = Professor.objects.filter(status='Permanente').count()
    prof_kontratadu = Professor.objects.filter(status='Kontratadu').count()
    prof_voluntariu = Professor.objects.filter(status='Voluntariu').count()

    context = {
        'total_estudante': total_estudante,
        'total_mane': total_mane,
        'total_feto': total_feto,
        'total_cn': total_cn,
        'total_csh': total_csh,
        'total_professores': total_professores,
        'prof_permanente': prof_permanente,
        'prof_kontratadu': prof_kontratadu,
        'prof_voluntariu': prof_voluntariu,
    }
    return render(request, 'dashboard.html', context)

#views estudante
def estudante_list_view(request):
    # 1. Ambil nilai pencarian dari URL (misal: ?q=Celio)
    query = request.GET.get('q', '').strip()
    
    # 2. Logika Filter
    if query:
        # Mencari berdasarkan Nama Lengkap ATAU Nomor Emis
        estudantes_list = Estudante.objects.filter(
            Q(naran_kompletu__icontains=query) | 
            Q(nu_emis__icontains=query)
        ).order_by('naran_kompletu')
    else:
        # Urutkan berdasarkan level kelas dan nama
        estudantes_list = Estudante.objects.all().order_by('klase__nivel', 'naran_kompletu')
    
    # 3. Pagination (10 data per halaman)
    paginator = Paginator(estudantes_list, 10)
    page_number = request.GET.get('page')
    estudantes = paginator.get_page(page_number)
    
    total_klase = Klase.objects.count()
    
    return render(request, 'users/lista_estudante.html', {
        'estudantes': estudantes,
        'total_klase': total_klase,
        'query': query
    })

def estudante_create_view(request, pk=None):
    klases = Klase.objects.all()
    # Pastikan data lama diambil untuk pengecekan
    estudante = get_object_or_404(Estudante, pk=pk) if pk else None
    
    if request.method == 'POST':
        # Gunakan .strip() untuk menghindari spasi tak sengaja yang bikin database bingung
        nu_emis = request.POST.get('nu_emis', '').strip()
        
        # --- LOGIKA CEK DUPLIKAT YANG LEBIH KUAT ---
        if nu_emis:
            check_emis = Estudante.objects.filter(nu_emis=nu_emis)
            
            # Jika sedang EDIT, abaikan record yang sedang kita pegang sekarang
            if pk:
                check_emis = check_emis.exclude(pk=pk)
                
            if check_emis.exists():
                messages.error(request, f"Erru!: Nu EMIS {nu_emis} eziste ona iha sistema!")
                return render(request, 'users/estudante_form.html', {
                    'klases': klases, 
                    'estudante': estudante, # Sangat penting agar Django tahu ini mode edit
                    'data': request.POST 
                })
        try:
            naran = request.POST.get('naran')
            sexu = request.POST.get('sexu')
            klase_id = request.POST.get('klase')
            klase_obj = Klase.objects.get(id=klase_id)
            foto = request.FILES.get('foto')

            if pk and estudante:
                # Proses UPDATE
                estudante.nu_emis = nu_emis
                estudante.naran_kompletu = naran
                estudante.sexu = sexu
                estudante.klase = klase_obj
                if foto:
                    estudante.foto = foto
                estudante.save()
                messages.success(request, f"Dadus {estudante.naran_kompletu} atualiza ona!")
            else:
                # Proses CREATE
                Estudante.objects.create(
                    nu_emis=nu_emis,
                    naran_kompletu=naran,
                    sexu=sexu,
                    klase=klase_obj,
                    foto=foto
                )
                messages.success(request, "Estudante foun rejistu ona!")
            
            return redirect('estudante_list')

        except Exception as e:
            messages.error(request, f"Erru iha tekniku: {e}")
            return render(request, 'users/estudante_form.html', {
                'klases': klases,
                'estudante': estudante,
                'data': request.POST
            })
            
    return render(request, 'users/estudante_form.html', {
        'klases': klases, 
        'estudante': estudante
    })

def hamoos_estudante(request, pk):
    estudante = get_object_or_404(Estudante, id=pk)
    if request.method == 'POST':
        estudante.delete()
        return redirect('estudante_list')
    return render(request, 'users/konfirm_delete_est.html', {'estudante': estudante})

def edit_estudante(request, pk):
    estudante = get_object_or_404(Estudante, id=pk)
    klases = Klase.objects.all()            
    if request.method == 'POST':

        estudante.nu_emis = request.POST.get('nu_emis')
        estudante.naran_kompletu = request.POST.get('naran')
        estudante.klase_id = request.POST.get('klase')
        estudante.sexu = request.POST.get('sexu')
        estudante.foto = request.FILES.get('foto')
        estudante.save()
        return redirect('estudante_list')
    return render(request, 'users/estudante_form.html', {
        'estudante': estudante, 
        'klases': klases
    })


#views professor
def professor_create_view(request):
    if request.method == 'POST':
        nis = request.POST.get('nis')
        id_funcionario = request.POST.get('id_funcionario')
        naran = request.POST.get('naran_kompletu')
        status = request.POST.get('status')
        nu_telemovel = request.POST.get('nu_telemovel')
        cargo = request.POST.get('cargo')
        
        # Validasaun Duplikadu
        if Professor.objects.filter(nis=nis).exists():
            return render(request, 'users/professor_form.html', {
                'error': f'NIS {nis} eziste ona!',
                'naran': naran
                })
        if Professor.objects.filter(id_funcionario=id_funcionario).exists():
            return render(request, 'users/professor_form.html', {
                'error': f'ID Funsionariu {id_funcionario} eziste ona!',
                'naran': naran
                })
        if Professor.objects.filter(nu_telemovel=nu_telemovel).exists():
            return render(request, 'users/professor_form.html', {
                'error': f'Nu Telemovel {nu_telemovel} eziste ona!',
                'naran': naran
                })
        if Professor.objects.filter(cargo=cargo).exists():
            return render(request, 'users/professor_form.html', {
                'error': f'Cargo {cargo} eziste ona!',
                'naran': naran
            })
        
        Professor.objects.create(
            nis=nis,
            id_funcionario=id_funcionario,
            naran_kompletu=naran,
            status=status,
            nu_telemovel=nu_telemovel,
            cargo=cargo
        )
        return redirect('professor_list')

    return render(request, 'users/professor_form.html')

def professor_list_view(request):
    # Mengurutkan berdasarkan nama secara alfabetis
    professores = Professor.objects.all().order_by('naran_kompletu')
    return render(request, 'users/lista_profesor.html', {'professores': professores})

def hamoos_profesor(request, pk):
    professor = get_object_or_404(Professor, id=pk)
    if request.method == 'POST':
        professor.delete()
        return redirect('professor_list')
    return render(request, 'users/konfirm_delete_prof.html', {'professor': professor})

def edit_professor(request, pk):
    professor = get_object_or_404(Professor, id=pk)

    if request.method == 'POST':
        professor.nis = request.POST.get('nis')
        professor.id_funcionario = request.POST.get('id_funcionario')
        professor.naran_kompletu = request.POST.get('naran_kompletu')
        professor.status = request.POST.get('status')
        professor.nu_telemovel = request.POST.get('nu_telemovel')
        professor.cargo = request.POST.get('cargo')

        # Validasaun Duplikadu (kecuali untuk dirinya sendiri)
        if Professor.objects.filter(nis=professor.nis).exclude(id=professor.id).exists():
            return render(request, 'users/professor_form.html', {
                'error': f'NIS {professor.nis} eziste ona!',
                'professor': professor
                })
        if Professor.objects.filter(id_funcionario=professor.id_funcionario).exclude(id=professor.id).exists():
            return render(request, 'users/professor_form.html', {
                'error': f'ID Funsionariu {professor.id_funcionario} eziste ona!',
                'professor': professor
                })
        if Professor.objects.filter(nu_telemovel=professor.nu_telemovel).exclude(id=professor.id).exists():
            return render(request, 'users/professor_form.html', {
                'error': f'Nu Telemovel {professor.nu_telemovel} eziste ona!',
                'professor': professor
                })
        if Professor.objects.filter(cargo=professor.cargo).exclude(id=professor.id).exists():
            return render(request, 'users/professor_form.html', {
                'error': f'Cargo {professor.cargo} eziste ona!',
            })

        professor.save()
        return redirect('professor_list')

    return render(request, 'users/professor_form.html', {
        'professor': professor
    })


