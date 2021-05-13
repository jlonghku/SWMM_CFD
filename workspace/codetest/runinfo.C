#include "runinfo.H"

std::vector<std::string> split(std::string a, std::string b)
{
  std::vector<std::string> result;
  std::string::size_type i = 0;
  std::string::size_type found = a.find(b);
  while (found != std::string::npos)
  {
    result.push_back(a.substr(i, found - i));
    i = found + b.size();
    found = a.find(b, i);
  }
  result.push_back(a.substr(i, a.size() - i));
  return result;
}

runinfo::runinfo(int argc, char **argv)
{
  int i = 0;
  while (i < argc)
  {
    if (!strncmp(argv[i], "--", 2))
    {
      options.push_back(argv[i] + 2);
      std::string strr;
      strr.insert(0, argv[0]);
      strr.insert(strr.length(), " ");
      strr.insert(strr.length(), argv[i + 1]);
      str.push_back(strr);
    }
    i++;
  }
}
int runinfo::getinfo(std::string option)
{
  int i = 0;
  while (i < str.size())
  {
    if (option == options[i])
    {
      argvs.clear();
      argvc.clear();
      argvs = split(str[i], " ");

      //convert to char**
      int j = 0;
      while (j < argvs.size())
      {
        argvc.push_back(&argvs[j][0]);
        j++;
      }
      argcc = argvc.size();
      argvv = &argvc[0];
      return 1;
    }
    i++;
  }
  return 0;
}
