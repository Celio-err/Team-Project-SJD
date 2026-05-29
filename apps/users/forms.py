from django import forms
from django.contrib.auth.models import User
from .models import Professor

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

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            return user