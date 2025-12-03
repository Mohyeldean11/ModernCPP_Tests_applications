#pragma once
#include "Account_class.hpp"

class Checking :public Account
{
public:
    using Account::Account;
    // Checking(const std::string &accname , float balance );
    ~Checking();
    void Withdraw(float amount);
};