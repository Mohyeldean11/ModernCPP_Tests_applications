#include "Contacts.hpp"
#include <iostream>
#include <cassert>

void print_test_header(const std::string &test_name)
{
    std::cout << "\n" << "=" << std::string(60, '=') << std::endl;
    std::cout << "TEST: " << test_name << std::endl;
    std::cout << "=" << std::string(60, '=') << std::endl;
}

void print_result(const std::string &test_case, bool passed)
{
    std::string status = passed ? "✓ PASS" : "✗ FAIL";
    std::cout << test_case << " : " << status << std::endl;
}

// Test 1: Parameterized Constructor with all parameters
void test_constructor_full_params()
{
    print_test_header("Parameterized Constructor (Full Parameters)");
    
    std::cout << "\nTest Case 1: Create contact with all parameters" << std::endl;
    std::cout << "Input: FirstName='John', LastName='Doe', Phone='555-1234', Company='TechCorp', Group=COWORKERS" << std::endl;
    
    Contacts contact1("John", "Doe", "555-1234", "TechCorp", Contactgroup::COWORKERS);
    
    std::cout << "Expected: FirstName='John', LastName='Doe', Phone='555-1234', Company='TechCorp', Group=COWORKERS(1)" << std::endl;
    std::cout << "Actual: FirstName='" << contact1.Get_FirstName() 
              << "', LastName='" << contact1.Get_LastName() 
              << "', Phone='" << contact1.Get_Phone_Number() 
              << "', Company='" << contact1.Get_Company() 
              << "', Group=" << static_cast<int>(contact1.Get_Group()) << std::endl;
    
    bool passed = (contact1.Get_FirstName() == "John" &&
                   contact1.Get_LastName() == "Doe" &&
                   contact1.Get_Phone_Number() == "555-1234" &&
                   contact1.Get_Company() == "TechCorp" &&
                   contact1.Get_Group() == Contactgroup::COWORKERS);
    
    print_result("Constructor with full parameters", passed);
}

// Test 2: Parameterized Constructor with default parameters
void test_constructor_default_params()
{
    print_test_header("Parameterized Constructor (Default Parameters)");
    
    std::cout << "\nTest Case 1: Create contact with default Company and Group" << std::endl;
    std::cout << "Input: FirstName='Alice', LastName='Smith', Phone='555-5678'" << std::endl;
    
    Contacts contact2("Alice", "Smith", "555-5678");
    
    std::cout << "Expected: FirstName='Alice', LastName='Smith', Phone='555-5678', Company='NA', Group=DEFAULT(0)" << std::endl;
    std::cout << "Actual: FirstName='" << contact2.Get_FirstName() 
              << "', LastName='" << contact2.Get_LastName() 
              << "', Phone='" << contact2.Get_Phone_Number() 
              << "', Company='" << contact2.Get_Company() 
              << "', Group=" << static_cast<int>(contact2.Get_Group()) << std::endl;
    
    bool passed = (contact2.Get_FirstName() == "Alice" &&
                   contact2.Get_LastName() == "Smith" &&
                   contact2.Get_Phone_Number() == "555-5678" &&
                   contact2.Get_Company() == "NA" &&
                   contact2.Get_Group() == Contactgroup::DEFAULT);
    
    print_result("Constructor with default parameters", passed);
}

// Test 3: Get_FirstName()
void test_get_firstname()
{
    print_test_header("Get_FirstName() Method");
    
    std::cout << "\nTest Case 1: Get first name from contact" << std::endl;
    Contacts contact("Robert", "Johnson", "555-9999");
    
    std::cout << "Expected: 'Robert'" << std::endl;
    std::cout << "Actual: '" << contact.Get_FirstName() << "'" << std::endl;
    
    bool passed = (contact.Get_FirstName() == "Robert");
    print_result("Get first name correctly", passed);
    
    std::cout << "\nTest Case 2: Get first name with special characters" << std::endl;
    Contacts contact2("Jean-Pierre", "Laurent", "555-8888");
    
    std::cout << "Expected: 'Jean-Pierre'" << std::endl;
    std::cout << "Actual: '" << contact2.Get_FirstName() << "'" << std::endl;
    
    bool passed2 = (contact2.Get_FirstName() == "Jean-Pierre");
    print_result("Get first name with special characters", passed2);
}

