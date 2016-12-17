#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void fvuln(char *str1, int age)
{
  char *ptr1;
  int local_age;
  char name[32];
  char *ptr2;

  local_age = age;

  ptr1 = (char *) malloc(256);
  printf("\nPTR1 = [ %p ]", ptr1);
  strcpy(name, str1);
  printf("\nPTR1 = [ %p ]\n", ptr1);

  free(ptr1);

  ptr2 = (char *) malloc(40);

  snprintf(ptr2, 40-1, "%s is %d years old", name, local_age);
  printf("\n%s\n", ptr2);
}

int main(int argc, char *argv[])
{
  int pad[10] = {0, 0, 0, 0, 0, 0, 0, 10, 0, 0};

  if (argc == 3)
    fvuln(argv[1], atoi(argv[2]));

  return 0;
}