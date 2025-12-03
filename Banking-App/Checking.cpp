#include "Checking.hpp"

// Checking::Checking(const std::string &accname , float balance):Account(accname ,balance)
// {

// }
void Checking::Withdraw(float amount)
{
    if((mBalance-amount) > 50)
    {
        Account::Withdraw(amount);
    }
    else
    {
        std::cout<<"no sufficient amount "<<std::endl;
    }
}
Checking::~Checking()
{
    
}