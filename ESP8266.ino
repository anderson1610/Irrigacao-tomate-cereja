#include <ESP8266WiFi.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <TimeLib.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <BlynkSimpleEsp8266.h>
//Credenciais para acessar o APP BlynkIOT
#define BLYNK_TEMPLATE_ID ""
#define BLYNK_TEMPLATE_NAME ""
#define BLYNK_AUTH_TOKEN ""
#define BLYNK_PRINT Serial 

#define SENSOR_UMIDADE_DE_SOLO A0 //Sensor umidade de solo que recebe sinal analogico
#define SENSOR_UMIDADE_DE_SOLO2 D0 //Sensor umidade de solo que recebe sinal digital
#define DHTPIN D3      
#define DHTTYPE DHT11
#define LED_1   D4 //Led de sinalização que o programa esta sendo executado
#define LED_2   D8 //Led de sinalização de algo negativo

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

const int boiaPin = D2; // Pino onde a boia está conectada
int bomba1 = D5; // Pino onde a mini bomba d'agua esta conectada
int bomba2 = D6; // Pino onde a mini bomba d'agua 2 esta conectada
int solenoide = D7; // Pino onde a solenoide esta conectada
int sensorFluxoAgua = D1; //Pino onde o sensor de fluxo de agua esta conectado
volatile long pulse;
float volume; //Onde é armazenada o consumo de agua
int dataInt; //Data atual em formato INT
String mes;  //Mês da probabilidade adquirida por Markov
float probabilidade; //Probabilidade do Mes atual por Markov
float temperatura_api; // Temperatura de São Paulo fornecida pela API openweathermap
float umidade_api; // Umidade de São Paulo fornecida pela API openweathermap
int umidade_solo_ideal = 410; //Valor da umidade em que o solo deve estar
int umidade_solo_maxima = 510; //Valor maximo seco que a umidade possa chegar
int umidade_solo_minima = 370; //Valor da umididade maxima umida que possa chegar o solo, para não prejudicar o plantio

unsigned long previousMillisBoia = 0;
unsigned long previousMillisTemperatura = 0;
unsigned long previousMillisUmidadeSolo = 0;
unsigned long previousMillisObterMarkov = 0;
unsigned long previousMillisInfoOpenweathermap = 0;
unsigned long previousMillisAddCustoAgua = 0;

//Variaveis que coletam a probabilidade de chuva de acordo com Markov e definem como pausa na irrigação visando economia de agua
float probabilidade_convertida = probabilidade * 1000;
float pausa_probabilidade = 1000 + probabilidade_convertida;

const unsigned long intervalBoia = 10; // Intervalo para verificar a boia e outras funções que necessitam de verificação constante
const unsigned long intervalTemperatura = 30000; // Intervalo para verificar a temperatura (30 segundos)
const unsigned long intervalUmidadeSolo = pausa_probabilidade; // Intervalo para verificar a umidade do solo 
const unsigned long intervalObterMarkov = 300000; // Intervalo para obter dados de Markov (5 minutos)
const unsigned long intervalInfoOpenweathermap = 600000; // Intervalo para obter dados de OpenWeatherMap (10 minutos)
const unsigned long intervalAddCustoAgua =  300000;// Intervalo para adicionar dados de custo de água (5 minutos)

void setup() {

  // Inicialize a comunicação serial
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(LED_1, OUTPUT);
  pinMode(LED_2, OUTPUT);
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

  // Conecte-se ao Blynk
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, password, "blynk.cloud", 80);

  Serial.println("Conectado ao WiFi");
  digitalWrite(LED_BUILTIN, HIGH);
  timeClient.begin();
  timeClient.setTimeOffset(0); // Defina o deslocamento de fuso horário, se necessário
  info_openweathermap(); // Inicia coletando as informações da temperatura e umidade de São Paulo
  obter_Markov(); // Inicia coletando a probabilidade de chuva de Markov do mês atual
}

