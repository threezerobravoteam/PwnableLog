/*
House of force vulnerable program. 
*/
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
        char *buf1;
        buf1 = malloc(256);

        free(buf1);
        return 0;
}