from django.db import connection
from django.db.models import Max, Subquery
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import LeituraSensor
from .serializers import LeituraSensorSerializer
from rest_framework import status

@api_view(['GET'])
def obter_status_atual_dispensers(request):
    """
    Retorna a última leitura de cada dispenser cadastrado,
    alimentando os cards e gráficos em tempo real do Frontend.
    """
    connection.close()

    # Busca as leituras cujo ID é o maior para cada dispenser
    ultimas_leituras = (
        LeituraSensor.objects
        .filter(id__in=Subquery(
            LeituraSensor.objects
            .values('dispenser')  # Agrupa por dispenser, não mais por andar livre
            .annotate(max_id=Max('id'))
            .values('max_id')
        ))
        .order_by('dispenser__andar')  # Ordena o resultado pelo andar mapeado no Dispenser
    )

    serializer = LeituraSensorSerializer(ultimas_leituras, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def endpoint_leituras_esp32(request):
    """
    Endpoint para o ESP32 enviar novas leituras via HTTPS POST.
    Payload esperado:
    {
        "dispenser": 1,
        "distancia_cm": 12.50
    }
    """
    serializer = LeituraSensorSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save() # Salva direto no PostgreSQL
        return Response(
            {"status": "sucesso", "dados": serializer.data}, 
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)