void loop() {
  unsigned long currentMillis = millis();
  

  // Verificar a boia e outras funções constantes
  if (currentMillis - previousMillisBoia >= intervalBoia) {
    previousMillisBoia = currentMillis;
    verificarBoia();
    verificarSoloSeco();
    verificarSoloUmidoMAIS();
    verificarSensorSolo2();
    Blynk.run();
    digitalWrite(LED_1, HIGH);
  }

  // Verificar a temperatura
  if (currentMillis - previousMillisTemperatura >= intervalTemperatura) {
    previousMillisTemperatura = currentMillis;
    verificarTemperatura();
    digitalWrite(LED_1, HIGH);
  }

  // Verificar a umidade do solo
  if (currentMillis - previousMillisUmidadeSolo >= intervalUmidadeSolo) {
    previousMillisUmidadeSolo = currentMillis;
    verificarUmidadeSolo();
    probabilidade_markov_umidadeAtual();
    digitalWrite(LED_1, HIGH);
  }

  // Obter dados de Markov
  if (currentMillis - previousMillisObterMarkov >= intervalObterMarkov) {
    previousMillisObterMarkov = currentMillis;
    obter_Markov();
    digitalWrite(LED_1, HIGH);
  }

  // Obter dados de OpenWeatherMap
  if (currentMillis - previousMillisInfoOpenweathermap >= intervalInfoOpenweathermap) {
    previousMillisInfoOpenweathermap = currentMillis;
    info_openweathermap();
    digitalWrite(LED_1, LOW);
  }

  // Adicionar dados de custo de água
  if (currentMillis - previousMillisAddCustoAgua >= intervalAddCustoAgua) {
    previousMillisAddCustoAgua = currentMillis;
    add_custoAgua();
    digitalWrite(LED_1, LOW);
  }
}

//Função que coleta a probabilidade mensal de markov + umidade atual do local + umidade atual de são paulo e nos retorna uma nova estimativa de pausa em segundos na irrigação
void probabilidade_markov_umidadeAtual(){
  float probabilidade_convertida = probabilidade * 1000;
  float umidade = dht.readHumidity();
  float umidade_geral = ((umidade_api + umidade) / 2) * 10;
  pausa_probabilidade = 1000 + probabilidade_convertida + umidade_geral;
  Serial.print("Tempo de pausa: ");
  Serial.println(pausa_probabilidade);
}

//função onde é realizado a coleta de temperatura e umidade referente a cidade de São Paulo
void info_openweathermap(){

  // Inicializar o cliente HTTP
  HTTPClient http;

  // Construir a URL da solicitação
  String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/obter_ultima_previsao";

  // Enviar uma solicitação GET para obter os dados da planilha previsao
  http.begin(wifiClient, url); // Use wifiClient como primeiro argumento

  int httpResponseCode = http.GET();

  // Verificar a resposta da solicitação
  if (httpResponseCode == 200) {
    String response = http.getString();

    // Analisar a resposta JSON para obter temperatura e umidade da API openweathermap
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, response);

    if (!error) {
      temperatura_api = doc["temperatura"];
      umidade_api = doc["umidade"];
      Serial.print("Temperatura de São Paulo: ");
      Serial.println(temperatura_api);
      Serial.print(" Umidade de São Paulo: ");
      Serial.println(umidade_api);
    } else {
      Serial.println("Erro ao analisar JSON");
    }
  } else {
    Serial.print("Erro na solicitação HTTP. Código de resposta: ");
    Serial.println(httpResponseCode);
    Serial.print("Temperatura de São Paulo: ");
    Serial.print(temperatura_api);
    Serial.print(" Umidade de São Paulo: ");
    Serial.println(umidade_api);
  }

  // Liberar recursos do cliente HTTP
  http.end();

}

