from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Emprestimo, Aluno, Servidor
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User, Group
from .forms import  AlunoCadastroForm, ServidorCadastroForm
from django.http import HttpResponseForbidden
from django import forms
from django.contrib import messages
import qrcode
import base64
from django.http import HttpResponse
from django.shortcuts import redirect, render

def logout_view(request):
    """Logout e redireciona para a página inicial."""
    logout(request)
    return redirect('index')

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
        ra = form.cleaned_data.get('ra')
        ano = form.cleaned_data.get('ano')
        data_nasc = form.cleaned_data.get('data_nasc')
        endereco = form.cleaned_data.get('endereco')
        fone = form.cleaned_data.get('fone')
        curso = form.cleaned_data.get('curso')
        cpf = form.cleaned_data.get('cpf')
        cidade = form.cleaned_data.get('cidade')
        nome = form.cleaned_data.get('nome')
        
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
        siape = form.cleaned_data.get('siape')
        nome = form.cleaned_data.get('nome')
        fone = form.cleaned_data.get('fone')
        endereco = form.cleaned_data.get('endereco')
        cidade = form.cleaned_data.get('cidade')
        tipo = form.cleaned_data.get('tipo')
        
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



from braces.views import GroupRequiredMixin
from django.db.models import Count
import json

class IndexView(TemplateView):
    template_name = "paginas/index.html"

    def get(self, request, *args, **kwargs):
        # Se o usuário for um servidor, mostre o dashboard
        if request.user.is_authenticated and request.user.groups.filter(name='Servidor').exists():
            self.template_name = 'paginas/dashboard.html'
            context = self.get_dashboard_context()
            return self.render_to_response(context)
        
        # Para outros usuários, mostre a página inicial padrão
        return super().get(request, *args, **kwargs)

    def get_dashboard_context(self):
        today = timezone.now().date()
        last_30_days = today - timedelta(days=30)

        # Cards
        emprestimos_ativos = Emprestimo.objects.filter(aluno_confirmacao=True, confirmacao_devolucao=False).count()
        emprestimos_atrasados = Emprestimo.objects.filter(aluno_confirmacao=True, confirmacao_devolucao=False, data_devolucao__lt=today).count()
        emprestimos_pendentes = Emprestimo.objects.filter(aluno_confirmacao=False).count()

        # Gráfico
        itens_mais_emprestados = Emprestimo.objects.filter(data__gte=last_30_days) \
            .values('descricao') \
            .annotate(total=Count('descricao')) \
            .order_by('-total')[:5]

        chart_labels = [item['descricao'] for item in itens_mais_emprestados]
        chart_data = [item['total'] for item in itens_mais_emprestados]

        return {
            'emprestimos_ativos': emprestimos_ativos,
            'emprestimos_atrasados': emprestimos_atrasados,
            'emprestimos_pendentes': emprestimos_pendentes,
            'chart_labels': json.dumps(chart_labels),
            'chart_data': json.dumps(chart_data),
        }

class SobreView(TemplateView):
    template_name = 'paginas/sobre.html'

class MenuView(LoginRequiredMixin, TemplateView):
    template_name = 'paginas/menu.html'

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Servidor').exists():
            return redirect('index') # Redireciona para o dashboard (IndexView)
        elif hasattr(request.user, 'aluno'):
            return redirect('meus-emprestimos')
        
        # Fallback para outros tipos de usuários autenticados
        return redirect('index')

class MenuListasView(TemplateView):
    template_name = 'paginas/menu-listas.html'

class EmprestimoCreate(LoginRequiredMixin , CreateView):
    template_name = 'paginas/form.html'
    model = Emprestimo
    fields = ['descricao', 'categoria', 'data', 'aluno']
    success_url = reverse_lazy('listar-emprestimo')
    extra_context = {'titulo': 'Cadastro de Empréstimo', 'botao': 'Salvar'}

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['aluno'].queryset = Aluno.objects.all()
        
        # Configurar o campo de data com widget DateInput e data mínima
        from datetime import date
        today = date.today()
        form.fields['data'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': today.strftime('%Y-%m-%d'),
            'value': today.strftime('%Y-%m-%d')
        })
        form.fields['data'].initial = today
        form.fields['data'].help_text = 'A data do empréstimo não pode ser anterior à data atual.'
        
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
    fields = ['descricao', 'categoria', 'emprestado', 'aluno']
    success_url = reverse_lazy('listar-emprestimo')
    extra_context = {'titulo': 'Atualização de Empréstimo', 'botao': 'Salvar'}



