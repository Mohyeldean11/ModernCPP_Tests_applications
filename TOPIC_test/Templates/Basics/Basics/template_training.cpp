#include <iostream>
#include <cmath>
#include <unordered_map>
// int Add(int x,int y) ; //Return the sum of two elements
// int ArraySum(const int *pArr, size_t arrSize); //Returns the sum of array elements
using namespace std;

template <typename T>
T ArraySum(const T *pArr, size_t arrSize)
{
    T sum = 0;
    for (auto i=0 ;i <arrSize ; i++)
    {
        sum += pArr[i];
    }
    return sum;
}

template<typename T> 
T Add(T x , T y)
{
    return x+y;
}

int main()
{
    // Create a dynamic array using new. Example: allocate 5 ints.
    size_t n = 5;
    int *ptr = new int[n];
    for (size_t i = 0; i < n; ++i)
        ptr[i] = static_cast<int>(i) + 1; // fill the array with 1..5

    auto x{3.4}, y{33.223};
    std::cout << "Add(x,y) = " << Add(x,y) << std::endl;
    std::cout << "ArraySum(ptr, n) = " << ArraySum(ptr, n) << std::endl;

    // Free the dynamically allocated array
    delete [] ptr;

    return 0;
}