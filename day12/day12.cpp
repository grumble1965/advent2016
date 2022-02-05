#include <iostream>
#include "day12.h"

int main()
{
    std::cout << "Hello World!\n";

    long a, b, c, d;
    a = b = c = d = 0;

    program(a, b, c, d);
    std::cout << "Registar a = " << a << "\n";

    a = b = d = 0;
    c = 1;
    program(a, b, c, d);
    std::cout << "Registar a = " << a << "\n";

    return 0;
}

void program(long& a, long& b, long& c, long& d)
{
    a = 1;
    b = 1;
    d = 26;
    if (c != 0) {
        d = 33;
        c = 0;
    }
    do {
        c = a;
        a += b;
        b = c;
        d--;
    } while (d != 0);
    a += 198;
}
