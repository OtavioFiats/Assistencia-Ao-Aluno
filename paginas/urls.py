from django.urls import path
from .views import (
    IndexView, SobreView, MenuView, MenuListasView,
    EmprestimoCreate, AlunoCreate, ServidorCreate,
    EmprestimoUpdate, AlunoUpdate, ServidorUpdate,
    EmprestimoDelete, AlunoDelete, ServidorDelete,
    EmprestimoList, AlunoList, ServidorList,

    EmprestimoUpdateConfirmacao,EmprestimoDetailView, MeuEmprestimoList,
    EscolherCadastroView, CadastroAlunoView, CadastroServidorView
)
from django.contrib.auth import views as auth_views
# from .views import CadastroUsuarioView

urlpatterns = [
    
    #criar uma rota "registrar" para o cadastro de usuários
    # path("registrar/", CadastroUsuarioView.as_view(), name="registrar"),

    #Rota para pagina de Login
    path("login/", auth_views.LoginView.as_view(
        template_name='paginas/login.html',
        extra_context={'titulo': 'Autenticação', 'botao': 'Entrar'}
        ), name="login"),
    
    path("senha/", auth_views.PasswordChangeView.as_view(
        template_name='paginas/form.html',
        extra_context={'titulo': 'Atualizar Senha', 'botao': 'Salvar'}
    ), name="senha"),

    # Rota para pagina de Logout
    path("sair/", auth_views.LogoutView.as_view(), name="Logout"),

    
    path('', IndexView.as_view(), name="index"),
    path('sobre/', SobreView.as_view(), name="sobre"),
    path('menu/', MenuView.as_view(), name="menu"),
    path('menu/listas/', MenuListasView.as_view(), name="menu-listas"),

    path('cadastrar/emprestimo/', EmprestimoCreate.as_view(), name="cadastrar-emprestimo"),
    path('cadastrar/aluno/', AlunoCreate.as_view(), name="cadastrar-aluno"),
    path('cadastrar/servidor/', ServidorCreate.as_view(), name="cadastrar-servidor"),
    
    path('editar/emprestimo/<int:pk>/', EmprestimoUpdate.as_view(), name="editar-emprestimo"),
    path('confirmar/emprestimo/<int:pk>/', EmprestimoUpdateConfirmacao.as_view(), name="confirmar-emprestimo"),
    path('editar/aluno/<int:pk>/', AlunoUpdate.as_view(), name="editar-aluno"),
    path('editar/servidor/<int:pk>/', ServidorUpdate.as_view(), name="editar-servidor"),

    path('excluir/emprestimo/<int:pk>/', EmprestimoDelete.as_view(), name="excluir-emprestimo"),
    path('excluir/aluno/<int:pk>/', AlunoDelete.as_view(), name="excluir-aluno"),
    path('excluir/servidor/<int:pk>/', ServidorDelete.as_view(), name="excluir-servidor"),

    
    path('listar/emprestimo/', EmprestimoList.as_view(), name="listar-emprestimo"),
    path('listar/aluno/', AlunoList.as_view(), name="listar-aluno"),
    path('listar/servidor/', ServidorList.as_view(), name="listar-servidor"),

    path('detalhes/emprestimo/<int:pk>/', EmprestimoDetailView.as_view(), name="detalhes-emprestimo"),

    path("listar/meus-emprestimos/", MeuEmprestimoList.as_view(), name="meus-emprestimos"),

    path("escolher-cadastro/", EscolherCadastroView.as_view(), name="escolher-cadastro"),
    path("cadastro/aluno/", CadastroAlunoView.as_view(), name="cadastro-aluno"),
    path("cadastro/servidor/", CadastroServidorView.as_view(), name="cadastro-servidor"),
]
