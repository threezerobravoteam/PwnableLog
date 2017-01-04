#include <stdio.h>
#include <time.h>
#include <string.h>
int menu();
void write_blog();
void read_blog();
int list_blog(char *s);
int check_vaild(char c);
int menu()
{
    int i;
    fprintf(stdout, "---- UAV Pilot Blog Version 1.0 ----\n");
    fprintf(stdout, "1. List Blog\n");
    fprintf(stdout, "2. Write Blog\n");
    fprintf(stdout, "3. Read Blog\n");
    fprintf(stdout, "4. Exit\n");
    fprintf(stdout, "------------------------------------\n");
    fprintf(stdout, "Your choice: ");
    fflush(stdout);
    scanf("%d", &i);
    getchar();
    return i;
}
int check_vaild(char c)
{
    if(((c>=97)&&(c<=122))||((c>=65)&&(c<=90))||(c==32)||(c==46)||((c>=48)&&(c<=57))||(c==0)||(c==10))
    {
        return 1;
    }
    else
    {
        return 0;
    }
}
void write_blog()
{
    int flag;
    char c;
    FILE *fp;
    char filename[255];
    char content[1024] = {0};
    flag = 1;
    time_t now;
    time(&now);
    int i;
    i = 0;
    fprintf(stdout, "Please input blog content: \n");
    fflush(stdout);
    while(1)
    {
        c = getchar();
        if((c==0)||(i>=1022)||(flag != 1))
        {
            break;
        }
        if(check_vaild(c))
        {
            content[i] = c;
        }else{
            exit(0);
        }
        i += 1;
    }
    content[i+1] = 0;
    sprintf(filename, "%ld.em", now);
    // printf("filename : %s\n", filename);
    fp = fopen(filename, "a+");
    if (fp == NULL)
    {
        fprintf(stdout, "Open file error!\n");
        fprintf(stdout, "Bye\n");
        fflush(stdout);
        exit(0);
    }
    fprintf(fp, "%s", content);
    fclose(fp);
    fp = fopen("bloglist.txt", "a+");
    fprintf(fp, "%s\n", filename);
    fclose(fp);
}
void read_blog()
{
    char filename[255] = {0};
    char content[2048];
    char c;
    int flag;
    flag = 1;
    FILE *fp;
    int i;
    i = 0;
    fprintf(stdout, "Please input blog name: \n");
    fflush(stdout);
    while(1)
    {
        c = getchar();
        if((c==10)||(i>=200)||(flag != 1))
        {
            break;
        }
        if(check_vaild(c))
        {
            filename[i] = c;
        }else{
            exit(0);
        }
        i += 1;
    }
    filename[i+1] = 0;
    if(list_blog(filename))
    {
        fp = fopen(filename, "r");
        if (fp == NULL)
        {
            fprintf(stdout, "Open file error!\n");
            fprintf(stdout, "Bye\n");
            fflush(stdout);
            exit(0);
        }
        int count = 0;
        while (!feof(fp))
        {
            c = fgetc(fp);
            content[count] = c;
            count += 1;
        }
        content[count] = 0;
        fclose(fp);
        fprintf(stdout, content);
        fflush(stdout);
        fprintf(stdout, "\n");
        fflush(stdout);
    }
    else
    {
        fprintf(stdout, "Blog not exist!\n");
        fprintf(stdout, "Bye!\n");
        fflush(stdout);
    }
}
int list_blog(char *s)
{
    FILE *fp;
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    fp = fopen("bloglist.txt", "r");
    if (fp == NULL)
    {
        fprintf(stdout, "Open file error!\n");
        fprintf(stdout, "Bye\n");
        fflush(stdout);
        exit(0);
    }
    int cmp, flag;
    cmp = strcmp("main", s);
    flag = 0;
    char tmp_str[20];
    memset(tmp_str,0,20);
    if(cmp == 0)
    {
        fprintf(stdout, "----- Blog List -----\n");
        fflush(stdout);
    }
    while ((read = getline(&line, &len, fp)) != -1) 
    {
        if(cmp == 0)
        {
            fprintf(stdout, "%s", line);
            fflush(stdout);
        }
        else
        {
            strncpy(tmp_str, line, 13);
            if(!strcmp(tmp_str, s))
            {
                flag = 1;
                return 1;
            }
        }
    }
    if(cmp == 0)
    {
        fprintf(stdout, "---------------------\n");
        fflush(stdout);
    }
    fclose(fp);
    return 0;
}
int main()
{
    int choice;
    while(1)
    {
        choice = menu();    
        switch(choice)
        {
            case 1:
                list_blog("main");
                break;
            case 2:
                write_blog();
                break;
            case 3:
                read_blog();
                break;
            case 4:
                return 0;
        }
    }
    return 0;
}
