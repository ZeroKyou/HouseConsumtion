#include "uart.h"
#include "strings.h"
#include "msp430g2553.h"
#include "energy_meter.h"

static unsigned char uart_rx_data;
static unsigned char uart_rx_data_flag;
static unsigned char *uart_tx_data;
static unsigned short uart_tx_data_size;

/**
 * Initializes the USCI in UART Mode
 * Baud rate: 9600
 * Clock source: SMCLK @ 1MHz
 */
void UART_Init(void)
{
	P1SEL |= RX + TX;
	P1SEL2 |= RX + TX;

	UCA0CTL1 |= UCSWRST;	// Start of UCA0 config
	UCA0CTL1 |= UCSSEL_2;	// SMCLK
	UCA0BR0 = 104;			// (1,000,000/9600) = 104.166
	UCA0BR1 = 0;
	UCA0MCTL = UCBRS0;		// UCBRSx = 1
	UCA0CTL1 &= ~UCSWRST;

	uart_tx_data_size = 0;

	IE2 |= UCA0RXIE;		// Enable USCIA0 RX interrupt
}

/**
 * Sends a char "src" through the UART serial communication
 */
void UART_SendChar(unsigned char src)
{
	UART_SendArray(&src, 1);
}

/**
 * Sends a "size" sized string "src" through the UART serial communication
 */
void UART_SendArray(unsigned char* src, unsigned int size)
{
	while(uart_tx_data_size != 0) __bis_SR_register(LPM3_bits + GIE);
	uart_tx_data = src;
	uart_tx_data_size = size;
	IE2 |= UCA0TXIE;
}

/**
 * Checks for an OK message in from the ESP8266.
 * Returns 1 if OK is found, 0 otherwise.
 */
unsigned char Got_OK_Message()
{
	unsigned char found_o = 0;
	int timeout = 10;
	char c;
	do
	{
		if(uart_rx_data_flag)
		{
			c = uart_rx_data;
			switch(c)
			{
				case 'O':
					found_o = 1;
					break;
				case 'K':
					if(found_o)
						return 1;
					found_o= 0;
					break;
				default:
					found_o = 0;
			}
		}
	}
	while((timeout-- > 0) && (c != '\r'));
	return 0;
}

/**
 * Resets the ESP8266
 */
void AT_RSTModule(void)
{
	UART_SendArray("AT+RST\r\n", 8);
	sleep(TIMERA_1S);
}


/**
 * Joins the AP where the webserver is.
 */
void AT_JoinAccessPoint(void)
{
	int timeout = 2;
	unsigned char connected = 0;

	do
	{
		UART_SendArray("AT+CWJAP=\"HC\",\"ProjetoFinal9119\"\r\n", 34);
		sleep(TIMERA_5S);
		connected = Got_OK_Message();
	}
	while((timeout-- > 0) && !connected);
}

/* ________________________
 * Connects to the website.
 * ________________________
 */
void AT_ConnectToWebsite(void)
{
	UART_SendArray("AT+CIPSTART=\"TCP\",\"192.168.1.11\",8000\r\n", 39);
}

/* ________________________________
 * Specifies the number of bytes to
 * be sent in the POST request.
 * ________________________________
 */
void AT_BytesToSend(int size)
{
	unsigned char str[] = "AT+CIPSEND=";
	unsigned char size_s[5] = {'\0'};
	unsigned char final_str[17] = {'\0'};
	unsigned char new_line[] = "\r\n";
	itos(size, size_s, 5);
	append_str(str, size_s, final_str);
	append_str(final_str, new_line, final_str);
	UART_SendArray(final_str, 16);
}

/* ______________________________________________________
 * Sends Irms ADC readings, and the number of water meter
 * pulses.
 * ______________________________________________________
 */
void AT_SendReadings(int irms, int water_meter_cycles)
{
	int post_length;
	int post_content_length;
	unsigned char post[200] = {'\0'};
	unsigned char post_header[] = "POST /meter/reading/ HTTP/1.1\r\nHost: 192.168.1.11:8000\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: ";
	unsigned char new_lines[] = "\r\n\r\n";
	unsigned char irms_s[4] = {'\0'};
	unsigned char water_meter_cycles_s[4] = {'\0'};
	itos(irms, irms_s, 4);
	itos(water_meter_cycles, water_meter_cycles_s, 4);
	post_content_length = 25 + length(irms_s) + length(water_meter_cycles_s);
	post_length = 130 + post_content_length;
	unsigned char post_content_length_s[4] = {'\0'};
	unsigned char post_irms_s[] = "irms=";
	unsigned char post_water_meter_cycles_s[] = "&water_meter_cycles=";

	AT_ConnectToWebsite();
	sleep(TIMERA_100MS);
	AT_BytesToSend(post_length);
	sleep(TIMERA_100MS);
	itos(post_content_length, post_content_length_s, 4);
	append_str(post_header, post_content_length_s, post);
	append_str(post, new_lines, post);
	append_str(post, post_irms_s, post);
	append_str(post, irms_s, post);
	append_str(post, post_water_meter_cycles_s, post);
	append_str(post, water_meter_cycles_s, post);
	append_str(post, new_lines, post);

	UART_SendArray(post, 200);
	sleep(TIMERA_1S);
}

#pragma vector=USCIAB0RX_VECTOR
__interrupt void USCI0RX_ISR(void)
{
	uart_rx_data = UCA0RXBUF;
	uart_rx_data_flag = 1;
}

#pragma vector=USCIAB0TX_VECTOR
__interrupt void USCI0TX_ISR(void)
{
	if(uart_tx_data_size > 0)
	{
		if(*uart_tx_data == '\0')
		{
			uart_tx_data_size = 0;
			return;
		}
		UCA0TXBUF = *(uart_tx_data++);
		uart_tx_data_size--;
	}
	else
		IE2 &= ~UCA0TXIE;
}
