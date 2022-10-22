#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// Floor sensor
const int HLPIN = A0;

//Sensors data
String request;

void setup() {
  Serial.begin(9600);
  pinMode(HLPIN, INPUT);
  dht.begin();
}

void loop() {
  readDHTSensor();
  readHLSensor();
}

void readDHTSensor() {
  delay(2000);

  float relativeHumitity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (!isnan(relativeHumitity) || !isnan(temperature)) {
    float hic = dht.computeHeatIndex(temperature, relativeHumitity, false);    
    Serial.print(String("relative_humidity:") + relativeHumitity + String(",temperature:") + temperature + String(",heat_index:") + hic);
    Serial.print('\n'); 
  } else {    
    Serial.print(String("DHT_ERROR"));
    Serial.print('\n');
  }
}

void readHLSensor() {
  bool isOn = false;
  int hlSensorValue = analogRead(HLPIN);

  if(hlSensorValue >= 700) {
   isOn = true;
   delay(1000);
  } else {
    isOn = false;
  }

  delay(1000);
  Serial.print(String("hl_sensor:") + hlSensorValue + String(",auto_watering:") + isOn);
  Serial.print('\n');
}