//Função responsalvel por coletar a probabilidade de chuva calculada pelo metodo de Markov referente a cada Mês do ano, mais precisamente ela coleta do mês atual
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

    // Fazer o parsing dos dados JSON
    DynamicJsonDocument doc(1024); // Tamanho do buffer deve ser ajustado conforme necessário
    deserializeJson(doc, response);

    // Extrair os valores das colunas Mes e Probabilidade
    mes = doc["Mes"].as<String>();
    probabilidade = doc["Probabilidade"].as<float>();

    // Agora você pode usar as variáveis mes e probabilidade conforme necessário
    Serial.print("Mês da coleta Markov: ");
    Serial.println(mes);
    Serial.print("Markov: ");
    Serial.println(probabilidade);

    String markov = mes + " chuvoso:";
    Blynk.virtualWrite(V6, markov); // Pino Virtual 6 para texto
    int probabilidade_porcent = probabilidade * 100;
    String probabilidade_string = String(probabilidade_porcent);
    probabilidade_string = probabilidade_string + "%" + " viabilidade";
    Blynk.virtualWrite(V5, probabilidade_string); // Pino Virtual 0 para a temperatura DHT 11


  } else {
    Serial.print("Erro na solicitação HTTP. Código de resposta: ");
    Serial.println(httpResponseCode);
    Serial.print("Mês da coleta Markov: ");
    Serial.println(mes);
    Serial.print("Probabilidade Markov: ");
    Serial.println(probabilidade);
  }

  // Liberar recursos do cliente HTTP
  http.end();
}

//Função responsavel por adicionar ao banco de dados o consumo de agua coletado pelo sensor de fluxo de agua
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

//Função que retorna a data atual
int dataAtual(){

  timeClient.update();

  // Obter a data e hora atual
  time_t rawTime = timeClient.getEpochTime();
  struct tm *timeInfo = localtime(&rawTime);

  // Formatar a data no formato numérico (ddmmyyyy)
  int dataInt = (timeInfo->tm_mday * 1000000) + ((timeInfo->tm_mon + 1) * 10000) + (1900 + timeInfo->tm_year);
  //Serial.println(dataInt);
  return dataInt;
}

//Função que coleta as informações do sensor de fluxo de agua
void medirFluxoAgua(){

  volume = (pulse * 4.5) / 1000.0;
  Serial.print( volume);
  String consumo = " Consumo de Água";
  Blynk.virtualWrite(V9, consumo); // Pino Virtual 9 para texto
  Serial.println(" L/min");
  Blynk.virtualWrite(V8, volume); // Pino Virtual 8 para o consumo de agua
}

ICACHE_RAM_ATTR void increase() {
  pulse++;
}

//Função que verifica a posição do sensor tipo boia de nivel de agua
void verificarBoia(){
  int estado = digitalRead(boiaPin); /*estado é igual a leitura digital*/
  Serial.print("Estado sensor : "); /*Printa "Estado do sensor:" */
  Serial.println(estado); /*Printa a leitura de estado*/
  if (estado == 0){
    Serial.print("Enchendo o reservatorio ");
    digitalWrite(solenoide, LOW);
    Blynk.virtualWrite(V7, estado); //Indicador no Blynk se o Reservatorio esta cheio ou não
    medirFluxoAgua();
  } else{
    Serial.print("Reservatorio cheio ");
    Blynk.virtualWrite(V7, estado); //Indicador no Blynk se o Reservatorio esta cheio ou não
    digitalWrite(solenoide, HIGH);
  }
  delay(100); /*atraso de 0,1s*/
}

