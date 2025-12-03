#include "Integer_m.hpp"

int main()
{
    // Test default constructor
    Integer a;
    std::cout << "Default constructor: a = " << a << std::endl;

    // Test parameterized constructor
    Integer b(10);
    std::cout << "Parameterized constructor: b = " << b << std::endl;

    // Test copy constructor
    Integer c(b);
    std::cout << "Copy constructor: c = " << c << std::endl;

    // Test move constructor
    Integer d(std::move(b));
    std::cout << "Move constructor: d = " << d << std::endl;

    // Test getter and setter
    c.Set_value(20);
    std::cout << "Set_value: c = " << c << std::endl;
    std::cout << "Get_value: c = " << c.Get_value() << std::endl;

    // Test operator+
    Integer e = a + c;
    std::cout << "operator+: e = a + c = " << e << std::endl;

    // Test operator-(subtraction)
    Integer f = c - a;
    std::cout << "operator-: f = c - a = " << f << std::endl;

    // Test pre-increment
    ++c;
    std::cout << "Pre-increment: ++c = " << c << std::endl;

    // Test operator==
    std::cout << "operator==: (a == c) = " << (a == c) << std::endl;

    // Test copy assignment
    a = c;
    std::cout << "Copy assignment: a = c = " << a << std::endl;

    // Test move assignment
    a = std::move(d);
    std::cout << "Move assignment: a = std::move(d) = " << a << std::endl;

    // Test friend operator<< (already used above)

    // Test global operator+ (int + Integer)
    Integer g = 5 + c;
    std::cout << "Global operator+: g = 5 + c = " << g << std::endl;

    // Test operator>> (input)
    std::cout << "Enter value for h: ";
    Integer h;
    std::cin >> h;
    std::cout << "You entered: h = " << h << std::endl;

    return 0;
}