class EmprestimoUpdateConfirmacao(LoginRequiredMixin, UpdateView):
    template_name = 'paginas/form.html'
    model = Emprestimo
    fields = []
    success_url = reverse_lazy('listar-emprestimo')
    extra_context = {'titulo': 'Confirmação de Empréstimo', 'botao': 'Confirmar'}

    def dispatch(self, request, *args, **kwargs):
        emprestimo = self.get_object()
        # Permite confirmação tanto pelo aluno quanto pelo servidor
        if not (hasattr(request.user, 'aluno') and emprestimo.aluno.usuario == request.user) and not hasattr(request.user, 'servidor'):
            return HttpResponseForbidden("Apenas aluno ou servidor podem confirmar este empréstimo.")
        # Se já confirmado, redireciona
        if emprestimo.aluno_confirmacao:
            messages.info(request, "Empréstimo já confirmado!")
            return super().form_invalid(self.get_form())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.aluno_confirmacao = True
        form.instance.emprestado = True
        form.instance.aluno_data_confirmacao = timezone.now()
        messages.success(self.request, "Empréstimo confirmado com sucesso!")
        # Não chama o super().form_valid(form) para não salvar duas vezes
        form.save()
        return redirect('emprestimo-qrcode', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['emprestimo'] = self.object
        context['ja_confirmado'] = self.object.aluno_confirmacao
        return context


class AlunoUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'paginas/form.html'
    model = Aluno
    form_class = None
    success_url = reverse_lazy('listar-aluno')
    extra_context = {'titulo': 'Atualização de alunos', 'botao': 'Salvar'}

    def get_form_class(self):
        # Importa localmente para evitar import cycles
        from .forms import AlunoUpdateForm
        return AlunoUpdateForm
  
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


from django.db.models import Q
from django.utils import timezone

from django.db.models import Q


class EmprestimoList(LoginRequiredMixin, ListView):
    model = Emprestimo
    template_name = "paginas/listas/emprestimo.html"
    paginate_by = 10
    context_object_name = 'emprestimos'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-data')
        search_query = self.request.GET.get('q')
        status_filter = self.request.GET.get('status')

        if search_query:
            queryset = queryset.filter(
                Q(aluno__nome__icontains=search_query) |
                Q(descricao__icontains=search_query)
            )

        if status_filter:
            today = timezone.now().date()
            if status_filter == 'pendente':
                queryset = queryset.filter(aluno_confirmacao=False)
            elif status_filter == 'aprovado':
                queryset = queryset.filter(aluno_confirmacao=True, confirmacao_devolucao=False, data_devolucao__gte=today)
            elif status_filter == 'atrasado':
                queryset = queryset.filter(aluno_confirmacao=True, confirmacao_devolucao=False, data_devolucao__lt=today)
            elif status_filter == 'devolvido':
                queryset = queryset.filter(confirmacao_devolucao=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['status_filter'] = self.request.GET.get('status', '')
        # Passa os parâmetros de busca para a paginação
        context['pagination_params'] = f"q={context['search_query']}&status={context['status_filter']}"
        return context


class MeuEmprestimoList(LoginRequiredMixin, ListView):
    model = Emprestimo
    template_name = "paginas/listas/emprestimo.html"
    context_object_name = 'emprestimos' 

    # Filtra os empréstimos para mostrar apenas os do aluno logado
    def get_queryset(self):
        if hasattr(self.request.user, 'aluno'):
            return Emprestimo.objects.filter(aluno=self.request.user.aluno)
        return Emprestimo.objects.none()


class AlunoList(LoginRequiredMixin, ListView):
    model = Aluno
    template_name = "paginas/listas/aluno.html"
    paginate_by = 10


class HistoricoAlunoView(LoginRequiredMixin, ListView):
    model = Emprestimo
    template_name = 'paginas/listas/historico_aluno.html'
    context_object_name = 'emprestimos'
    paginate_by = 10

    def get_queryset(self):
        aluno_pk = self.kwargs.get('pk')
        return Emprestimo.objects.filter(aluno__pk=aluno_pk).order_by('-data')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aluno'] = Aluno.objects.get(pk=self.kwargs.get('pk'))
        return context


class ServidorList(LoginRequiredMixin, ListView):
    model = Servidor
    template_name = "paginas/listas/servidor.html"
    paginate_by = 10


 
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

class EmprestimoQRCodeView(LoginRequiredMixin, TemplateView):
    template_name = 'paginas/emprestimo_qrcode.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emprestimo_id = self.kwargs.get('pk')
        emprestimo = Emprestimo.objects.get(pk=emprestimo_id)
        url = self.request.build_absolute_uri(
            reverse_lazy('confirmar-emprestimo-qr', kwargs={'pk': emprestimo_id})
        )
        qr = qrcode.make(url)
        import io
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        image_stream = buf.getvalue()
        qr_code_base64 = base64.b64encode(image_stream).decode('utf-8')
        context['qr_code_base64'] = qr_code_base64
        context['emprestimo_id'] = emprestimo_id
        context['url'] = url
        context['emprestimo'] = emprestimo
        return context

from django.views import View
class EmprestimoConfirmarQRView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect(f"{reverse_lazy('login')}?next={reverse_lazy('confirmar-emprestimo-qr', kwargs={'pk': pk})}")
        from .models import Emprestimo
        emprestimo = Emprestimo.objects.get(pk=pk)
        # Só o aluno do empréstimo pode confirmar
        if not hasattr(request.user, 'aluno') or emprestimo.aluno.usuario != request.user:
            messages.error(request, "Apenas o aluno responsável pode confirmar este empréstimo.")
            return HttpResponseForbidden("Apenas o aluno responsável pode confirmar este empréstimo.")
        if emprestimo.aluno_confirmacao:
            messages.info(request, "Empréstimo já confirmado!")
            return render(request, 'paginas/emprestimo_confirmado_sucesso.html')
        emprestimo.aluno_confirmacao = True
        emprestimo.aluno_data_confirmacao = timezone.now()
        emprestimo.save()
        messages.success(request, "Empréstimo confirmado com sucesso!")
        return render(request, 'paginas/emprestimo_confirmado_sucesso.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def confirmar_devolucao(request, pk):
    if not hasattr(request.user, 'servidor'):
        messages.error(request, "Apenas servidores podem realizar esta ação.")
        return redirect('listar-emprestimo')

    emprestimo = get_object_or_404(Emprestimo, pk=pk)

    if emprestimo.confirmacao_devolucao:
        messages.info(request, "A devolução deste item já foi confirmada.")
    else:
        emprestimo.confirmacao_devolucao = True
        emprestimo.save()
        messages.success(request, "Devolução confirmada com sucesso!")

    return redirect('listar-emprestimo')


from django.views.generic import TemplateView

class EscolherCadastroView(TemplateView):
    template_name = "paginas/escolher_cadastro.html"
