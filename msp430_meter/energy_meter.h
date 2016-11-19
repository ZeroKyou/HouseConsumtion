#ifndef ENERGY_METER_H_
#define ENERGY_METER_H_

#include <msp430.h>
#include <math.h>

#define TIMERA_FREQ			2048
#define TIMERA_1MS	(TIMERA_FREQ >> 10)	// Aproximately 1 ms (TimerFreq/1024 + 1 ~  TimerFreq/1000)
#define TIMERA_100MS		205					// Aprox. 100ms
#define TIMERA_1S			2047
#define TIMERA_3S			6141				// 2047*3
#define TIMERA_5S			10235				// 2047*5
#define TIMERA_60S			122820				// 2047*60

#define LED_RED 			BIT0
#define LED_GREEN 			BIT6
#define LEDS_OFF 			BIT0 | BIT6

#define WATER_METER			BIT0

#define ADC_BITS			10
#define N_SAMPLES			20

#define SUPPLY_VOLTAGE		2.5f
#define VREF_OUT_PIN		BIT4
#define I_CAL				30.0f				// Calibration constant to get the value of the primary current
												// 30 (primary current) / 1 (voltage across burden resistor)


extern const float I_RATIO;						// Calculates the ratio between the primary current and the ADC count
												// of the CT's secondary current
unsigned short adc_sample[N_SAMPLES];			// ADC samples will be stored here

void configCLKS(void);
void sleep(int time);
void configTimerA(unsigned int t_adc_on);
void configPorts(void);
void configADC(void);
void configLED(void);
int calcIrms(void);

#endif /* ENERGY_METER_H_ */
