from decimal import Decimal

from django.test import TestCase

from app.models import Dispenser, LeituraSensor
from .callbacks import processar_payload


class ProcessarPayloadTests(TestCase):
    def setUp(self):
        self.dispenser = Dispenser.objects.create(
            nome='Dispenser 1',
            localizacao='Corredor principal',
            instituicao='Instituição A',
            bloco='A',
            andar=1,
        )

    def test_processa_payload_canonico_sem_perder_distancia_bruta(self):
        leitura = processar_payload({
            'dispenser_id': self.dispenser.id,
            'distancia_cm': 35.4,
        })

        self.assertEqual(leitura.distancia_cm, Decimal('35.4'))
        self.assertEqual(leitura.quantidade_estimada, 0)
        self.assertEqual(leitura.porcentagem_ocupacao, Decimal('0.00'))

    def test_aceita_payload_legado_quando_andar_identifica_um_dispenser(self):
        leitura = processar_payload({'andar': 1, 'measure': 2})

        self.assertEqual(leitura.dispenser, self.dispenser)
        self.assertEqual(leitura.quantidade_estimada, 20)

    def test_rejeita_payload_sem_identificacao_do_dispenser(self):
        with self.assertRaisesMessage(ValueError, "dispenser_id"):
            processar_payload({'distancia_cm': 10})

        self.assertFalse(LeituraSensor.objects.exists())

    def test_rejeita_andar_legado_ambiguo(self):
        Dispenser.objects.create(
            nome='Dispenser 2',
            localizacao='Outro corredor',
            instituicao='Instituição A',
            bloco='B',
            andar=1,
        )

        with self.assertRaisesMessage(ValueError, "exatamente um"):
            processar_payload({'andar': 1, 'measure': 10})

    def test_rejeita_distancia_invalida(self):
        with self.assertRaisesMessage(ValueError, "fora do intervalo"):
            processar_payload({
                'dispenser_id': self.dispenser.id,
                'distancia_cm': -1,
            })
