/*! \file cc2511_map.h
 * This header file provides access to the special registers on the CC2511F32, which
 * allow direct manipulation of the chip's hardware.
 *
 * This file also provides macros for defining Interrupt Service Routines (ISRs).
 *
 * For documentation, see the
 * <a href="http://www.ti.com/product/CC2511">CC2511F32 datasheet</a>.
 */

#ifndef _CC254X_MAP_H
#define _CC254X_MAP_H

// Avoid false-alarm syntax errors in Eclipse.
#include <stdbool.h>
#include "cc254x_types.h"
#include "mcs51/compiler.h"

#define SFRBIT(address, name, bit7, bit6, bit5, bit4, bit3, bit2, bit1, bit0) \
  SFR(name, address);    \
  SBIT(bit0, address, 0); \
  SBIT(bit1, address, 1); \
  SBIT(bit2, address, 2); \
  SBIT(bit3, address, 3); \
  SBIT(bit4, address, 4); \
  SBIT(bit5, address, 5); \
  SBIT(bit6, address, 6); \
  SBIT(bit7, address, 7);

#if defined (__SDCC) || defined (__CDT_PARSER__) || defined (__INTELLISENSE__)

/*! Defines or declares an interrupt service routine (ISR).
 * <b>For the interrupt to work, SDCC requires that the declaration must
 * be present in the file that defines main().</b>
 *
 * \param source
 *    The source of the interrupt.  Must be either the first word of one of
 *    the *_VECTOR macros defined in this file (e.g. "P1INT").
 *
 * \param bank
 *    The register bank to use.  Must be a number from 0 to 3, inclusive.
 *    If you choose a non-zero bank, then the compiler will assume that the
 *    ISR can modify the registers in that bank, and not bother to restore
 *    them to their original value.
 *    Therefore, we recommend choosing bank 0 unless you want to save some
 *    CPU time and you can guarantee that it is OK for the interrupt to
 *    modify those registers.
 *
 * Example ISR declaration (in a .h file):
\code
ISR(UTX1, 0);
\endcode
 *
 * Example ISR definition (in a .c file):
\code
ISR(UTX1, 0)
{
    // code for handling event and clearing interrupt flag
}
\endcode
 */
#define ISR(source, bank) void ISR_##source() __interrupt(source##_VECTOR) __using(bank)

#else
#error "Unknown compiler."
#endif

// Interrupt vectors (SWRU191F Table 2-5. Interrupts Overview)
#define RFTXRX_VECTOR 0
#define ADC_VECTOR    1
#define URX0_VECTOR   2
#define URX1_VECTOR   3
#define ENC_VECTOR    4
#define ST_VECTOR     5
#define P2INT_VECTOR  6
#define UTX0_VECTOR   7
#define DMA_VECTOR    8
#define T1_VECTOR     9
#define T2_VECTOR     10
#define T3_VECTOR     11
#define T4_VECTOR     12
#define P0INT_VECTOR  13
#define UTX1_VECTOR   14
#define P1INT_VECTOR  15
#define RF_VECTOR     16
#define WDT_VECTOR    17

// Special Function Registers (SWRU191F Table 2-1. SFR Overview)

SFRBIT(0x80, P0, P0_7, P0_6, P0_5, P0_4, P0_3, P0_2, P0_1, P0_0)
SFR(SP,    0x81);
SFR(DPL0,  0x82);
SFR(DPH0,  0x83);
SFR(DPL1,  0x84);
SFR(DPH1,  0x85);
SFR(U0CSR, 0x86);
SFR(PCON,  0x87);

SFRBIT(0x88, TCON, URX1IF, _TCON_6, ADCIF, _TCON_4, URX0IF, _TCON_2, RFTXRXIF, _TCON_0)
SFR(P0IFG, 0x89);
SFR(P1IFG, 0x8A);
SFR(P2IFG, 0x8B);
SFR(PICTL, 0x8C);
SFR(P1IEN, 0x8D);
//  0x8E
SFR(P0INP, 0x8F);

