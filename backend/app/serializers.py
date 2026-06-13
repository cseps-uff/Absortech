from rest_framework import serializers
from .models import LeituraSensor, Dispenser

class DispenserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispenser
        fields = [
            'id',
            'nome',
            'localizacao',
            'instituicao',
            'bloco',
            'andar',
            'ativo',
            'created_at'
        ]

class LeituraSensorSerializer(serializers.ModelSerializer):
    dispenser = DispenserSerializer(read_only=True)

    class Meta:
        model = LeituraSensor
        fields = [
            'id',
            'dispenser',
            'timestamp',
            'distancia_cm',
            'quantidade_estimada',
            'porcentagem_ocupacao'
        ]
