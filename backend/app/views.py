import json
from django.db import connection  # ADIÇÃO: Necessário para a view obter_leituras
from django.db.models import Max, Subquery  # ADIÇÃO: Necessário para as queries da view obter_leituras
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import LeituraSensor
from .serializers import LeituraSensorSerializer


@api_view(['GET'])
def obter_leituras(request):
    connection.close()  # Mantido seu comportamento original para renovar a conexão

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


@api_view(['POST'])  # CORREÇÃO: Removido o caractere incorreto '@apit_view'
def receber_leitura(request):
    try:
        payload = request.data
        measure = payload["measure"]
        andar = payload["andar"]  # Definição correta da variável

        now = timezone.now()

        print("========== DEBUG HTTPS ==========")
        print(f"Decoded JSON: {payload}")
        print(f"Floor received: {andar}")  # CORREÇÃO: Substituído 'floor' por 'andar'
        print(f"Measure value received: {measure}")

        # Parâmetros para conversão
        VALOR_MAXIMO = 3.35  # Valor quando a caixa está cheia (10 absorventes)
        VALOR_MINIMO = 16.32  # Valor quando a caixa está vazia (0 absorventes)
        ABSORVENTES_TOTAL = 10  # Capacidade máxima da caixa
        
        # Garantir que a medida está dentro dos limites esperados
        measure_clamped = max(min(measure, VALOR_MINIMO), VALOR_MAXIMO)
        
        # Converter valor do sensor para quantidade de absorventes
        proporcao = (measure_clamped - VALOR_MINIMO) / (VALOR_MAXIMO - VALOR_MINIMO)
        
        # Quantidade de absorventes (arredondado para inteiro)
        absorventes_restantes = round(proporcao * ABSORVENTES_TOTAL)
        absorventes_restantes = max(0, min(ABSORVENTES_TOTAL, absorventes_restantes))
        
        print(f"Valor original do sensor: {measure}")
        print(f"Valor limitado: {measure_clamped}")
        print(f"Absorventes restantes: {absorventes_restantes}")
        print("=================================")

        # Criando o objeto com os dados corrigidos
        leitura = LeituraSensor(
            data=now.date(),
            hora=now.time(),
            andar=andar,  # CORREÇÃO: Substituído 'floor' por 'andar'
            valor_leitura=absorventes_restantes
        )
        
        # Salvando no banco de dados PostgreSQL
        leitura.save()

        print(f"Data saved to database -> Date: {leitura.data}, Time: {leitura.hora}, "
              f"Floor: {leitura.andar}, Sensor Value: {leitura.valor_leitura}")

        serializer = LeituraSensorSerializer(leitura)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except KeyError as error:
        # CORREÇÃO: Captura chaves ausentes no JSON antes de estourar erro 500
        print(f"Missing key in payload: {error}")
        return Response({'error': f'Chave obrigatória ausente: {error}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        print("Error processing message:", error)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)