SFRBIT(0x90, P1, P1_7, P1_6, P1_5, P1_4, P1_3, P1_2, P1_1, P1_0)
SFR(RFIM,  0x91);
SFR(DPS,   0x92);
SFR(MPAGE, 0x93);
/**
 * see "2.2.4 XDATA Memory Access" in the datasheet
 * see "4.1.1 pdata access by SFR" in SDCC manual
 * this MCU uses a non standard way to access XDATA
 * this is how we tell SDCC which register to use
 * without this trick the CRT code for initializing globals silently fails
**/
SFR(_XPAGE, 0x93);
SFR(T2CTRL, 0x94);
SFR(ST0, 0x95);
SFR(ST1, 0x96);
SFR(ST2, 0x97);

SFRBIT(0x98, S0CON, _SOCON7, _SOCON6, _SOCON5, _SOCON4, _SOCON3, _SOCON2, ENCIF_1, ENCIF_0)
//  0x99
SFR(IEN2, 0x9A);
SFR(S1CON, 0x9B);
SFR(T2EVTCFG, 0x9C);
SFR(SLEEPSTA, 0x9D);
SFR(CLKCONSTA, 0x9E);
SFR(FMAP, 0x9F);

SFRBIT(0xA0, P2, P2_7, P2_6, P2_5, P2_4, P2_3, P2_2, P2_1, P2_0)
SFR(T2IRQF, 0xA1);
SFR(T2M0, 0xA2);
SFR(T2M1, 0xA3);
SFR(T2MOVF0, 0xA4);
SFR(T2MOVF1, 0xA5);
SFR(T2MOVF2, 0xA6);
SFR(T2IRQM, 0xA7);

SFRBIT(0xA8, IEN0, EA, _IEN06, STIE, ENCIE, URX1IE, URX0IE, ADCIE, RFTXRXIE)
SFR(IP0, 0xA9);
//  0xAA
SFR(P0IEN, 0xAB);
SFR(P2IEN, 0xAC);
SFR(STLOAD, 0xAD);
SFR(PMUX, 0xAE);
SFR(T1STAT, 0xAF);

//  0xB0
SFR(ENCDI, 0xB1);
SFR(ENCDO, 0xB2);
SFR(ENCCS, 0xB3);
SFR(ADCCON1, 0xB4);
SFR(ADCCON2, 0xB5);
SFR(ADCCON3, 0xB6);
//  0xB7

SFRBIT(0xB8, IEN1, _IEN17, _IEN16, P0IE, T4IE, T3IE, T2IE, T1IE, DMAIE)
SFR(IP1, 0xB9);
SFR(ADCL, 0xBA);
SFR(ADCH, 0xBB);
SFR(RNDL, 0xBC);
SFR(RNDH, 0xBD);
SFR(SLEEP, 0xBE);
SFR(RFERRF, 0xBF);

SFRBIT(0xC0, IRCON, STIF, _IRCON6, P0IF, T4IF, T3IF, T2IF, T1IF, DMAIF)
SFR(U0DBUF, 0xC1);
SFR(U0BAUD, 0xC2);
SFR(T2MSEL, 0xC3);
SFR(U0UCR, 0xC4);
SFR(U0GCR, 0xC5);
SFR(CLKCON, 0xC6);
SFR(MEMCTR, 0xC7);

//  0xC8
SFR(WDCTL, 0xC9);
SFR(T3CNT, 0xCA);
SFR(T3CTL, 0xCB);
SFR(T3CCTL0, 0xCC);
SFR(T3CC0, 0xCD);
SFR(T3CCTL1, 0xCE);
SFR(T3CC1, 0xCF);

SFRBIT(0xD0, PSW, CY, AC, F0, RS1, RS0, OV, F1, P)
SFR(DMAIRQ, 0xD1);
SFR(DMA1CFGL, 0xD2);
SFR(DMA1CFGH, 0xD3);
SFR(DMA0CFGL, 0xD4);
SFR(DMA0CFGH, 0xD5);
SFR(DMAARM, 0xD6);
SFR(DMAREQ, 0xD7);

SFRBIT(0xD8, TIMIF, _TIMIF7, OVFIM, T4CH1IF, T4CH0IF, T4OVFIF, T3CH1IF, T3CH0IF, T3OVFIF)
SFR(RFD, 0xD9);
SFR(T1CC0L, 0xDA);
SFR(T1CC0H, 0xDB);
SFR(T1CC1L, 0xDC);
SFR(T1CC1H, 0xDD);
SFR(T1CC2L, 0xDE);
SFR(T1CC2H, 0xDF);

