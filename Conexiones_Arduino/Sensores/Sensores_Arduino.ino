#include <OneWire.h>
#include <DallasTemperature.h>
#include <EEPROM.h>
#include "GravityTDS.h"

// Pines sensores y reles
#define RELAY_TEMP 9
#define RELAY_US 10
#define RELAY_PH 11
#define RELAY_TDS 12

#define TEMP_DATA_PIN 2

#define TRIG_PIN 3
#define ECHO_PIN 4

#define PH_PIN A0
#define TDS_PIN A1

// Objetos sensores
OneWire oneWire(TEMP_DATA_PIN);
DallasTemperature tempSensor(&oneWire);

GravityTDS gravityTds;
float temperature = 25;  // Para el TDS

void setup() {
  Serial.begin(9600);

  // Configurar reles como salida
  pinMode(RELAY_TEMP, OUTPUT);
  pinMode(RELAY_US, OUTPUT);
  pinMode(RELAY_PH, OUTPUT);
  pinMode(RELAY_TDS, OUTPUT);

  // Apagar todos los reles al inicio
  digitalWrite(RELAY_TEMP, HIGH);
  digitalWrite(RELAY_US, HIGH);
  digitalWrite(RELAY_PH, HIGH);
  digitalWrite(RELAY_TDS, HIGH);

  // Inicializar sensores
  tempSensor.begin();
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  gravityTds.setPin(TDS_PIN);
  gravityTds.setAref(5.0);
  gravityTds.setAdcRange(1024);
  gravityTds.begin();
}

void loop() {
  // Sensor de Temperatura
  digitalWrite(RELAY_TEMP, LOW); // Activar relé
  delay(5000);  // Estabilización
  for (int i = 0; i < 30; i++) {
    tempSensor.requestTemperatures();
    float tempC = tempSensor.getTempCByIndex(0);
    Serial.print("Temperatura: ");
    Serial.print(tempC);
    Serial.println(" °C");
    delay(1000);
  }
  digitalWrite(RELAY_TEMP, HIGH); // Desactivar relé
  delay(1000);

  // Sensor Ultrasónico
  digitalWrite(RELAY_US, LOW); // Activar relé
  delay(5000);  // Estabilización
  for (int i = 0; i < 30; i++) {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    long duration = pulseIn(ECHO_PIN, HIGH);
    if (duration > 0) {
      long distance = duration * 0.034 / 2;
      Serial.print("Distancia: ");
      Serial.print(distance);
      Serial.println(" cm");
    } else {
      Serial.println("Error: No se detectó señal de echo.");
    }
    delay(1000);
  }
  digitalWrite(RELAY_US, HIGH); // Desactivar relé
  delay(1000);

  // Sensor de pH
  digitalWrite(RELAY_PH, LOW); // Activar relé
  delay(5000);  // Estabilización
  for (int i = 0; i < 30; i++) {
    int val = analogRead(PH_PIN);
    float volt = float(val) / 1023.0 * 5.0;
    Serial.print("El valor del PH es de: ");
    Serial.println(volt);
    delay(1000);
  }
  digitalWrite(RELAY_PH, HIGH); // Desactivar relé
  delay(1000);

  // Sensor de Conductividad (TDS)
  digitalWrite(RELAY_TDS, LOW); // Activar relé
  delay(5000);  // Estabilización
  for (int i = 0; i < 30; i++) {
    gravityTds.setTemperature(temperature);
    gravityTds.update();
    float tdsValue = gravityTds.getTdsValue();
    Serial.print("TDS: ");
    Serial.print(tdsValue, 0);
    Serial.println(" ppm");
    delay(1000);
  }
  digitalWrite(RELAY_TDS, HIGH); // Desactivar relé
  delay(1000);
}