from django.db import connection
from django.db.models import Max, Subquery
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import LeituraSensor
from .serializers import LeituraSensorSerializer
from rest_framework import status

@api_view(['GET'])
def obter_leituras(request):
    connection.close()  # Fecha a conexão para garantir que busque dados novos

    # Busca as leituras cujo ID é o maior de cada andar (último registro inserido)
    leituras_recentes = (
        LeituraSensor.objects
        .filter(id__in=Subquery(
            LeituraSensor.objects
            .values('andar')
            .annotate(max_id=Max('id'))
            .values('max_id')
        ))
        .order_by('andar')
    )

    # Serializa e retorna a resposta
    serializer = LeituraSensorSerializer(leituras_recentes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def receber_leitura(request):
    """
    Endpoint para o ESP32 enviar novas leituras via HTTPS POST.
    Payload esperado: {"andar": "3º Andar", "valor_leitura": 12.50}
    """
    serializer = LeituraSensorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save() # Salva direto no PostgreSQL
        return Response(
            {"status": "sucesso", "dados": serializer.data}, 
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)