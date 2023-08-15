#include "dht.h" //Inclusão da biblioteca

const int pinoSensorUmidadeSolo = A1; //Pino sensor ligado a porta A1
const int pinoDHT11 = A0; //Pino sinal do sensor ligado a porta A0
dht DHT; //Variável para fazer referencia a biblioteca DHT


void setup() {
  Serial.begin(9600); // Inicia comunicação serial em 9600
  pinMode(pinoSensorUmidadeSolo, INPUT);
}

void loop() {
  DHT.read11(pinoDHT11); //Lê os valores do sensor
  Serial.print("| Umidade: "); //Imprime Umidade na porta serial
  Serial.print(DHT.humidity); //Imprime o Valor de umidade lido pelo sensor
  Serial.print("%"); 
  Serial.print(" | Temperatura: "); //Imprime Temperatura na porta serial
  Serial.print(DHT.temperature, 0); //Imprime o valor medido e remove a parte decimal
  Serial.println("C"); 
  Serial.print(" Umidade solo: ");
  Serial.print(analogRead(pinoSensorUmidadeSolo));
}