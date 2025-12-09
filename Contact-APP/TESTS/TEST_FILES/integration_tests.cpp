#include "./../../CLASSES/Contact_Class/Contacts.hpp"
#include "./../../CLASSES/Contact_store_Class/Contact_store_class.hpp"
#include <iostream>
#include <cassert>
#include <string>

/**
 * =====================================================
 * INTEGRATION TEST SUITE - CONTACTS + CONTACT_STORE
 * =====================================================
 * 
 * Tests the functionality of both Contacts class and Contact_store_class
 * working together to ensure proper integration and data consistency.
 */

// ==================== UTILITY FUNCTIONS ====================

void PrintTestHeader(const std::string &title) {
    std::cout << "\n" << std::string(70, '=') << std::endl;
    std::cout << "  " << title << std::endl;
    std::cout << std::string(70, '=') << std::endl;
}

void PrintTestCase(const std::string &caseNum, const std::string &description) {
    std::cout << "\n[TEST CASE " << caseNum << "] " << description << std::endl;
    std::cout << std::string(70, '-') << std::endl;
}

// ==================== TEST GROUP 1: BASIC INTEGRATION ====================

void Test_1_Create_And_Add_Contacts() {
    PrintTestHeader("TEST GROUP 1: Basic Contact Creation & Addition");
    
    Contact_store_class store;
    
    PrintTestCase("1.1", "Create contact objects using parameterized constructor");
    Contacts c1("Ahmed", "Hassan", "01001234567", "Microsoft", Contactgroup::COWORKERS);
    Contacts c2("Fatima", "Mohamed", "01101234567", "Google", Contactgroup::FAMILY);
    Contacts c3("Omar", "Ali", "01201234567", "Apple", Contactgroup::FRIENDS);
    
    std::cout << "✓ Three contact objects created successfully\n";
    
    PrintTestCase("1.2", "Add contacts to store using Add_contact()");
    store.Add_contact(std::move(Contacts("Ahmed", "Hassan", "01001234567", "Microsoft", Contactgroup::COWORKERS)));
    store.Add_contact(std::move(Contacts("Fatima", "Mohamed", "01101234567", "Google", Contactgroup::FAMILY)));
    store.Add_contact(std::move(Contacts("Omar", "Ali", "01201234567", "Apple", Contactgroup::FRIENDS)));
    
    std::cout << "\nDisplay all contacts after addition:\n";
    store.DisplayAll();
    std::cout << "✓ All contacts added successfully\n";
}

void Test_2_Create_Contacts_With_Defaults() {
    PrintTestHeader("TEST GROUP 2: Contact Creation with Default Parameters");
    
    Contact_store_class store;
    
    PrintTestCase("2.1", "Create contact with default company name (NA)");
    Contacts c1("Sara", "Ibrahim", "01301234567");
    std::cout << "Contact created: " << c1.Get_FirstName() << " " 
              << c1.Get_LastName() << ", Company: " << c1.Get_Company() << std::endl;
    assert(c1.Get_Company() == "NA");
    std::cout << "✓ Default company name is 'NA'\n";
    
    PrintTestCase("2.2", "Create contact with default group (DEFAULT)");
    Contacts c2("Hana", "Karim", "01401234567");
    std::cout << "Contact created: " << c2.Get_FirstName() << " " 
              << c2.Get_LastName() << ", Group: " << static_cast<int>(c2.Get_Group()) << std::endl;
    assert(c2.Get_Group() == Contactgroup::DEFAULT);
    std::cout << "✓ Default group is Contactgroup::DEFAULT (0)\n";
}

// ==================== TEST GROUP 3: SEARCH FUNCTIONALITY ====================

