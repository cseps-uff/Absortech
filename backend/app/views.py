from django.db import connection
from django.db.models import Max, Subquery
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import LeituraSensor, Dispenser
from .serializers import LeituraSensorSerializer, DispenserSerializer
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def obter_leituras(request):
    try:
        connection.close()  # Fecha a conexão para garantir que busque dados novos

        # Busca as leituras mais recentes de cada dispenser ativo
        subquery = LeituraSensor.objects \
            .filter(dispenser__ativo=True) \
            .values('dispenser_id') \
            .annotate(max_id=Max('id')) \
            .values('max_id')
        
        leituras_recentes = LeituraSensor.objects \
            .filter(
                dispenser__ativo=True,
                id__in=Subquery(subquery)
            ) \
            .order_by('dispenser__andar', 'dispenser__bloco') \
            .select_related('dispenser')

        # Serializa e retorna a resposta
        serializer = LeituraSensorSerializer(leituras_recentes, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.exception("Erro ao buscar leituras")
        return Response({"error": str(e)}, status=500)
