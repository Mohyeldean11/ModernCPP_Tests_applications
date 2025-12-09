#include "./../../CLASSES/Contact_Class/Contacts.hpp"
#include <iostream>
#include <vector>
#include <algorithm>

void TestBasicConstruction() {
    std::cout << "\n==== TestBasicConstruction ====\n";
    Contacts c1("Mohamed", "Badawy", "0100000000", "Bosch", Contactgroup::COWORKERS);
    std::cout << c1.Get_FirstName() << " "
              << c1.Get_LastName() << " "
              << c1.Get_Phone_Number() << " "
              << c1.Get_Company() << " "
              << static_cast<int>(c1.Get_Group()) << std::endl;
}

void TestDefaultParameters() {
    std::cout << "\n==== TestDefaultParameters ====\n";
    Contacts c2("Sara", "Ali", "0123456789");
    std::cout << c2.Get_FirstName() << " "
              << c2.Get_LastName() << " "
              << c2.Get_Phone_Number() << " "
              << c2.Get_Company() << " "
              << static_cast<int>(c2.Get_Group()) << std::endl;
}

void TestSorting() {
    std::cout << "\n==== TestSorting ====\n";
    std::vector<Contacts> contacts = {
        Contacts("Ziad","Kamal","0150000000"),
        Contacts("Ahmed","Sami","0110001111"),
        Contacts("Laila","Hassan","0102222222"),
        Contacts("Bassem","George","0103333333")
    };

    std::sort(contacts.begin(), contacts.end());

    for (const auto& c : contacts) {
        std::cout << c.Get_FirstName() << std::endl;
    }
}

void TestEdgeCases() {
    std::cout << "\n==== TestEdgeCases ====\n";

    // Empty last name
    Contacts c3("Omar", "", "0177777777");
    std::cout << c3.Get_FirstName() << " | " << c3.Get_LastName() << std::endl;

    // Empty phone number
    Contacts c4("Hana", "Mostafa", "", "Apple", Contactgroup::FRIENDS);
    std::cout << c4.Get_FirstName() << " | " << c4.Get_Phone_Number() << std::endl;

    // Empty first name (should still work but may affect sorting)
    Contacts c5("", "Something", "0999999999");
    std::cout << "First name empty: '" << c5.Get_FirstName() << "'" << std::endl;
}

int main_not_used() {
    TestBasicConstruction();
    TestDefaultParameters();
    TestSorting();
    TestEdgeCases();
    return 0;
}
