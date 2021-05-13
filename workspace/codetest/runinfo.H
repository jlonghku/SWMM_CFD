#ifndef runinfo_H
#define runinfo_H

#include <iostream>
#include <string>
#include <cstring>
#include <vector>

std::vector<std::string> split(std::string a, std::string b);

class runinfo
{
public:
  std::vector<std::string> options;
  std::vector<std::string> str;
  int argcc;
  std::vector<std::string> argvs;
  std::vector<char *> argvc;
  char **argvv;

  //constructor
  runinfo(int a, char **b);
  ~runinfo(){};
  int getinfo(std::string option);
};
#endif
