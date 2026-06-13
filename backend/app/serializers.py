from rest_framework import serializers
from .models import LeituraSensor, Dispenser

class DispenserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispenser
        fields = '__all__'

class LeituraSensorSerializer(serializers.ModelSerializer):
    dispenser = DispenserSerializer(read_only=True)
    
    class Meta:
        model = LeituraSensor
        fields = '__all__'
