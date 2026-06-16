import json
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import LeituraSensor
from .serializers import LeituraSensorSerializer

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

@apit_view(['POST'])
def receber_leitura(request):
    try:
        payload = request.data
        measure = payload["measure"]
        andar = payload["andar"]

        now = timezone.now()

        print("========== DEBUG ==========")
        print(f"Raw message received: {message.payload}")
        print(f"Decoded JSON: {payload}")
        print(f"Floor received: {floor}")
        print(f"Measure value received: {measure}")

        # Parâmetros para conversão
        VALOR_MAXIMO = 3.35  # Valor quando a caixa está cheia (10 absorventes)
        VALOR_MINIMO = 16.32  # Valor quando a caixa está vazia (0 absorventes)
        ABSORVENTES_TOTAL = 10  # Capacidade máxima da caixa
        
        # Garantir que a medida está dentro dos limites esperados
        measure_clamped = max(min(measure, VALOR_MINIMO), VALOR_MAXIMO)
        
        # Converter valor do sensor para quantidade de absorventes
        # Mapeamento linear inverso: valor menor = mais cheio
        proporcao = (measure_clamped - VALOR_MINIMO) / (VALOR_MAXIMO - VALOR_MINIMO)
        
        # Quantidade de absorventes (arredondado para inteiro)
        absorventes_restantes = round(proporcao * ABSORVENTES_TOTAL)
        
        # Garantir que fique entre 0 e 10
        absorventes_restantes = max(0, min(ABSORVENTES_TOTAL, absorventes_restantes))
        
        print(f"Valor original do sensor: {measure}")
        print(f"Valor limitado: {measure_clamped}")
        print(f"Absorventes restantes: {absorventes_restantes}")
        print("===========================")

        # Creating object with JSON data
        leitura = LeituraSensor(
            data=now.date(),
            hora=now.time(),
            andar=floor,
            valor_leitura=absorventes_restantes
        )
        # Saving to database
        leitura.save()

        print(f"Data saved to database -> Date: {leitura.data}, Time: {leitura.hora}, "
              f"Floor: {leitura.andar}, Sensor Value: {leitura.valor_leitura}")

        serializer = LeituraSensorSerializer(leitura)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
       

    except json.JSONDecodeError as error:
        print("Invalid JSON message!", error)
    except Exception as error:
        print("Error processing message:", error)

        
