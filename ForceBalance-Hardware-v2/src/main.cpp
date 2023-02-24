#include <Arduino.h>
#include <math.h>
#include "filter.h"
#include "calibrate.h"
#include "startScale.h"
#include "read.h"

int *read_loadcell;
// RD, RP, RY, RS, RR, RL
String name_loadcell[6] = {"RD", "RP", "RY", "RS", "RR", "RL"};
String debug_data = "";
String send_data;

void debug()
{
  read_loadcell = read_all();
  for (int i = 0; i < 6; i++)
  {
    if (i < 5)
    {
      debug_data = debug_data + name_loadcell[i] + " : " + String(read_loadcell[i]) + ", ";
    }
    else
    {
      debug_data = debug_data + name_loadcell[i] + " : " + String(read_loadcell[i]);
    }
  }

  Serial.println(debug_data);
  debug_data = "";
}

String send_to_app()
{
  send_data = "";
  read_loadcell = read_all();
  for (int i = 0; i < 6; i++)
  {
    if (i < 5)
    {
      if (send_data.length() != 0)
      {
        send_data = send_data + "," + String(read_loadcell[i]);
      }
      else
      {
        send_data = send_data + String(read_loadcell[i]);
      }
    }
    else
    {
      send_data = send_data + "," + String(read_loadcell[i]);
    }
  }
  return send_data;
}

void get_command(String message)
{
  bool cal_status, measure_status = false;

  if (Serial.available() > 0)
  {
    String command = Serial.readString();
    if (command == "CALIBRATE")
    {
      Serial.println("Arduino Calibrate");
      cal_status = true;
      if (cal_status)
      {
        Serial.println(message);
        cal_status = false;
      }
    }

    else if (command == "Start Measure")
    {
      Serial.println("Arduino start measyre");
      measure_status = true;
    }
    else if (command == "Stop Measure")
    {
      Serial.println("Arduino close measyre");
      measure_status = false;
    }
    if (measure_status)
    {
      Serial.println(message);
    }
  }
}

void setup()
{
  Serial.begin(57600);
  start_loadcell();
  // for (byte i = 0; i < 5; i++)
  // {
  //   // RP.set_scale();
  //   // RP.tare();
  //   // long zero_factor = RP.read_average();
  //   // Serial.println(zero_factor);
  //   calibrate_RP();
  // }
  setScaleAll();
}

void loop()
{
  // RD d, RP , RY d, RS d, RR d, RL d
  String message = send_to_app();
  Serial.println(message);
  // debug();
}