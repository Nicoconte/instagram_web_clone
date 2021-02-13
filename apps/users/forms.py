from django import forms

class UserRegisterForm(forms.Form):
    email = forms.EmailField(label="", widget=forms.EmailInput(
        attrs={
            "class" : "form-control bg-light text-secondary mt-3",
            "placeholder" : "Correo electronico"
        }
    ))

    name = forms.CharField(label="", widget=forms.TextInput(
        attrs={
            "class" : "form-control bg-light mt-2 text-secondary",
            "placeholder" : "Nombre completo"
        }
    ))

    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={
            "class" : "form-control bg-light mt-2 text-secondary",
            "placeholder" : "Nombre de usuario"
        }
    ))

    password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={
            "class" : "form-control bg-light mt-2 text-secondary",
            "placeholder" : "Contraseña"
        }
    ))

class UserLoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={
            "class" : "form-control bg-light text-secondary",
            "placeholder" : "Teléfono, usuario o correo electrónico"
        }
    ))

    password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={
            "class" : "form-control bg-light text-secondary mt-2",
            "placeholder" : "Contraseña"
        }
    ))