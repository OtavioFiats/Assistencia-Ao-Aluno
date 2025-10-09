from django.test import TestCase
from .models import Aluno, Servidor, Emprestimo
from django.contrib.auth.models import User
from datetime import date

class AlunoModelTest(TestCase):
    def test_create_aluno(self):
        user = User.objects.create(username='testealuno')
        aluno = Aluno.objects.create(ra=123, nome='Teste', endereco='Rua A', fone='99999-9999', curso='Curso', ano=2025, cpf='000.000.000-00', cidade='Cidade', data_nasc=date(2000,1,1), usuario=user)
        self.assertEqual(aluno.nome, 'Teste')

class ServidorModelTest(TestCase):
    def test_create_servidor(self):
        user = User.objects.create(username='testeservidor')
        servidor = Servidor.objects.create(siape=456, nome='Servidor', endereco='Rua B', fone='88888-8888', cidade='Cidade', tipo='Tipo', usuario=user)
        self.assertEqual(servidor.nome, 'Servidor')

class EmprestimoModelTest(TestCase):
    def test_create_emprestimo(self):
        user = User.objects.create(username='testeservidor')
        servidor = Servidor.objects.create(siape=789, nome='Servidor', endereco='Rua C', fone='77777-7777', cidade='Cidade', tipo='Tipo', usuario=user)
        user2 = User.objects.create(username='testealuno2')
        aluno = Aluno.objects.create(ra=321, nome='Aluno', endereco='Rua D', fone='66666-6666', curso='Curso', ano=2025, cpf='111.111.111-11', cidade='Cidade', data_nasc=date(2001,2,2), usuario=user2)
        emprestimo = Emprestimo.objects.create(descricao='Livro', data=date.today(), data_devolucao=date.today(), aluno=aluno, servidor=servidor)
        self.assertEqual(emprestimo.descricao, 'Livro')
