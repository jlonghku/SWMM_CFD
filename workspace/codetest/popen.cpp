#include <stdio.h> 
#include <iostream>
int main(int argc, char *argv[])
{ 
    FILE *fp; 
    char buffer[280]; 
    

    fp=popen("ls -a", "r"); 
    while(fgets(buffer,sizeof(buffer),fp)){ 
    printf("%s",buffer);}
    return 0;
}
