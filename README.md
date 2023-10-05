# TCC UNIP 2023 - em andamento 
 
Componentes utilizados até o momento:

- NodeMCU ESP8266

- Sensor de temperatura

- Sensor de umidade de solo com sinal analogico
 
- Sensor de umidade de solo com sinal digital
 
- Sensor de fluxo de agua 

- Sensor tipo boia 

- Sensor de temperatura 

- 2 Mini Bomba d'água 

- Solenoide 12V

- Fonte com saída 12V 20A chaveada

- Protoboard 400 pontos

Testando os sensores:


![20231004_105241.jpg](https://github.com/anderson1610/Irrigacao-tomate-cereja/assets/74426791/2b29fcb9-ae13-4cda-b757-7a55c7468d10)


Descrição do projeto:

Este projeto está estrategicamente voltado para o aprimoramento do cultivo de tomate cereja, um fruto amplamente cultivado em hortas caseiras, particularmente no Brasil, devido ao seu clima tropical que é altamente propício para o cultivo dessas plantas.

O principal objetivo do nosso projeto é otimizar o uso da água, proporcionando uma economia substancial em comparação com os métodos de cultivo tradicionais em residências.

Para atingir esse objetivo, desenvolvemos um algoritmo que utiliza o método de Markov para calcular a probabilidade de um determinado mês ser chuvoso ou não. Esse cálculo é essencial para determinar quando é necessário irrigar as plantas, garantindo um uso eficiente dos recursos hídricos.

Além disso, implementamos um servidor dedicado que coleta informações de previsão do tempo da cidade de São Paulo, utilizando a API OPENWEATHERMAP. Esses dados são armazenados em nosso banco de dados, juntamente com as probabilidades calculadas pelo algoritmo de Markov. Também integramos a capacidade de coletar dados de consumo de água por meio do dispositivo ESP8266, o qual envia essas informações para o banco de dados. A partir desses dados, o sistema realiza cálculos com base nas tarifas de água da Sabesp e, em seguida, envia relatórios detalhados por e-mail para os usuários.

Para facilitar a comunicação entre o banco de dados e o dispositivo ESP8266, desenvolvemos uma API que é responsável por processar as solicitações recebidas do ESP e fornecer as informações apropriadas. Isso inclui a transmissão de dados de consumo de água, a coleta de informações de probabilidade de Markov e as previsões meteorológicas.

O dispositivo ESP8266 foi programado meticulosamente para otimizar seu desempenho e fornecer os resultados prometidos: um método de cultivo eficiente de tomate cereja com um consumo de água minimizado. A abordagem tecnológica adotada neste projeto visa criar um sistema integrado que permita aos agricultores domésticos tomar decisões informadas sobre a irrigação, economizando recursos e contribuindo para a sustentabilidade ambiental.

