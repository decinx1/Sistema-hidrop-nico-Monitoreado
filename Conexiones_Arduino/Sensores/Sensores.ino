#include <OneWire.h>
#include <DallasTemperature.h>
#include "GravityTDS.h"

// Definición de pines
const int pinDatosDQ = 3;          // Sensor de temperatura
const int phPin = A0;              // Sensor de pH
const int trigPin = 12;            // Sensor ultrasónico (trigger)
const int echoPin = 11;            // Sensor ultrasónico (echo)
#define TdsSensorPin A1            // Sensor TDS
const int relayPin = 4;            // Pin para controlar el relé

// Variables para el sensor ultrasónico
long duration = 0;
long distance = 0;

// Variables para el sensor TDS
float temperature = 25;
float tdsValue = 0;

// Objetos de los sensores
OneWire oneWireObjeto(pinDatosDQ);
DallasTemperature sensorDS18B20(&oneWireObjeto);
GravityTDS gravityTds;

void setup() {
  Serial.begin(115200);
  
  // Configurar pin del relé
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH); // Inicia con sensores APAGADOS
  
  // Inicializar sensor de temperatura
  sensorDS18B20.begin();
  
  // Inicializar sensor de pH
  pinMode(phPin, INPUT);
  
  // Inicializar sensor ultrasónico
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  // Inicializar sensor TDS
  gravityTds.setPin(TdsSensorPin);
  gravityTds.setAref(5.0);
  gravityTds.setAdcRange(1024);
  gravityTds.begin();
  
  Serial.println("Sistema de monitoreo iniciado. Las lecturas se realizarán cada 10 segundos.");
}

void leerTemperatura() {
  sensorDS18B20.requestTemperatures();
  float temp = sensorDS18B20.getTempCByIndex(0);
  Serial.print("Temperatura: ");
  Serial.print(temp);
  Serial.println(" °C");
  temperature = temp; // Actualiza la temperatura para compensación del TDS
}

void leerPH() {
  int val = analogRead(phPin);
  float volt = float(val) / 1023.0 * 5.0;
  Serial.print("Valor de pH: ");
  Serial.println(volt);
}

void leerUltrasonico() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  
  if (duration <= 0) {
    Serial.println("Error: No se detectó señal de echo en sensor ultrasónico.");
    return;
  }

  distance = duration * 0.034 / 2;
  Serial.print("Distancia: ");
  Serial.print(distance);
  Serial.println(" cm");
}

void leerTDS() {
  gravityTds.setTemperature(temperature);
  gravityTds.update();
  tdsValue = gravityTds.getTdsValue();
  Serial.print("TDS: ");
  Serial.print(tdsValue, 0);
  Serial.println(" ppm");
}

void loop() {
  static unsigned long ultimaLectura = 0;
  unsigned long ahora = millis();
  
  if (ahora - ultimaLectura >= 10000) { // 10 segundos = 10000 ms
    ultimaLectura = ahora;
    
    // Encender sensores
    digitalWrite(relayPin, LOW);
    Serial.println("\n--- Iniciando lecturas ---");
    delay(5000); // Tiempo de estabilización reducido (ya que el voltaje es estable)
    
    // Tomar lecturas
    leerTemperatura();
    leerPH();
    leerUltrasonico();
    leerTDS();
    
    // Apagar sensores
    digitalWrite(relayPin, HIGH);
    Serial.println("--- Lecturas completadas ---\n");
  }
  
  delay(100); // Pequeño delay para evitar sobrecargar el procesador
}