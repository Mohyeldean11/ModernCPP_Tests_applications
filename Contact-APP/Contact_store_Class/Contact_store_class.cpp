#include "Contact_store_class.hpp"


Contact_store_class::Contact_store_class()
{
    //do nothing
}

Contact_store_class::~Contact_store_class()
{
    //do nothing
}

/*Contact Add*/
void Contact_store_class::Add_contact(Contacts &&contact)
{
    Contact_Book.push_back(std::move(contact));
    std::cout<<"Contact has been added..."<<std::endl;
}
void Contact_store_class::Remove_by_Name(const std::string &name,bool WhichName)
{
    auto itr = std::find_if(Contact_Book.begin(), Contact_Book.end(), [&](const Contacts &contact)
    {
        if(WhichName == false)
        {
            return  (contact.Get_FirstName() == name);
        }
        else
        {
            return  (contact.Get_LastName() == name);
        }
    });

    if( itr != Contact_Book.end())
    {
        Contact_Book.erase(itr);
        std::cout<<"Contact was deleted.."<<std::endl;
    }
    else
    {
        std::cout<<"This name was not found in your contact book..."<<std::endl;
    }
}

Contacts* Contact_store_class::Search_by_Name(const std::string &name,bool WhichName)
{
    auto itr = std::find_if(Contact_Book.begin(), Contact_Book.end(), [&](const Contacts &contact)
    {
        if(WhichName == false)
        {
            return  (contact.Get_FirstName() == name);
        }
        else
        {
            return  (contact.Get_LastName() == name);
        }
    });

    if(itr != Contact_Book.end())
    {
        return &(*itr);
    }
    else
    {
        //returning null pointer
        return nullptr;
    }

}


void Contact_store_class::DisplayAll()const
{
    std::cout << "==============================\n";
    for( const auto &x : Contact_Book)
    {
        x.Print_ContactData();
    }
    std::cout << "==============================\n";

}
void Contact_store_class::Sort_By_A_D_Name(bool orderFlag)
{
    if(orderFlag)
    {
        std::sort(Contact_Book.begin(),Contact_Book.end());
    }
    else
    {
        std::sort(Contact_Book.begin(),Contact_Book.end(),[](const Contacts &a ,const Contacts &b )
        {
            return (b < a);
        });
    }
    DisplayAll();
}