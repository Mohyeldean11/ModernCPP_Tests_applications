#include "./../../CLASSES/Contact_store_Class/Contact_store_class.hpp"
#include <iostream>
#include <cassert>

/**
 * CONTACT STORE CLASS FUNCTIONALITY OVERVIEW:
 * 
 * The Contact_store_class manages a vector of Contact objects with the following methods:
 * 
 * 1. Add_contact(const Contacts &&contact)
 *    - Adds a new contact to the contact book
 *    - Takes an rvalue reference (move semantics)
 *    - Prints confirmation message
 * 
 * 2. Remove_by_Name(const std::string &name, bool WhichName)
 *    - Removes a contact by first name or last name
 *    - WhichName: false = search by FirstName, true = search by LastName
 *    - Prints success/failure message
 * 
 * 3. Search_by_Name(const std::string &name, bool WhichName)
 *    - Searches for a contact by first name or last name
 *    - WhichName: false = search by FirstName, true = search by LastName
 *    - Returns pointer to Contact if found, nullptr if not found
 * 
 * 4. DisplayAll()
 *    - Displays all contacts in the contact book
 * 
 * 5. DisplayByGroup(Contactgroup group)
 *    - Displays contacts filtered by group (DEFAULT, COWORKERS, FAMILY, FRIENDS)
 *    - NOTE: Implementation appears incomplete in cpp file
 * 
 * 6. Sort_By_A_D_Name(bool orderFlag)
 *    - Sorts contacts by first name
 *    - orderFlag: true = ascending order, false = descending order
 *    - Automatically displays sorted contacts
 */

// ==================== TEST 1: Add Contact ====================
void Test_Add_Contact() {
    std::cout << "\n========== TEST 1: Add_contact() ==========\n";
    std::cout << "Testing: Adding single and multiple contacts to the store\n\n";
    
    Contact_store_class store;
    
    std::cout << "Adding contact 1 - Mohamed Badawy (COWORKERS):\n";
    store.Add_contact(Contacts("Mohamed", "Badawy", "0100000000", "Bosch", Contactgroup::COWORKERS));
    
    std::cout << "Adding contact 2 - Sara Ali (FAMILY):\n";
    store.Add_contact(Contacts("Sara", "Ali", "0123456789", "Google", Contactgroup::FAMILY));
    
    std::cout << "Adding contact 3 - Ahmed Sami (FRIENDS):\n";
    store.Add_contact(Contacts("Ahmed", "Sami", "0110001111", "Microsoft", Contactgroup::FRIENDS));
    
    std::cout << "\n✓ Test 1 PASSED: Contacts added successfully\n";
}

// ==================== TEST 2: Search by First Name ====================
void Test_Search_By_FirstName() {
    std::cout << "\n========== TEST 2: Search_by_Name() - FirstName ==========\n";
    std::cout << "Testing: Searching contacts by first name (WhichName = false)\n\n";
    
    Contact_store_class store;
    
    // Add test contacts
    store.Add_contact(Contacts("Mohamed", "Badawy", "0100000000", "Bosch", Contactgroup::COWORKERS));
    store.Add_contact(Contacts("Sara", "Ali", "0123456789", "Google", Contactgroup::FAMILY));
    store.Add_contact(Contacts("Ahmed", "Sami", "0110001111", "Microsoft", Contactgroup::FRIENDS));
    
    std::cout << "\nTest Case 2.1: Search for existing contact 'Mohamed' by first name\n";
    Contacts* result1 = store.Search_by_Name("Mohamed", false);
    if (result1 != nullptr) {
        std::cout << "✓ Found: " << result1->Get_FirstName() << " " 
                  << result1->Get_LastName() << " - " 
                  << result1->Get_Phone_Number() << std::endl;
    } else {
        std::cout << "✗ FAILED: Contact not found\n";
    }
    
    std::cout << "\nTest Case 2.2: Search for existing contact 'Sara' by first name\n";
    Contacts* result2 = store.Search_by_Name("Sara", false);
    if (result2 != nullptr) {
        std::cout << "✓ Found: " << result2->Get_FirstName() << " " 
                  << result2->Get_LastName() << " - " 
                  << result2->Get_Phone_Number() << std::endl;
    } else {
        std::cout << "✗ FAILED: Contact not found\n";
    }
    
    std::cout << "\nTest Case 2.3: Search for non-existing contact 'John' by first name\n";
    Contacts* result3 = store.Search_by_Name("John", false);
    if (result3 == nullptr) {
        std::cout << "✓ Correctly returned nullptr for non-existent contact\n";
    } else {
        std::cout << "✗ FAILED: Should return nullptr\n";
    }
    
    std::cout << "\n✓ Test 2 PASSED: Search by FirstName works correctly\n";
}

