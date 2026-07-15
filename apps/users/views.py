from django.shortcuts import get_object_or_404, render, redirect
from .models import Estudante, Professor
from apps.academic.models import Klase, MisaunVizaun, IstoriaEskola
from django.core.paginator import Paginator
from django.db.models import Q 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .forms import UserCreateForm
from django.core.paginator import Paginator as DjangoPaginator
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
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
    return redirect('home')

def index_view(request):
    total_estudante = Estudante.objects.count()
    total_professores = Professor.objects.count()
    vizaun = MisaunVizaun.objects.filter(id=1).first()
    misaun = MisaunVizaun.objects.filter(id=2).first()
    istoria = IstoriaEskola.objects.first()
    

    context = {
         'total_estudante': total_estudante,
         'total_professores': total_professores,
         'vizaun': vizaun,
         'misaun': misaun,
         'istoria': istoria,
        
         
    }

    return render(request, 'home_portal.html', context)

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

    if not request.user.is_superuser:
        messages.error(request, "Ita-boot la iha permisaun ba asesu asaun refere!")
        return redirect('estudante_list')
    
    estudante = get_object_or_404(Estudante, id=pk)
    if request.method == 'POST':
        estudante.delete()
        return redirect('estudante_list')
    return render(request, 'users/konfirm_delete_est.html', {'estudante': estudante})

@login_required
def edit_estudante(request, pk):
    #grouping ba asaun edit estudante(so superuser mak bele asesu)
    if not request.user.is_superuser:
        messages.error(request, "Ita-boot la iha autorizasaun ba asaun refere!")
        return redirect ('estudante_list')
    
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
    if not request.user.is_superuser:
        messages.error(request, "Ita-boot la iha permisaun ba asesu asaun refere!")
        return redirect('professor_list')
    if request.method == 'POST':
        nis = request.POST.get('nis')
        id_funcionario = request.POST.get('id_funcionario')
        naran = request.POST.get('naran_kompletu')
        status = request.POST.get('status')
        nu_telemovel = request.POST.get('nu_telemovel')
        cargo = request.POST.get('cargo')
        
        # Konteks default untuk mengembalikan data input jika terjadi erru
        context_error = {
            'naran': naran,
            'request': request 
        }

        # 1. Validasaun Unik Data Pribadi (Pastikan Anda mengisi data berbeda saat test!)
        if Professor.objects.filter(nis=nis).exists():
            context_error['error'] = f'Erru! NIS {nis} eziste ona iha sistema!'
            return render(request, 'users/professor_form.html', context_error)
            
        if Professor.objects.filter(id_funcionario=id_funcionario).exists():
            context_error['error'] = f'Erru! ID Funsionariu {id_funcionario} eziste ona iha sistema!'
            return render(request, 'users/professor_form.html', context_error)
            
        if Professor.objects.filter(nu_telemovel=nu_telemovel).exists():
            context_error['error'] = f'Erru! Numeru Telemovel {nu_telemovel} eziste ona iha sistema!'
            return render(request, 'users/professor_form.html', context_error)
        
        #  2. VALIDASAUN KUNCI CARGO 
        # Hanya mengunci jika yang dipilih adalah Direktur
        if cargo == 'Diretor/a da Escola':
            if Professor.objects.filter(cargo='Diretor/a da Escola').exists():
                context_error['error'] = 'Erru! Kargu Diretor/a da Escola eziste ona. Eskola bele iha de\'it Diretór ida!'
                return render(request, 'users/professor_form.html', context_error)
        
        # Passa Validasi -> Simpan ke Database
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
        
        if professor.cargo == 'Diretor/a da Escola':
            if Professor.objects.filter(cargo='Diretor/a da Escola').exclude(id=professor.id).exists():
                return render(request, 'users/professor_form.html', {
                    'error': 'Erru! Kargu Diretor/a da Escola eziste ona. Eskola bele iha de\'it Diretór ida!',
                    'professor': professor
                })

        professor.save()
        return redirect('professor_list')

    return render(request, 'users/professor_form.html', {
        'professor': professor
    })

def is_admin(user):
    return user.is_superuser or user.is_staff