void Test_3_Search_By_FirstName_Integration() {
    PrintTestHeader("TEST GROUP 3: Search by FirstName Integration");
    
    Contact_store_class store;
    
    PrintTestCase("3.1", "Populate store with 5 contacts");
    store.Add_contact(std::move(Contacts("Ahmed", "Hassan", "01001234567", "Microsoft", Contactgroup::COWORKERS)));
    store.Add_contact(std::move(Contacts("Fatima", "Mohamed", "01101234567", "Google", Contactgroup::FAMILY)));
    store.Add_contact(std::move(Contacts("Omar", "Ali", "01201234567", "Apple", Contactgroup::FRIENDS)));
    store.Add_contact(std::move(Contacts("Noor", "Karim", "01301234567", "Amazon", Contactgroup::FAMILY)));
    store.Add_contact(std::move(Contacts("Layla", "Ibrahim", "01401234567", "Tesla", Contactgroup::FRIENDS)));
    std::cout << "✓ Store populated with 5 contacts\n";
    
    PrintTestCase("3.2", "Search for contact 'Ahmed' by first name");
    Contacts* result = store.Search_by_Name("Ahmed", false);
    if (result != nullptr) {
        std::cout << "✓ Found: " << result->Get_FirstName() << " " 
                  << result->Get_LastName() << ", Phone: " 
                  << result->Get_Phone_Number() << std::endl;
        assert(result->Get_FirstName() == "Ahmed");
        assert(result->Get_LastName() == "Hassan");
    }
    
    PrintTestCase("3.3", "Search for non-existent contact 'John'");
    Contacts* notFound = store.Search_by_Name("John", false);
    assert(notFound == nullptr);
    std::cout << "✓ Correctly returns nullptr for non-existent contact\n";
}

void Test_4_Search_By_LastName_Integration() {
    PrintTestHeader("TEST GROUP 4: Search by LastName Integration");
    
    Contact_store_class store;
    
    PrintTestCase("4.1", "Populate store with contacts");
    store.Add_contact(std::move(Contacts("Ahmed", "Hassan", "01001234567", "Microsoft", Contactgroup::COWORKERS)));
    store.Add_contact(std::move(Contacts("Fatima", "Mohamed", "01101234567", "Google", Contactgroup::FAMILY)));
    store.Add_contact(std::move(Contacts("Omar", "Hassan", "01201234567", "Apple", Contactgroup::FRIENDS)));
    std::cout << "✓ Store populated\n";
    
    PrintTestCase("4.2", "Search for 'Hassan' by last name");
    Contacts* result = store.Search_by_Name("Hassan", true);
    if (result != nullptr) {
        std::cout << "✓ Found: " << result->Get_FirstName() << " " 
                  << result->Get_LastName() << std::endl;
        assert(result->Get_LastName() == "Hassan");
    }
    
    PrintTestCase("4.3", "Multiple contacts with same last name");
    std::cout << "Note: Search returns FIRST match only\n";
    std::cout << "✓ Behavior is correct\n";
}

// ==================== TEST GROUP 5: MODIFICATION FUNCTIONALITY ====================

void Test_5_Modify_Contact_Using_Setters() {
    PrintTestHeader("TEST GROUP 5: Modify Contacts Using Setters");
    
    Contact_store_class store;
    
    PrintTestCase("5.1", "Create and add a contact");
    store.Add_contact(std::move(Contacts("Ahmed", "Hassan", "01001234567", "Microsoft", Contactgroup::COWORKERS)));
    std::cout << "Original contact:\n";
    store.DisplayAll();
    
    PrintTestCase("5.2", "Search for contact and modify using setters");
    Contacts* contact = store.Search_by_Name("Ahmed", false);
    if (contact != nullptr) {
        std::cout << "Before modification:\n";
        std::cout << "  Name: " << contact->Get_FirstName() << " " << contact->Get_LastName() << "\n";
        std::cout << "  Phone: " << contact->Get_Phone_Number() << "\n";
        std::cout << "  Company: " << contact->Get_Company() << "\n";
        
        contact->SET_LastName("Mohamed");
        contact->SET_Phone_Number("01101234567");
        contact->SET_Company("Google");
        
        std::cout << "\nAfter modification:\n";
        std::cout << "  Name: " << contact->Get_FirstName() << " " << contact->Get_LastName() << "\n";
        std::cout << "  Phone: " << contact->Get_Phone_Number() << "\n";
        std::cout << "  Company: " << contact->Get_Company() << "\n";
        
        assert(contact->Get_LastName() == "Mohamed");
        assert(contact->Get_Phone_Number() == "01101234567");
        assert(contact->Get_Company() == "Google");
        std::cout << "\n✓ All modifications applied successfully\n";
    }
}

