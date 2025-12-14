#include "UI_Class.hpp"
#include "memory"


std::string MainMenu = "\n1.Display Menu\n2.Contacts Managements\n3.use another PhoneBook\n4.Exit\n";
std::string DisplayMenu = "\n1.Display All contacts\n2.Display by group\n3.Display by names(First<->Last)\n4.Main Menu\n5.Exit\n";
std::string ContactsManagMenu = "\n1.Add Contact\n2.Remove Contact\n3.Search for a Contact\n4.Main Menu\n5.Exit\n";


UI_Class::UI_Class()
{
}

UI_Class::~UI_Class()
{
}


void UI_Class::Operate()
{
    MainContactOBJ.Load_all_contacts();
    while(true)
    {
        Preview_Menu(std::move(UI_Class::GetMenuInput()));
    }
    MainContactOBJ.Save_all_contacts();
}
void  UI_Class::Preview_Menu(const MainMenuOptions &&chosedMenu)
{

    switch (chosedMenu)
    {
    case MainMenuOptions::DisplayMenu:
        std::cout<<DisplayMenu;
            Display_Menu(std::move(GetDisplayMenuInput()));
            break;
    case MainMenuOptions::ContactsManagMenu:
        Contact_Menu();
        break;
    case MainMenuOptions::AnotherDB:
        std::cout<<"Coming in future....\n";
        Preview_Menu(std::move(UI_Class::GetMenuInput()));
        break;
    case MainMenuOptions::Exit:
        MainContactOBJ.Save_all_contacts();
        exit(1);
        break;
    default :
        std::cout<<"Wrong Input\n";
        std::cout<<MainMenu;
        break;
    }
}

MainMenuOptions UI_Class::GetMenuInput()
{
    int input = 0 ; 
    std::cout<<MainMenu;
    std::cout<<"Please Enter Your Choice: (from 1 <---> 4) : ";
    std::cin>> input;
    int tryouts{0};
    while(input >4 || input <1)
    {
        std::cout<<"Please Enter a valid option : (from 1 <---> 4) : ";
        try
        {
            std::cin>> input;
            ++tryouts;
        }
        catch(const std::exception& e)
        {
            std::cerr<<e.what()<<std::endl;
            exit(0);
        }
        if(tryouts> 5)
        {
            std::cout << "too much failed trials... exiting :)"<< '\n';
            throw;
        }
        
    }

    return static_cast<MainMenuOptions>(input);

}
DisplayMenuOptions UI_Class::GetDisplayMenuInput()
{
    int input = 0 ; 
    std::cout<<"Please Enter Your Choice: (from 1 <---> 5) : ";
    std::cin>> input;
    int tryouts{0};
    while(input >5 || input <1)
    {
        std::cout<<"Please Enter a valid option : (from 1 <---> 5) : ";
        try
        {
            std::cin>> input;
            ++tryouts;
        }
        catch(const std::exception& e)
        {
            std::cerr<<e.what()<<std::endl;
            exit(0);
        }
        if(tryouts> 5)
        {
            std::cout << "too much failed trials... exiting :)"<< '\n';
            throw;
        }
        
    }
    return static_cast<DisplayMenuOptions>(input);  
}

ContactMenuOptions UI_Class::GetContactMenuInput()
{
    int input = 0 ; 
    std::cout<<"Please Enter Your Choice: (from 1 <---> 5) : ";
    std::cin>> input;
    int tryouts{0};
    while(input >5 || input <1)
    {
        std::cout<<"Please Enter a valid option : (from 1 <---> 5) : ";
        try
        {
            std::cin>> input;
            ++tryouts;
        }
        catch(const std::exception& e)
        {
            std::cerr<<e.what()<<std::endl;
            exit(0);
        }
        if(tryouts> 5)
        {
            std::cout << "too much failed trials... exiting :)"<< '\n';
            throw;
        }
        
    }
    return static_cast<ContactMenuOptions>(input);  
}


