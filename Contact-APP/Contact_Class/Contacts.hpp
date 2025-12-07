#include <iostream>
#include <string>
enum class Contactgroup {DEFAULT=0,COWORKERS,FAMILY,FRIENDS};
class Contacts
{
private:
    /* data */
    std::string Firstname;
    std::string Lastname;    
    std::string Primary_number;    
    std::string Company;
    Contactgroup Mygroup;
    

public:
    //constructors
    Contacts();
    Contacts(const std::string &first_name,
             const std::string &lastname,
             const std::string &phone_number,
             const std::string &company_name = "NA",
             Contactgroup group = Contactgroup::DEFAULT);
    ~Contacts();
    
    //getters
    std::string Get_FirstName()const;
    std::string Get_LastName()const;
    std::string Get_Phone_Number()const;
    std::string Get_Company()const;
    Contactgroup Get_Group()const;

    //viewer
    void Print_ContactData()const;
    //setters (for future imp if the contact are editable)


    //operator overloading
    bool operator <(const Contacts &obj)const;

};