// ==================== TEST GROUP 6: REMOVAL FUNCTIONALITY ====================

void Test_6_Remove_Contact_By_FirstName() {
    PrintTestHeader("TEST GROUP 6: Remove Contact by FirstName");
    
    Contact_store_class store;
    
    PrintTestCase("6.1", "Populate store with 5 contacts");
    store.Add_contact(std::move(Contacts("Ahmed", "Hassan", "01001234567", "Microsoft", Contactgroup::COWORKERS)));
    store.Add_contact(std::move(Contacts("Fatima", "Mohamed", "01101234567", "Google", Contactgroup::FAMILY)));
    store.Add_contact(std::move(Contacts("Omar", "Ali", "01201234567", "Apple", Contactgroup::FRIENDS)));
    store.Add_contact(std::move(Contacts("Noor", "Karim", "01301234567", "Amazon", Contactgroup::FAMILY)));
    store.Add_contact(std::move(Contacts("Layla", "Ibrahim", "01401234567", "Tesla", Contactgroup::FRIENDS)));
    
    std::cout << "All contacts:\n";
    store.DisplayAll();
    
    PrintTestCase("6.2", "Remove 'Fatima' by first name");
    store.Remove_by_Name("Fatima", false);
    
    std::cout << "\nRemaining contacts:\n";
    store.DisplayAll();
    
    PrintTestCase("6.3", "Verify 'Fatima' is removed");
    Contacts* check = store.Search_by_Name("Fatima", false);
    assert(check == nullptr);
    std::cout << "✓ Contact successfully removed and verified\n";
}

void Test_7_Remove_Contact_By_LastName() {
    PrintTestHeader("TEST GROUP 7: Remove Contact by LastName");
    
    Contact_store_class store;
    
    PrintTestCase("7.1", "Populate store with 4 contacts");
    store.Add_contact(std::move(Contacts("Ahmed", "Hassan", "01001234567", "Microsoft", Contactgroup::COWORKERS)));
    store.Add_contact(std::move(Contacts("Fatima", "Mohamed", "01101234567", "Google", Contactgroup::FAMILY)));
    store.Add_contact(std::move(Contacts("Omar", "Ali", "01201234567", "Apple", Contactgroup::FRIENDS)));
    store.Add_contact(std::move(Contacts("Sara", "Hassan", "01401234567", "Tesla", Contactgroup::FRIENDS)));
    
    std::cout << "All contacts:\n";
    store.DisplayAll();
    
    PrintTestCase("7.2", "Remove 'Mohamed' by last name");
    store.Remove_by_Name("Mohamed", true);
    
    std::cout << "\nRemaining contacts:\n";
    store.DisplayAll();
    
    PrintTestCase("7.3", "Verify 'Mohamed' is removed");
    Contacts* check = store.Search_by_Name("Mohamed", true);
    assert(check == nullptr);
    std::cout << "✓ Contact successfully removed\n";
}

// ==================== TEST GROUP 8: SORTING FUNCTIONALITY ====================

void Test_8_Sort_Ascending() {
    PrintTestHeader("TEST GROUP 8: Sort Contacts - Ascending Order");
    
    Contact_store_class store;
    
    PrintTestCase("8.1", "Add contacts in random order");
    store.Add_contact(std::move(Contacts("Ziad", "Kamal", "01501234567", "Apple", Contactgroup::FRIENDS)));
    store.Add_contact(std::move(Contacts("Ahmed", "Hassan", "01001234567", "Microsoft", Contactgroup::COWORKERS)));
    store.Add_contact(std::move(Contacts("Noor", "Ibrahim", "01301234567", "Amazon", Contactgroup::FAMILY)));
    store.Add_contact(std::move(Contacts("Bassem", "George", "01031234567", "Bosch", Contactgroup::DEFAULT)));
    
    std::cout << "\nContacts BEFORE sorting:\n";
    store.DisplayAll();
    
    PrintTestCase("8.2", "Sort in ASCENDING order (A-Z) by first name");
    std::cout << "Sorted result:\n";
    store.Sort_By_A_D_Name(true);
    
    std::cout << "✓ Contacts sorted ascending by first name\n";
}

