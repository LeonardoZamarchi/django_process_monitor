from django.contrib import admin

from .models import Processo, Agendamento

class ProcessoAdmin(admin.ModelAdmin):
    model = Processo
    list_display = ['Processo','Linguagem','Atualizacao','Descricao']
    list_filter = ['Atualizacao', 'Linguagem']
    search_fields = ['Processo']

admin.site.register(Processo, ProcessoAdmin)


class AgendamentoAdmin(admin.ModelAdmin):
    model = Agendamento
    list_display = ['Processo','Horario']
    search_fields = ['Processo']

admin.site.register(Agendamento, AgendamentoAdmin)