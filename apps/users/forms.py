from django import forms
from django.contrib.auth.models import User
from ..academic.models import Professor

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-6 py-5 bg-slate-50 border-2 border-transparent rounded-[24px] font-extrabold text-slate-700 focus:bg-white focus:border-blue-500 transition-all outline-none shadow-sm'
    }))

    professor = forms.ModelChoiceField(
        queryset=Professor.objects.filter(user__isnull=True),
        required=False,
        empty_label="--Eskolla Professor--",
        widget=forms.Select(attrs={
            'class': 'w-full px-6 py-5 bg-slate-50 border-2 border-transparent rounded-[24px] font-extrabold text-slate-700 focus:bg-white focus:border-blue-500 transition-all outline-none shadow-sm'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-6 py-5 bg-slate-50 border-2 border-transparent rounded-[24px] font-extrabold text-slate-700 focus:bg-white focus:border-blue-500 transition-all outline-none shadow-sm'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-6 py-5 bg-slate-50 border-2 border-transparent rounded-[24px] font-extrabold text-slate-700 focus:bg-white focus:border-blue-500 transition-all outline-none shadow-sm'}),
        }

    # 🌟 URUTAN SUDAH BENAR: Sejajar dengan 'class Meta', di luar struktur Meta.
    def save(self, commit=True):
        # 1. Ambil objek user asli dari ModelForm
        user = super().save(commit=False)
        
        # 2. Ambil password yang diketik, lalu amankan (hash password)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
            
        # Biarkan view yang menentukan status is_superuser dan is_staff
        if commit:
            user.save()
        return user