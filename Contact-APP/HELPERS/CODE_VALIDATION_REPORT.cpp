/**
 * =====================================================
 * CONTACT APP - CODE VALIDATION & BUG REPORT
 * =====================================================
 * 
 * This document contains a detailed analysis of bugs and issues found
 * in the Contact App codebase, along with their locations and fixes.
 */

// =====================================================
// CRITICAL BUGS FOUND
// =====================================================

/*
 * BUG #1: DUPLICATE MEMBER VARIABLE IN Contacts.hpp
 * ===================================================
 * Location: Contact_Class/Contacts.hpp (Lines 11-12)
 * Severity: CRITICAL - Will cause compilation error
 * 
 * Issue:
 *   std::string Mygroup;     // Line 11 - DUPLICATE
 *   Contactgroup Mygroup;    // Line 12 - CORRECT
 * 
 * Problem:
 *   - Declares Mygroup as both std::string and Contactgroup
 *   - This causes a compilation error: "redeclaration of 'Mygroup'"
 *   - The std::string version should be REMOVED
 * 
 * Fix:
 *   REMOVE line: std::string Mygroup;
 *   KEEP: Contactgroup Mygroup;
 */

/*
 * BUG #2: MISSING BREAK IN Contact_store_class.cpp (Line 154)
 * ============================================================
 * Location: Contact_store_Class/Contact_store_class.cpp
 * Severity: HIGH - Logic error in file parsing
 * 
 * Issue:
 *   case 3:
 *       Temp_contact.SET_Phone_Number(token);
 *   case 4:  // <-- MISSING break statement
 *       Temp_contact.SET_Company(token);
 * 
 * Problem:
 *   - Missing break statement after case 3
 *   - This causes fall-through: if count==3, it sets Phone_Number AND Company
 *   - The next case 4 will execute even though it shouldn't
 *   - All subsequent phone numbers will be overwritten with company data
 * 
 * Fix:
 *   Add "break;" after SET_Phone_Number(token);
 * 
 * Corrected Code:
 *   case 3:
 *       Temp_contact.SET_Phone_Number(token);
 *       break;  // <-- ADD THIS
 *   case 4:
 *       Temp_contact.SET_Company(token);
 *       break;
 */

/*
 * BUG #3: UNSAFE POINTER RETURNED FROM Search_by_Name()
 * =======================================================
 * Location: Contact_store_Class/Contact_store_class.cpp (Line 48)
 * Severity: MEDIUM - Dangling pointer risk
 * 
 * Issue:
 *   Contacts* Contact_store_class::Search_by_Name(...)
 *   {
 *       auto itr = std::find_if(...);
 *       if(itr != Contact_Book.end())
 *       {
 *           return &(*itr);  // <-- DANGEROUS
 *       }
 *   }
 * 
 * Problem:
 *   - Returns pointer to element in std::vector
 *   - If vector reallocates (due to Add_contact), pointer becomes INVALID
 *   - Using the pointer after adding new contacts causes undefined behavior
 *   - This is a use-after-free vulnerability
 * 
 * Recommended Fix:
 *   Option 1: Return iterator instead of pointer
 *   Option 2: Return const reference instead of pointer
 *   Option 3: Document that returned pointer is only valid until next modification
 *   Option 4: Store contacts in std::list or other container that doesn't reallocate
 * 
 * Best Practice:
 *   Consider refactoring to avoid raw pointers:
 *   - Use std::reference_wrapper<Contacts>
 *   - Return std::optional<std::reference_wrapper<Contacts>>
 */

/*
 * BUG #4: INCOMPLETE DISPLAYBYGROUP() IMPLEMENTATION
 * ===================================================
 * Location: Contact_store_Class/Contact_store_class.cpp
 * Severity: MEDIUM - Feature not implemented
 * 
 * Issue:
 *   The method is declared in .hpp but NOT implemented in .cpp
 *   void DisplayByGroup(Contactgroup group) const;
 * 
 * Problem:
 *   - Method declaration exists but implementation is missing
 *   - Will cause linker error if called
 *   - Feature advertised but not functional
 * 
 * Fix:
 *   Implement the method in Contact_store_class.cpp:
 *   
 *   void Contact_store_class::DisplayByGroup(Contactgroup group) const
 *   {
 *       std::cout << "==============================\n";
 *       for (const auto &contact : Contact_Book)
 *       {
 *           if (contact.Get_Group() == group)
 *           {
 *               contact.Print_ContactData();
 *           }
 *       }
 *       std::cout << "==============================\n";
 *   }
 */

