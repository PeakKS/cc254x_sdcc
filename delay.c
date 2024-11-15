/**
 *  Implementation Details:
 *    By experimenting, David determined that jumping (e.g. lcall, ret, or
 *    ajmp) to an odd address takes one more instruction cycle than jumping
 *    to an even address.
 *  
 *    To get around this, the delayMicroseconds loop contains two jumps:
 *    one of these jumps will be to an odd address, and one will be to an
 *    even address, so the effects of the object's parity will always
 *    cancel out.
 *  
 *    The ".even" directive doesn't guarantee that the absolute address of
 *    a label will be even, it seems to only effect relative positioning
 *    within an object file, so we could not use the .even directive.
**/

#include "util.h"

void delay_us(unsigned char microseconds)
{
  __asm__ (
      "ljmp check\n"
    "loopStart:\n"
      "nop\nnop\nnop\nnop\n"
      "ljmp loopJump\n"
      "nop\nnop\nnop\nnop\n"
    "loopJump:\n"
      "nop\nnop\nnop\nnop\n"
    "check:\n"
      "mov a, dpl\n"
      "jz loopEnd\n"
      "djnz dpl, loopStart\n"
    "loopEnd: ret"
  );
}