// Test 4: Get_LastName()
void test_get_lastname()
{
    print_test_header("Get_LastName() Method");
    
    std::cout << "\nTest Case 1: Get last name from contact" << std::endl;
    Contacts contact("Sarah", "Williams", "555-7777");
    
    std::cout << "Expected: 'Williams'" << std::endl;
    std::cout << "Actual: '" << contact.Get_LastName() << "'" << std::endl;
    
    bool passed = (contact.Get_LastName() == "Williams");
    print_result("Get last name correctly", passed);
}

// Test 5: Get_Phone_Number()
void test_get_phone_number()
{
    print_test_header("Get_Phone_Number() Method");
    
    std::cout << "\nTest Case 1: Get phone number from contact" << std::endl;
    Contacts contact("Michael", "Brown", "555-6666");
    
    std::cout << "Expected: '555-6666'" << std::endl;
    std::cout << "Actual: '" << contact.Get_Phone_Number() << "'" << std::endl;
    
    bool passed = (contact.Get_Phone_Number() == "555-6666");
    print_result("Get phone number correctly", passed);
    
    std::cout << "\nTest Case 2: Get phone number with international format" << std::endl;
    Contacts contact2("Emily", "Davis", "+1-555-0123");
    
    std::cout << "Expected: '+1-555-0123'" << std::endl;
    std::cout << "Actual: '" << contact2.Get_Phone_Number() << "'" << std::endl;
    
    bool passed2 = (contact2.Get_Phone_Number() == "+1-555-0123");
    print_result("Get international phone number", passed2);
}

// Test 6: Get_Company()
void test_get_company()
{
    print_test_header("Get_Company() Method");
    
    std::cout << "\nTest Case 1: Get company name" << std::endl;
    Contacts contact("David", "Miller", "555-4444", "Microsoft");
    
    std::cout << "Expected: 'Microsoft'" << std::endl;
    std::cout << "Actual: '" << contact.Get_Company() << "'" << std::endl;
    
    bool passed = (contact.Get_Company() == "Microsoft");
    print_result("Get company name correctly", passed);
    
    std::cout << "\nTest Case 2: Get default company name" << std::endl;
    Contacts contact2("Lisa", "Anderson", "555-3333");
    
    std::cout << "Expected: 'NA'" << std::endl;
    std::cout << "Actual: '" << contact2.Get_Company() << "'" << std::endl;
    
    bool passed2 = (contact2.Get_Company() == "NA");
    print_result("Get default company name (NA)", passed2);
}

// Test 7: Get_Group()
void test_get_group()
{
    print_test_header("Get_Group() Method");
    
    std::cout << "\nTest Case 1: Get group - COWORKERS" << std::endl;
    Contacts contact1("Tom", "Harris", "555-2222", "GoogleLabs", Contactgroup::COWORKERS);
    
    std::cout << "Expected: COWORKERS (value: 1)" << std::endl;
    std::cout << "Actual: " << (static_cast<int>(contact1.Get_Group()) == 1 ? "COWORKERS (value: 1)" : "OTHER") << std::endl;
    
    bool passed1 = (contact1.Get_Group() == Contactgroup::COWORKERS);
    print_result("Get COWORKERS group", passed1);
    
    std::cout << "\nTest Case 2: Get group - FAMILY" << std::endl;
    Contacts contact2("Nancy", "Clark", "555-1111", "NA", Contactgroup::FAMILY);
    
    std::cout << "Expected: FAMILY (value: 2)" << std::endl;
    std::cout << "Actual: " << (static_cast<int>(contact2.Get_Group()) == 2 ? "FAMILY (value: 2)" : "OTHER") << std::endl;
    
    bool passed2 = (contact2.Get_Group() == Contactgroup::FAMILY);
    print_result("Get FAMILY group", passed2);
    
    std::cout << "\nTest Case 3: Get group - FRIENDS" << std::endl;
    Contacts contact3("Chris", "Lewis", "555-0000", "NA", Contactgroup::FRIENDS);
    
    std::cout << "Expected: FRIENDS (value: 3)" << std::endl;
    std::cout << "Actual: " << (static_cast<int>(contact3.Get_Group()) == 3 ? "FRIENDS (value: 3)" : "OTHER") << std::endl;
    
    bool passed3 = (contact3.Get_Group() == Contactgroup::FRIENDS);
    print_result("Get FRIENDS group", passed3);
    
    std::cout << "\nTest Case 4: Get group - DEFAULT" << std::endl;
    Contacts contact4("Paul", "Walker", "555-9090");
    
    std::cout << "Expected: DEFAULT (value: 0)" << std::endl;
    std::cout << "Actual: " << (static_cast<int>(contact4.Get_Group()) == 0 ? "DEFAULT (value: 0)" : "OTHER") << std::endl;
    
    bool passed4 = (contact4.Get_Group() == Contactgroup::DEFAULT);
    print_result("Get DEFAULT group", passed4);
}

