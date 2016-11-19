#ifndef UART_H_
#define UART_H_

#define RX	BIT1
#define TX	BIT2

#define MAX_RX_DATA_SIZE 10

void UART_Init(void);
void UART_SendArray(unsigned char* src, unsigned int size);
void UART_SendChar(unsigned char src);
void AT_RSTModule(void);
void AT_JoinAccessPoint(void);
void AT_ConnectToWebsite(void);
void AT_SendReadings(int irms, int water_meter_pulses);

#endif /* UART_H_ */
