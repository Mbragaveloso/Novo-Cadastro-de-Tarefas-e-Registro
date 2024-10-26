from django.contrib import admin
from django.shortcuts import render, get_object_or_404, redirect
from .models import Usuario
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import Tarefa
from .models import Registro

def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login bem-sucedido!')
                return redirect('usuario')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'tarefas/home.html', {'form': form})

@login_required
def usuario(request):
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        funcao = request.POST.get('funcao')

        if not nome or not email or not funcao:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return redirect('usuario')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado.')
            return redirect('usuario')

        novo_usuario = Usuario(nome=nome, email=email, funcao=funcao, usuario=request.user) 
        novo_usuario.save()
        messages.success(request, 'Usuário criado com sucesso!')
        return redirect('usuario')

    usuarios = Usuario.objects.all()

    usuario_logado = get_object_or_404(Usuario, usuario=request.user)

    return render(request, 'tarefas/usuarios.html', {
        'usuarios': usuarios,
        'usuario_logado': usuario_logado, 
    })

@login_required
def perfil_usuario(request):
    
    usuario_logado = get_object_or_404(Usuario, usuario=request.user)
    
    return render(request, 'tarefas/perfil.html', {'usuario_logado': usuario_logado})

@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        funcao = request.POST.get('funcao')

        if not nome or not email or not funcao:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return redirect('editar_usuario', usuario_id=usuario_id)

        if Usuario.objects.filter(email=email).exclude(id=usuario_id).exists():
            messages.error(request, 'Este email já está cadastrado por outro usuário.')
            return redirect('editar_usuario', usuario_id=usuario_id)

        usuario.nome = nome
        usuario.email = email
        usuario.funcao = funcao
        usuario.save()
        
        messages.success(request, 'Usuário editado com sucesso!')
        return redirect('usuario') 

    return render(request, 'tarefas/editar_usuario.html', {'usuario': usuario})

@login_required
def registrar_entrada(request):
    if request.method == 'POST':
        entrada = timezone.now()
        usuario_atual = get_object_or_404(Usuario, usuario=request.user)  
        novo_registro = Registro(usuario=usuario_atual, entrada=entrada)
        novo_registro.save()
        messages.success(request, 'Entrada registrada com sucesso!')
        return redirect('registrar_tarefa')

    return render(request, 'tarefas/registrar_entrada.html')

def registrar_saida(request):
    if request.method == "POST":
        registro_id = request.POST.get("registro_id")
        registro = Registro.objects.get(id=registro_id)  
        
        registro.saida = timezone.now()
        registro.save()
        
        return redirect("sair") 

    registros = Registro.objects.filter(saida__isnull=True)  
    hora_atual = timezone.now()
    
    return render(request, "tarefas/registrar_saida.html", {
        "registros": registros,
        "hora_atual": hora_atual,
    })
    
    
@login_required
def listar_registros(request):
    registros = Registro.objects.filter(usuario=request.user.usuario)  
    return render(request, 'tarefas/listar_registros.html', {'registros': registros})

@login_required
def registrar_tarefa(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        relacionamento = request.POST.get('relacionamento')
        status = request.POST.get('status')
        
        usuario = request.user.usuario 

        tarefa = Tarefa.objects.create(
            descricao=descricao,
            relacionamento=relacionamento,
            status=status,
            usuario=usuario
        )

        return redirect('listar_tarefas') 

    return render(request, 'tarefas/registrar_tarefa.html')

def listar_tarefas(request):
    tarefas = Tarefa.objects.all()  
    return render(request, 'tarefas/listar_tarefas.html', {'tarefas': tarefas})

def editar_tarefa(request, id):
    tarefa = get_object_or_404(Tarefa, id=id)

    if request.method == 'POST':
     
        tarefa.descricao = request.POST['descricao']
        tarefa.save()
        return redirect('listar_tarefas')
    return render(request, 'tarefas/editar_tarefa.html', {'tarefa': tarefa})

def deletar_tarefa(request, id):
    tarefa = get_object_or_404(Tarefa, id=id)
    tarefa.delete()
    return redirect('listar_tarefas')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('usuario')

    def get_success_url(self):
        return self.success_url
