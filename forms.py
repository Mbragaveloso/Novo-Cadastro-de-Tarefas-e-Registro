from django import forms
from .models import Registro, Usuario, Lista

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['nome', 'email', 'descricao']

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['usuario', 'entrada', 'saida']
        
class ListagemForm(forms.ModelForm):
    class Meta:
        model = Lista
        fields = ['tarefas','registro_tempo','filtragem_campos']
