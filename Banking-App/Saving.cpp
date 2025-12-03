#include "Saving.hpp"


Saving::Saving(const std::string &mName , float balance ,float interest): Account(mName, balance),mInterest(interest)
{

}
float Saving::Getinterestrate()const
{
    return mInterest ; 
}
void Saving::Accumelate_interesteRate()
{
    mBalance += (mBalance *mInterest);
}
Saving::~Saving()
{

}