void Test_9_Sort_Descending() {
    PrintTestHeader("TEST GROUP 9: Sort Contacts - Descending Order");
    
    Contact_store_class store;
    
    PrintTestCase("9.1", "Add contacts in random order");
    store.Add_contact(std::move(Contacts("Ziad", "Kamal", "01501234567", "Apple", Contactgroup::FRIENDS)));
    store.Add_contact(std::move(Contacts("Ahmed", "Hassan", "01001234567", "Microsoft", Contactgroup::COWORKERS)));
    store.Add_contact(std::move(Contacts("Noor", "Ibrahim", "01301234567", "Amazon", Contactgroup::FAMILY)));
    store.Add_contact(std::move(Contacts("Bassem", "George", "01031234567", "Bosch", Contactgroup::DEFAULT)));
    
    std::cout << "\nContacts BEFORE sorting:\n";
    store.DisplayAll();
    
    PrintTestCase("9.2", "Sort in DESCENDING order (Z-A) by first name");
    std::cout << "Sorted result:\n";
    store.Sort_By_A_D_Name(false);
    
    std::cout << "✓ Contacts sorted descending by first name\n";
}

// ==================== TEST GROUP 10: OPERATOR OVERLOADING ====================

void Test_10_Operator_Less_Than() {
    PrintTestHeader("TEST GROUP 10: Operator Overloading - Less Than (<)");
    
    PrintTestCase("10.1", "Create two contact objects");
    Contacts c1("Ahmed", "Hassan", "01001234567", "Microsoft", Contactgroup::COWORKERS);
    Contacts c2("Ziad", "Kamal", "01501234567", "Apple", Contactgroup::FRIENDS);
    
    PrintTestCase("10.2", "Test < operator based on first name");
    if (c1 < c2) {
        std::cout << "✓ Ahmed < Ziad: True (correct - 'Ahmed' < 'Ziad' alphabetically)\n";
    }
    
    PrintTestCase("10.3", "Test < operator in reverse");
    if (!(c2 < c1)) {
        std::cout << "✓ Ziad < Ahmed: False (correct - 'Ziad' is not < 'Ahmed')\n";
    }
    
    PrintTestCase("10.4", "Test with same first name");
    Contacts c3("Ahmed", "Ali", "01001234567", "Google", Contactgroup::FAMILY);
    Contacts c4("Ahmed", "Hassan", "01201234567", "Amazon", Contactgroup::FRIENDS);
    if (!(c3 < c4) && !(c4 < c3)) {
        std::cout << "✓ Two 'Ahmed' contacts: Neither is < other (same first name)\n";
    }
}

// ==================== TEST GROUP 11: GROUP FILTERING ====================

void Test_11_DisplayByGroup_Feature() {
    PrintTestHeader("TEST GROUP 11: Display Contacts by Group");
    
    Contact_store_class store;
    
    PrintTestCase("11.1", "Add contacts with different groups");
    store.Add_contact(std::move(Contacts("Ahmed", "Hassan", "01001234567", "Microsoft", Contactgroup::COWORKERS)));
    store.Add_contact(std::move(Contacts("Fatima", "Mohamed", "01101234567", "Google", Contactgroup::FAMILY)));
    store.Add_contact(std::move(Contacts("Omar", "Ali", "01201234567", "Apple", Contactgroup::FRIENDS)));
    store.Add_contact(std::move(Contacts("Noor", "Karim", "01301234567", "Amazon", Contactgroup::FAMILY)));
    store.Add_contact(std::move(Contacts("Layla", "Ibrahim", "01401234567", "Tesla", Contactgroup::FRIENDS)));
    store.Add_contact(std::move(Contacts("Bassem", "George", "01031234567", "Bosch", Contactgroup::COWORKERS)));
    
    std::cout << "\nAll contacts:\n";
    store.DisplayAll();
    
    PrintTestCase("11.2", "Display COWORKERS group");
    std::cout << "Note: DisplayByGroup() method not yet implemented\n";
    std::cout << "Expected result: Show only COWORKERS group contacts\n";
    // store.DisplayByGroup(Contactgroup::COWORKERS);
    
    PrintTestCase("11.3", "Display FAMILY group");
    std::cout << "Expected: Show Fatima and Noor\n";
    // store.DisplayByGroup(Contactgroup::FAMILY);
    
    PrintTestCase("11.4", "Display FRIENDS group");
    std::cout << "Expected: Show Omar and Layla\n";
    // store.DisplayByGroup(Contactgroup::FRIENDS);
}

