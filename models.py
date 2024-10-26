from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) 
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    funcao = models.CharField(max_length=50, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Registro(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  
    entrada = models.DateTimeField()
    saida = models.DateTimeField(null=True, blank=True)

    @property
    def horas_trabalhadas(self):
        if self.saida:
            return (self.saida - self.entrada).total_seconds() / 3600
        return 0

    @property
    def horas_trabalhadas_formatado(self):
        horas = self.horas_trabalhadas
        print(f'Entrada: {self.entrada}, Saída: {self.saida}') 
        return f"{horas:.2f} horas"

    def __str__(self):
        return f"{self.usuario} - Entrada: {self.entrada}, Saída: {self.saida}"


class Lista(models.Model):
    tarefas = models.CharField(max_length=200)
    registro_tempo = models.DateTimeField(null=True)
    filtragem_campos = models.TextField(max_length=200)

    def __str__(self):
        return self.tarefas


class Tarefa(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em andamento', 'Em Andamento'),
        ('concluída', 'Concluída'),
    ]

    RELACIONAMENTO_CHOICES = [
        ('em análise', 'Em Análise'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
    ]

    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    relacionamento = models.CharField(max_length=20, choices=RELACIONAMENTO_CHOICES, default='em análise')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descricao
    
class Programador(models.Model):
    nome = models.CharField(max_length=80)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'programadores'
        ordering = ('nome', )
        
    def __str__(self):
        return self.nome
