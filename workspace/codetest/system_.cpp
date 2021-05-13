#include <stdlib.h>
#include <thread>
#include <csignal>
#include <iostream>
#include <sys>
void signalHandler( int signum )
{
    std::cout << "Interrupt signal (" << signum << ") received.\n";
    
   exit(signum);  
 
}
int main()
{
   signal(SIGINT, signalHandler);  
//std::thread t1(system,"cd /home/jlong/OFcase/cavity&&mpirun -np 8 icoFoam -parallel");
std::thread t2(system,"cd /home/jlong/OFcase/wave&&mpirun -np 8 interFoam -parallel");
 // system("cd /home/jlong/OFcase/cavity&&mpirun -np 6 icoFoam -parallel");
  //system("cd /home/jlong/OFcase/wave&& interFoam");
  //system("ls");
  //括号内是你的linux指令
  //std::thread t3(system,"cd /home/jlong/OFcase/wave&&mpirun -np 8 interFoam -parallel");
 // std::thread t4(popen,"cd /home/jlong/OFcase/wave&& interFoam ","r");
  //FILE* fp=popen("ls","r");
  std::thread t4(system,"ls");
  
  t2.join();
  t4.join();
  //t3.join();
  return 0;
}
