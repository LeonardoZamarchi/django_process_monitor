from django.db import models



class Atualizado(models.Model):
    Processo = models.CharField(max_length=200)
    Tamanho_Arquivo = models.CharField(max_length=10)
    Ultima_Atualizacao = models.DateField()
    Atualizado_Vigente = models.BooleanField(default=False)
    Log_Execucao = models.TextField(blank = True)
    


    def __str__(self):
        return self.Processo