SFRBIT(0xE0, ACC, ACC_7, ACC_6, ACC_5, ACC_4, ACC_3, ACC_2, ACC_1, ACC_0)
SFR(RFST, 0xE1);
SFR(T1CNTL, 0xE2);
SFR(T1CNTH, 0xE3);
SFR(T1CTL, 0xE4);
SFR(T1CCTL0, 0xE5);
SFR(T1CCTL1, 0xE6);
SFR(T1CCTL2, 0xE7);

SFRBIT(0xE8, IRCON2, _IRCON27, _IRCON26, _IRCON25, WDTIF, P1IF, UTX1IF, UTX0IF, P2IF)
SFR(RFIRQF0, 0xE9);
SFR(T4CNT, 0xEA);
SFR(T4CTL, 0xEB);
SFR(T4CCTL0, 0xEC);
SFR(T4CC0, 0xED);
SFR(T4CCTL1, 0xEE);
SFR(T4CC1, 0xEF);

SFRBIT(0xF0, B, B_7, B_6, B_5, B_4, B_3, B_2, B_1, B_0)
SFR(PERCFG, 0xF1);
SFR(ADCCFG, 0xF2);
SFR(P0SEL, 0xF3);
SFR(P1SEL, 0xF4);
SFR(P2SEL, 0xF5);
SFR(P1INP, 0xF6);
SFR(P2INP, 0xF7);

SFRBIT(0xF8, U1CSR, U1MODE, U1RE, U1SLAVE, U1FE, U1ERR, U1RX_BYTE, U1TX_BYTE, U1ACTIVE)
SFR(U1DBUF, 0xF9);
SFR(U1BAUD, 0xFA);
SFR(U1UCR, 0xFB);
SFR(U1GCR, 0xFC);
SFR(P0DIR, 0xFD);
SFR(P1DIR, 0xFE);
SFR(P2DIR, 0xFF);

#define USB_VECTOR P2INT_VECTOR
#define USBIF P2IF

// 16-bit SFRs
SFR16E(DMA0CFG, 0xD5D4);
SFR16E(DMA1CFG, 0xD3D2);
SFR16E(FADDR,   0xADAC);
SFR16E(ADC,     0xBBBA);
SFR16E(RND,     0xBDBC);
SFR16E(T1CC0,   0xDBDA);
SFR16E(T1CC1,   0xDDDC);
SFR16E(T1CC2,   0xDFDE);
SFR16E(T1CNT,   0xE3E2);

// XDATA Radio Registers (SWRS055F Table 32)

/* TODO SFRX(SYNC1, 0xDF00);
SFRX(SYNC0, 0xDF01);
SFRX(PKTLEN, 0xDF02);
SFRX(PKTCTRL1, 0xDF03);
SFRX(PKTCTRL0, 0xDF04);
SFRX(ADDR, 0xDF05);
SFRX(CHANNR, 0xDF06);
SFRX(FSCTRL1, 0xDF07);
SFRX(FSCTRL0, 0xDF08);
SFRX(FREQ2, 0xDF09);
SFRX(FREQ1, 0xDF0A);
SFRX(FREQ0, 0xDF0B);
SFRX(MDMCFG4, 0xDF0C);
SFRX(MDMCFG3, 0xDF0D);
SFRX(MDMCFG2, 0xDF0E);
SFRX(MDMCFG1, 0xDF0F);
SFRX(MDMCFG0, 0xDF10);
SFRX(DEVIATN, 0xDF11);
SFRX(MCSM2, 0xDF12);
SFRX(MCSM1, 0xDF13);
SFRX(MCSM0, 0xDF14);
SFRX(FOCCFG, 0xDF15);
SFRX(BSCFG, 0xDF16);
SFRX(AGCCTRL2, 0xDF17);
SFRX(AGCCTRL1, 0xDF18);
SFRX(AGCCTRL0, 0xDF19);
SFRX(FREND1, 0xDF1A);
SFRX(FREND0, 0xDF1B);
SFRX(FSCAL3, 0xDF1C);
SFRX(FSCAL2, 0xDF1D);
SFRX(FSCAL1, 0xDF1E);
SFRX(FSCAL0, 0xDF1F);

SFRX(TEST2, 0xDF23);
SFRX(TEST1, 0xDF24);
SFRX(TEST0, 0xDF25);

SFRX(PA_TABLE0, 0xDF2E);
SFRX(IOCFG2, 0xDF2F);
SFRX(IOCFG1, 0xDF30);
SFRX(IOCFG0, 0xDF31);

SFRX(PARTNUM, 0xDF36);
SFRX(VERSION, 0xDF37);
SFRX(FREQEST, 0xDF38);
SFRX(LQI, 0xDF39);
SFRX(RSSI, 0xDF3A);
SFRX(MARCSTATE, 0xDF3B);
SFRX(PKTSTATUS, 0xDF3C);
SFRX(VCO_VC_DAC, 0xDF3D);


// I2S Registers (SWRS055F Table 33)
SFRX(I2SCFG0, 0xDF40);
SFRX(I2SCFG1, 0xDF41);
SFRX(I2SDATL, 0xDF42);
SFRX(I2SDATH, 0xDF43);
SFRX(I2SWCNT, 0xDF44);
SFRX(I2SSTAT, 0xDF45);
SFRX(I2SCLKF0, 0xDF46);
SFRX(I2SCLKF1, 0xDF47);
SFRX(I2SCLKF2, 0xDF48); */