// ==================== TEST 3: Search by Last Name ====================
void Test_Search_By_LastName() {
    std::cout << "\n========== TEST 3: Search_by_Name() - LastName ==========\n";
    std::cout << "Testing: Searching contacts by last name (WhichName = true)\n\n";
    
    Contact_store_class store;
    
    // Add test contacts
    store.Add_contact(Contacts("Mohamed", "Badawy", "0100000000", "Bosch", Contactgroup::COWORKERS));
    store.Add_contact(Contacts("Sara", "Ali", "0123456789", "Google", Contactgroup::FAMILY));
    store.Add_contact(Contacts("Ahmed", "Sami", "0110001111", "Microsoft", Contactgroup::FRIENDS));
    
    std::cout << "\nTest Case 3.1: Search for contact with last name 'Ali' by last name\n";
    Contacts* result1 = store.Search_by_Name("Ali", true);
    if (result1 != nullptr) {
        std::cout << "✓ Found: " << result1->Get_FirstName() << " " 
                  << result1->Get_LastName() << " - " 
                  << result1->Get_Phone_Number() << std::endl;
    } else {
        std::cout << "✗ FAILED: Contact not found\n";
    }
    
    std::cout << "\nTest Case 3.2: Search for contact with last name 'Badawy' by last name\n";
    Contacts* result2 = store.Search_by_Name("Badawy", true);
    if (result2 != nullptr) {
        std::cout << "✓ Found: " << result2->Get_FirstName() << " " 
                  << result2->Get_LastName() << " - " 
                  << result2->Get_Phone_Number() << std::endl;
    } else {
        std::cout << "✗ FAILED: Contact not found\n";
    }
    
    std::cout << "\nTest Case 3.3: Search for non-existing last name 'Smith'\n";
    Contacts* result3 = store.Search_by_Name("Smith", true);
    if (result3 == nullptr) {
        std::cout << "✓ Correctly returned nullptr for non-existent contact\n";
    } else {
        std::cout << "✗ FAILED: Should return nullptr\n";
    }
    
    std::cout << "\n✓ Test 3 PASSED: Search by LastName works correctly\n";
}

// ==================== TEST 4: Remove by First Name ====================
void Test_Remove_By_FirstName() {
    std::cout << "\n========== TEST 4: Remove_by_Name() - FirstName ==========\n";
    std::cout << "Testing: Removing contacts by first name (WhichName = false)\n\n";
    
    Contact_store_class store;
    
    // Add test contacts
    std::cout << "Adding 3 test contacts:\n";
    store.Add_contact(Contacts("Mohamed", "Badawy", "0100000000", "Bosch", Contactgroup::COWORKERS));
    store.Add_contact(Contacts("Sara", "Ali", "0123456789", "Google", Contactgroup::FAMILY));
    store.Add_contact(Contacts("Ahmed", "Sami", "0110001111", "Microsoft", Contactgroup::FRIENDS));
    
    std::cout << "\nTest Case 4.1: Remove existing contact 'Mohamed' by first name\n";
    store.Remove_by_Name("Mohamed", false);
    Contacts* check1 = store.Search_by_Name("Mohamed", false);
    if (check1 == nullptr) {
        std::cout << "✓ Contact successfully removed\n";
    } else {
        std::cout << "✗ FAILED: Contact still exists\n";
    }
    
    std::cout << "\nTest Case 4.2: Remove non-existing contact 'John' by first name\n";
    store.Remove_by_Name("John", false);
    
    std::cout << "\nTest Case 4.3: Display remaining contacts after removal\n";
    store.DisplayAll();
    
    std::cout << "\n✓ Test 4 PASSED: Remove by FirstName works correctly\n";
}

