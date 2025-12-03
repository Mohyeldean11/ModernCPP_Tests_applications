#include "Account_class.hpp"
class Saving : public Account{

    float mInterest ; 
public:
        Saving(const std::string &mName ,float balance , float interest);
        ~Saving();
        void Accumelate_interesteRate() override;
        float Getinterestrate()const override;

};