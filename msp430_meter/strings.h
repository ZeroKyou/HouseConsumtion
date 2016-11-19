#ifndef STRINGS_H_
#define STRINGS_H_

#define ASCII_0 48

void append_str(unsigned char* str1, unsigned char* str2, unsigned char* dst);
void itos(int n, unsigned char* dst, int size);
int length(unsigned char* str);

#endif /* STRINGS_H_ */
