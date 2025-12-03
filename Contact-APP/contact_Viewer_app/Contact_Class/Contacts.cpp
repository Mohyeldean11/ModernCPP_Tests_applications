#include "Contacts.hpp"


//constructors & Destructors
   Contacts::Contacts(const std::string &first_name,const std::string &lastname,const std::string &phone_number,const std::string &company_name,Contactgroup group):
            Firstname(first_name),
            Lastname (lastname),
            Primary_number(phone_number),
            Company(company_name),
            Mygroup(group)
{
    std::cout<<"paramterized constructor for contact object"<<std::endl;
}

Contacts::~Contacts()
{
    // std::cout<<"contact object is deleted"<<std::endl;
}

std::string Contacts::Get_FirstName()const
{
    return Firstname;
}
std::string Contacts::Get_LastName()const
{
    return Lastname;
}
std::string Contacts::Get_Phone_Number()const
{
    return Primary_number;
}
std::string Contacts::Get_Company()const
{
    return Company;
}
Contactgroup Contacts::Get_Group()const
{
    return Mygroup;
}


//operator overloading
bool Contacts::operator<(const Contacts &obj)const
{
    return (Firstname < obj.Firstname);
}