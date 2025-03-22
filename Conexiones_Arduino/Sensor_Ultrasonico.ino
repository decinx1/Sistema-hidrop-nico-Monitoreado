const int trigPin = 12;  // Pin de trigger
const int echoPin = 11;  // Pin de echo

void setup() {
  Serial.begin(9600);  // Inicia la comunicación serial a 115200 baudios
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.println("Iniciando sensor ultrasónico...");
}

void loop() {
  // Envía un pulso corto al pin de trigger
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Mide la duración del pulso en el pin de echo
  long duration = pulseIn(echoPin, HIGH);

  // Verifica si la medición es válida
  if (duration <= 0) {
    Serial.println("Error: No se detectó señal de echo.");
    return;  // Salir del loop si no hay señal
  }

  // Calcula la distancia en centímetros
  long distance = duration * 0.034 / 2;

  // Muestra la distancia en el monitor serial
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  delay(100);  // Espera 100 ms antes de la siguiente medición
}