from django.db import connection
from django.db.models import Max, Subquery
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