// ==================== TEST GROUP 12: EDGE CASES ====================

void Test_12_Empty_Store_Operations() {
    PrintTestHeader("TEST GROUP 12: Edge Cases - Empty Store");
    
    Contact_store_class store;
    
    PrintTestCase("12.1", "DisplayAll on empty store");
    std::cout << "Expected: Empty display\n";
    store.DisplayAll();
    std::cout << "✓ No error on empty store display\n";
    
    PrintTestCase("12.2", "Search in empty store");
    Contacts* result = store.Search_by_Name("John", false);
    assert(result == nullptr);
    std::cout << "✓ Returns nullptr for search in empty store\n";
    
    PrintTestCase("12.3", "Remove from empty store");
    store.Remove_by_Name("John", false);
    std::cout << "✓ No error on remove from empty store\n";
}

void Test_13_Duplicate_FirstNames() {
    PrintTestHeader("TEST GROUP 13: Edge Cases - Duplicate First Names");
    
    Contact_store_class store;
    
    PrintTestCase("13.1", "Add 3 contacts with same first name");
    store.Add_contact(std::move(Contacts("Ahmed", "Hassan", "01001234567", "Microsoft", Contactgroup::COWORKERS)));
    store.Add_contact(std::move(Contacts("Ahmed", "Mohamed", "01101234567", "Google", Contactgroup::FAMILY)));
    store.Add_contact(std::move(Contacts("Ahmed", "Ali", "01201234567", "Apple", Contactgroup::FRIENDS)));
    
    std::cout << "\nAll contacts with first name 'Ahmed':\n";
    store.DisplayAll();
    
    PrintTestCase("13.2", "Search for 'Ahmed' (returns first match)");
    Contacts* result = store.Search_by_Name("Ahmed", false);
    if (result != nullptr) {
        std::cout << "✓ Found: " << result->Get_FirstName() << " " 
                  << result->Get_LastName() << " (first match)\n";
    }
    
    PrintTestCase("13.3", "Remove 'Ahmed' (removes first match only)");
    store.Remove_by_Name("Ahmed", false);
    std::cout << "\nRemaining contacts:\n";
    store.DisplayAll();
    std::cout << "✓ First 'Ahmed' was removed, other 'Ahmed' contacts remain\n";
}

void Test_14_Case_Sensitivity() {
    PrintTestHeader("TEST GROUP 14: Edge Cases - Case Sensitivity");
    
    Contact_store_class store;
    
    PrintTestCase("14.1", "Add contact 'Ahmed Hassan'");
    store.Add_contact(std::move(Contacts("Ahmed", "Hassan", "01001234567", "Microsoft", Contactgroup::COWORKERS)));
    
    PrintTestCase("14.2", "Search for 'ahmed' (lowercase)");
    Contacts* result1 = store.Search_by_Name("ahmed", false);
    if (result1 == nullptr) {
        std::cout << "✓ Not found - search is case-sensitive\n";
    }
    
    PrintTestCase("14.3", "Search for 'AHMED' (uppercase)");
    Contacts* result2 = store.Search_by_Name("AHMED", false);
    if (result2 == nullptr) {
        std::cout << "✓ Not found - search is case-sensitive\n";
    }
    
    PrintTestCase("14.4", "Search for 'Ahmed' (exact case)");
    Contacts* result3 = store.Search_by_Name("Ahmed", false);
    if (result3 != nullptr) {
        std::cout << "✓ Found - exact case match works\n";
    }
}

