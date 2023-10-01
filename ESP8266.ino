// Inclua a biblioteca ESP8266WiFi
#include <ESP8266WiFi.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

#define SENSOR_TEMPERATURA A0
#define DHTPIN D3      // Defina a porta onde o sensor está conectado
#define DHTTYPE DHT11   // Defina o tipo de sensor 
DHT dht(DHTPIN, DHTTYPE);

// Defina o nome da sua rede Wi-Fi e a senha
const char* ssid = "Anderson";
const char* password = "";

// Pino onde a boia está conectada
const int boiaPin = D2;
int bomba1 = D5;
int bomba2 = D6;
int solenoide = D7;
int sensorFluxoAgua = D1;
volatile long pulse;
unsigned long lastTime;
float volume;


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
}

void loop() /*laço de repetição*/
{ 
  verificarBoia();
  verificarTemperatura();
  verificarUmidadeSolo();
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

  delay(100);  // Aguarde alguns segundos entre as leituras

}