void UI_Class::Display_Menu(const DisplayMenuOptions &&movedOption)
{
    std::string Name;
    bool Flag= false;
   switch (movedOption)
   {
    case DisplayMenuOptions::DisplayAll:
        MainContactOBJ.DisplayAll();
        break;
    case DisplayMenuOptions::Displaybygroup:
    {
        int Input =0;
        std::cout<<"Please enter the group name : \n";
        std::cin>> Input;
        if(Input<0 || Input > 3)
        {
            Input = 0;
        }
        MainContactOBJ.DisplayByGroup(std::move(static_cast<Contactgroup>(Input)));
        break;
    }
    case DisplayMenuOptions::DisplayByname:
    {        
        
        std::cout<<"How Do you want to search for the contact : \n 0.First Name\n1.Last Name\n";
        std::cin>>Flag; 
        std::cout<<"Please Enter the name you want to search\n";
        std::cin>>Name;
        Contacts* foundContact = MainContactOBJ.Search_by_Name(Name, Flag);
        if (foundContact != nullptr) {
            std::cout<<"\nFirst Name : "<< foundContact->Get_FirstName() 
                     <<"\nLast Name : "<< foundContact->Get_LastName()
                     <<"\nPhone Number : "<< foundContact->Get_Phone_Number()
                     <<"\nCompany name : "<< foundContact->Get_Company()
                     <<"\nGroup : "<< static_cast<int>(foundContact->Get_Group()) << '\n';
        } else {
            std::cout << "\nContact not found!\n";
        }
        break;
    }
    case DisplayMenuOptions::MainMenu:
        std::cout<<"Main Menu Loading....\n";
        Preview_Menu(std::move(UI_Class::GetMenuInput()));
        break;
    case DisplayMenuOptions::Exit:
        MainContactOBJ.Save_all_contacts();
        exit(0);
        break;

   default:
        break;
   }
   std::cout<<DisplayMenu<<std::endl;
   Display_Menu(std::move(GetDisplayMenuInput()));
}

void UI_Class::Contact_Menu()
{
    std::cout << ContactsManagMenu;
    ContactMenuOptions choice = GetContactMenuInput();
    
    switch (choice)
    {
    case ContactMenuOptions::AddContact:
    {
        std::string firstName, lastName, phone, company;
        int groupChoice;
        
        std::cout << "Enter First Name: ";
        std::cin >> firstName;
        std::cout << "Enter Last Name: ";
        std::cin >> lastName;
        std::cout << "Enter Phone Number: ";
        std::cin >> phone;
        std::cout << "Enter Company (or 'NA'): ";
        std::cin >> company;
        std::cout << "Enter Group (0=DEFAULT, 1=COWORKERS, 2=FAMILY, 3=FRIENDS): ";
        std::cin >> groupChoice;
        
        if (groupChoice < 0 || groupChoice > 3) {
            groupChoice = 0; // Default
        }
        
        MainContactOBJ.Add_contact(Contacts(firstName, lastName, phone, company, 
                                          static_cast<Contactgroup>(groupChoice)));
        break;
    }
    case ContactMenuOptions::RemoveContact:
    {
        std::string name;
        bool byLastName;
        
        std::cout << "Remove by (0=First Name, 1=Last Name): ";
        std::cin >> byLastName;
        std::cout << "Enter name to remove: ";
        std::cin >> name;
        
        MainContactOBJ.Remove_by_Name(name, byLastName);
        break;
    }
    case ContactMenuOptions::SearchContact:
    {
        std::string name;
        bool byLastName;
        
        std::cout << "Search by (0=First Name, 1=Last Name): ";
        std::cin >> byLastName;
        std::cout << "Enter name to search: ";
        std::cin >> name;
        
        Contacts* foundContact = MainContactOBJ.Search_by_Name(name, byLastName);
        if (foundContact != nullptr) {
            std::cout << "\nContact Found:\n";
            std::cout << "First Name : " << foundContact->Get_FirstName() << "\n";
            std::cout << "Last Name : " << foundContact->Get_LastName() << "\n";
            std::cout << "Phone Number : " << foundContact->Get_Phone_Number() << "\n";
            std::cout << "Company : " << foundContact->Get_Company() << "\n";
            std::cout << "Group : " << static_cast<int>(foundContact->Get_Group()) << "\n";
        } else {
            std::cout << "\nContact not found!\n";
        }
        break;
    }
    case ContactMenuOptions::MainMenu:

        std::cout << "Returning to Main Menu...\n";
        Preview_Menu(std::move(UI_Class::GetMenuInput()));
        return; // Don't continue to Contact_Menu again
    case ContactMenuOptions::Exit:
        MainContactOBJ.Save_all_contacts();
        exit(0);
    default:
        std::cout << "Invalid choice!\n";
        break;
    }
    
    // After handling the choice, show the menu again
    Contact_Menu();
}
void UI_Class::Another_DB()
{
    std::string dbPath;
    std::cout << "Enter the path to the new phonebook file: ";
    std::cin >> dbPath;
    
    // Note: This is a simplified implementation
    // In a real application, you might want to create a new Contact_store_class
    // instance with a different file path, or implement a way to switch databases
    
    std::cout << "Loading database from: " << dbPath << "\n";
    std::cout << "Note: This feature is not fully implemented yet.\n";
    std::cout << "Currently, the application uses a fixed database path.\n";
    std::cout << "Returning to main menu...\n";
    
    Preview_Menu(std::move(UI_Class::GetMenuInput()));
}

