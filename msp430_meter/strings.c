#include "strings.h"

/* _____________________________________________
 * Appends two given strings, "str1" and "str2",
 * and saves them in a given char array "dst".
 * _____________________________________________
 */
void append_str(unsigned char* str1, unsigned char* str2, unsigned char* dst)
{
    int i_eos_1 = 0;
    int i_eos_2 = 0;
    while(str1[i_eos_1] != '\0')
    {
        dst[i_eos_1] = str1[i_eos_1];
        i_eos_1++;
    }
    while(str2[i_eos_2] != '\0')
    {
        dst[i_eos_1] = str2[i_eos_2];
        i_eos_2++;
        i_eos_1++;
    }
    dst[i_eos_1] = '\0';
}

/* __________________________________________________________
 * Converts an integer "n" to a string with a null terminator
 * and stores it in a char array "dst" with size "size".
 * __________________________________________________________
 */
void itos(int n, unsigned char* dst, int size)
{
    int i = 0;
    int last_digit_i;

    if((n == 0) && (size > 1))
    {
        dst[0] = ASCII_0;
        dst[1] = '\0';
        return;
    }

    while((i < size - 1) && (n > 0))
    {
        dst[i++] = ASCII_0 + (n % 10);
        n /= 10;
    }
    dst[i] = '\0';
    last_digit_i = i - 1;
    i = 0;
    while(i < last_digit_i)
    {
        char temp = dst[i];
        dst[i] = dst[last_digit_i];
        dst[last_digit_i] = temp;
        i++;
        last_digit_i--;
    }
}

/* __________________________________________
 * Calculates the length of a null terminated
 * string.
 * __________________________________________
 */
int length(unsigned char* str)
{
	int i = 0;
	int size = 0;
	while(str[i] != '\0')
	{
		size += 1;
		i++;
	}
	return size;
}
