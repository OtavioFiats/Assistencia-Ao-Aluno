from django.db import models

class Emprestimo(models.Model):
    descricao = models.CharField(max_length=250)
    data = models.DateField()
    emprestado = models.BooleanField(default=False) 
    
    def __str__(self):
        return f"{self.descricao} ({self.data.strftime('%d/%m/%Y')})"

class Aluno(models.Model):
    ra = models.PositiveIntegerField(unique=True, verbose_name="RA")
    nome = models.CharField(max_length=100, verbose_name="Nome")
    endereco = models.CharField(max_length=200, verbose_name="Endereço")
    fone = models.CharField(max_length=15, verbose_name="Telefone")
    email = models.EmailField(verbose_name="E-mail")
    curso = models.CharField(max_length=100, verbose_name="Curso")
    ano = models.PositiveSmallIntegerField(verbose_name="Ano")
    cpf = models.CharField(max_length=14, verbose_name="CPF")
    rg = models.CharField(max_length=20, verbose_name="RG")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    data_nasc = models.DateField(verbose_name="Data de Nascimento")

    def __str__(self):
        return f"{self.nome} (RA: {self.ra})"

class Servidor(models.Model):
    siape = models.PositiveIntegerField(unique=True, verbose_name="SIAPE")
    nome = models.CharField(max_length=100, verbose_name="Nome")
    endereco = models.CharField(max_length=200, verbose_name="Endereço")
    fone = models.CharField(max_length=15, verbose_name="Telefone")
    email = models.EmailField(verbose_name="E-mail")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    tipo = models.CharField(max_length=50, verbose_name="Tipo")

    def __str__(self):
        return f"{self.nome} (SIAPE: {self.siape})"
