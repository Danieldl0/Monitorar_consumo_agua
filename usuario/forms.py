from django import forms
from django.contrib.auth.models import User


class CadastroUserForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        required=True,
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True,
    )
    first_name = forms.CharField(
        label="Nome",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )
    last_name = forms.CharField(
        label="Sobrenome",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    class Meta:
        model = User
        fields = ("username", "email", "password", 'first_name', 'last_name',)
    

    def save(self, commit=True):
        instance = super().save(commit=False)
        senha = self.cleaned_data.get("password")
        if senha is not None:
            instance.set_password(senha)
        
        if commit:
            instance.save()
        return instance


class LoginFormView(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True,
    )
    class Meta:
        model = User
        fields = (
            'username', 'password',
        )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = User.objects.filter(
            username=username
        ).first()

        if not user:
            self.add_error("username", "Usuario não cadastrado")
            return

        if not user.check_password(password):
            self.add_error("password", "Senha Incorreta")
            return
