#include <thread>
#include <cstdlib>
#include <iostream>
#include <chrono>
#include <exception>
#include <csignal>

using namespace std;

void sigFunc(int signal)
{
    cout << "signal SIGABRT" << endl;
}

int main()
{
    signal(SIGABRT, sigFunc);

    thread t1([]()
              {
                  int cnt = 20;
                  while (cnt-- > 0)
                  {
                      cout << "cnt=" << cnt << endl;
                      this_thread::sleep_for(std::chrono::seconds(1));
                  }
              });

    thread t2([]()
              {
                  this_thread::sleep_for(std::chrono::seconds(2));
                  cout << "t2 abort" << endl;
                  try
                  {
                      abort();
                  }
                  catch (exception &e)
                  {
                  }
              });

    if (t1.joinable())
        t1.join();
    if (t2.joinable())
        t2.join();

    return 1;
}