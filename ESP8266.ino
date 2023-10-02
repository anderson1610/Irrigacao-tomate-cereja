// Inclua a biblioteca ESP8266WiFi
#include <ESP8266WiFi.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

#define SENSOR_TEMPERATURA A0
#define DHTPIN D3      
#define DHTTYPE DHT11   
DHT dht(DHTPIN, DHTTYPE);

// Defina o nome da sua rede Wi-Fi e a senha
const char* ssid = "Anderson";
const char* password = "";

const char* serverIP = "192.168.15.48"; // Endereço IP do servidor onde a API Flask está hospedada
const int serverPort = 5000; // Porta na qual a API Flask está escutando
const String apiEndpoint = "/adicionar_dados"; // Rota da API para adicionar dados
const String apiEndpoint2 = "/obter_dados_markov"; // Rota da API para obter dados da planilha Markov2023

WiFiClient wifiClient; // Criar um objeto WiFiClient

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

// Pino onde a boia está conectada
const int boiaPin = D2;
int bomba1 = D5;
int bomba2 = D6;
int solenoide = D7;
int sensorFluxoAgua = D1;
volatile long pulse;
float volume; //Onde é armazenada o consumo de agua
int dataInt; //Data atual em formato INT
String mes;
float probabilidade;


void setup() {

  // Inicialize a comunicação serial
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(boiaPin, INPUT); //define o pino do sensor como entrada 
  dht.begin();
  pinMode(bomba1, OUTPUT);
  pinMode(bomba2, OUTPUT);
  pinMode(solenoide, OUTPUT);
  pinMode(sensorFluxoAgua, INPUT);
  attachInterrupt(digitalPinToInterrupt(sensorFluxoAgua), increase, RISING);
  

  // Conecte-se à rede Wi-Fi
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }
  Serial.println("Conectado ao WiFi");
  digitalWrite(LED_BUILTIN, HIGH);
  timeClient.begin();
  timeClient.setTimeOffset(0); // Defina o deslocamento de fuso horário, se necessário
}

void loop() /*laço de repetição*/
{ 
  verificarBoia();
  verificarTemperatura();
  verificarUmidadeSolo();
  obter_Markov();
}

void obter_Markov(){

// Inicializar o cliente HTTP
  HTTPClient http;

  // Construir a URL da solicitação
  String url = "http://" + String(serverIP) + ":" + String(serverPort) + apiEndpoint2;

  // Enviar uma solicitação GET para obter os dados da planilha Markov2023
  http.begin(wifiClient, url); // Use wifiClient como primeiro argumento

  int httpResponseCode = http.GET();

  // Verificar a resposta da solicitação
  if (httpResponseCode == HTTP_CODE_OK) {
    String response = http.getString();
    Serial.println("Resposta da API:");
    Serial.println(response);

    // Fazer o parsing dos dados JSON
    DynamicJsonDocument doc(1024); // Tamanho do buffer deve ser ajustado conforme necessário
    deserializeJson(doc, response);

    // Extrair os valores das colunas Mes e Probabilidade
    mes = doc["Mes"].as<String>();
    probabilidade = doc["Probabilidade"].as<float>();

    // Agora você pode usar as variáveis mes e probabilidade conforme necessário
    Serial.print("Mês: ");
    Serial.println(mes);
    Serial.print("Probabilidade: ");
    Serial.println(probabilidade);
  } else {
    Serial.print("Erro na solicitação HTTP. Código de resposta: ");
    Serial.println(httpResponseCode);
  }

  // Liberar recursos do cliente HTTP
  http.end();
}

void add_custoAgua(){
  int valorData = dataAtual();

  // Montar os dados em um formato JSON
  String jsonData = "{\"Data\":" + String(valorData) + ",\"Gasto\":" + String(volume) + "}";

  // Inicializar o cliente HTTP
  HTTPClient http;

  // Construir a URL da solicitação
  String url = "http://" + String(serverIP) + ":" + String(serverPort) + apiEndpoint;

  // Enviar uma solicitação POST com os dados JSON
  http.begin(wifiClient, url); // Use wifiClient como primeiro argumento

  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(jsonData);

  // Verificar a resposta da solicitação
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("Resposta da API: " + response);
  } else {
    Serial.print("Erro na solicitação HTTP. Código de resposta: ");
    Serial.println(httpResponseCode);
  }

  // Liberar recursos do cliente HTTP
  http.end();

}


int dataAtual(){

  timeClient.update();

  // Obter a data e hora atual
  time_t rawTime = timeClient.getEpochTime();
  struct tm *timeInfo = localtime(&rawTime);

  // Formatar a data no formato numérico (ddmmyyyy)
  int dataInt = (timeInfo->tm_mday * 1000000) + ((timeInfo->tm_mon + 1) * 10000) + (1900 + timeInfo->tm_year);

  Serial.print("Data atual em formato numérico: ");
  //Serial.println(dataInt);
  return dataInt;
}

void medirFluxoAgua(){

  volume = (pulse * 4.5) / 1000.0;
  Serial.print(volume);
  Serial.println(" L/min");
}

ICACHE_RAM_ATTR void increase() {
  pulse++;
}

void verificarBoia(){
  int estado = digitalRead(boiaPin); /*estado é igual a leitura digital*/
  Serial.print("Estado sensor : "); /*Printa "Estado do sensor:" */
  Serial.println(estado); /*Printa a leitura de estado*/
  if (estado == 0){
    Serial.println("Enchendo o reservatorio");
    digitalWrite(solenoide, LOW);
    medirFluxoAgua();
  } else{
    Serial.println("Reservatorio cheio");
    digitalWrite(solenoide, HIGH);
  }
  delay(100); /*atraso de 0,1s*/
}

void verificarTemperatura(){
  delay(100);  // Aguarde alguns segundos entre as leituras

  float temperatura = dht.readTemperature();  // Leia a temperatura em graus Celsius
  float umidade = dht.readHumidity();         // Leia a umidade relativa

  if (isnan(temperatura) || isnan(umidade)) {
    Serial.println("Falha ao ler o sensor DHT11!");
  } else {
    Serial.print("Temperatura: ");
    Serial.print(temperatura);
    Serial.println(" °C");

    Serial.print("Umidade: ");
    Serial.print(umidade);
    Serial.println(" %");
  }

}

void verificarUmidadeSolo(){

  int valorAnalogico = analogRead(SENSOR_TEMPERATURA);
  float umidadeSolo = valorAnalogico;
  
  Serial.print("Umidade do solo: ");
  Serial.print(umidadeSolo);
  Serial.println("%");
  digitalWrite(bomba1, LOW);

  delay(100);  // Aguarde alguns segundos entre as leituras

}
