from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import UsersCustomUser
from django.contrib.auth import get_user_model
from apps.lugar.models import Lugar
from apps.equipo.models import Equipo

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



User = get_user_model() # Esto obtiene tu modelo UsersCustomUser

class UserCreateForm(forms.ModelForm):
    # Campos de contraseña que no están en el modelo, pero son necesarios
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'border rounded p-2 w-full'}), 
        label="Contraseña"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'border rounded p-2 w-full'}), 
        label="Confirmar Contraseña"
    )

    class Meta:
        model = User
        # Lista de campos que manejará el formulario
        fields = [
            'username', 'email', 'password',
            'codigo', 'role', 'id_equipo', 'id_lugar', 'is_active', 'firma',
            'nombre', 'apellido_p', 'apellido_m', 'telefono',
        ]
        
        # Aplicamos las clases de Tailwind a los widgets
        widgets = {
            'username': forms.TextInput(attrs={'class': 'border rounded p-2 w-full', 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'border rounded p-2 w-full', 'placeholder': 'correo@ejemplo.com'}),
            'codigo': forms.TextInput(attrs={'class': 'border rounded p-2 w-full', 'placeholder': 'Ingresa el código'}),
            'role': forms.Select(attrs={'class': 'border rounded p-2 w-full'}),
            'id_equipo': forms.Select(attrs={'class': 'border rounded p-2 w-full'}),
            'id_lugar': forms.Select(attrs={'class': 'border rounded p-2 w-full'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded h-5 w-5'}),
            'firma': forms.FileInput(attrs={'class': 'border rounded p-1 w-full'}),
            'nombre': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'apellido_p': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'apellido_m': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'telefono': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populamos los QuerySets de los 'select'
        self.fields['id_equipo'].queryset = Equipo.objects.all()
        self.fields['id_lugar'].queryset = Lugar.objects.all()
        
        # Añadimos el 'placeholder' para los 'select'
        self.fields['id_equipo'].empty_label = "-- Selecciona un equipo --"
        self.fields['id_lugar'].empty_label = "-- Selecciona un lugar --"

        # Hacemos que los campos opcionales del modelo no sean requeridos en el form
        self.fields['id_equipo'].required = False
        self.fields['id_lugar'].required = False
        self.fields['firma'].required = False
        self.fields['codigo'].required = False
        self.fields['nombre'].required = False
        self.fields['apellido_p'].required = False
        self.fields['apellido_m'].required = False
        self.fields['telefono'].required = False

    def clean_password_confirm(self):
        # Validación para asegurar que las contraseñas coinciden
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password_confirm

    def save(self, commit=True):
        # Sobrescribimos el 'save' para hashear la contraseña
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