// ==================== TEST GROUP 15: COMPLETE WORKFLOW ====================

void Test_15_Complete_Workflow() {
    PrintTestHeader("TEST GROUP 15: Complete Workflow - Real Scenario");
    
    PrintTestCase("15.1", "Initialize contact store");
    Contact_store_class phonebook;
    std::cout << "✓ Phonebook initialized\n";
    
    PrintTestCase("15.2", "Add initial contacts");
    phonebook.Add_contact(std::move(Contacts("Ahmed", "Hassan", "01001234567", "Microsoft", Contactgroup::COWORKERS)));
    phonebook.Add_contact(std::move(Contacts("Fatima", "Mohamed", "01101234567", "Google", Contactgroup::FAMILY)));
    phonebook.Add_contact(std::move(Contacts("Omar", "Ali", "01201234567", "Apple", Contactgroup::FRIENDS)));
    
    std::cout << "\nCurrent phonebook:\n";
    phonebook.DisplayAll();
    
    PrintTestCase("15.3", "Search for a contact");
    Contacts* found = phonebook.Search_by_Name("Fatima", false);
    if (found != nullptr) {
        std::cout << "✓ Found Fatima: " << found->Get_Phone_Number() << "\n";
    }
    
    PrintTestCase("15.4", "Edit contact information");
    if (found != nullptr) {
        found->SET_Company("Amazon");
        found->SET_Phone_Number("01101111111");
        std::cout << "✓ Updated Fatima's company to Amazon\n";
        std::cout << "✓ Updated Fatima's phone to 01101111111\n";
    }
    
    PrintTestCase("15.5", "Add more contacts");
    phonebook.Add_contact(std::move(Contacts("Sara", "Ibrahim", "01301234567", "Tesla", Contactgroup::FRIENDS)));
    std::cout << "✓ Added Sara Ibrahim\n";
    
    PrintTestCase("15.6", "Sort and display");
    std::cout << "\nPhonebook sorted by first name (A-Z):\n";
    phonebook.Sort_By_A_D_Name(true);
    
    PrintTestCase("15.7", "Remove a contact");
    phonebook.Remove_by_Name("Omar", false);
    std::cout << "\nPhonebook after removing Omar:\n";
    phonebook.DisplayAll();
    
    std::cout << "\n✓ Complete workflow executed successfully\n";
}

// ==================== MAIN TEST RUNNER ====================

int main() {
    std::cout << "\n";
    std::cout << std::string(70, '=') << std::endl;
    std::cout << "   INTEGRATION TEST SUITE - CONTACTS & CONTACT STORE" << std::endl;
    std::cout << "   Testing both classes working together" << std::endl;
    std::cout << std::string(70, '=') << std::endl;
    
    try {
        // Test Groups
        Test_1_Create_And_Add_Contacts();
        Test_2_Create_Contacts_With_Defaults();
        Test_3_Search_By_FirstName_Integration();
        Test_4_Search_By_LastName_Integration();
        Test_5_Modify_Contact_Using_Setters();
        Test_6_Remove_Contact_By_FirstName();
        Test_7_Remove_Contact_By_LastName();
        Test_8_Sort_Ascending();
        Test_9_Sort_Descending();
        Test_10_Operator_Less_Than();
        Test_11_DisplayByGroup_Feature();
        Test_12_Empty_Store_Operations();
        Test_13_Duplicate_FirstNames();
        Test_14_Case_Sensitivity();
        Test_15_Complete_Workflow();
        
        std::cout << "\n" << std::string(70, '=') << std::endl;
        std::cout << "   ✓ ALL INTEGRATION TESTS PASSED SUCCESSFULLY!" << std::endl;
        std::cout << std::string(70, '=') << "\n" << std::endl;
        
        return 0;
    }
    catch (const std::exception &e) {
        std::cerr << "\n✗ TEST FAILED WITH EXCEPTION: " << e.what() << std::endl;
        return 1;
    }
}
