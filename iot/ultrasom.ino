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

// Configurações HTTPS
const char* server_url = "https://ec2-18-231-186-125.sa-east-1.compute.amazonaws.com/api/leituras/enviar/";

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

  //Le as informacoes do sensor, em cm e pol
  float cmMsec;
  long microsec = ultrasonic.timing();
  
  cmMsec = ultrasonic.convert(microsec, Ultrasonic::CM);

  //Exibe informacoes no serial monitor
  Serial.print("Distancia em cm: ");
  Serial.print(cmMsec);

  if (Wifi.status() == WL_CONNECTED){
    WifiClient client;
    HTTPClient http;

    http.begin(client, server_url);
    http.addHeader("Content-Type", "application.json");

    // GUARDA AS INFORMAÇÕES NO OBJETO JSON
    StaticJsonDocument<128> doc;
    doc["measure"] = cmMsec;
    doc["andar"] = ANDAR;
    
    String jsonOutput;
    serializeJson(doc, jsonOutput);

    // Executa o POST (Operação síncrona, aguarda resposta do Django)
    int httpResponseCode = http.POST(jsonOutput);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("Código de resposta HTTP: ");
      Serial.println(httpResponseCode);
      Serial.print("Resposta do servidor: ");
      Serial.println(response);
    } else {
      Serial.print("Erro no envio do POST: ");
      Serial.println(httpResponseCode);
    }

    // Encerra a conexão HTTP aberta
    http.end();
  }

  // Desconecta o Wi-Fi de forma limpa antes de dormir para poupar energia do roteador
  WiFi.disconnect(true);
  
  // Imprime aviso final e entra em Deep Sleep por 10 minutos
  Serial.println("Entrando em modo Deep Sleep...");
  esp_sleep_enable_timer_wakeup(MINUTES_TO_SLEEP * uS_TO_MINUTE_FACTOR);
  esp_deep_sleep_start();
}

void loop() {
  
}