// Test 8: Operator < (less than) - for sorting
void test_operator_less_than()
{
    print_test_header("Operator < (Less Than) - Sorting Comparison");
    
    std::cout << "\nTest Case 1: Compare 'Alice' < 'Bob'" << std::endl;
    Contacts contact1("Alice", "A", "111-1111");
    Contacts contact2("Bob", "B", "222-2222");
    
    std::cout << "Expected: true (Alice comes before Bob alphabetically)" << std::endl;
    std::cout << "Actual: " << (contact1 < contact2 ? "true" : "false") << std::endl;
    
    bool passed1 = (contact1 < contact2);
    print_result("'Alice' < 'Bob' is true", passed1);
    
    std::cout << "\nTest Case 2: Compare 'Bob' < 'Alice'" << std::endl;
    std::cout << "Expected: false (Bob comes after Alice alphabetically)" << std::endl;
    std::cout << "Actual: " << (contact2 < contact1 ? "true" : "false") << std::endl;
    
    bool passed2 = !(contact2 < contact1);
    print_result("'Bob' < 'Alice' is false", passed2);
    
    std::cout << "\nTest Case 3: Compare 'Alice' < 'Alice'" << std::endl;
    Contacts contact3("Alice", "C", "333-3333");
    
    std::cout << "Expected: false (same first name, not less than)" << std::endl;
    std::cout << "Actual: " << (contact1 < contact3 ? "true" : "false") << std::endl;
    
    bool passed3 = !(contact1 < contact3);
    print_result("'Alice' < 'Alice' is false", passed3);
    
    std::cout << "\nTest Case 4: Compare 'Zoe' < 'Aaron'" << std::endl;
    Contacts contact4("Zoe", "Z", "444-4444");
    Contacts contact5("Aaron", "A", "555-5555");
    
    std::cout << "Expected: false (Zoe comes after Aaron alphabetically)" << std::endl;
    std::cout << "Actual: " << (contact4 < contact5 ? "true" : "false") << std::endl;
    
    bool passed4 = !(contact4 < contact5);
    print_result("'Zoe' < 'Aaron' is false", passed4);
}

// Test 9: Destructor (implicit test)
void test_destructor()
{
    print_test_header("Destructor");
    
    std::cout << "\nTest Case 1: Create and destroy contact object" << std::endl;
    {
        Contacts contact("Temporary", "Contact", "555-9999");
        std::cout << "Contact created: " << contact.Get_FirstName() << " " << contact.Get_LastName() << std::endl;
    }
    std::cout << "Contact object destroyed (end of scope)" << std::endl;
    print_result("Destructor called successfully (no crash)", true);
}

int main()
{
    std::cout << "\n" << std::string(70, '*') << std::endl;
    std::cout << "        CONTACTS CLASS - COMPREHENSIVE TEST SUITE" << std::endl;
    std::cout << std::string(70, '*') << std::endl;

    // Run all tests
    test_constructor_full_params();
    test_constructor_default_params();
    test_get_firstname();
    test_get_lastname();
    test_get_phone_number();
    test_get_company();
    test_get_group();
    test_operator_less_than();
    test_destructor();

    std::cout << "\n" << std::string(70, '*') << std::endl;
    std::cout << "        ALL TESTS COMPLETED" << std::endl;
    std::cout << std::string(70, '*') << std::endl;

    return 0;
}
