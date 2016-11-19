#include <msp430.h> 

#include "energy_meter.h"
#include "uart.h"
#include "strings.h"

static volatile int water_meter_cycles;
int irms;

int main(void) {
    WDTCTL = WDTPW | WDTHOLD;	// Stop watchdog timer

    irms = 0;
    water_meter_cycles = 0;
    configCLKS();
    configPorts();
    configTimerA(TIMERA_5S);
    TA0CCTL0 &= ~CCIE;	// Disable timer a ccr0 interrupts for the rest of the configuration
    configADC();
    configLED();
    UART_Init();

    AT_RSTModule();
    AT_JoinAccessPoint();

    TA0CCTL0 |= CCIE;	// End of configuration. Enable timer a ccr0 interrupts

    do{
    	__bis_SR_register(LPM3_bits + GIE);
    	irms = calcIrms();
    	AT_SendReadings(irms, water_meter_cycles);
    	//water_meter_cycles = 0;
    	TACCTL0 |= CCIE;
    }
    while(1);
}

#pragma vector=ADC10_VECTOR
__interrupt void ADC10_ISR(void)
{
	// Disables conversion and reference voltage
	ADC10CTL0 &= ~ENC;
	ADC10CTL0 = 0;

	// Disable Timer_A CCR0 interrupts
	TACCTL0 &= ~CCIE;
	__bic_SR_register_on_exit(LPM3_bits);	// Exits low power mode 3 to calculate irms.
}

#pragma vector=NMI_VECTOR
__interrupt void NMI_ISR(void)
{
	IFG1 &= ~OFIFG;
}

#pragma vector=PORT1_VECTOR
#pragma vector=PORT2_VECTOR
__interrupt void P2_ISR(void)
{
	if(P2IFG & WATER_METER)
	{
		P2IFG &= ~WATER_METER;
		P2IE &= ~WATER_METER;			/* Debounce */
		water_meter_cycles++;
		TACCR2 = 72;					// Wait 35ms before answering another interrupt
		TACCTL2 |= CCIE;
	}
}

#pragma vector=TIMER0_A0_VECTOR
#pragma vector=TIMER0_A1_VECTOR
__interrupt void TA_ISR(void)
{
	switch(TAIV)
	{
		case TA0IV_NONE:				// TACCR0
			P1OUT ^= LED_GREEN;			//FOR TESTING

			ADC10CTL0 |= REFON|SREF_1|REF2_5V|ADC10SHT_1|ADC10ON|ADC10IE|MSC|REFOUT;
			__delay_cycles(30);			// Delay 30us to allow the vref and the capacitor to stabilize
			ADC10CTL0 |= ENC|ADC10SC;	// Start conversion
			break;
		case TA0IV_TACCR1:				// TACCR1
			__bic_SR_register_on_exit(LPM3_bits);
			break;
		case TA0IV_TACCR2:				// TACCR2
			P2IFG &= ~WATER_METER;
			P2IE |= WATER_METER;
			TACCTL2 = 0;
			TACCR2 = 0;
			break;
		default:
			break;
	}
}
