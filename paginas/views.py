from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Emprestimo, Aluno, Servidor
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User, Group
from .forms import  AlunoCadastroForm, ServidorCadastroForm
from django.http import HttpResponseForbidden
from django import forms


# Crie a view no final do arquivo ou em outro local que faça sentido
class CadastroAlunoView(CreateView):
    model = User
    # Não tem o fields, pois ele é definido no forms.py
    form_class = AlunoCadastroForm
    # Pode utilizar o seu form padrão
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('login')
    extra_context = {'titulo': 'Cadastro de aluno', 'botao': 'cadastrar'}


    def form_valid(self, form):
        ra = self.cleaned_data.get('ra')
        ano = self.cleaned_data.get('ano')
        data_nasc = self.cleaned_data.get('data_nasc')
        endereco = self.cleaned_data.get('endereco')
        fone = self.cleaned_data.get('fone')
        curso = self.cleaned_data.get('curso')
        cpf = self.cleaned_data.get('cpf')
        cidade = self.cleaned_data.get('cidade')
        nome = self.cleaned_data.get('nome')
        
        # Faz o comportamento padrão do form_valid
        url = super().form_valid(form)
        # Busca ou cria um grupo com esse nome
        grupo, criado = Group.objects.get_or_create(name='Estudante')
        # Acessa o objeto criado e adiciona o usuário no grupo acima
        self.object.groups.add(grupo)

        try:
            # Cria o aluno associado ao usuário criado
            Aluno.objects.create(
                ra=ra,
                nome=nome,
                endereco=endereco,
                fone=fone,
                curso=curso,
                ano=ano,
                cpf=cpf,
                cidade=cidade,
                data_nasc=data_nasc,
                usuario=self.object
            )
        except Exception as e:
            # Se der algum erro, deleta o usuário criado e mostra o erro
            self.object.delete()
            form.add_error(None, f"Erro ao criar aluno: {e}")
            return super().form_invalid(form)
        
        # Retorna a URL de sucesso
        return url


