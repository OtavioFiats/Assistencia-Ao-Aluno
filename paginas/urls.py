from django.urls import path
from .views import (
    IndexView, SobreView, MenuView, MenuListasView,
    EmprestimoCreate, AlunoCreate, ServidorCreate,
    EmprestimoUpdate, AlunoUpdate, ServidorUpdate,
    EmprestimoDelete, AlunoDelete, ServidorDelete,
    EmprestimoList, AlunoList, ServidorList
)

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('sobre/', SobreView.as_view(), name="sobre"),
    path('menu/', MenuView.as_view(), name="menu"),
    path('menu/listas/', MenuListasView.as_view(), name="menu-listas"),


    path('cadastrar/emprestimo/', EmprestimoCreate.as_view(), name="cadastrar-emprestimo"),
    path('cadastrar/aluno/', AlunoCreate.as_view(), name="cadastrar-aluno"),
    path('cadastrar/servidor/', ServidorCreate.as_view(), name="cadastrar-servidor"),
    
    path('editar/emprestimo/<int:pk>/', EmprestimoUpdate.as_view(), name="editar-emprestimo"),
    path('editar/aluno/<int:pk>/', AlunoUpdate.as_view(), name="editar-aluno"),
    path('editar/servidor/<int:pk>/', ServidorUpdate.as_view(), name="editar-servidor"),

    path('excluir/emprestimo/<int:pk>/', EmprestimoDelete.as_view(), name="excluir-emprestimo"),
    path('excluir/aluno/<int:pk>/', AlunoDelete.as_view(), name="excluir-aluno"),
    path('excluir/servidor/<int:pk>/', ServidorDelete.as_view(), name="excluir-servidor"),

    
    path('listar/emprestimo/', EmprestimoList.as_view(), name="listar-emprestimo"),
    path('listar/aluno/', AlunoList.as_view(), name="listar-aluno"),
    path('listar/servidor/', ServidorList.as_view(), name="listar-servidor"),
]
