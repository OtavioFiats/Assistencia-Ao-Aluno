from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Emprestimo, Aluno, Servidor

from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(TemplateView):
    template_name = "paginas/index.html"

class SobreView(TemplateView):
    template_name = 'paginas/sobre.html'

class MenuView(TemplateView):
    template_name = 'paginas/menu.html'

class MenuListasView(TemplateView):
    template_name = 'paginas/menu-listas.html'

class EmprestimoCreate(LoginRequiredMixin , CreateView):
    template_name = 'paginas/form.html'
    model = Emprestimo
    fields = ['descricao', 'data']
    success_url = reverse_lazy('listar-emprestimo')
    extra_context = {'titulo': 'Cadastro de Empréstimo', 'botao': 'Salvar'}


class AlunoCreate(LoginRequiredMixin, CreateView):
    template_name = 'paginas/form.html'
    model = Aluno
    fields = ['ra', 'nome', 'endereco', 'fone', 'email', 'curso', 'ano', 'cpf', 'cidade', 'data_nasc']
    success_url = reverse_lazy('listar-aluno')
    extra_context = {'titulo': 'Cadastro de alunos', 'botao': 'Salvar'}


class ServidorCreate(LoginRequiredMixin, CreateView):
    template_name = 'paginas/form.html'
    model = Servidor
    fields = ['siape', 'nome', 'fone', 'email']
    success_url = reverse_lazy('listar-servidor')
    extra_context = {'titulo': 'Cadastro de Servidor', 'botao': 'Salvar'}


class EmprestimoUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'paginas/form.html'
    model = Emprestimo
    fields = ['descricao', 'data', 'emprestado']
    success_url = reverse_lazy('listar-emprestimo')
    extra_context = {'titulo': 'Atualização de Empréstimo', 'botao': 'Salvar'}


class AlunoUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'paginas/form.html'
    model = Aluno
    fields = ['ra', 'nome', 'endereco', 'fone', 'email', 'curso', 'ano', 'cpf',  'cidade', 'data_nasc']
    success_url = reverse_lazy('listar-aluno')
    extra_context = {'titulo': 'Atualização de alunos', 'botao': 'Salvar'}


class ServidorUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'paginas/form.html'
    model = Servidor
    fields = ['siape', 'nome', 'fone', 'email', ]
    success_url = reverse_lazy('listar-servidor')
    extra_context = {'titulo': 'Atualização de Servidor', 'botao': 'Salvar'}


class EmprestimoDelete(LoginRequiredMixin, DeleteView):
    model = Emprestimo
    template_name = 'paginas/form-excluir.html'
    success_url = reverse_lazy('listar-emprestimo')


class AlunoDelete(LoginRequiredMixin, DeleteView):
    model = Aluno
    template_name = 'paginas/form-excluir.html'
    success_url = reverse_lazy('listar-aluno')


class ServidorDelete(LoginRequiredMixin, DeleteView):
    model = Servidor
    template_name = 'paginas/form-excluir.html'
    success_url = reverse_lazy('listar-servidor')


class EmprestimoList(LoginRequiredMixin, ListView):
    model = Emprestimo
    template_name = "paginas/listas/emprestimo.html"


class AlunoList(LoginRequiredMixin, ListView):
    model = Aluno
    template_name = "paginas/listas/aluno.html"


class ServidorList(LoginRequiredMixin, ListView):
    model = Servidor
    template_name = "paginas/listas/servidor.html"
