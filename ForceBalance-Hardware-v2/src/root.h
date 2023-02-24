#ifndef ROOT_H
#include <Arduino.h>
#include "HX711.h"
#define ROOT_H
#endif

#define RS_DOUT_PIN 27
#define RS_SCK_PIN 25
#define RL_DOUT_PIN 31
#define RL_SCK_PIN 29
#define RR_DOUT_PIN 17
#define RR_SCK_PIN 15
#define RD_DOUT_PIN 5
#define RD_SCK_PIN 3
#define RP_DOUT_PIN 9
#define RP_SCK_PIN 7
#define RY_DOUT_PIN 23
#define RY_SCK_PIN 21

HX711 RL;
HX711 RS;
HX711 RD;
HX711 RP;
HX711 RR;
HX711 RY;

long RS_reading, RL_reading, RD_reading, RY_reading, RP_reading, RR_reading;
float RS_cf, RL_cf, RD_cf, RY_cf, RP_cf, RR_cf;
float scale = 313.4;

void start_loadcell()
{
    RD.begin(RD_DOUT_PIN, RD_SCK_PIN);
    RS.begin(RS_DOUT_PIN, RS_SCK_PIN);
    RL.begin(RL_DOUT_PIN, RL_SCK_PIN);
    RR.begin(RR_DOUT_PIN, RR_SCK_PIN);
    RP.begin(RP_DOUT_PIN, RP_SCK_PIN);
    RY.begin(RY_DOUT_PIN, RY_SCK_PIN);
}