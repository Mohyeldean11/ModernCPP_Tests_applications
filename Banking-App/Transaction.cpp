#include "Transaction.hpp"

void Transact(Account *pAccount)
{
    std::cout << "Transaction started..."<<std::endl;
    std::cout << "Initial balance : " << pAccount->GetBalance() <<std::endl;
    pAccount->Deposit(100);
    pAccount->Accumelate_interesteRate();
    pAccount->Withdraw(170);
    std::cout << "the interest rate : " << pAccount->Getinterestrate()<<std::endl;
    std::cout << "the balance now : "<< pAccount->GetBalance()<<std::endl;
}