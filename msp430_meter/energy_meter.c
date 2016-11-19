#include "energy_meter.h"

const float I_RATIO = I_CAL * (SUPPLY_VOLTAGE / 1024);

/* ____________________________________________
 * 	Configures the ACLK, setting the required
 * 	capacitor load for the 32kHz crystal.
 * ____________________________________________
 */
void configCLKS(void)
{
	//Configure MCLK and SMCLK to 1MHz for UART
	BCSCTL1 = CALBC1_1MHZ;
	DCOCTL = CALDCO_1MHZ;

	//Configure ACLK
	BCSCTL1 |= DIVA_1;				// ACLK /2
	BCSCTL3 |= XCAP_3;				// required capacitor load for crystal osc
}

/* ____________________________________________
 * Puts the CPU to sleep for a given time.
 * ____________________________________________
 */
void sleep(int time)
{
    TACCR1 = time;
    TACCTL1 |= CCIE;
    __bis_SR_register(LPM3_bits + GIE);
    TACCTL1 &= ~CCIE;
}

/* ____________________________________________
 * 	Configures the Timer_A.
 *
 * 	- TACCR0 will be used to trigger ADC every
 * 	time it counts to "t_adc_on" seconds,
 * 	to read the voltage.
 * ____________________________________________
 */
void configTimerA(unsigned int t_adc_on)
{
	TACCTL0 |= CCIE;							// CCR0 interrupt enabled
	TACCR0 = t_adc_on;							// 2048 -> 1 sec PWM Period
	//TACCTL1 |= OUTMOD_3;						// TACCR1 set/reset
	//TACCR1 = 2;								// TACCR1 PWM duty cycle
	TACTL = TASSEL_1 | ID_3 | MC_1 | TAIE;		// ACLK, /8 (2048Hz), Up to TACCR0, enable interrupt
}


/* _____________________________________________
 * Configures the ports and pins that are going
 * to be used and make necessary configurations
 * to reduce current consumption to the minimum.
 * _____________________________________________
 */
void configPorts(void)
{
	// Configuring pins that won't be used:
	// Select the unused port pins function to I/O
	//P1SEL |= 0xDF;		// Unused pins (1101 1111)
	P2SEL |= 0x3E;		// Unused pins (0011 1110)

	// Select the unused port pins direction to output
	//P1DIR |= 0xDF;
	P2DIR |= 0x3E;

	// Activating the internal resistor will prevent
	// floating input into the unused pins.
	//P1REN |= 0xDF;
	P2REN |= 0x3E;

	// Configuring the pins that will be used:
	// Configuring the Pin 2.0 to measure water consuption
	P2IFG &= ~WATER_METER;
	P2IE |= WATER_METER;
	P2DIR &= ~WATER_METER;	// Input
	P2REN |= WATER_METER;	// Resistor on
	P2IES |= WATER_METER;	// falling edge
	P2OUT |= WATER_METER;	// pullup

	//P1SEL &= ~BIT5;
	//P1DIR &= ~BIT5;			// Input direction
	//P1DIR |= VREF_OUT_PIN;	// Pin used to output internal VREF+
}

/* ____________________________________________
 * 	Configures the ADC10 to sample and convert
 * 	the voltage on the pin P1.5.
 * 	The ADC10 is enabled by the TimerA0 ISR.
 * ____________________________________________
 */
void configADC(void)
{
	// fmains = 50Hz, fadcclk = 16,384Hz
	// Tmains = 1/50 = 20ms, Tadcsht+Tadcconv = (4SHT cycles + 13CON cycles)/16,384 = 1.04ms
	// Nsamples = Tmains/(Tadcsht+Tadcconv) = 20ms/1.04ms = 19.27 ~ 20 samples
	ADC10CTL1 = INCH_5 | ADC10SSEL_1 | ADC10DIV_0 | CONSEQ_2 | SHS_0;			// P1.5, ACLK, /1 (16,384Hz), repeat single ch, triggered by SC bit

	// Tref_settle = 30us
	ADC10CTL0 |= REFON|SREF_1|REF2_5V|ADC10SHT_1|ADC10ON|ADC10IE|MSC|REFOUT;	// enable internal Vref (Vref+=2.5V Vref-=0V), 8 ADC10CLKs, enable ADC10
																				// enable int, vref+ output on P1.4, multiple samples
																				// REFON enables the built-in reference to settle
																				// before starting an A/D conversion.


	ADC10AE0 = BIT5 | BIT4;	// Enables channel 5(P1.5) as ADC input and channel 4(P1.4) as Vref+ output

	// DTC configuration
	ADC10DTC0 = ADC10CT;					// Data is transferred continuously after every conversion
	ADC10DTC1 = N_SAMPLES;					// Number of samples
	ADC10SA = (unsigned short)adc_sample;	// Samples will be stored here
}

/* ____________________________________________
 * 	Configures the LED's
 * ____________________________________________
 */
void configLED(void)
{
	P1DIR |= LED_GREEN;		//FOR TESTING
	P1OUT &= ~LED_GREEN;	//FOR TESTING
}

/* ___________________________________________
 *  Calculates the RMS value of the current
 * 	based on N_SAMPLES samples, and multiplies
 * 	it by 100 to store it in an integer with an
 * 	error of 10^-2.
 * ___________________________________________
 */
int calcIrms(void)
{
	unsigned short i = N_SAMPLES;
	float irms_f = 0;
	float squared_sample;
	short offset = 504;//(1 << ADC_BITS) >> 1; // 1024/2 = 512
	short filtered_sample;

	float sum = 0;
	while(i--)
	{
		filtered_sample = adc_sample[i] - offset;
		offset = (offset + (filtered_sample-offset) / 1024);
		squared_sample = powf((float)filtered_sample, 2.0f);
		sum += squared_sample;
	}
	irms_f = I_RATIO * sqrt(sum/N_SAMPLES);

	irms_f *= 100;

	return (int)irms_f;
}