@user_passes_test(is_admin)
def user_list_view(request):
    # 1. Jalankan query data user
    user_query = User.objects.all().exclude(id=request.user.id).order_by('-id')

    # 2. Ambil parameter halaman dari URL (?page=1)
    page_number = request.GET.get('page')

    # 3. Buat objek paginasi dengan nama variabel yang sangat jelas
    sistema_paginator = DjangoPaginator(user_query, 10)
    
    # 4. Ambil data halaman spesifik
    user_data = sistema_paginator.get_page(page_number)

    # 5. Kirim data ke template
    return render(request, 'users/admin_user/user_list.html', {
        'user_data': user_data
    })

@user_passes_test(is_admin)
def user_create_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            # 1. Ambil data mentah dari form, JANGAN panggil form.save() dulu
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            profesor_terpilih = form.cleaned_data.get('professor')
            
            # 2. Buat objek User baru secara manual lewat memori (belum ke database)
            user_obj = User(
                username=username,
                email=email,
                is_superuser=False 
            )
            
            # 3. Setel password secara aman (di-hash)
            if password:
                user_obj.set_password(password)
            
            # 4. Tentukan status is_staff berdasarkan cargo profesor
            if profesor_terpilih:
                if profesor_terpilih.cargo == 'Diretor/a da Escola':
                    user_obj.is_staff = True
                else:
                    user_obj.is_staff = False
            else:
                user_obj.is_staff = False

            # 5. KUNCI TERAKHIR: Simpan objek user secara paksa ke database auth_user
            user_obj.save() 
            
            # 6. Hubungkan dengan profil profesor jika ada
            if profesor_terpilih:
                profesor_terpilih.user = user_obj
                profesor_terpilih.save()
                
                # Atur Grup Django
                if profesor_terpilih.cargo == 'Diretor/a da Escola':
                    group, created = Group.objects.get_or_create(name='Diretor')
                    user_obj.groups.add(group)
                else:
                    group, created = Group.objects.get_or_create(name='Professor')
                    user_obj.groups.add(group)
                
            messages.success(request, "Akun User foun kria ona ho susesu!")
            return redirect('user_list')
    else:
        form = UserCreateForm()
    return render(request, 'users/admin_user/user_form.html', {'form': form, 'title': 'Kria Akun User'})

@user_passes_test(is_admin)
def user_delete_view(request, pk):
    user_obj = get_object_or_404(User, id=pk)
    user_obj.delete()
    messages.success(request, "Konta refere hamoos ona!")
    return redirect('user_list')
    
@login_required
def perfil_view(request):
    user = request.user
    # Mengambil profil professor yang melekat pada user login (jika ada)
    professor_profile = getattr(user, 'professor_profile', None)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            # 1. Ambil data dari form input template
            full_name = request.POST.get('full_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            nu_telemovel = request.POST.get('nu_telemovel') # Field tambahan

            # 2. Update data pada model Auth User bawaan Django
            user.username = username
            user.email = email
            
            # Memisahkan full_name menjadi first_name & last_name untuk Django User (opsional)
            names = full_name.split(' ', 1)
            user.first_name = names[0]
            user.last_name = names[1] if len(names) > 1 else ''
            user.save()

            # 3. SINKRONISASI: Update data pada model Professor
            if professor_profile:
                professor_profile.naran_kompletu = full_name
                professor_profile.nu_telemovel = nu_telemovel
                professor_profile.save()

            messages.success(request, "Dadus perfil atualiza ho susesu!")
            return redirect('perfil') 
        
        elif 'change_password' in request.POST:
            password_tuan = request.POST.get('password_tuan')
            password_foun = request.POST.get('password_foun')
            konfirma_password = request.POST.get('konfirma_password')

            if not user.check_password(password_tuan):
                messages.error(request, "Password Atual la loos!")
                return redirect('perfil')

            if konfirma_password != password_foun:
                messages.error(request, "Password konfirmasaun la hanesan")
                return redirect('perfil')
            
            user.set_password(password_foun)
            user.save()

            update_session_auth_hash(request, user)
            messages.success(request, "Password Atualiza ho susesu!")
            return redirect('perfil')


    return render(request, 'users/perfil.html', {'user': user})