/*
 * BUG #5: UNUSED INCLUDES IN Contact_store_class.hpp
 * ===================================================
 * Location: Contact_store_Class/Contact_store_class.hpp (Lines 4-6)
 * Severity: LOW - Code cleanliness issue
 * 
 * Issue:
 *   #include "sstream"
 *   #include "filesystem"
 *   #include "fstream"
 * 
 * Problem:
 *   - These should be in .cpp file, not header
 *   - Headers should only include what they directly need
 *   - Increases compilation time for users of this header
 * 
 * Fix:
 *   Move these includes to Contact_store_class.cpp
 *   Keep only: #include "./../Contact_Class/Contacts.hpp"
 *             #include <vector>
 *             #include <algorithm>
 */

/*
 * BUG #6: INCONSISTENT INCLUDE GUARD / HEADER STRUCTURE
 * =======================================================
 * Location: Contact_Class/Contacts.hpp
 * Severity: LOW - Best practices
 * 
 * Issue:
 *   Missing #ifndef / #define / #endif guards
 * 
 * Problem:
 *   - Can lead to multiple inclusion issues
 *   - Should use either #pragma once or traditional guards
 * 
 * Fix:
 *   Add at top of Contacts.hpp:
 *   #ifndef CONTACTS_HPP
 *   #define CONTACTS_HPP
 *   
 *   Add at end of Contacts.hpp:
 *   #endif
 */

/*
 * BUG #7: MAGIC PATH IN Contact_store_class.hpp
 * ===============================================
 * Location: Contact_store_Class/Contact_store_class.hpp (Line 7)
 * Severity: MEDIUM - Portability issue
 * 
 * Issue:
 *   const fs::path phonebook{std::move("./Contact-APP/utilities/Phonebook.csv")};
 * 
 * Problem:
 *   - Hard-coded path will only work from specific directory
 *   - Will break if run from different location
 *   - Should use relative paths or configuration
 *   - Directory might not exist
 * 
 * Fix:
 *   Make path configurable or create it dynamically
 */

// =====================================================
// CODE QUALITY ISSUES
// =====================================================

/*
 * ISSUE #1: Inconsistent naming conventions
 * - Variables: Contact_Book, Mygroup (inconsistent snake_case vs camelCase)
 * - Methods: Add_contact vs SET_FirstName (inconsistent)
 * - Use either snake_case OR camelCase consistently
 * 
 * ISSUE #2: No input validation
 * - Empty strings accepted for names and phone numbers
 * - No format validation for phone numbers
 * - No error handling for invalid group values
 * 
 * ISSUE #3: Print statements in business logic
 * - std::cout used directly in methods (tightly coupled to console)
 * - Should use a logger or pass output stream
 * - Makes testing difficult
 * 
 * ISSUE #4: No const correctness on Add_contact
 * - Takes Contacts && (rvalue reference)
 * - But Contacts has no move constructor/assignment
 * - Should be clearer whether this moves or copies
 * 
 * ISSUE #5: Missing destructor cleanup
 * - Contact_Book vector automatically cleaned by destructor
 * - But if you add dynamic memory later, you'll forget
 * - Consider explicitly clearing
 */

// =====================================================
// SUMMARY
// =====================================================

/*
 * CRITICAL ISSUES TO FIX IMMEDIATELY:
 * 1. Remove duplicate "std::string Mygroup;" from Contacts.hpp
 * 2. Add missing "break;" statement in case 3 of Load_all_contacts()
 * 3. Implement DisplayByGroup() method
 * 
 * IMPORTANT ISSUES TO FIX:
 * 4. Redesign pointer return from Search_by_Name() - use safer alternatives
 * 5. Move filesystem-related includes to .cpp file
 * 6. Add header guards to .hpp files
 * 7. Fix hard-coded file path
 * 
 * NICE TO FIX:
 * 8. Standardize naming conventions
 * 9. Add input validation
 * 10. Decouple from std::cout (use logging instead)
 */
