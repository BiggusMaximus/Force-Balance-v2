#include "root.h"

#define ZERO_FACTOR_RS 16901
#define ZERO_FACTOR_RR 226847
#define ZERO_FACTOR_RP 99479
#define ZERO_FACTOR_RL 264780
#define ZERO_FACTOR_RY 386390
#define ZERO_FACTOR_RD 10395

void calibrate_RS()
{
    if (RS.is_ready())
    {
        RS.set_scale();
        Serial.println("(RS) Remove any weights");
        RS.tare();
        Serial.println("(RS) Tare done...");
        Serial.print("(RS) Place a known weight");
        delay(5000);
        RS_reading = RS.get_units(10);
        RS_cf = RS_reading / scale;
        Serial.print("RS: ");
        Serial.print(RS_cf, 5);
        RS.set_scale(RS_cf);
        Serial.println("RS:" + String(RS.get_units()));
    }
    else
    {
        Serial.println("RS HX711 not found.");
    }
    delay(10000);
}

void calibrate_RL()
{
    if (RL.is_ready())
    {
        RL.set_scale();
        Serial.println("(RL) Remove any weights");
        RL.tare();
        Serial.println("(RL) Tare done...");
        delay(3000);
        Serial.println("(RL) Place a known weight");
        delay(5000);
        RL_reading = RL.get_units(10);
        RL_cf = RL_reading / scale;
        Serial.print("RL: ");
        Serial.print(RL_cf, 5);
        Serial.print("\n");
        RL.set_scale(RL_cf);
        Serial.println(String(RL.get_units()));
        delay(5000);
    }
    else
    {
        Serial.println("RL HX711 not found.");
    }
    delay(1000);
}

void calibrate_RD()
{
    if (RD.is_ready())
    {
        RD.set_scale();
        Serial.println("(RD) Remove any weights");
        RD.tare();
        Serial.println("(RD) Tare done...");
        Serial.println("(RD) Place a known weight");
        delay(5000);
        RD_reading = RD.get_units(10);
        Serial.print("RD : ");
        Serial.print(RD_reading, 5);
        Serial.print("\n");
        RD.set_scale(RD_cf);
        Serial.println(String(RD.get_units()));
        delay(5000);
    }
    else
    {
        Serial.println("RD HX711 not found.");
    }
    delay(5000);
}

void calibrate_RY()
{
    if (RY.is_ready())
    {
        RY.set_scale();
        Serial.println("(RY) Remove any weights");
        RY.tare();
        Serial.println("(RYRD) Tare done...");
        Serial.print("(RY) Place a known weight");
        delay(3000);
        RY_reading = RY.get_units(10);
        RY_cf = RY_reading / scale;
        Serial.print("RY : ");
        Serial.print(RY_cf, 5);
        RY.set_scale(RY_cf);
        Serial.println("RY : " + String(RY.get_units()));
    }
    else
    {
        Serial.println("RY HX711 not found.");
    }
    delay(1000);
}

void calibrate_RP()
{
    if (RP.is_ready())
    {
        RP.set_scale();
        Serial.println("(RP) Remove any weights");
        RP.tare();
        Serial.println("(RP) Tare done...");
        Serial.print("(RP) Place a known weight");
        delay(3000);
        RP_reading = RP.get_units(10);
        RP_cf = RP_reading / scale;
        Serial.print("RP : ");
        Serial.print(RP_cf, 5);
        RP.set_scale(RP_cf);
        Serial.println("RP : " + String(RP.get_units()));
    }
    else
    {
        Serial.println("RP HX711 not found.");
    }
    delay(1000);
}

void calibrate_RR()
{
    if (RR.is_ready())
    {
        RR.set_scale();
        Serial.println("(RR) Remove any weights");
        RR.tare();
        Serial.println("(RR) Tare done...");
        delay(1000);
        Serial.print("(RR) Place a known weight");
        delay(3000);
        RR_reading = RR.get_units(10);
        RR_cf = RR_reading / scale;
        Serial.print("RR : ");
        Serial.print(RR_cf, 5);
        Serial.print("\n");
        RR.set_scale(RR_cf);
        Serial.println("RR : " + String(RR.get_units()));
    }
    else
    {
        Serial.println("RR HX711 not found.");
    }
    delay(1000);
}

void calibrate_all()
{
    calibrate_RD();
    calibrate_RY();
    calibrate_RP();
    calibrate_RR();
    calibrate_RS();
    calibrate_RL();
}
