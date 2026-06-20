from django.db import models

class Dispenser(models.Model):
    nome = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=255)    
    instituicao = models.CharField(max_length=100)
    bloco = models.CharField(max_length=50)
    andar = models.IntegerField()
    ativo = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nome} - {self.instituicao} (Bloco {self.bloco}, {self.andar}º Andar)"
    
class LeituraSensor(models.Model):

    dispenser = models.ForeignKey(
        Dispenser, 
        on_delete=models.CASCADE, 
        related_name='leituras'
    )
    timestamp = models.DateTimeField(auto_now_add=True)  # Unificação de data + hora
    distancia_cm = models.DecimalField(max_digits=6, decimal_places=2)
    
    # Dados processados pelo Backend (calculados automaticamente antes de salvar)
    quantidade_estimada = models.IntegerField(blank=True, null=True)
    porcentagem_ocupacao = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Leitura #{self.id} | Dispenser: {self.dispenser.nome} | {self.distancia_cm} cm"

    def save(self, *args, **kwargs):
        MIN_CM = 2
        MAX_CM = 30

        if self.distancia_cm < MIN_CM:
            porcentagem = 100.0
        elif self.distancia_cm > MAX_CM:
            porcentagem = 0.0
        else:
            porcentagem = ((MAX_CM - float(self.distancia_cm)) / (MAX_CM - MIN_CM)) * 100
        
        self.porcentagem_ocupacao = round(porcentagem, 2)


        CAPACIDADE_MAXIMA = 20 # REVISAR
        self.quantidade_estimada = int((porcentagem / 100) * CAPACIDADE_MAXIMA)

        super().save(*args, **kwargs)