// Common USB Registers (SWRS055F Table 34)
SFRX(USBADDR, 0x6200);
SFRX(USBPOW, 0x6201);
SFRX(USBIIF, 0x6202);

SFRX(USBOIF, 0x6204);

SFRX(USBCIF, 0x6206);
SFRX(USBIIE, 0x6207);

SFRX(USBOIE, 0x6209);

SFRX(USBCIE, 0x620B);
SFRX(USBFRML, 0x620C);
SFRX(USBFRMH, 0x620D);
SFRX(USBINDEX, 0x620E);
SFRX(USBCTRL, 0x620F);

// Indexed USB Endpoint Registers (SWRS055F Table 35)
SFRX(USBMAXI, 0x6210);
SFRX(USBCSIL, 0x6211);
SFRX(USBCSIH, 0x6212);
SFRX(USBMAXO, 0x6213);
SFRX(USBCSOL, 0x6214);
SFRX(USBCSOH, 0x6215);
SFRX(USBCNTL, 0x6216);
SFRX(USBCNTH, 0x6217);

// USB Fifo addresses
SFRX(USBF0, 0x6220);
SFRX(USBF1, 0x6222);
SFRX(USBF2, 0x6224);
SFRX(USBF3, 0x6226);
SFRX(USBF4, 0x6228);
SFRX(USBF5, 0x622A);

#define USBCS0     USBCSIL
#define USBCNT0    USBCNTL

/*! Evaluates to the XDATA address of an SFR.
 *
 * Most of the internal SFRs are also part of the XDATA memory space,
 * which means you can have pointers to them of type
 * <code>uint8 XDATA *</code> and you can read or write to them using
 * DMA transfers.
 *
 * This macro does NOT work with the SFRs that are highlighted in gray
 * in Table 30 of the CC2511F32 datasheet (the "SFR Address Overview"
 * table). */
#define XDATA_SFR_ADDRESS(sfr) (0x6300 + ((unsigned int)&(sfr))) /* NOT SURE */

/*! This struct represents the configuration of a single DMA channel.
 * See the "DMA Controller" section of the CC2511F32 datasheet
 * for information on how to use this struct and DMA in general.
 *
 * Also see dma.h.
 *
 * NOTE: You won't find DC6 or DC7 in the datasheet, the names of
 * those bytes were invented for this struct. */
typedef struct
{
    unsigned char SRCADDRH;
    unsigned char SRCADDRL;
    unsigned char DESTADDRH;
    unsigned char DESTADDRL;

    /*! Bits 7:5 are VLEN, bits 4:0 are LEN[12:8] */
    unsigned char VLEN_LENH;
    unsigned char LENL;

    /*! Bit 7 is WORDSIZE, Bits 6:5 are TMODE, Bits 4:0 are TRIG. */
    unsigned char DC6;

    /*! Bits 7:6 are SRCINC, 5:4 are DESTINC, 3 is IRQMASK, 2 is M8, 1:0 are PRIORITY. */
    unsigned char DC7;
} DMA_CONFIG;


#endif /* _CC254X_MAP_H */
