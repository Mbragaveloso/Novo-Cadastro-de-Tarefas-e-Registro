from django.urls import path
from .views import (
    home, usuario, registrar_entrada, registrar_saida,
    listar_registros, registrar_tarefa,
    listar_tarefas, editar_usuario, editar_tarefa, deletar_tarefa,
)

urlpatterns = [
    path('', home, name='home'),
    path('usuario/', usuario, name='usuario'),
    path('usuario/editar/<int:usuario_id>/', editar_usuario, name='editar_usuario'),
    path('registrar_entrada/', registrar_entrada, name='registrar_entrada'),
    path('registrar_saida/', registrar_saida, name='registrar_saida'),
    path('listar_registros/', listar_registros, name='listar_registros'),
    path('registrar_tarefa/', registrar_tarefa, name='registrar_tarefa'),
    path('tarefa/editar/<int:id>/', editar_tarefa, name='editar_tarefa'),
    path('tarefa/deletar/<int:id>/', deletar_tarefa, name='deletar_tarefa'),
    path('listar_tarefas/', listar_tarefas, name='listar_tarefas'),
    ]