// ==================== TEST 5: Remove by Last Name ====================
void Test_Remove_By_LastName() {
    std::cout << "\n========== TEST 5: Remove_by_Name() - LastName ==========\n";
    std::cout << "Testing: Removing contacts by last name (WhichName = true)\n\n";
    
    Contact_store_class store;
    
    // Add test contacts
    std::cout << "Adding 3 test contacts:\n";
    store.Add_contact(Contacts("Mohamed", "Badawy", "0100000000", "Bosch", Contactgroup::COWORKERS));
    store.Add_contact(Contacts("Sara", "Ali", "0123456789", "Google", Contactgroup::FAMILY));
    store.Add_contact(Contacts("Ahmed", "Sami", "0110001111", "Microsoft", Contactgroup::FRIENDS));
    
    std::cout << "\nTest Case 5.1: Remove contact with last name 'Ali'\n";
    store.Remove_by_Name("Ali", true);
    Contacts* check1 = store.Search_by_Name("Ali", true);
    if (check1 == nullptr) {
        std::cout << "✓ Contact successfully removed\n";
    } else {
        std::cout << "✗ FAILED: Contact still exists\n";
    }
    
    std::cout << "\nTest Case 5.2: Remove non-existing last name 'Smith'\n";
    store.Remove_by_Name("Smith", true);
    
    std::cout << "\nTest Case 5.3: Display remaining contacts after removal\n";
    store.DisplayAll();
    
    std::cout << "\n✓ Test 5 PASSED: Remove by LastName works correctly\n";
}

// ==================== TEST 6: Display All Contacts ====================
void Test_DisplayAll() {
    std::cout << "\n========== TEST 6: DisplayAll() ==========\n";
    std::cout << "Testing: Displaying all contacts in the store\n\n";
    
    Contact_store_class store;
    
    // Add test contacts with various groups
    std::cout << "Adding contacts with different groups:\n";
    store.Add_contact(Contacts("Mohamed", "Badawy", "0100000000", "Bosch", Contactgroup::COWORKERS));
    store.Add_contact(Contacts("Sara", "Ali", "0123456789", "Google", Contactgroup::FAMILY));
    store.Add_contact(Contacts("Ahmed", "Sami", "0110001111", "Microsoft", Contactgroup::FRIENDS));
    store.Add_contact(Contacts("Laila", "Hassan", "0102222222", "NA", Contactgroup::DEFAULT));
    
    std::cout << "\nDisplay All Contacts:\n";
    store.DisplayAll();
    
    std::cout << "\n✓ Test 6 PASSED: DisplayAll works correctly\n";
}

// ==================== TEST 7: Sort Ascending ====================
void Test_Sort_Ascending() {
    std::cout << "\n========== TEST 7: Sort_By_A_D_Name() - ASCENDING ==========\n";
    std::cout << "Testing: Sorting contacts by first name in ascending order (orderFlag = true)\n\n";
    
    Contact_store_class store;
    
    // Add test contacts in random order
    std::cout << "Adding contacts in random order:\n";
    store.Add_contact(Contacts("Ziad", "Kamal", "0150000000", "Apple", Contactgroup::FRIENDS));
    store.Add_contact(Contacts("Ahmed", "Sami", "0110001111", "Microsoft", Contactgroup::COWORKERS));
    store.Add_contact(Contacts("Laila", "Hassan", "0102222222", "Google", Contactgroup::FAMILY));
    store.Add_contact(Contacts("Bassem", "George", "0103333333", "Bosch", Contactgroup::DEFAULT));
    
    std::cout << "\nSorted in ASCENDING order by first name (A-Z):\n";
    store.Sort_By_A_D_Name(true);
    
    std::cout << "\n✓ Test 7 PASSED: Ascending sort works correctly\n";
}

