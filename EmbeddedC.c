/*
Summary
Library of Embedded C Functions made by ME
*/

// Imports
//#include<LM4F120H5QR.h>
//#include<tm4c123gh6pm.h>
//#include<stdio.h>
#include<time.h>

// Definitions
#define BLACK 0x00U
#define RED 0x02U
#define BLUE 0x04U
#define GREEN 0x08U
#define PURPLE 0x06U
#define YELLOW 0x0AU
#define CYAN 0x0CU
#define WHITE 0x0EU
#define PressedCode 0x00U
#define LeftButton *((unsigned int*)0x40025040)
#define RightButton *((unsigned int*)0x40025004)

// Util Functions
void delay(int second)
{
  float milsec = 50 * second;
  clock_t startTime = clock();
  while(clock() < (startTime + milsec));
}

// TIVAC Board Functions
void LEDClock()
{
  
  *((unsigned int*)0x400FE608)=0x20U;
  *((unsigned int*)0x40025400)=0x0EU;
  *((unsigned int*)0x4002551C)=0x0EU;
  while(1){
    *((unsigned int*)0x400253FC)=GREEN;
    delay(5);
    *((unsigned int*)0x400253FC)=YELLOW;
    delay(2);
    *((unsigned int*)0x400253FC)=RED;
    delay(8);
  }
}

void LEDColorSwitch()
{
  *((unsigned int*)0x400FE608)=0x20U;
  *((unsigned int*)0x40025400)=0x0EU;
  *((unsigned int*)0x4002551C)=0x1FU;
  *((unsigned int*)0x40025524)=0xFFU;
  *((unsigned int*)0x40025510)=0x11U;
  *((unsigned int*)0x40025520)=0x4C4F434BU;

// Q1 - ButtonPress Color Change
  int counter = 1;
  int Colors[] = {RED, PURPLE, BLUE, CYAN, GREEN, YELLOW};
  *((unsigned int*)0x40025038) = Colors[0];
  int buttonPressed = 0;
  while(1)
  {
    if (buttonPressed == 0 && *((unsigned int*)0x40025040) == PressedCode)
    {
      buttonPressed = 1;
      *((unsigned int*)0x40025038) = Colors[counter];
      counter = (counter + 1)%(sizeof(Colors)/sizeof(Colors[0]));
    }
    else if (buttonPressed == 1 && *((unsigned int*)0x40025040) != PressedCode)
    {
      buttonPressed = 0;
    }
  }
}

void ButtonClickLEDGlow()
{
  
  *((unsigned int*)0x400FE608)=0x20U;
  *((unsigned int*)0x40025400)=0x0EU;
  *((unsigned int*)0x4002551C)=0x1FU;
  *((unsigned int*)0x40025524)=0xFFU;
  *((unsigned int*)0x40025510)=0x11U;
  *((unsigned int*)0x40025520)=0x4C4F434BU;

  // Q2 - Multi Button Color
  // Initlal Color
  *((unsigned int*)0x40025038) = BLACK;
  int BothPressed = GREEN;
  int LeftPressed = RED;
  int RightPressed = BLUE;
  int NonePressed = BLACK;
  
  while(1)
  {
    if (LeftButton == PressedCode &&  RightButton == PressedCode)
    {
      *((unsigned int*)0x40025038) = BothPressed;
    }
    else if (LeftButton == PressedCode && RightButton != PressedCode)
    {
      *((unsigned int*)0x40025038) = LeftPressed;
    }
    else if (LeftButton != PressedCode && RightButton == PressedCode)
    {
      *((unsigned int*)0x40025038) = RightPressed;
    }
    else 
    {
      *((unsigned int*)0x40025038) = NonePressed;
    }
  }
}

void BuzzerAlarm()
{
  // Q3 Alarm using Buzzer
  *((volatile unsigned int *)0x400FE608)=(0x04U); // Clock Gating Enable
  *((volatile unsigned int *)0x40006400)=(0xF0U); // Data Direction
  *((volatile unsigned int *)0x4000651C)=(0xF0U); // Digital Enable
  while(1) 
  {  
    
    //*((unsigned int*)0x40025038) = RED;
    *((volatile unsigned int *)(0x400063C0))=(0x00U);  delay(5);// 0000
    *((volatile unsigned int *)(0x400063C0))=(0x10U);  delay(5);// 0001
    *((volatile unsigned int *)(0x400063C0))=(0x20U);  delay(5);// 0010
    *((volatile unsigned int *)(0x400063C0))=(0x30U);  delay(5);// 0011
    
    //*((unsigned int*)0x40025038) = BLUE;
    *((volatile unsigned int *)(0x400063C0))=(0x40U);  delay(5);// 0100
    *((volatile unsigned int *)(0x400063C0))=(0x50U);  delay(5);// 0101
    *((volatile unsigned int *)(0x400063C0))=(0x60U);  delay(5);// 0110
    *((volatile unsigned int *)(0x400063C0))=(0x70U);  delay(5);// 0111
    
    //*((unsigned int*)0x40025038) = GREEN;
    *((volatile unsigned int *)(0x400063C0))=(0x80U);  delay(5);// 1000
    *((volatile unsigned int *)(0x400063C0))=(0x90U);  delay(5);// 1001
    *((volatile unsigned int *)(0x400063C0))=(0xA0U);  delay(5);// 1010
    *((volatile unsigned int *)(0x400063C0))=(0xB0U);  delay(5);// 1011
    
    //*((unsigned int*)0x40025038) = WHITE;
    *((volatile unsigned int *)(0x400063C0))=(0xC0U);  delay(5);// 1100
    *((volatile unsigned int *)(0x400063C0))=(0xD0U);  delay(5);// 1101
    *((volatile unsigned int *)(0x400063C0))=(0xE0U);  delay(5);// 1110
    *((volatile unsigned int *)(0x400063C0))=(0xF0U);  delay(5);// 1111
    
    /*
    *((volatile unsigned int *)(0x40006040))=(0x10U); delay(1); // C4
    *((volatile unsigned int *)(0x40006080))=(0x20U); delay(1); // C5
    *((volatile unsigned int *)(0x40006100))=(0x30U); delay(1); // C6
    *((volatile unsigned int *)(0x40006200))=(0x40U); delay(1); // C7  
    */
  }
}