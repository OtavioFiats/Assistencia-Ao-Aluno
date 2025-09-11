from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Aluno, Servidor


# Crie uma classe de formulário para o cadastro de usuários
# A herança é feita para poder tornar o email único e obrigatório
# E outros campos, se necessário
class AlunoCadastroForm(UserCreationForm):


    email = forms.EmailField(required=True, help_text="Informe um email válido.")

    nome = forms.CharField(
        required=True,
        help_text="Informe o nome (apenas para alunos).",
        widget=forms.TextInput(attrs={'class': 'form-control servidor-field'})
    )
    fone = forms.CharField(
        required=True,
        help_text="Informe o telefone (apenas para alunos).",
        widget=forms.TextInput(attrs={'class': 'form-control servidor-field'})
    )
    ra = forms.IntegerField(
        required=True,
        help_text="Informe o RA (apenas para alunos).",
        widget=forms.NumberInput(attrs={'class': 'form-control aluno-field'})
    )
    ano = forms.IntegerField(
        required=True,
        help_text="Informe o ano (apenas para alunos).",
        widget=forms.NumberInput(attrs={'class': 'form-control aluno-field'})
    )
    data_nasc = forms.DateField(
        required=True,
        help_text="Informe a data de nascimento (apenas para alunos).",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control aluno-field'})
    )
    endereco = forms.CharField(
        required=True,
        help_text="Informe o endereço (apenas para alunos).",
        widget=forms.TextInput(attrs={'class': 'form-control aluno-field'})
    )
    curso = forms.CharField(
        required=True,
        help_text="Informe o curso (apenas para alunos).",
        widget=forms.TextInput(attrs={'class': 'form-control aluno-field'})
    )
    cpf = forms.CharField(
        required=True,
        help_text="Informe o CPF (apenas para alunos).",
        widget=forms.TextInput(attrs={'class': 'form-control aluno-field'})
    )
    cidade = forms.CharField(
        required=True,
        help_text="Informe a cidade (apenas para alunos).",
        widget=forms.TextInput(attrs={'class': 'form-control aluno-field'})
    )


    # Define o model e os fields que vão aparecer na tela
    class Meta:
        model = User
        # Esses dois passwords são para verificar se as senhas são iguais
        fields = ['username', 'email', 'password1', 'password2']


    # O metodo clean no forms serve de validação para os campos
    def clean_email(self):
        # recebe o email do formulário
        email = self.cleaned_data.get('email')
        # Verifica se já existe algum usuário com este email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email

class ServidorCadastroForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Informe um email válido.")

    nome = forms.CharField(
        required=True,
        help_text="Informe o nome (apenas para Servidores).",
        widget=forms.TextInput(attrs={'class': 'form-control servidor-field'})
    )
    fone = forms.CharField(
        required=True,
        help_text="Informe o telefone (apenas para Servidores).",
        widget=forms.TextInput(attrs={'class': 'form-control servidor-field'})
    )
    siape = forms.IntegerField(
        required=True,
        help_text="Informe o SIAPE (apenas para servidores).",
        widget=forms.NumberInput(attrs={'class': 'form-control servidor-field'})
    )
    tipo = forms.CharField(
        required=True,
        help_text="Informe o tipo (apenas para servidores).",
        widget=forms.TextInput(attrs={'class': 'form-control servidor-field'})
    )
    endereco = forms.CharField(
        required=True,
        help_text="Informe o endereço (apenas para Servidores).",
        widget=forms.TextInput(attrs={'class': 'form-control aluno-field'})
    )
    cidade = forms.CharField(
        required=True,
        help_text="Informe a cidade (apenas para Servidores).",
        widget=forms.TextInput(attrs={'class': 'form-control aluno-field'})
    )


    # Define o model e os fields que vão aparecer na tela
    class Meta:
        model = User
        # Esses dois passwords são para verificar se as senhas são iguais
        fields = ['username', 'email', 'password1', 'password2']


    # O metodo clean no forms serve de validação para os campos
    def clean_email(self):
        # recebe o email do formulário
        email = self.cleaned_data.get('email')
        # Verifica se já existe algum usuário com este email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email   