include <DHT.h>
include <WiFi.h>
include <ThingsBoard.h>
include <PubSubClient.h>
include <ArduinoJson.h>
define DHTPIN 5
define DHTTYPE DHT11
const int trigPin = 18;
const int echoPin = 19;
long duration;
int distance;
DHT dht(DHTPIN, DHTTYPE);
WiFiClient wifiClient;
ThingsBoard tb(wifiClient);
const char* ssid = "V2037";
const char* password = "123456780";
const char* tbHost = "demo.thingsboard.io";
const char* tbToken = "j2A5RpJUO15pu1VhsVXW";
void setup()
 {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(115200);
  dht.begin();
  Serial.println("Connecting to Wi-Fi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to Wi-Fi...");
  }
  Serial.println("Connected to Wi-Fi");
  Serial.println("Connecting to ThingsBoard...");
  if (!tb.connect(tbHost, tbToken))
 {
    Serial.println("Failed to connect to ThingsBoard");
    while (1);
  }
  Serial.println("Connected to ThingsBoard");
}void loop() 
{
  int moist_value = analogRead(34);
  int rain_value = analogRead(35);
  int smoke_value = analogRead(33);
  int moisture = map(moist_value,4095,25,0,100);
  int rain = map(rain_value,4095,25,0,100);
  int smoke = map(smoke_value,4095,25,0,100);
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance= duration*0.034/2;
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  Serial.print("Soil moisture: ");
  Serial.print(moisture);
  Serial.println("%");
  Serial.print("Rain: ");
  Serial.print(rain);
  Serial.println("%");
  Serial.print("smoke value: ");
  Serial.print(smoke);
  Serial.println("%");
  Serial.print("WATER LEVEL: ");
  Serial.println(distance);
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");
  tb.sendTelemetryFloat("WATER LEVEL", distance);
  tb.sendTelemetryFloat("temperature", temperature);
  tb.sendTelemetryFloat("humidity", humidity);
  tb.sendTelemetryFloat("Soil moisture", moisture);
  tb.sendTelemetryFloat("Rain", rain);
  tb.sendTelemetryFloat("smoke value", smoke);
  delay(2000);
}

