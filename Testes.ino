#include "dht.h" //Inclusão da biblioteca

int pinoSolenoide = 7; //Pino do rele que ativa a solenoide 
const int pinoNivelAgua = 6; //Define sensor como pino 6
const int pinoSensorUmidadeSolo = A1; //Pino sensor ligado a porta A1
const int pinoDHT11 = A0; //Pino sinal do sensor ligado a porta A0
dht DHT; //Variável para fazer referencia a biblioteca DHT

int soloSECO = 900; //A verificar, medida do solo seco
unsigned long ultimoTempoFuncao1 = 0;
unsigned long ultimoTempoFuncao2 = 0;
const unsigned long intervaloFuncao1 = 1000;  // 1 segundo
const unsigned long intervaloFuncao2 = 60000; // 1 minuto


void setup() {
  Serial.begin(9600); // Inicia comunicação serial em 9600
  pinMode(pinoSensorUmidadeSolo, INPUT);
  pinMode(pinoNivelAgua, INPUT);
  pinMode(pinoSolenoide, OUTPUT);
}


void loop() {

  int umidadeSolo = analogRead(pinoSensorUmidadeSolo);
  int estadoNivelAgua = digitalRead(pinoNivelAgua);
  unsigned long tempoAtual = millis();
  
  // Chama as funções a cada intervaloFuncao1
  if (tempoAtual - ultimoTempoFuncao1 >= intervaloFuncao1) {

    verificarTemperatura();
    obterInfo(umidadeSolo, estadoNivelAgua);
    solenoideStatus(estadoNivelAgua, pinoSolenoide);

    ultimoTempoFuncao1 = tempoAtual;
  }

  //Chama as funções a cada intervaloFuncao2
  if (tempoAtual - ultimoTempoFuncao2 >= intervaloFuncao2) {
    verificarUmidade(umidadeSolo);
    ultimoTempoFuncao2 = tempoAtual;
  }

}

//Obtem o status do nivel da agua e passa a informação para o rele, que ativa ou permanece com a solenoide desligada
void solenoideStatus(int estadoNivelAgua, int pinoSolenoide){

  if (estadoNivelAgua == 1) {
  digitalWrite(b, true);
  Serial.println("| Solenoide ligada ");
  } else {
  digitalWrite(pinoSolenoide, false);
  Serial.println("| Solenoide desligada ");
  }

}

//coleta as informações de todos o sensores e printa no serial motor
void obterInfo(int umidadeSolo, int estadoNivelAgua){

  DHT.read11(pinoDHT11); //Lê os valores do sensor
  Serial.print("| Umidade: "); //Imprime Umidade na porta serial
  Serial.print(DHT.humidity); //Imprime o Valor de umidade lido pelo sensor
  Serial.print("%"); 

  Serial.print(" | Temperatura: "); //Imprime Temperatura na porta serial
  Serial.print(DHT.temperature, 0); //Imprime o valor medido e remove a parte decimal
  Serial.println("C"); 


  Serial.print("| Umidade solo: ");
  Serial.print(umidadeSolo);

   // define que estado esta a boia 0 ou 1
  Serial.print(" | Estado sensor nivel de agua: "); //Printa Estado sensor
  Serial.println(estadoNivelAgua); //Printa a leitura de estado

}


//Verifica a umidade do solo
void verificarUmidade(int umidadeSolo){

  if (umidadeSolo >= soloSECO) {
  Serial.println("| Solo seco VERIFICAR");
  //Add ação
  } else {
  Serial.println("| Umidade solo OK");
  //Add ação
  }

}

//verifica a temperatura do ambiente
void verificarTemperatura(){
  //add condição para escolher geminação de semente ou desenvolvimento e produção do tomate

  //Germinação da semente  
  if ( DHT.temperature >= 15 && DHT.temperature <= 25 ) {
  Serial.println("| Temperatura OK para germinação");
  } else {
  Serial.println("| Temperatura fora das recomendadas para germinação da semente");
  //Add ação
  }

  //desenvolvimento e produção do tomate
  if (DHT.temperature >= 10 && DHT.temperature <= 34 ) {
  Serial.println("| Temperatura OK para desenvolvimento e produção do tomate");
  } else {
  Serial.println("| Temperatura fora das recomendadas para desenvolvimento e produção do tomate");
  //Add ação
  }

}
