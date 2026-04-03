import json
from django.utils import timezone
from app.models import LeituraSensor
from src.config.broker_configs import mqtt_broker_configs


def on_connect(client, user_data, flags, rc):
    if rc == 0:
        print("Client connected successfully! {}".format(client))
        client.subscribe(mqtt_broker_configs["TOPIC"])
    else:
        print("Connection error! code = {}".format(rc))


def on_subscribe(client, user_data, message_id, granted_qos):
    print("Client subscribed to {}".format(mqtt_broker_configs["TOPIC"]))
    print("QOS {}".format(granted_qos))


def on_message(client, user_data, message):
    print("Message received!")
    print(client)

    try:
        payload_str = message.payload.decode("utf-8")
    except UnicodeDecodeError:
        payload_str = message.payload.decode("latin-1")

    try:
        now = timezone.now()

        # Decoding dos dados JSON
        payload = json.loads(payload_str)
        measure = payload["measure"]
        floor = payload["andar"]

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

        # Cria um objeto com dados JSON
        leitura = LeituraSensor(
            data=now.date(),
            hora=now.time(),
            andar=floor,
            valor_leitura=absorventes_restantes
        )

        # Salva no banco de dados
        leitura.save()

        print(f"Data saved to database -> Date: {leitura.data}, Time: {leitura.hora}, "
              f"Floor: {leitura.andar}, Sensor Value: {leitura.valor_leitura}")

    except json.JSONDecodeError as error:
        print("Invalid JSON message!", error)
    except Exception as error:
        print("Error processing message:", error)