//Função que coleta as informações do sensor DHT11
void verificarTemperatura(){
  delay(100);  // Aguarde alguns segundos entre as leituras

  float temperatura = dht.readTemperature();  // Leia a temperatura em graus Celsius
  float umidade = dht.readHumidity();         // Leia a umidade relativa

  if (isnan(temperatura) || isnan(umidade)) {
    Serial.println("Falha ao ler o sensor DHT11!");
    digitalWrite(LED_2, HIGH);
  } else {
    Serial.print("Temperatura local: ");
    Serial.print(temperatura);
    Serial.println(" °C");

    Serial.print("Umidade local: ");
    Serial.print(umidade);
    Serial.println(" %");

    String casa = "Plantio ºC: ";
    Blynk.virtualWrite(V3, casa); // Pino Virtual 3 para texto
    Blynk.virtualWrite(V0, temperatura); // Pino Virtual 0 para a temperatura DHT 11
    


    //desenvolvimento e produção do tomate
    if (temperatura >= 10 && temperatura <= 34 ) {
      Serial.print("| Temperatura do local esta ideal para desenvolvimento e produção do tomate ");
      
      if (temperatura_api >= 10 && temperatura_api <= 34){
        Serial.print("| Temperatura de São Paulo esta ideal para desenvolvimento e produção do tomate ");
        String SaoPaulo = "São Paulo ºC: ";
        Blynk.virtualWrite(V4, SaoPaulo); // Pino Virtual 4 para texto
        Blynk.virtualWrite(V1, temperatura_api); // Pino Virtual 1 para temperatura de são paulo
      }

    } else {
      Serial.print("| Temperatura local fora das recomendadas para desenvolvimento e produção do tomate ");
      Blynk.logEvent("temperaturawarning", "Temperatura do plantio fora dos parâmetros recomendados!");
      digitalWrite(LED_2, HIGH);
    }

  }

}

//Função que coleta as informações do sensor de umidade de solo
void verificarUmidadeSolo(){
  int valorAnalogico = analogRead(SENSOR_UMIDADE_DE_SOLO);
  float umidadeSolo = valorAnalogico;

  int valorDigital = digitalRead(SENSOR_UMIDADE_DE_SOLO2);

  if (valorDigital){
    Serial.print("Solo seco ");
  } else{
    Serial.print("Solo umido ");
  }

  Serial.print("Umidade do solo: ");
  Serial.print(umidadeSolo);
  Serial.println("%");
  Blynk.virtualWrite(V2, umidadeSolo); // Pino Virtual 2 para umidade de  solo

  if (umidadeSolo < umidade_solo_maxima && umidadeSolo > umidade_solo_minima ){
      digitalWrite(bomba1, LOW); //Mantem apenas a bomba 1
      Serial.print("Solo na umidade ideal, bomba 1 ligada");
      delay(500); 
      digitalWrite(bomba1, HIGH); //Desliga a bomba 1

  } else{
    verificarSoloUmidoMAIS();
    verificarSoloSeco();
  }
}

//Função que verifica se o solo esta umido demais e toma as medidas necessarias
void verificarSoloUmidoMAIS(){

  int valorAnalogico = analogRead(SENSOR_UMIDADE_DE_SOLO);
  float umidadeSolo = valorAnalogico;

  if (umidadeSolo < umidade_solo_minima ){
      Serial.print("Solo umido demais");
      Serial.print(" Desligando bombas d'água ");

      digitalWrite(bomba1, HIGH); //Desliga a bomba 1
      digitalWrite(bomba2, HIGH); //Desliga a bomba 2
  }

}

//Função que verifica se o solo esta seco demais e toma as medidas necessarias
void verificarSoloSeco(){

  int valorAnalogico = analogRead(SENSOR_UMIDADE_DE_SOLO);
  float umidadeSolo = valorAnalogico;

  int valorDigital = digitalRead(SENSOR_UMIDADE_DE_SOLO2);

  if (valorDigital){
    Serial.print("Solo seco");
    digitalWrite(bomba2, LOW);  //Liga a bomba 2
  } 

  if (umidadeSolo >= umidade_solo_maxima ){
      Serial.print(" Solo seco demais");
      Serial.println(" Ligando bombas d'água ");

      digitalWrite(bomba1, LOW);  //Liga a bomba 1
      digitalWrite(bomba2, LOW);  //Liga a bomba 2
  }

}

//Função que verifica a localização do sensor de umidade de solo 2 que envia sinal digital
void verificarSensorSolo2(){
  int valorDigital = digitalRead(SENSOR_UMIDADE_DE_SOLO2);
  if (valorDigital){
    Serial.print("Localização do sensor de umidade de solo 2 está seco | Ligando bomba 2 ");
    digitalWrite(bomba2, LOW);  //Liga a bomba 2
  } else {
    digitalWrite(bomba2, HIGH);  //desliga a bomba 2
  }
}
