from django.contrib import admin
from .models import  Emprestimo, Aluno,Servidor


class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'data', 'data_devolucao', 'aluno', 'servidor', 'aluno_confirmacao')
    list_filter = ('aluno_confirmacao', 'data', 'data_devolucao')
    search_fields = ('descricao', 'aluno__nome', 'servidor__nome')

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('ra', 'nome', 'curso', 'ano', 'cpf', 'cidade')
    search_fields = ('nome', 'ra', 'cpf', 'curso')

class ServidorAdmin(admin.ModelAdmin):
    list_display = ('siape', 'nome', 'tipo', 'cidade')
    search_fields = ('nome', 'siape', 'tipo')

admin.site.register(Emprestimo, EmprestimoAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Servidor, ServidorAdmin)
# Register your models here.
