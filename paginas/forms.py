from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Aluno, Servidor
from collections import OrderedDict


# Crie uma classe de formulário para o cadastro de usuários
# A herança é feita para poder tornar o email único e obrigatório
# E outros campos, se necessário
class AlunoCadastroForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Garantir que o email apareça logo após o username na renderização
        desired_order = [
            'username', 'email', 'password1', 'password2',
            'nome', 'fone', 'ra', 'ano', 'data_nasc', 'endereco', 'curso', 'cpf', 'cidade'
        ]
        # Reordenar apenas os campos que existem no formulário
        new_fields = OrderedDict()
        for name in desired_order:
            if name in self.fields:
                new_fields[name] = self.fields[name]
        for name, field in list(self.fields.items()):
            if name not in new_fields:
                new_fields[name] = field
        self.fields = new_fields



    email = forms.EmailField(required=True, help_text="Informe um email válido.")

    nome = forms.CharField(
        required=True,
        help_text="Informe o nome (apenas para alunos).",
        widget=forms.TextInput(attrs={'class': 'form-control servidor-field'})
    )
    fone = forms.CharField(
        required=True,
        help_text="Informe o telefone no formato (XX) XXXXX-XXXX",
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control servidor-field',
            'placeholder': '(XX) XXXXX-XXXX'
        })
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

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        import re
        if not cpf:
            raise forms.ValidationError('CPF é obrigatório.')
        # Remove qualquer caractere que não seja dígito
        digits = re.sub(r'\D', '', cpf)
        if len(digits) != 11:
            raise forms.ValidationError('CPF deve conter 11 dígitos.')
        # Formata como 000.000.000-00 antes de retornar
        formatted = f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
        return formatted

    def clean_fone(self):
        fone = self.cleaned_data.get('fone')
        import re
        if not fone:
            raise forms.ValidationError('Telefone é obrigatório.')
        # Remove tudo que não for dígito
        digits = re.sub(r'\D', '', fone)
        if len(digits) == 10:
            # (XX) XXXX-XXXX
            formatted = f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
        elif len(digits) == 11:
            # (XX) XXXXX-XXXX
            formatted = f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
        else:
            raise forms.ValidationError('Telefone inválido. Deve conter 10 ou 11 dígitos.')
        return formatted

class ServidorCadastroForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Informe um email válido.")

    nome = forms.CharField(
        required=True,
        help_text="Informe o nome (apenas para Servidores).",
        widget=forms.TextInput(attrs={'class': 'form-control servidor-field'})
    )
    fone = forms.CharField(
        required=True,
        help_text="Informe o telefone no formato (XX) XXXXX-XXXX",
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control servidor-field',
            'placeholder': '(XX) XXXXX-XXXX'
        })
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


class AlunoUpdateForm(forms.ModelForm):
    """Form de atualização do Aluno que inclui o email do User associado."""
    email = forms.EmailField(required=True, help_text="Informe um email válido.")

    class Meta:
        model = Aluno
        fields = ['ra', 'nome', 'endereco', 'fone', 'curso', 'ano', 'cpf', 'cidade', 'data_nasc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se temos uma instância com usuário associado, preenche o email inicial
        instance = kwargs.get('instance')
        if instance and hasattr(instance, 'usuario') and instance.usuario:
            self.fields['email'].initial = instance.usuario.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=getattr(self.instance.usuario, 'pk', None)).exists():
            raise forms.ValidationError('Este email já está em uso por outro usuário.')
        return email

    def save(self, commit=True):
        # Atualiza o usuário associado com o email e salva o aluno
        aluno = super().save(commit=False)
        email = self.cleaned_data.get('email')
        try:
            user = aluno.usuario
            if user and email:
                user.email = email
                user.save()
        except Exception:
            # Se não houver usuário associado, ignore (ou poderia criar)
            pass
        if commit:
            aluno.save()
        return aluno