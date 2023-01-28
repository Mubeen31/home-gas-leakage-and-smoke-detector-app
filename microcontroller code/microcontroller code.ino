#include "DHT.h"
#define DHTPIN 13
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

#include <Arduino.h>
#if defined(ESP32)
  #include <WiFi.h>
#elif defined(ESP8266)
  #include <ESP8266WiFi.h>
#endif
#include <Firebase_ESP_Client.h>

#include<ESP8266WebServer.h>
#include<WiFiManager.h>
#include<DNSServer.h>

//Provide the token generation process info.
#include "addons/TokenHelper.h"
//Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

// Insert Firebase project API Key
#define API_KEY "AIzaSyCPzA7m7sAGLkVdfv3Sn5JpvQPaenbzukk"

// Insert RTDB URLefine the RTDB URL */
#define DATABASE_URL "home-gas-leakage-default-rtdb.firebaseio.com"

//Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

//some important variables
bool signupOK = false;

int airQuality = A0;

void setup() {
  Serial.begin(9600);
  dht.begin();
  
  WiFiManager wifiManager;
  Serial.println("Connecting.....");  
  wifiManager.autoConnect("gas leakage","");
  Serial.println("Connected");

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Sign up */
  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("ok");
    signupOK = true;
  }
  else {
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void loop() {
  float t = dht.readTemperature();
  int airQualityData = analogRead(airQuality);
  if (Firebase.ready() && signupOK ) {
    if (Firebase.RTDB.setFloat(&fbdo, "DHT/temperature", t)){
       Serial.print("Temperature: ");
       Serial.println(t);
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
    }
    if (Firebase.RTDB.setFloat(&fbdo, "MQ135/gas", airQualityData)){
       Serial.print("Gas: ");
       Serial.println(airQualityData);
    }
    else {
      Serial.println("FAILED");
      Serial.println("REASON: " + fbdo.errorReason());
    }       
  }
  delay(5000);
}
