from rest_framework import serializers
from .models import LeituraSensor

class LeituraSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeituraSensor
        fields = '__all__'
        
        read_only_fields = ['id', 'timestamp', 'quantidade_estimada', 'porcentagem_ocupacao']