#include "Contact_store_class.hpp"
#include <sstream>
#include <filesystem>
#include <fstream>

namespace fs = std::filesystem;
const fs::path phonebook{std::move("./Contact-APP/utilities/Phonebook.csv")} ;


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

void Contact_store_class::DisplayByGroup(Contactgroup group) const
{
    std::cout << "==============================\n";
    std::cout << "Contacts in Group " << static_cast<int>(group) << ":\n";
    for (const auto &contact : Contact_Book)
    {
        if (contact.Get_Group() == group)
        {
            contact.Print_ContactData();
        }
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



void Contact_store_class::Load_all_contacts()
{
    try
    {
        if(!(fs::exists(phonebook)))
        {
            std::cout << "file is not availabe \n Creating a new file" << std::endl;
            std::ofstream file{phonebook};
            std::cout<<"file created"<<std::endl;
            if(!(file.is_open()))
                throw;
            file.close();
        }
        else
        {
            //do nothing
        }
    }
    catch(const std::exception& e)
    {
        std::cerr << e.what() << "the file is not existing, can't be created at the moment " << '\n';
    }
    std::ifstream File{phonebook};
    try
    {
        if(!File)
        {
            throw;
        }
    }
    catch(const std::exception& e)
    {
        std::cerr << "the file can't be loaded"<< e.what() << '\n';
    }
    std::string streamLine;
    while (std::getline(File,streamLine))
    {
        Contacts Temp_contact;
        std::stringstream ss(streamLine);
        std::string token;
        uint8_t count{0};
        while(std::getline(ss,token,','))
        {
            ++count;
            switch (count)
            {
            case 1:
                Temp_contact.SET_FirstName(token);
                break;
            case 2:
                Temp_contact.SET_LastName(token);
                break;
            case 3:
                Temp_contact.SET_Phone_Number(token);
                break;
            case 4:
                Temp_contact.SET_Company(token);
                break;
            case 5:
                Temp_contact.SET_Group(token);
                break;
            default:
                break;
            }
        }
        Contact_Book.push_back(Temp_contact);
        count = 0;
    }
    
    
    
}
void Contact_store_class::Save_all_contacts()
{
    //std::ios::app seek and search for the next blank area to write
    std::ofstream File(phonebook);
    try
    {
        if(!File)
        {
            throw;
        }
    }
    catch(const std::exception& e)
    {
        std::cerr << "the file can't be loaded"<< e.what() << '\n';
    }
    for(const auto &contact : Contact_Book)
    {
        File <<'\n';
        File<< contact.Get_FirstName();
        File <<',';
        File<< contact.Get_LastName();
        File <<',';
        File<< contact.Get_Phone_Number();
        File <<',';
        File<< contact.Get_Company();
        File <<',';
        File<< static_cast<int>(contact.Get_Group());
    }
    std::cout<<"file " <<phonebook<<  " is saved"<<std::endl;
}