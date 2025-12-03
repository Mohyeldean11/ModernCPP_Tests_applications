#include <iostream>
#include <stdlib.h>
#include <limits>
#include <memory>
#include <vector>
#include <random>
class test
{
private:
    /* data */
public:
    test(/* args */);
    ~test();
};

test::test(/* args */)
{
    std::cout<<"data is accuired"<<std::endl;
}

test::~test()
{
    std::cout<<"data is released"<<std::endl;
}

void processRecords(long long count)
{
    // test *t1 = new test;
    std::unique_ptr<test> t1(new test);

    // int *ptr = (int*)malloc(count * sizeof(int));
    //  if(count <10)
    //      throw std::out_of_range("count should be greater than 10");
    // 
    // int *ptr = new  int[count];
    std::vector<int> p;
    int errors{};
    p.reserve(count);
    std::default_random_engine eng;
    std::bernoulli_distribution ber;
    for(int i=0 ; i<count;i++)
    {
        try
        {
            p.push_back(i);
            std::cout<<"processing process #"<<i<<" "<<std::endl;
            if(!ber(eng))
            {
                ++errors;
                throw std::runtime_error("too many error");
            }
        }
        catch(std::runtime_error &ex)
        {
            std::cout<<"[ERROR ]" <<ex.what()<<"]"<<std::endl;
            if(errors>4)
            {
                std::runtime_error err("Too many errors");
                ex = err ;
                throw;
            }
        }


    }
    // if(ptr == NULL)
    // {
    //     throw std::runtime_error("failed to initialize");
    // }
    // for(int i = 0 ; i< count ; i++)
    // {
    //     std::cout<<ptr[i]<<"\n";

    // }


}

int main()
{
    try
    {
        // processRecords(std::numeric_limits<long long>::max());
        // processRecords(5);
        processRecords(10);
    }
    // catch(const std::runtime_error &e)
    // {
    //     std::cout<<e.what()<<std::endl;
    // }
    catch(const std::exception &e)
    {
        std::cout<<e.what()<<std::endl;
    }
    
}