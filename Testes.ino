#include "dht.h" //Inclusão da biblioteca

//int pinoSolenoide = 7
const int pinoNivelAgua = 6; //Define sensor como pino 6
const int pinoSensorUmidadeSolo = A1; //Pino sensor ligado a porta A1
const int pinoDHT11 = A0; //Pino sinal do sensor ligado a porta A0
dht DHT; //Variável para fazer referencia a biblioteca DHT
int soloSECO = 900 //A verificar, medida do solo seco


void setup() {
  Serial.begin(9600); // Inicia comunicação serial em 9600
  pinMode(pinoSensorUmidadeSolo, INPUT);
  pinMode(pinoNivelAgua, INPUT)
  //pinMode(pinoSolenoide, OUTPUT)
}

void loop() {
  DHT.read11(pinoDHT11); //Lê os valores do sensor
  Serial.print("| Umidade: "); //Imprime Umidade na porta serial
  Serial.print(DHT.humidity); //Imprime o Valor de umidade lido pelo sensor
  Serial.print("%"); 

  Serial.print(" | Temperatura: "); //Imprime Temperatura na porta serial
  Serial.print(DHT.temperature, 0); //Imprime o valor medido e remove a parte decimal
  Serial.println("C"); 

  int umidadeSolo = analogRead(pinoSensorUmidadeSolo)
  Serial.print(" Umidade solo: ");
  Serial.print(umidadeSolo);

  int estadoNivelAgua = digitalRead(sensor); // define que estado esta a boia 0 ou 1
  Serial.print("Estado sensor : "); //Printa Estado sensor
  Serial.println(estadoNivelAgua); //Printa a leitura de estado
  
  verificarUmidade()
  verificarTemperatura()

}


void verificarUmidade(){

  if (umidadeSolo >= soloSECO) {
  Serial.print("Solo seco VERIFICAR")
  } else {
  Serial.print("Umidade solo OK")
  }

  delay(64000)

}

void verificarTemperatura(){

  //Germinação da semente  
  if (DHT.temperature >= 15 and DHT.temperature <= 25 ) {
  Serial.print("Temperatura OK para germinação")
  } else {
  Serial.print("Temperatura fora das recomendadas para germinação da semente")
  }

  //desenvolvimento e produção do tomate
  if (DHT.temperature >= 10 and DHT.temperature <= 34 ) {
  Serial.print("Temperatura OK para desenvolvimento e produção do tomate")
  } else {
  Serial.print("Temperatura fora das recomendadas para desenvolvimento e produção do tomate")
  }
  delay(64000)

}