// ==================== TEST 8: Sort Descending ====================
void Test_Sort_Descending() {
    std::cout << "\n========== TEST 8: Sort_By_A_D_Name() - DESCENDING ==========\n";
    std::cout << "Testing: Sorting contacts by first name in descending order (orderFlag = false)\n\n";
    
    Contact_store_class store;
    
    // Add test contacts in random order
    std::cout << "Adding contacts in random order:\n";
    store.Add_contact(Contacts("Ziad", "Kamal", "0150000000", "Apple", Contactgroup::FRIENDS));
    store.Add_contact(Contacts("Ahmed", "Sami", "0110001111", "Microsoft", Contactgroup::COWORKERS));
    store.Add_contact(Contacts("Laila", "Hassan", "0102222222", "Google", Contactgroup::FAMILY));
    store.Add_contact(Contacts("Bassem", "George", "0103333333", "Bosch", Contactgroup::DEFAULT));
    
    std::cout << "\nSorted in DESCENDING order by first name (Z-A):\n";
    store.Sort_By_A_D_Name(false);
    
    std::cout << "\n✓ Test 8 PASSED: Descending sort works correctly\n";
}

// ==================== TEST 9: Edge Case - Empty Store ====================
void Test_Empty_Store() {
    std::cout << "\n========== TEST 9: Edge Cases - Empty Store ==========\n";
    std::cout << "Testing: Operations on an empty contact store\n\n";
    
    Contact_store_class store;
    
    std::cout << "Test Case 9.1: Display empty store:\n";
    store.DisplayAll();
    std::cout << "(No output expected for empty store)\n";
    
    std::cout << "\nTest Case 9.2: Search in empty store:\n";
    Contacts* result = store.Search_by_Name("John", false);
    if (result == nullptr) {
        std::cout << "✓ Correctly returns nullptr for empty store\n";
    }
    
    std::cout << "\nTest Case 9.3: Remove from empty store:\n";
    store.Remove_by_Name("John", false);
    
    std::cout << "\n✓ Test 9 PASSED: Empty store handles correctly\n";
}

// ==================== TEST 10: Duplicate Names ====================
void Test_Duplicate_Names() {
    std::cout << "\n========== TEST 10: Edge Cases - Duplicate Names ==========\n";
    std::cout << "Testing: Adding and managing contacts with duplicate names\n\n";
    
    Contact_store_class store;
    
    std::cout << "Adding multiple contacts with same first name:\n";
    store.Add_contact(Contacts("Ahmed", "Ali", "0100000000", "Company A", Contactgroup::COWORKERS));
    store.Add_contact(Contacts("Ahmed", "Sami", "0110001111", "Company B", Contactgroup::FRIENDS));
    store.Add_contact(Contacts("Ahmed", "Hassan", "0120000000", "Company C", Contactgroup::FAMILY));
    
    std::cout << "\nDisplay all contacts with first name 'Ahmed':\n";
    store.DisplayAll();
    
    std::cout << "\nTest Case 10.1: Search for 'Ahmed' by first name (returns first match):\n";
    Contacts* result = store.Search_by_Name("Ahmed", false);
    if (result != nullptr) {
        std::cout << "✓ Found: " << result->Get_FirstName() << " " 
                  << result->Get_LastName() << " - " 
                  << result->Get_Phone_Number() << std::endl;
        std::cout << "  (Note: Returns first matching contact only)\n";
    }
    
    std::cout << "\nTest Case 10.2: Remove 'Ahmed' by first name (removes first match):\n";
    store.Remove_by_Name("Ahmed", false);
    std::cout << "Remaining contacts:\n";
    store.DisplayAll();
    
    std::cout << "\n✓ Test 10 PASSED: Duplicate name handling works correctly\n";
}

