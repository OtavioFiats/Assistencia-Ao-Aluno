from django.db import models
from django.contrib.auth.models import User


class Aluno(models.Model):
    ra = models.PositiveIntegerField(unique=True, verbose_name="RA")
    nome = models.CharField(max_length=100, verbose_name="Nome")
    endereco = models.CharField(max_length=200, verbose_name="Endereço")
    fone = models.CharField(max_length=15, verbose_name="Telefone")
    curso = models.CharField(max_length=100, verbose_name="Curso")
    ano = models.PositiveSmallIntegerField(verbose_name="Ano")
    cpf = models.CharField(max_length=14, verbose_name="CPF")
    rg = models.CharField(max_length=20, verbose_name="RG")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    data_nasc = models.DateField(verbose_name="Data de Nascimento")
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aluno')

    def __str__(self):
        return f"{self.nome} (RA: {self.ra})"


class Servidor(models.Model):
    siape = models.PositiveIntegerField(unique=True, verbose_name="SIAPE")
    nome = models.CharField(max_length=100, verbose_name="Nome")
    endereco = models.CharField(max_length=200, verbose_name="Endereço")
    fone = models.CharField(max_length=15, verbose_name="Telefone")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    tipo = models.CharField(max_length=50, verbose_name="Tipo")
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='servidor')

    def __str__(self):
        return f"{self.nome} (SIAPE: {self.siape})"


class Emprestimo(models.Model):
    descricao = models.CharField(max_length=250)
    data = models.DateField()
    emprestado = models.BooleanField(default=True) 

    data_devolucao = models.DateField()
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='emprestimos')
    aluno_confirmacao = models.BooleanField(default=False)
    aluno_data_confirmacao = models.DateTimeField(null=True, blank=True)

    servidor = models.ForeignKey(Servidor, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.descricao} ({self.data.strftime('%d/%m/%Y')})"
    
    