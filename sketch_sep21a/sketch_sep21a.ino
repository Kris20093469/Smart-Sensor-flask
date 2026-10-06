#include <WiFiS3.h>

int redPin = 6; // the pin that the LED is atteched to
int bluePin = 9;
int greenPin = 5;
String doorStat;
String motionStat;
int sensor = 2; // the pin that the sensor is atteched to
int dSwitch = 4;
int magnetsense = 0;
int state = LOW; // by default, no motion detected
int val = 0; // variable to store the sensor status (value)
char ssid[] = "BPstudent";
char pass[] = "studentuse";
unsigned long myTime;
WiFiClient client;

void setup() {

  while (WiFi.begin(ssid, pass) != WL_CONNECTED){
    
    Serial.println("Connecting...");
  }
  
 pinMode(dSwitch, INPUT_PULLUP);
 pinMode(greenPin, OUTPUT); // initalize LED as an output
 pinMode(bluePin, OUTPUT);
 pinMode(redPin, OUTPUT);
 pinMode(sensor, INPUT); // initialize sensor as an input
 Serial.begin(9600); // initialize serial
 Serial.println("Connected!");
 delay(2000);
 Serial.println(WiFi.localIP());
}

void loop(){
  
  if (client.connect("10.30.1.6", 5000)) {

        String json = "{\"doorState\":\"" + String(doorStat) +
              "\",\"motion\":\"" + String(motionStat) + "\"}";

        client.println("POST /api/sensor HTTP/1.1");
        client.println("Host: 192.168.1.100");
        client.println("Content-Type: application/json");
        client.print("Content-Length: ");
        client.println(json.length());
        client.println();
        client.println(json);

        client.stop();
    }
  
  magnetsense = digitalRead(dSwitch);
 val = digitalRead(sensor); // read sensor value

 if(magnetsense == HIGH){
    doorStat = "opened";
    setColor(255,70,0);
    
  }
 
  
  else{
    doorStat = "closed";
   

  }
  if (magnetsense == HIGH && state == HIGH){
   setColor(0,0,255);
   doorStat = "opened";
   motionStat = "detected";
  } else{
    
    
    
  }
 if (val == HIGH) { // check if the sensor is HIGH

 

 if (state == LOW) {
  myTime = millis();
  motionStat ="detected";

 setColor(255,0,0);

 state = HIGH; // update variable state to HIGH
 
 }
 } 
 else {
  

 if (state == HIGH && millis()- myTime >= 5000){
  motionStat = "stopped";
 Serial.println("Motion stopped!");
  setColor(0,255,0);


 state = LOW; // update variable state to LOW
 }
 
 }
  
 
}

void setColor(int red, int green, int blue)
{
  analogWrite(redPin , red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);
}
