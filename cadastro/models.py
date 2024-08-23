from django.db import models

atualizacao_choices = (('Diário','Diário'),('Mensal','Mensal'),('Semanal','Semanal'),('Anual','Anual'),('Sob Demanda','Sob Demanda'),('Inativado','Inativado'))
linguagem_choices = (('Python','Python'),('R','R'))

class Processo(models.Model):
    Processo = models.CharField(max_length=200)
    Path_Arquivo_Saida = models.CharField(max_length=200, blank=True)
    Script_File = models.CharField(max_length=200, blank=True)
    Linguagem = models.CharField(max_length = 10,choices= linguagem_choices,default= 'Python')
    Atualizacao = models.CharField(max_length = 13,choices= atualizacao_choices,default= 'Mensal')
    Descricao = models.TextField(blank = True)

    def __str__(self):
        return str(self.Processo)

processo_choices = [(processo.Processo, processo.Processo) for processo in Processo.objects.all()]

class Agendamento(models.Model):
    Processo = models.CharField(max_length=200, choices = processo_choices)
    Horario = models.TimeField(auto_now=False, auto_now_add=False, blank=True)
    Descricao = models.TextField(blank = True)

    def __str__(self):
        return str(self.Processo)