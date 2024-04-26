// Code as been edited so the only serial communication is meant for python interpreter

#include <Wire.h>
#include "rgb_lcd.h"

#define Vin A0
#define Iin A1
rgb_lcd lcd;

float current=0.0;
float current_avg=0.0;
float voltage=0.0;
float voltage_avg=0.0;
float zero=2.5;
float energy_Joules = 0.0;
float energy_kwh = 0.0;

void setup() {
  

  Serial.begin(115200);
  pinMode(Vin,INPUT);
  pinMode(Iin,INPUT);
  // setting up the lcd
  lcd.begin(16, 2);
    lcd.setRGB(237,234,222);
    lcd.setCursor(0,0);
    lcd.print("V=");
    lcd.setCursor(8,0);
    lcd.print("A=");
    lcd.setCursor(0,1);
    lcd.print("P=");
    lcd.setCursor(8,1);
    lcd.print("E=");

  calibrate();

  delay(2000);
}

void loop() {
  current=0.00;
  voltage=0.00;
  for ( int i = 0;i<300;i++){
    voltage += getVoltages();
    current += getCurrent();

    delay(50);
  }
  
  current_avg = current/300;
  voltage_avg = voltage/300;
  
  if(current_avg<0.1 && current_avg>-0.1){
    current_avg=0.000;
  }

  lcd.setCursor(2, 0);       
  lcd.print(voltage_avg); 

  lcd.setCursor(10, 0);       
  lcd.print(current_avg); 

  lcd.setCursor(2, 1);       
  lcd.print(getPower()); 

  lcd.setCursor(10, 1);       
  lcd.print(energy_kwh);

  update_energy();

}

float getVoltages(){
  float adc= analogRead(Vin);
  float voltages = (adc/1023)*5.0*5.06;

  Serial.print(voltages);
  Serial.print(",");

  return voltages;
}


float getCurrent(){
  float adc=analogRead(Iin);
  float vin=adc*5.0/1023.0;
  float current=(vin-zero)/0.66;   // 30A current sensor
  if(current<0.1 && current>-0.1){
    current=0.000;
  }
  
  Serial.println(current);

  return abs(current);
}


void calibrate(){
  float current=0.00;
  float current_avg;

  for (int i=0;i<100;i++){

    float adc=analogRead(Iin);
    current += adc*5.0/1023.0;
    delay(2);

  }

  current_avg = current / 100.00;
  zero = current_avg;
}

float getPower(){
  float power =0.0;
  power = current_avg * voltage_avg; // watts
  return power;
}

void update_energy(){
    static uint32_t last_sample_time;
    uint32_t now = millis();
    uint32_t delta_t = now - last_sample_time; // delta in milli seconds
    float power = getPower();
    energy_Joules += (power * delta_t) / 1000.0; 
    energy_kwh += (power * delta_t) / 3600000000.0 ;
    last_sample_time = now;
}