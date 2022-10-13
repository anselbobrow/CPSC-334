#include <WiFi.h>
#include <WiFiUdp.h>

const char * networkName = "yale wireless";
const char * networkPswd = "";

const char * udpAddress = "172.29.31.240";
const int udpPort = 5070;

WiFiUDP udp;
boolean connected = false;

int sensorPin = 13;
int sensorValue = 0;

void setup() {
  Serial.begin(115200);
  connectToWiFi(networkName, networkPswd);

  pinMode(sensorPin, INPUT);
}

void loop() {
  // read the value from the photoresistor
  sensorValue = analogRead(sensorPin);
  Serial.println(sensorValue);

  if(connected){
    //Send a packet
    udp.beginPacket(udpAddress,udpPort);
    udp.printf("Sensor Value: %d", sensorValue);
    udp.endPacket();
  }

  delay(100);
}

// after this point code found from Examples -> WiFiUDPClient
void connectToWiFi(const char * ssid, const char * pwd){
  Serial.println("Connecting to WiFi network: " + String(ssid));

  // delete old config
  WiFi.disconnect(true);
  //register event handler
  WiFi.onEvent(WiFiEvent);
  
  //Initiate connection
  WiFi.begin(ssid, pwd);

  Serial.println("Waiting for WIFI connection...");
}

//wifi event handler
void WiFiEvent(WiFiEvent_t event){
    switch(event) {
      case ARDUINO_EVENT_WIFI_STA_GOT_IP:
          //When connected set 
          Serial.print("WiFi connected! IP address: ");
          Serial.println(WiFi.localIP());  
          //initializes the UDP state
          //This initializes the transfer buffer
          udp.begin(WiFi.localIP(),udpPort);
          connected = true;
          break;
      case ARDUINO_EVENT_WIFI_STA_DISCONNECTED:
          Serial.println("WiFi lost connection");
          connected = false;
          break;
      default: break;
    }
}