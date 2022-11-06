#include <WiFi.h>
#include <WiFiUdp.h>
#include <OSCMessage.h>

// wifi configuration
const char * networkName = "yale wireless";
const char * networkPswd = "";
// const char * udpAddress = "172.27.117.153"; // ip address of target (raspi)
const char * udpAddress = "172.27.114.61"; // ip address of target (macbook)
const int udpPort = 57120; // default port for SC to listen for OSC messages

WiFiUDP udp;
boolean connected = false;

// photoresistor pins (make sure not impacted by wifi)
int r1 = 34;
int r2 = 35;
int r3 = 32;
int r4 = 33;
int r5 = 25;

void setup() {
  analogReadResolution(12);
  Serial.begin(115200);
  connectToWiFi(networkName, networkPswd);
  pinMode(r1, INPUT_PULLUP);
  pinMode(r2, INPUT_PULLUP);
  pinMode(r3, INPUT_PULLUP);
  pinMode(r4, INPUT_PULLUP);
  pinMode(r5, INPUT_PULLUP);
}

void loop() {
  // take reading from resisitors
  int r1val = analogRead(r1);
  int r2val = analogRead(r2);
  int r3val = analogRead(r3);
  int r4val = analogRead(r4);
  int r5val = analogRead(r5);

  if (connected) {
    // create osc message
    OSCMessage message("/esp/sensors");
    message.add(r1val);
    message.add(r2val);
    message.add(r3val);
    message.add(r4val);
    message.add(r5val);
    
    // send UDP packet with OSC message
    udp.beginPacket(udpAddress, udpPort);
    message.send(udp);
    udp.endPacket();
    message.empty();
  }

  delay(200);
}

// after this point code is found from Examples -> WiFiUDPClient
void connectToWiFi(const char * ssid, const char * pwd){
  Serial.println("Connecting to WiFi network: " + String(ssid));

  //delete old config
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