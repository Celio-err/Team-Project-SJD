from django.shortcuts import render
from apps.users.models import Estudante, Professor
from apps.academic.models import Disiplina, Klase
from django.db.models import Q
import datetime
from .models import ValorFinalista
from apps.academic.models import Klase
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ValorFinalista, DokumentuSetting
from django.utils import timezone

def print_lista_prezensa(request, klase_id):
    """Mencetak daftar hadir siswa per kelas"""
    klase = get_object_or_404(Klase, id=klase_id)
    lista_estudante = Estudante.objects.filter(klase=klase).order_by('naran_kompletu')
    
    context = {
        'klase': klase,
        'lista_estudante': lista_estudante,
        'data_ohin': datetime.date.today(),
    }
    return render(request, 'attendance/print_prezensa.html', context)

def alokasi_create_view(request):
    """Form untuk membuat alokasi mata pelajaran"""
    if request.method == 'POST':
        # Logic simpan alokasi materia bisa ditambahkan di sini
        pass
    
    # Pastikan variabel ini didefinisikan dengan benar untuk dikirim ke context
    lista_professor = Professor.objects.all()
    lista_disiplina = Disiplina.objects.all()
    lista_klase = Klase.objects.all()
    
    return render(request, 'academic/alokasaun_form.html', {
        'professores': lista_professor,
        'disiplinas': lista_disiplina,
        'klases': lista_klase
    })


# ========================================================
# 2. FUNGSI DEKLARASAUN FINALISTA (ALUR LENGKAP)
# ========================================================

def lista_klase_finalista(request):
    """ALUR 1: Muncul Lista Klase (Hanya Nivel 12)"""
    klase_12 = Klase.objects.filter(nivel='12')
    return render(request, 'attendance/lista_klase.html', {
        'klase': klase_12
    })

def lista_estudante_finalista(request, klase_id):
    """ALUR 2: Klik Klase -> Muncul Lista Estudante di kelas tersebut"""
    klase = get_object_or_404(Klase, id=klase_id)
    estudantes = Estudante.objects.filter(klase=klase).order_by('naran_kompletu')
    return render(request, 'attendance/lista_estudante.html', {
        'klase': klase,
        'estudantes': estudantes
    })

def input_valor_estudante(request, estudante_id):
    estudante = get_object_or_404(Estudante, id=estudante_id)
    
    # Ambil disiplina yang sesuai dengan departemen mahasiswa
    disiplinas = Disiplina.objects.filter(
        Q(departamentu='Geral') | Q(departamentu=estudante.klase.departamentu)
    )

    if request.method == 'POST':
        try:
            # Loop setiap mata pelajaran untuk disimpan sebagai baris baru
            for d in disiplinas:
                nilai = request.POST.get(f'valor_{d.id}')
                
                if nilai:
                    # Update jika data sudah ada, atau buat baru jika belum ada
                    # Ini kunci agar 'disiplina_id' tidak NULL
                    ValorFinalista.objects.update_or_create(
                        estudante=estudante,
                        disiplina=d, # Kita masukkan disiplina di sini
                        defaults={'valor': nilai}
                    )
            
            messages.success(request, "Valor rai ho susesu!")
            return redirect('print_deklarasaun', estudante_id=estudante.id)
            
        except Exception as e:
            messages.error(request, f"Erru selama menyimpan data: {e}")

    return render(request, 'attendance/form_valor.html', {
        'estudante': estudante,
        'disiplinas': disiplinas,
    })

def print_deklarasaun(request, estudante_id):
    estudante = get_object_or_404(Estudante, id=estudante_id)
    # Ambil semua objek nilai milik mahasiswa ini
    lista_valor = ValorFinalista.objects.filter(estudante=estudante)
    
    # Hitung total secara dinamis untuk tfoot
    total_valor = sum(val.valor for val in lista_valor if val.valor)

    today = timezone.now()

    # AMBIL ATAU BUAT DATA SETTING (Penting!)
    # Ini memastikan variabel 'setting' tidak akan pernah None/Kosong
    setting, created = DokumentuSetting.objects.get_or_create(
        is_active=True, 
        defaults={'data_ezame': '14 a 20 de Outubru de 2026'}
    )

    # LOGIKA UNTUK MENERIMA INPUT DARI TEMPLATE
    if request.method == 'POST':
        data_input = request.POST.get('data_ezame')
        if data_input:
            setting.data_ezame = data_input
            setting.save()
            # Redirect kembali ke halaman yang sama agar data ter-refresh
            return redirect('print_deklarasaun', estudante_id=estudante_id)
        
    # Cari profesor yang menjabat sebagai Diretor/a da Escola
    diretor = Professor.objects.filter(cargo__icontains='Diretor').first()


    return render(request, 'attendance/print_deklarasaun.html', {
        'estudante': estudante,
        'lista_valor': lista_valor,
        'total_valor': total_valor,
        'diretor':diretor,
        'setting': setting,
        'today':today
    })

def angka_ke_teks(valor):
    map_angka = {
        0: 'Zero', 1: 'Ida', 2: 'Rua', 3: 'Tolu', 4: 'Haat', 
        5: 'Lima', 6: 'Neen', 7: 'Hitu', 8: 'Ualu', 9: 'Sia', 10: 'Sanulu'
    }
    # Jika Anda menggunakan Bahasa Portugis (Oito, Nove, dll):
    map_portugis = {
        0: 'Zero', 1: 'Um', 2: 'Dois', 3: 'Três', 4: 'Quatro', 
        5: 'Cinco', 6: 'Seis', 7: 'Sete', 8: 'Oito', 9: 'Nove', 10: 'Dez'
    }
    return map_portugis.get(int(valor), "")