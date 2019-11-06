/*
 * Make crc32 works in Python communicating with MCU C Programming Language Evironment
 */
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <stdint.h>
#include <unistd.h>

#define CRC32_POLYNOMIAL_REV 0xEDB88320L

/* 
 * Copy from
 * third_party/exactle/ws-core/sw/util/alternates/crc32_notable.c:CalcCrc32()
 * in AmbiqSuite-R2.3.0
 */
uint32_t apollo3_crc32_notable_c(uint8_t *buf, uint32_t init, uint32_t len)
{
    uint32_t crc = init;
    uint32_t j;

    while (len > 0) {
        crc ^= *buf;

        for (j = 8; j > 0; j--) {
            if (crc & 1)
                crc = crc >> 1 ^ CRC32_POLYNOMIAL_REV;
            else
                crc = crc >> 1;
        }
        buf++;
        len--;
    }

    crc = crc ^ 0xFFFFFFFFU;

    return crc;
}

/* 
 * Rewrite from crc32_v1.cpp
 */ 
uint32_t crc32(uint8_t *buf, uint32_t init, uint32_t len)
{ 
    uint32_t crc = init; 
    uint32_t crc_temp; 
    int j; 

    while (len > 0) { 

        crc_temp = (crc ^ *buf) & 0xff; 

        for (j = 8; j > 0; j--) { 
            if (crc_temp & 1) 
                crc_temp = (crc_temp >> 1)^CRC32_POLYNOMIAL_REV; 
            else 
                crc_temp >>= 1; 
        }

        crc = ((crc >> 8) & 0x00FFFFFFL)^crc_temp; 
        len--;
        buf++;
    } 

    /* 
     * If removing here's comments, this function is same as above function
     * apollo3_crc32_notable_c() 
     */
    /* crc = crc ^ 0xFFFFFFFFU; */
    return(crc); 
} 

int main(int argc, char *argv[])
{
    uint8_t buffer[] = {
        0x0a, 0x0b, 0x0c, 0x0d
    };

    printf("data\'s crc32: 0x%x\n", apollo3_crc32_notable_c(buffer, 0xffffffff, sizeof(buffer)));
    printf("data\'s crc32: 0x%x\n", crc32(buffer, 0xffffffff, sizeof(buffer)));

    return 0;
}
