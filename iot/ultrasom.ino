#include <WiFi.h>
#include <PubSubClient.h>
#include <Ultrasonic.h>
#include <ArduinoJson.h>

#define MINUTES_TO_SLEEP    10
#define uS_TO_MINUTE_FACTOR 60000000
#define ANDAR 1

// Configurações de Wi-Fi
const char* ssid = "nomeWifi";
const char* password = "SenhaWifi";

// Configurações do MQTT
const char *mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char *mqtt_topic = "SENSOR/ULTRASSOM";

// Criação dos objetos WiFi e MQTT
WiFiClient espClient;
PubSubClient client(espClient);

//Define os pinos para o trigger e echo
#define pino_trigger 23
#define pino_echo 22

//Inicializa o sensor nos pinos definidos acima
Ultrasonic ultrasonic(pino_trigger, pino_echo);

// Função para conectar ao Wi-Fi
void setup_wifi() {
  delay(10);

  Serial.println();
  Serial.print("Conectando-se a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

// Função de callback do MQTT (não será usada, mas precisa ser declarada)
void callback(char* topic, byte* message, unsigned int length) {}

// Função para conectar ao servidor MQTT
void reconnect() {
  while (!client.connected()) {
    Serial.print("Tentando conexão MQTT...");

    if (client.connect("ESP32Client")) {
      Serial.println("conectado");
    } else {
      Serial.print("falha, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 5 segundos");

      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  setup_wifi();

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

// INICIALIZANDO UM OBJETO JSON
StaticJsonDocument<128> doc;

void loop() {
  if (!client.connected())
    reconnect();

  //Le as informacoes do sensor, em cm e pol
  float cmMsec;
  long microsec = ultrasonic.timing();
  
  cmMsec = ultrasonic.convert(microsec, Ultrasonic::CM);

  //Exibe informacoes no serial monitor
  Serial.print("Distancia em cm: ");
  Serial.print(cmMsec);

  // GUARDA AS INFORMAÇÕES NO OBJETO JSON
  doc["measure"] = cmMsec;
  doc["andar"] = ANDAR;

  // TRANSFORMA O OBJETO JSON EM UMA STRING PARA SER ENVIADA
  String jsonOutput;
  serializeJson(doc, jsonOutput);

  Serial.print("\nPublicando: ");
  Serial.println(jsonOutput);

  // PUBLICA OS DADOS DO SENSOR
  client.publish(mqtt_topic, jsonOutput.c_str());
  client.loop();

  delay(300);

  // COLOCA O ESP32 PARA ESPERAR (MODO DE ECONOMIA) PELA QUANTIDADE DE MINUTOS ESPECIFICADA
  esp_sleep_enable_timer_wakeup(MINUTES_TO_SLEEP * uS_TO_MINUTE_FACTOR);
  esp_deep_sleep_start();
}
