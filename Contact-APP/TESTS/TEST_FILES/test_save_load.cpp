#include "./../../CLASSES/Contact_store_Class/Contact_store_class.hpp"
#include "./../../CLASSES/Contact_Class/Contacts.hpp"
#include <iostream>
#include <filesystem>

// Simple test for Save_all_contacts() and Load_all_contacts()
// Behavior:
// 1) Ensure the phonebook directory exists (the code uses a hard-coded path)
// 2) Create a Contact_store_class and add a few contacts
// 3) Call Save_all_contacts()
// 4) Create a fresh Contact_store_class and call Load_all_contacts()
// 5) Call DisplayAll() to print loaded contacts to the terminal

int main()
{
    namespace fs = std::filesystem;

    // NOTE: Contact_store_class.cpp uses a hard-coded path:
    //   "./Contact-APP/utilities/Phonebook.csv"
    // The test will create the parent directory used by that path so
    // Save_all_contacts() can create/write the file.
    fs::path phonebook_dir{"./Contact-APP/utilities"};

    if(!fs::exists(phonebook_dir)) {
        std::cout << "Creating directory: " << phonebook_dir << std::endl;
        try {
            fs::create_directories(phonebook_dir);
        } catch(const std::exception &e) {
            std::cerr << "Failed to create directory '" << phonebook_dir << "': " << e.what() << std::endl;
            return 1;
        }
    }

    std::cout << "\n-- Creating store and adding contacts --\n";
    Contact_store_class writerStore;
    writerStore.Add_contact(Contacts("Alice", "Smith", "0101010101", "CompanyA", Contactgroup::FRIENDS));
    writerStore.Add_contact(Contacts("Bob", "Jones", "0111111111", "CompanyB", Contactgroup::COWORKERS));
    writerStore.Add_contact(Contacts("Carol", "White", "0122222222")); // defaults

    std::cout << "\nSaving contacts to CSV...\n";
    writerStore.Save_all_contacts();

    std::cout << "\n-- Creating new store and loading from CSV --\n";
    Contact_store_class readerStore;
    readerStore.Load_all_contacts();

    std::cout << "\nDisplaying loaded contacts:\n";
    readerStore.DisplayAll();

    std::cout << "\nTest complete. Please inspect the CSV file at the path used by the project.\n";
    return 0;
}
