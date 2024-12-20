#include "cc254x_types.h"
#include "cc254x_map.h"

typedef uint8 hciStatus_t;
typedef hciStatus_t (*hciFunc_t)(uint8 XDATA *);

typedef struct {
    uint16 opCode;
    hciFunc_t hciFunc;
} cmdPktTable_t;

uint8 XDATA hciTaskID;
uint8 XDATA hciTestTaskID;
uint8 XDATA hciGapTaskID;
uint8 XDATA hciL2capTaskID;
uint8 XDATA hciSmpTaskID;
uint8 XDATA hxiExtTaskID;

const cmdPktTable_t hciCmdTable[1];