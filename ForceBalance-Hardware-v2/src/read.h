int read[6] = {};

int read_RL()
{

    float RL_read = RL.get_units();
    return round(RL_read);
}

int read_RS()
{
    float RS_read = RS.get_units();

    return round(RS_read);
}
int read_RD()
{
    float RD_read = RD.get_units();
    return round(RD_read);
}
int read_RY()
{
    float RY_read = RY.get_units();
    return round(RY_read);
}

int read_RR()
{
    float RR_read = RR.get_units();
    return round(RR_read);
}
int read_RP()
{
    float RP_read = RP.get_units();
    return round(RP_read);
}

int *read_all()
{
    // RD, RP, RY, RS, RR, RL
    read[0] = read_RD();
    read[1] = read_RP();
    read[2] = read_RY();
    read[3] = read_RS();
    read[4] = read_RR();
    read[5] = read_RL();
    return read;
}