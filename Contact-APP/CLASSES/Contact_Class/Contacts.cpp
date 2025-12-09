#include "Contacts.hpp"


//constructors & Destructors

Contacts::Contacts()
{
    //do nothing
}
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

//getters
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

//setters
void Contacts::SET_FirstName(const std::string &var)
{
    this->Firstname = var;
}
void Contacts::SET_LastName(const std::string &var)
{
    this->Lastname = var;
}
void Contacts::SET_Phone_Number(const std::string &var)
{
    this->Primary_number = var;
}
void Contacts::SET_Company(const std::string &var)
{
    this->Company = var;
}
void Contacts::SET_Group(const std::string &var)
{
    this->Mygroup = static_cast<Contactgroup>(std::stoi(var));
}


//display
void Contacts::Print_ContactData()const
{
    std::cout<<"Name : " << this->Firstname<<" "<<this->Lastname << "\n" <<"Phone number : "<<this->Primary_number<<"\n"<<"Company : "<<this->Company<<"\n"<<std::endl;
}


//operator overloading
bool Contacts::operator<(const Contacts &obj)const
{
    return (Firstname < obj.Firstname);
}



