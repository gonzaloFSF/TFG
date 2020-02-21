#include <stdio.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>


int main(){

int i;
int j;
int a;
int fd;
char buf[2000];

a = 0;


for(i = 0; i < 100000; i++){
    a++;
}


printf("hola que tal\n");
getgid();
fd = open("/etc/passwd",O_RDONLY);
read(fd,buf,1000);
system("ls");
printf("hola que tal\n");
printf("hola que tal\n");
printf("hola que tal\n");
printf("hola que tal\n");
printf("hola que tal\n");

}