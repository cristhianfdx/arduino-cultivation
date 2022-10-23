#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// Floor sensor
const int HLPIN = A0;

void setup() {
  Serial.begin(9600);
  pinMode(HLPIN, INPUT);
  dht.begin();
}

void loop() {
  delay(2000);

  float relativeHumitity = dht.readHumidity();
  float temperature = dht.readTemperature();
  float hic = 0;

  if (!isnan(relativeHumitity) || !isnan(temperature)) {
    hic = dht.computeHeatIndex(temperature, relativeHumitity, false);
  }

  bool isOn = false;
  int hlSensorValue = analogRead(HLPIN);

  if(hlSensorValue >= 700) {
   isOn = true;
   delay(1000);
  } else {
    isOn = false;
  }

  delay(500);
  Serial.print(String("hl_sensor:") + hlSensorValue + String(",relative_humidity:") + relativeHumitity + String(",auto_watering:") + isOn + String(",temperature:") + temperature + String(",heat_index:") + hic);
}