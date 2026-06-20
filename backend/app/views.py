import logging

from django.db.models import OuterRef, Subquery
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import LeituraSensor
from .serializers import LeituraSensorSerializer

logger = logging.getLogger(__name__)


@api_view(['GET'])
def obter_leituras(request):
    try:
        leitura_mais_recente = (
            LeituraSensor.objects
            .filter(dispenser_id=OuterRef('dispenser_id'))
            .order_by('-timestamp', '-id')
            .values('id')[:1]
        )

        leituras_recentes = (
            LeituraSensor.objects
            .filter(
                dispenser__ativo=True,
                id=Subquery(leitura_mais_recente)
            )
            .select_related('dispenser')
            .order_by(
                'dispenser__instituicao',
                'dispenser__bloco',
                'dispenser__andar',
                'dispenser__nome'
            )
        )

        serializer = LeituraSensorSerializer(leituras_recentes, many=True)
        return Response(serializer.data)
    except Exception:
        logger.exception("Erro ao buscar leituras")
        return Response(
            {'error': 'Nao foi possivel buscar as leituras.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
