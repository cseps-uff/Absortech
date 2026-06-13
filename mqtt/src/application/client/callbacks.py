import json
from django.utils import timezone
from app.models import LeituraSensor, Dispenser
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
        distancia_cm = float(payload.get("measure", payload.get("distance", 0)))
        
        # Tentar obter dispenser_id do payload, ou usar floor como fallback
        dispenser_id = payload.get("dispenser_id")
        floor = payload.get("andar", payload.get("floor", "1"))

        print("========== DEBUG ==========")
        print(f"Raw message received: {message.payload}")
        print(f"Decoded JSON: {payload}")
        print(f"Floor received: {floor}")
        print(f"Distance value received: {distancia_cm}")
        print(f"Dispenser ID: {dispenser_id}")
        
        # Parâmetros para conversão
        MIN_CM = 2       # Distância quando está cheio (máxima leitura)
        MAX_CM = 30      # Distância quando está vazio (mínima leitura)
        
        # Garantir que a medida está dentro dos limites esperados
        distancia_clamped = max(min(distancia_cm, MAX_CM), MIN_CM)
        
        # Calcular porcentagem de ocupação
        if distancia_clamped < MIN_CM:
            porcentagem = 100.0
        elif distancia_clamped > MAX_CM:
            porcentagem = 0.0
        else:
            porcentagem = ((MAX_CM - distancia_clamped) / (MAX_CM - MIN_CM)) * 100
        
        porcentagem_ocupacao = round(porcentagem, 2)
        
        # Calcular quantidade estimada (capacidade máxima = 20 absorventes)
        CAPACIDADE_MAXIMA = 20
        quantidade_estimada = int((porcentagem / 100) * CAPACIDADE_MAXIMA)
        
        print(f"Distância original do sensor: {distancia_cm} cm")
        print(f"Distância limitada: {distancia_clamped} cm")
        print(f"Percentual de ocupação: {porcentagem_ocupacao}%")
        print(f"Quantidade estimada: {quantidade_estimada}")
        print("===========================")

        # Buscar ou criar dispenser
        if dispenser_id:
            try:
                dispenser = Dispenser.objects.get(id=dispenser_id, ativo=True)
            except Dispenser.DoesNotExist:
                print(f"Dispenser com ID {dispenser_id} não encontrado")
                return
        else:
            # Se não houver dispenser_id, tentar buscar pelo andar ou criar um padrão
            dispenser, _ = Dispenser.objects.get_or_create(
                andar=int(floor) if floor.isdigit() else 1,
                defaults={
                    'nome': f'Dispenser Andar {floor}',
                    'localização': f'Andar {floor}',
                    'instituicao': 'Padrão',
                    'bloco': 'Geral',
                    'ativo': True
                }
            )

        # Criar registro de leitura
        leitura = LeituraSensor(
            timestamp=now,
            dispenser=dispenser,
            distancia_cm=distancia_clamped,
            quantidade_estimada=quantidade_estimada,
            porcentagem_ocupacao=porcentagem_ocupacao
        )

        # Salvar no banco de dados
        leitura.save()

        print(f"Data saved to database -> Timestamp: {leitura.timestamp}, "
              f"Dispenser: {leitura.dispenser.nome}, Distance: {leitura.distancia_cm} cm, "
              f"Quantity: {leitura.quantidade_estimada}, Occupancy: {leitura.porcentagem_ocupacao}%")

    except json.JSONDecodeError as error:
        print("Invalid JSON message!", error)
    except Exception as error:
        print("Error processing message:", error)
        import traceback
        traceback.print_exc()
