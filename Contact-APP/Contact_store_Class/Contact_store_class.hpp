#include "./../Contact_Class/Contacts.hpp"
#include <vector>
#include <algorithm>

class Contact_store_class
{
private:
    /* vector for storing contacts in it */
    std::vector<Contacts> Contact_Book{0};
public:
    //constructors
    Contact_store_class();
    ~Contact_store_class();

        /***methods***/
    // contacts management
    void Add_contact(Contacts &&contact);
    void Remove_by_Name(const std::string &name , bool WhichName);
    Contacts* Search_by_Name(const std::string &name , bool WhichName);

    // Display phonebook
    void DisplayAll() const;
    void DisplayByGroup(Contactgroup group) const;

    //sort Contacts
    void Sort_By_A_D_Name(bool orderFlag);
};

