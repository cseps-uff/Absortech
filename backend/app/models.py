from decimal import Decimal, ROUND_FLOOR

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Dispenser(models.Model):
    nome = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=255)
    instituicao = models.CharField(max_length=100)
    bloco = models.CharField(max_length=50)
    andar = models.IntegerField()
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['instituicao', 'bloco', 'andar', 'nome']
        indexes = [
            models.Index(
                fields=['instituicao', 'bloco', 'andar'],
                name='dispenser_location_idx'
            )
        ]

    def __str__(self):
        return f"{self.nome} - {self.instituicao} (Bloco {self.bloco}, {self.andar}º Andar)"


class LeituraSensor(models.Model):
    DISTANCIA_CHEIO_CM = Decimal('2.00')
    DISTANCIA_VAZIO_CM = Decimal('30.00')
    CAPACIDADE_MAXIMA = 20

    dispenser = models.ForeignKey(
        Dispenser,
        on_delete=models.PROTECT,
        related_name='leituras',
    )
    timestamp = models.DateTimeField(default=timezone.now)
    distancia_cm = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    quantidade_estimada = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
        validators=[MinValueValidator(0)]
    )
    porcentagem_ocupacao = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        editable=False,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )

    class Meta:
        ordering = ['-timestamp', '-id']
        indexes = [
            models.Index(fields=['timestamp'], name='leitura_timestamp_idx'),
            models.Index(
                fields=['dispenser', '-timestamp'],
                name='leitura_disp_ts_idx'
            )
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(distancia_cm__gte=0),
                name='leitura_distancia_nonneg'
            ),
            models.CheckConstraint(
                condition=Q(quantidade_estimada__isnull=True)
                | Q(quantidade_estimada__gte=0),
                name='leitura_quantidade_nonneg'
            ),
            models.CheckConstraint(
                condition=Q(porcentagem_ocupacao__isnull=True)
                | Q(
                    porcentagem_ocupacao__gte=0,
                    porcentagem_ocupacao__lte=100
                ),
                name='leitura_ocupacao_range'
            )
        ]

    def __str__(self):
        return f"Leitura #{self.id} | Dispenser: {self.dispenser.nome} | {self.distancia_cm} cm"

    def save(self, *args, **kwargs):
        distancia = Decimal(str(self.distancia_cm))
        distancia_limitada = min(
            max(distancia, self.DISTANCIA_CHEIO_CM),
            self.DISTANCIA_VAZIO_CM
        )
        porcentagem = (
            (self.DISTANCIA_VAZIO_CM - distancia_limitada)
            / (self.DISTANCIA_VAZIO_CM - self.DISTANCIA_CHEIO_CM)
            * Decimal('100')
        )

        self.porcentagem_ocupacao = porcentagem.quantize(Decimal('0.01'))
        self.quantidade_estimada = int(
            (
                porcentagem
                / Decimal('100')
                * self.CAPACIDADE_MAXIMA
            ).to_integral_value(rounding=ROUND_FLOOR)
        )

        if kwargs.get('update_fields') is not None:
            kwargs['update_fields'] = set(kwargs['update_fields']) | {
                'quantidade_estimada',
                'porcentagem_ocupacao',
            }

        super().save(*args, **kwargs)
