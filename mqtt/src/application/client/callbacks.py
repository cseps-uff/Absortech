import json
import logging
from decimal import Decimal, InvalidOperation

from app.models import Dispenser, LeituraSensor

from ...config.broker_configs import mqtt_broker_configs


logger = logging.getLogger(__name__)
MAX_DISTANCIA_CM = Decimal('9999.99')


def on_connect(client, user_data, flags, rc):
    if rc == 0:
        logger.info("Cliente MQTT conectado")
        client.subscribe(mqtt_broker_configs["TOPIC"])
    else:
        logger.error("Falha ao conectar ao MQTT: código %s", rc)


def on_subscribe(client, user_data, message_id, granted_qos):
    logger.info(
        "Inscrito no tópico %s com QoS %s",
        mqtt_broker_configs["TOPIC"],
        granted_qos,
    )


def _obter_distancia(payload):
    valor = payload.get(
        'distancia_cm',
        payload.get('measure', payload.get('distance')),
    )
    if valor is None:
        raise ValueError("Campo 'distancia_cm' não informado")

    try:
        distancia = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError) as error:
        raise ValueError("Campo 'distancia_cm' inválido") from error

    if not distancia.is_finite() or distancia < 0 or distancia > MAX_DISTANCIA_CM:
        raise ValueError("Campo 'distancia_cm' fora do intervalo aceito")

    return distancia


def _obter_dispenser(payload):
    dispenser_id = payload.get('dispenser_id')
    if dispenser_id is not None:
        try:
            return Dispenser.objects.get(id=int(dispenser_id), ativo=True)
        except (TypeError, ValueError, Dispenser.DoesNotExist) as error:
            raise ValueError("Dispenser ativo não encontrado") from error

    # Compatibilidade temporária com o firmware antigo, que identificava apenas o andar.
    andar = payload.get('andar', payload.get('floor'))
    if andar is None:
        raise ValueError("Campo 'dispenser_id' não informado")

    try:
        andar = int(andar)
    except (TypeError, ValueError) as error:
        raise ValueError("Campo legado 'andar' inválido") from error

    dispensers = Dispenser.objects.filter(andar=andar, ativo=True)
    if dispensers.count() != 1:
        raise ValueError(
            "O payload legado por andar exige exatamente um dispenser ativo"
        )
    return dispensers.get()


def processar_payload(payload):
    if not isinstance(payload, dict):
        raise ValueError("O payload MQTT deve ser um objeto JSON")

    dispenser = _obter_dispenser(payload)
    distancia = _obter_distancia(payload)

    return LeituraSensor.objects.create(
        dispenser=dispenser,
        distancia_cm=distancia,
    )


def on_message(client, user_data, message):
    try:
        payload = json.loads(message.payload.decode('utf-8'))
        leitura = processar_payload(payload)
        logger.info(
            "Leitura salva: dispenser=%s distância=%scm quantidade=%s ocupação=%s%%",
            leitura.dispenser_id,
            leitura.distancia_cm,
            leitura.quantidade_estimada,
            leitura.porcentagem_ocupacao,
        )
    except UnicodeDecodeError:
        logger.exception("Payload MQTT não está codificado em UTF-8")
    except json.JSONDecodeError:
        logger.exception("Payload MQTT não contém JSON válido")
    except ValueError as error:
        logger.warning("Payload MQTT rejeitado: %s", error)
    except Exception:
        logger.exception("Erro inesperado ao processar mensagem MQTT")
