void start_RL()
{
    RL.set_scale(789.20233);
    RL.set_offset(ZERO_FACTOR_RL);
}
void start_RD()
{
    RD.set_scale(770.07);
    RD.set_offset(ZERO_FACTOR_RD);
}

void start_RS()
{
    RS.set_scale(757.39630);
    RS.set_offset(ZERO_FACTOR_RS);
}

void start_RY()
{
    // 764.47
    RY.set_scale(762.91003);
    RY.set_offset(ZERO_FACTOR_RY);
}

void start_RR()
{
    RR.set_scale(758.05999);
    RR.set_offset(ZERO_FACTOR_RR);
}
void start_RP()
{
    RP.set_scale(752.22082);
    RP.set_offset(ZERO_FACTOR_RP);
}

void setScaleAll()
{
    start_RL();
    start_RY();
    start_RR();
    start_RP();
    start_RD();
    start_RS();
}
