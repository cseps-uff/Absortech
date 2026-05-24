from django.db import models

class Dispenser(models.Model):
    nome = models.CharField(max_length=100)
    localização = models.CharField(max_length=255)
    instituicao = models.CharField(max_length=100)
    bloco = models.CharField(max_length=50)
    andar = models.IntegerField()
    ativo = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nome} - {self.instituicao} (Bloco {self.bloco}, {self.andar}º Andar)"
    
class LeituraSensor(models.Model):
    andar = models.CharField(max_length=50)
    data = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    valor_leitura = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.andar} - {self.data} {self.hora} - {self.valor_leitura} cm"

    def calcular_porcentagem(self):
        """
        Converte o valor da leitura de centímetros para porcentagem.
        2 cm = 100%, 30 cm = 0%
        """
        MIN_CM = 2
        MAX_CM = 30

        # Garantir que o valor esteja dentro do intervalo esperado
        if self.valor_leitura < MIN_CM:
            return 100.0  # 100% se for menor que o mínimo
        elif self.valor_leitura > MAX_CM:
            return 0.0  # 0% se for maior que o máximo

        # Cálculo da porcentagem
        porcentagem = ((MAX_CM - float(self.valor_leitura)) / (MAX_CM - MIN_CM)) * 100
        return round(porcentagem, 2)  # Retorna com 2 casas decimais
