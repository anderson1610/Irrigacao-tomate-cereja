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

Servidor:


![Screenshot_20231004-231955_Microsoft Remote Desktop.jpg](https://github.com/anderson1610/Irrigacao-tomate-cereja/assets/74426791/6b5e3d12-26e7-4079-9148-879883bb7eb5)

Interface que relata o que está sendo feito pelo servidor e o horário que foi feito.

Funções:

1. Backup do Banco de Dados:

O servidor é encarregado de realizar cópias de segurança regulares do nosso banco de dados. Os dados são formatados em arquivos CSV para facilitar o acesso. Essas cópias de segurança são salvas localmente na máquina e, em seguida, enviadas por e-mail aos usuários para garantir a segurança dos dados.

2. Coleta e Cálculo de Consumo de Água:

O servidor coleta os dados de consumo de água do nosso projeto. Com base nas tarifas da Sabesp, realiza cálculos precisos para determinar o custo do consumo. Os resultados são enviados aos usuários para que tenham uma compreensão clara do seu gasto com água.

3. Requisições à API OPENWEATHERMAP:

Para manter nossos usuários informados sobre as condições climáticas em tempo real na cidade de São Paulo, o servidor faz requisições constantes à API OPENWEATHERMAP. Esses dados são coletados e armazenados em nosso banco de dados, permitindo que os usuários tenham acesso às informações mais recentes.

4. Coleta de Probabilidade de Chuva pelo Algoritmo de Markov:

O servidor desempenha um papel fundamental na obtenção da probabilidade de chuva por meio do algoritmo de Markov. Esses valores são coletados e integrados ao nosso banco de dados para uso em cálculos relacionados à irrigação e outras decisões importantes relacionadas ao cultivo de tomate cereja.

Em resumo, o servidor é o núcleo central do nosso projeto, coordenando várias tarefas essenciais para um cultivo eficiente e bem-sucedido de tomate cereja. Ele garante que nossos usuários tenham acesso a informações atualizadas, economizem recursos e tomem decisões informadas com base nas condições climáticas locais.

API responsável por responder as requisições do ESP8266: 

![IMG-20231003-WA0026.jpg](https://github.com/anderson1610/Irrigacao-tomate-cereja/assets/74426791/7594492e-76e4-4c07-ae3c-c0f50697e6d8)

funções:

- Coletar informações do banco de dados.

- Inserir informações ao banco de dados.

ESP8266:

![IMG-20230927-WA0007.jpg](https://github.com/anderson1610/Irrigacao-tomate-cereja/assets/74426791/272bc0ed-5122-4b43-8871-4888975303e5)

O ESP8266 é uma peça incrível de tecnologia que desempenha um papel crucial em projetos de IoT (Internet das Coisas) e automação residencial. Vamos dar uma visão geral do que é e do que ele faz.

É um módulo de comunicação Wi-Fi altamente versátil e de baixo custo.

Funções:

- Conexão à Internet: O ESP8266 permite que dispositivos se conectem à Internet sem fio, abrindo um mundo de possibilidades para controle remoto e monitoramento.

- Automação: É frequentemente usado para automatizar dispositivos domésticos, como luzes, termostatos e fechaduras, tornando-os inteligentes e controláveis por meio de smartphones ou comandos de voz.

- Coleta de Dados: Pode ser usado para coletar dados de sensores, como temperatura, umidade e movimento, e transmiti-los para a nuvem.

- Integração: Pode ser integrado a plataformas como o Arduino, tornando-o uma escolha popular para projetos de hardware DIY.

Em resumo, o ESP8266 é uma ferramenta poderosa que permite a conexão de dispositivos e a criação de soluções de IoT de maneira econômica. Sua versatilidade e capacidade de comunicação sem fio tornam-no uma escolha popular para uma ampla gama de projetos, desde controle de dispositivos domésticos até coleta de dados e automação industrial.

Interface aplicativo BlynkIOT: 
![Interface 123](https://github.com/anderson1610/Irrigacao-tomate-cereja/assets/74426791/83cdf79f-8bc3-451f-b14f-eae77767f154)

A aplicação é dividida em duas telas distintas, cada uma fornecendo informações valiosas e relevantes para a gestão eficaz do plantio do tomate cereja.

- Tela 1: Informações de Ambiente
Na primeira tela, o usuário é apresentado a informações críticas relacionadas ao ambiente de cultivo.
Isso inclui a temperatura atual do local de plantio, a temperatura atual da cidade de São Paulo (um ponto de referência geográfico relevante) e dados sobre a umidade do solo, que desempenha um papel vital na agricultura.
Essas informações servem como uma base fundamental para tomar decisões informadas sobre o cultivo e seu manejo.

- Tela 2: Probabilidade de Chuva e Consumo de Água
A segunda tela fornece informações sobre a probabilidade de chuva com base em um modelo de previsão avançado, implementado por meio do método de Markov.
Além disso, apresenta o consumo de água em litros pelo cultivo, permitindo uma avaliação precisa dos recursos hídricos necessários.
Um indicador visual é incorporado para sinalizar se o reservatório de água associado ao plantio está cheio ou requer recarga, na qual é feito de forma automatica por meio da solenoide implementada.
