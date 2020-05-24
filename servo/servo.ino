#include <Servo.h>
#include <stdio.h>
#include <unistd.h>
 
Servo servoVer;
Servo servoHor;

int horizontalServoAngle;
int verticalServoAngle;

void setup()
{
  Serial.begin(9600);
  servoVer.attach(5); 
  servoHor.attach(6);
  servoVer.write(0);
  servoHor.write(90);
}

void loop()
{
  if (Serial.available()) {
    horizontalServoAngle = Serial.parseInt();
    Serial.print(horizontalServoAngle); 

    //Serial.print(" - ");
    
    verticalServoAngle = Serial.parseInt();
    Serial.println(verticalServoAngle);
    
    servoHor.write(horizontalServoAngle);
    servoVer.write(verticalServoAngle);
  }

}
  
