/* 
 * main.c
 * https://blog.csdn.net/qq_43176116/article/details/110388321
 */

#include <stdio.h>
#include "sha256.h"
#include <stdlib.h>

int main(int argc, char *argv[])
{
	/* unsigned char in[] = "hello world"; */
	unsigned char in[] = "abcdefghij\n";
	unsigned char buff[32];/* unsigned is necessary */

	memset(buff, 0, 32);
	sha256(in, strlen(in), buff);

	printf("The data is: %s\n", in);
	printf("Which length is: %d\n", (int)strlen(in));
	printf("The sha256 hash is:\n");

	for(int i = 0; i < 32; i++) {
		printf("%02x", buff[i]);	
	}
	printf("\n");

	return 0;
}
