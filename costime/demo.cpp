#include "costime.h"

#include <iostream>

double testfunc(const int& n)
{
    double sum = .0;
    for (int i = 0; i < n; i++)
    {
        sum += (i / 1.11);
    }
    return sum;
}

void testfunc1(const int& n)
{
    double sum = .0;
    for (int i = 0; i < n; i++)
    {
        sum += (i / 1.11);
    }
}

using namespace std;

int main()
{
    double cost = .0;
    int result = 0;
    std::tie(cost, result) = costTimeMs(testfunc, 10000);
    cout << cost << ", " << result << endl;
    std::tie(cost, std::ignore) = costTimeMs(testfunc, 10000);
    cout << cost << endl;
    cost = costTimeMs(testfunc1, 10000);
    cout << cost << endl;
}