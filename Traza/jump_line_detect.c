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
int p;
int fd;
char buf[2000];

a = 0;
p = 0;

for(i = 0; i < 100000; i++){

    /*if(a == 2434345545){
	p++;
    }
    
    if(a == 123343455){
	p++;
    }
    if(a == 4434343434){
	p++;
    }
    if(a == 34242323){
	p++;
    }
    if(a == 34545566){
	p++;
    }
    if(a == 354554545){
	p++;
    }
    if(a == 343442443){
	p++;    
    }
    if(a == 4454545){
	p++;
    }
    if(a == 1232344){
	p++;
    }
    if(a == 2343242){
	p++;
    }
    if(a == 123213213){
	p++;
    }
    if(a == 45645645){
	p++;
    }
    if(a == 342434){
	p++;
    }
    if(a == 12121212){
	p++;
    }
    if(a == 999999){
	p++;
    }
    if(a == 555555){
	p++;
    }
    if(a == 444444){
	p++;
    }
    if(a == 222222){
	p++;
    }
    if(a == 1111){
	p++;
    }
    if(a == 11111111){
	p++;
    }*/
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