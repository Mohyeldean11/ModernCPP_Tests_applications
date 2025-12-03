#include "Account_class.hpp"
static int AccountRefnum = 1000;

Account::Account(std::string Accname ,float initBalance):mName(Accname),mBalance (initBalance)
{
    mAccnum = ++AccountRefnum;
}
Account::~Account()
{

}
const std::string Account::Getname()const
{
    return mName;
}

float Account::GetBalance()const
{
    return mBalance;
}
int Account::GetAccountnum()const
{
    return mAccnum;
}
void Account::Withdraw(float amount)
{
    if (amount < mBalance)
    {
        mBalance -= amount;
    }
    else
    {
        std::cout<<"no sufficient funds"<<std::endl;
    }
}

void Account::Deposit(float amount)
{
    mBalance += amount ;
}
void Account::Accumelate_interesteRate()
{

}
float Account::Getinterestrate()const
{
    return 0;
}
