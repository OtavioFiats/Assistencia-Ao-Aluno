from django.core.management.base import BaseCommand
from paginas.models import Emprestimo


class Command(BaseCommand):
    help = 'Deleta todos os empréstimos do banco de dados'

    def handle(self, *args, **kwargs):
        # Conta quantos empréstimos existem
        count = Emprestimo.objects.count()
        
        if count == 0:
            self.stdout.write(self.style.WARNING('Nenhum empréstimo encontrado no banco de dados.'))
            return
        
        # Pergunta confirmação
        self.stdout.write(self.style.WARNING(f'Você está prestes a deletar {count} empréstimo(s).'))
        confirm = input('Tem certeza que deseja continuar? (sim/não): ')
        
        if confirm.lower() in ['sim', 's', 'yes', 'y']:
            # Deleta todos os empréstimos
            Emprestimo.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Todos os {count} empréstimo(s) foram deletados com sucesso!'))
        else:
            self.stdout.write(self.style.ERROR('Operação cancelada.'))