class CadastroServidorView(CreateView):
    model = User
    # Não tem o fields, pois ele é definido no forms.py
    form_class = ServidorCadastroForm
    # Pode utilizar o seu form padrão
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('login')
    extra_context = {'titulo': 'Cadastro de servidor', 'botao': 'cadastrar'}

    def form_valid(self, form):
        siape = self.cleaned_data.get('siape')
        nome = self.cleaned_data.get('nome')
        fone = self.cleaned_data.get('fone')
        endereco = self.cleaned_data.get('endereco')
        cidade = self.cleaned_data.get('cidade')
        tipo = self.cleaned_data.get('tipo')
        
        # Faz o comportamento padrão do form_valid
        url = super().form_valid(form)
        # Busca ou cria um grupo com esse nome
        grupo, criado = Group.objects.get_or_create(name='Servidor')
        # Acessa o objeto criado e adiciona o usuário no grupo acima
        self.object.groups.add(grupo)

        try:
            # Cria o aluno associado ao usuário criado
            Servidor.objects.create(
                siape=siape,
                nome=nome,
                fone=fone,
                endereco=endereco,
                cidade=cidade,
                tipo=tipo,
                usuario=self.object
            )
        except Exception as e:
            # Se der algum erro, deleta o usuário criado e mostra o erro
            self.object.delete()
            form.add_error(None, f"Erro ao criar servidor: {e}")
            return super().form_invalid(form)
        
        # Retorna a URL de sucesso
        return url



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
    fields = ['descricao', 'data', 'aluno']
    success_url = reverse_lazy('listar-emprestimo')
    extra_context = {'titulo': 'Cadastro de Empréstimo', 'botao': 'Salvar'}

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['aluno'].queryset = Aluno.objects.all()
        return form

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'servidor'):
            return HttpResponseForbidden("Apenas servidores podem acessar esta página.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.servidor = self.request.user.servidor
        # A data de devolução é a data + 7 dias
        form.instance.data_devolucao = form.instance.data + timedelta(days=7)

        return super().form_valid(form)


class AlunoCreate(LoginRequiredMixin, CreateView):
    template_name = 'paginas/form.html'
    model = Aluno
    fields = ['ra', 'nome', 'endereco', 'fone', 'curso', 'ano', 'cpf', 'cidade', 'data_nasc']
    success_url = reverse_lazy('listar-aluno')
    extra_context = {'titulo': 'Cadastro de alunos', 'botao': 'Salvar'}


class ServidorCreate(LoginRequiredMixin, CreateView):
    template_name = 'paginas/form.html'
    model = Servidor
    fields = ['siape', 'nome', 'fone']
    success_url = reverse_lazy('listar-servidor')
    extra_context = {'titulo': 'Cadastro de Servidor', 'botao': 'Salvar'}


class EmprestimoUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'paginas/form.html'
    model = Emprestimo
    fields = ['descricao', 'emprestado', 'aluno']
    success_url = reverse_lazy('listar-emprestimo')
    extra_context = {'titulo': 'Atualização de Empréstimo', 'botao': 'Salvar'}



class EmprestimoUpdateConfirmacao(LoginRequiredMixin, UpdateView):
    template_name = 'paginas/form.html'
    model = Emprestimo
    fields = []
    success_url = reverse_lazy('listar-emprestimo')
    extra_context = {'titulo': 'Confirmação de Empréstimo', 'botao': 'Confirmar'}

    def form_valid(self, form):
        form.instance.aluno_confirmacao = True
        # Confirmação é agora
        form.instance.aluno_data_confirmacao = timezone.now()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['emprestimo'] = self.object
        return context


class AlunoUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'paginas/form.html'
    model = Aluno
    fields = ['ra', 'nome', 'endereco', 'fone', 'email', 'curso', 'ano', 'cpf',  'cidade', 'data_nasc']
    success_url = reverse_lazy('listar-aluno')
    extra_context = {'titulo': 'Atualização de alunos', 'botao': 'Salvar'}
  
class ServidorUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'paginas/form.html'
    model = Servidor
    fields = ['siape', 'nome', 'fone', 'endereco', 'cidade', 'tipo']
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


class MeuEmprestimoList(LoginRequiredMixin, ListView):
    model = Emprestimo
    template_name = "paginas/listas/emprestimo.html" 

    # Filtra os empréstimos para mostrar apenas os do aluno logado
    def get_queryset(self):
        if hasattr(self.request.user, 'aluno'):
            return Emprestimo.objects.filter(aluno__usuario=self.request.user)
        return Emprestimo.objects.none()


class AlunoList(LoginRequiredMixin, ListView):
    model = Aluno
    template_name = "paginas/listas/aluno.html"


class ServidorList(LoginRequiredMixin, ListView):
    model = Servidor
    template_name = "paginas/listas/servidor.html"


 
class MeuLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm
    extra_context = {'botao': 'Entrar', 'titulo': 'Login'}

class EmprestimoDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'paginas/emprestimo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emprestimo_id = self.kwargs.get('pk')
        emprestimo = Emprestimo.objects.get(pk=emprestimo_id)
        context['emprestimo'] = emprestimo
        #pwga a url e cria o caminho para confimar o emprestimo
        context['url'] = reverse_lazy('confirmar-emprestimo', kwargs={'pk': emprestimo_id})
        context['return_url'] = self.request.META.get('HTTP_REFERER', reverse_lazy('listar-emprestimo'))
        if 'return_url' not in context:
            context['return_url'] = reverse_lazy('listar-emprestimo')
        if 'url' not in context:
            context['url'] = self.request.META.get('HTTP_REFERER', reverse_lazy('listar-emprestimo'))
        context['url']
        return context

from django.views.generic import TemplateView

class EscolherCadastroView(TemplateView):
    template_name = "paginas/escolher_cadastro.html"
