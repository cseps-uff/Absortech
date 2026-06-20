from datetime import timedelta
from decimal import Decimal

from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Dispenser, LeituraSensor


class LeituraSensorModelTests(TestCase):
    def setUp(self):
        self.dispenser = Dispenser.objects.create(
            nome='Dispenser principal',
            localizacao='Corredor central',
            instituicao='Instituicao A',
            bloco='A',
            andar=1
        )

    def test_calcula_ocupacao_e_quantidade_a_partir_da_distancia(self):
        leitura = LeituraSensor.objects.create(
            dispenser=self.dispenser,
            distancia_cm=Decimal('16.00')
        )

        self.assertEqual(leitura.porcentagem_ocupacao, Decimal('50.00'))
        self.assertEqual(leitura.quantidade_estimada, 10)

    def test_limita_apenas_o_calculo_e_preserva_a_leitura_bruta(self):
        leitura = LeituraSensor.objects.create(
            dispenser=self.dispenser,
            distancia_cm=Decimal('35.00')
        )

        self.assertEqual(leitura.distancia_cm, Decimal('35.00'))
        self.assertEqual(leitura.porcentagem_ocupacao, Decimal('0.00'))
        self.assertEqual(leitura.quantidade_estimada, 0)

    def test_recalcula_campos_processados_com_update_fields(self):
        leitura = LeituraSensor.objects.create(
            dispenser=self.dispenser,
            distancia_cm=Decimal('30.00')
        )

        leitura.distancia_cm = Decimal('2.00')
        leitura.save(update_fields=['distancia_cm'])
        leitura.refresh_from_db()

        self.assertEqual(leitura.porcentagem_ocupacao, Decimal('100.00'))
        self.assertEqual(leitura.quantidade_estimada, 20)

    def test_preserva_historico_ao_excluir_dispenser(self):
        LeituraSensor.objects.create(
            dispenser=self.dispenser,
            distancia_cm=Decimal('10.00'),
        )

        with self.assertRaises(ProtectedError):
            self.dispenser.delete()


class ObterLeiturasApiTests(TestCase):
    def setUp(self):
        self.dispenser = Dispenser.objects.create(
            nome='Dispenser principal',
            localizacao='Corredor central',
            instituicao='Instituicao A',
            bloco='A',
            andar=1
        )
        self.inativo = Dispenser.objects.create(
            nome='Dispenser inativo',
            localizacao='Almoxarifado',
            instituicao='Instituicao A',
            bloco='B',
            andar=2,
            ativo=False
        )

    def test_retorna_apenas_a_leitura_mais_recente_de_cada_dispenser_ativo(self):
        agora = timezone.now()
        LeituraSensor.objects.create(
            dispenser=self.dispenser,
            timestamp=agora - timedelta(minutes=10),
            distancia_cm=Decimal('20.00')
        )
        recente = LeituraSensor.objects.create(
            dispenser=self.dispenser,
            timestamp=agora,
            distancia_cm=Decimal('10.00')
        )
        LeituraSensor.objects.create(
            dispenser=self.inativo,
            timestamp=agora,
            distancia_cm=Decimal('5.00')
        )

        response = self.client.get(reverse('obter_leituras'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], recente.id)
        self.assertEqual(
            response.json()[0]['dispenser']['localizacao'],
            'Corredor central'
        )
        self.assertEqual(response.json()[0]['distancia_cm'], '10.00')
