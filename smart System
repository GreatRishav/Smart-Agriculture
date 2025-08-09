#include <WiFiClient.h>
#include <DHT.h>
#include <WiFi.h>
#include <ThingSpeak.h>
// Pin Definitions
#define LDRPIN 36
#define MOISTUREPIN 34
#define DHTPIN 32
#define DHTTYPE DHT11
#define RELAYPIN1 27  // Soil moisturizer
#define Rainfall_Sensor 33
#define B1_pin 18
#define B2_pin 5
#define Enable_pin 35
int flag=1;
char ssid[] = "Redmi Note 11T 5G";
char password[] = "abcdefgh";       // WiFi Password

// ThingSpeak Credentials
unsigned long myChannelNumber = 2535721;
const char *myWriteAPIKey = "Y20SAH0DX2W2S6WG";
const char *myReadAPIKey = "NCG9CGQ8RJNV35HF";

DHT dht(DHTPIN, DHTTYPE);
WiFiClient client;

void setup() {
  Serial.begin(9600);
  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);  // Adding delay to avoid spamming the Serial output
  }
  Serial.println();
  Serial.println("WiFi connected");

  // Begin DHT sensor
  dht.begin();

  // Begin ThingSpeak communication
  ThingSpeak.begin(client);

  // Initialize pins
  pinMode(RELAYPIN1, OUTPUT);
  pinMode(Rainfall_Sensor, INPUT);
  digitalWrite(RELAYPIN1, LOW);  // Ensure motor is off initially
  pinMode(B1_pin, OUTPUT);
  pinMode(B2_pin, OUTPUT);
  pinMode(Enable_pin,OUTPUT);   
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  int light_value = analogRead(LDRPIN);
  int moisture_value = analogRead(MOISTUREPIN);
  int soil_moisture_value = 100 - ((moisture_value / 4095.0) * 100);

  // Print sensor values
  Serial.println("Temperature: " + String(temperature));
  Serial.println("Humidity: " + String(humidity));
  Serial.println("Light: " + String(light_value));
  Serial.println("Moisture: " + String(soil_moisture_value));

  // Update ThingSpeak fields
  ThingSpeak.setField(1, temperature);
  ThingSpeak.setField(2, humidity);
  ThingSpeak.setField(3, light_value);
  ThingSpeak.setField(4, soil_moisture_value);
  ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);

  // Read values from ThingSpeak (use readFloatField if needed)
  float temperatureTS = ThingSpeak.readFloatField(myChannelNumber, 1, myReadAPIKey);
  float humidityTS = ThingSpeak.readFloatField(myChannelNumber, 2, myReadAPIKey);
  float light_valueTS = ThingSpeak.readFloatField(myChannelNumber, 3, myReadAPIKey);
  float soil_moisture_valueTS = ThingSpeak.readFloatField(myChannelNumber, 4, myReadAPIKey);

  // Control actuator based on moisture value
  if (soil_moisture_valueTS < 20) {
    digitalWrite(RELAYPIN1, HIGH);  // Turn motor on (soil moisturizer)
    Serial.println("Soil Moisturizer ON");
  } else {
    digitalWrite(RELAYPIN1, LOW);  // Turn motor off (soil moisturizer)
    Serial.println("Soil Moisturizer OFF");
  }
  int rainfall = analogRead(Rainfall_Sensor);
  Serial.println("Ranifall:");
  Serial.println(rainfall);
  if (rainfall <3000 and flag==1) {
    Serial.println(rainfall);
    digitalWrite(Enable_pin,HIGH);
    digitalWrite(B1_pin,HIGH);
    digitalWrite(B2_pin,LOW);
    delay(3000);//adjust
    digitalWrite(B1_pin,LOW);
    digitalWrite(B2_pin,LOW);
    flag=0;
  }
  if(rainfall>3000 and flag==0)
  {
    Serial.println(rainfall);
    digitalWrite(Enable_pin,HIGH);
    digitalWrite(B1_pin,LOW);
    digitalWrite(B2_pin,HIGH);
    delay(3000);//adjust
    digitalWrite(B1_pin,LOW);
    digitalWrite(B2_pin,LOW);
    flag=1;
  }
}