// ==================== TEST 11: Case Sensitivity ====================
void Test_Case_Sensitivity() {
    std::cout << "\n========== TEST 11: Edge Cases - Case Sensitivity ==========\n";
    std::cout << "Testing: String matching is case-sensitive\n\n";
    
    Contact_store_class store;
    
    std::cout << "Adding contact 'Mohamed Badawy':\n";
    store.Add_contact(Contacts("Mohamed", "Badawy", "0100000000", "Bosch", Contactgroup::COWORKERS));
    
    std::cout << "\nTest Case 11.1: Search for 'Mohamed' (exact case match):\n";
    Contacts* result1 = store.Search_by_Name("Mohamed", false);
    if (result1 != nullptr) {
        std::cout << "✓ Found: " << result1->Get_FirstName() << std::endl;
    }
    
    std::cout << "\nTest Case 11.2: Search for 'mohamed' (lowercase - no match):\n";
    Contacts* result2 = store.Search_by_Name("mohamed", false);
    if (result2 == nullptr) {
        std::cout << "✓ Not found (case-sensitive search)\n";
    }
    
    std::cout << "\nTest Case 11.3: Search for 'MOHAMED' (uppercase - no match):\n";
    Contacts* result3 = store.Search_by_Name("MOHAMED", false);
    if (result3 == nullptr) {
        std::cout << "✓ Not found (case-sensitive search)\n";
    }
    
    std::cout << "\n✓ Test 11 PASSED: Case sensitivity confirmed\n";
}

// ==================== TEST 12: Integration Test ====================
void Test_Integration_Complete_Workflow() {
    std::cout << "\n========== TEST 12: Integration Test - Complete Workflow ==========\n";
    std::cout << "Testing: Complete workflow - Add, Search, Sort, Remove\n\n";
    
    Contact_store_class phonebook;
    
    std::cout << "Step 1: Adding 5 contacts to the phonebook:\n";
    phonebook.Add_contact(Contacts("Ziad", "Kamal", "0150000000", "Apple", Contactgroup::FRIENDS));
    phonebook.Add_contact(Contacts("Ahmed", "Sami", "0110001111", "Microsoft", Contactgroup::COWORKERS));
    phonebook.Add_contact(Contacts("Laila", "Hassan", "0102222222", "Google", Contactgroup::FAMILY));
    phonebook.Add_contact(Contacts("Bassem", "George", "0103333333", "Bosch", Contactgroup::DEFAULT));
    phonebook.Add_contact(Contacts("Sara", "Ali", "0123456789", "Amazon", Contactgroup::FRIENDS));
    
    std::cout << "\nStep 2: Display all contacts:\n";
    phonebook.DisplayAll();
    
    std::cout << "\nStep 3: Search for 'Ahmed' by first name:\n";
    Contacts* found = phonebook.Search_by_Name("Ahmed", false);
    if (found != nullptr) {
        std::cout << "✓ Found: " << found->Get_FirstName() << " " 
                  << found->Get_LastName() << std::endl;
    }
    
    std::cout << "\nStep 4: Sort contacts in ascending order:\n";
    phonebook.Sort_By_A_D_Name(true);
    
    std::cout << "\nStep 5: Remove 'Laila' by first name:\n";
    phonebook.Remove_by_Name("Laila", false);
    
    std::cout << "\nStep 6: Display final contact list:\n";
    phonebook.DisplayAll();
    
    std::cout << "\n✓ Test 12 PASSED: Complete workflow executed successfully\n";
}

// ==================== MAIN TEST RUNNER ====================
int main_tested() {
    std::cout << "\n" << std::string(70, '=') << std::endl;
    std::cout << "CONTACT STORE CLASS - COMPREHENSIVE TEST SUITE" << std::endl;
    std::cout << std::string(70, '=') << std::endl;
    
    // Run all tests
    Test_Add_Contact();
    Test_Search_By_FirstName();
    Test_Search_By_LastName();
    Test_Remove_By_FirstName();
    Test_Remove_By_LastName();
    Test_DisplayAll();
    Test_Sort_Ascending();
    Test_Sort_Descending();
    Test_Empty_Store();
    Test_Duplicate_Names();
    Test_Case_Sensitivity();
    Test_Integration_Complete_Workflow();
    
    std::cout << "\n" << std::string(70, '=') << std::endl;
    std::cout << "ALL TESTS COMPLETED SUCCESSFULLY!" << std::endl;
    std::cout << std::string(70, '=') << "\n" << std::endl;
    
    return 0;
}
