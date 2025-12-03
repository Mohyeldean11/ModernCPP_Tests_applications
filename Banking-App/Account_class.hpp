#include <iostream>
#include <string>
#pragma once

class Account
{
private:
    std::string mName ;
    int mAccnum ; 
protected:
    float mBalance;

public:
    Account(std::string Accname ,float initBalance);
    virtual ~Account();
    const std::string Getname()const;
    float GetBalance()const;
    int GetAccountnum()const;
    void Withdraw(float amount);
    void Deposit(float amount);
    virtual float Getinterestrate()const ;
    virtual void Accumelate_interesteRate();

};

