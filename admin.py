from django.contrib import admin
from .models import Usuario, Registro, Lista, Tarefa
from .models import Programador

admin.site.register(Usuario)
admin.site.register(Registro)
admin.site.register(Lista)
admin.site.register(Tarefa)

class ProgramadorAdmin(admin.ModelAdmin):
    readonly_fields = ('criado_por',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Se o objeto está sendo criado (não tem ID)
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Programador, ProgramadorAdmin)