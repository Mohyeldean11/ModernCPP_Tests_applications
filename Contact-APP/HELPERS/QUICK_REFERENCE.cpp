/**
 * =====================================================
 * CONTACT APP - QUICK REFERENCE GUIDE
 * =====================================================
 * 
 * This file provides quick access to important information
 * about the Contact App implementation.
 */

// =====================================================
// CONTACTS CLASS - PUBLIC API
// =====================================================

/*
 * CONSTRUCTORS:
 * =============
 * Contacts();
 *   - Creates empty contact (all fields empty)
 * 
 * Contacts(const string &first_name,
 *          const string &lastname,
 *          const string &phone_number,
 *          const string &company_name = "NA",
 *          Contactgroup group = Contactgroup::DEFAULT);
 *   - Creates contact with all fields
 *   - company_name defaults to "NA"
 *   - group defaults to Contactgroup::DEFAULT
 * 
 * EXAMPLE:
 *   Contacts c1("Ahmed", "Hassan", "01001234567", "Google", Contactgroup::FRIENDS);
 *   Contacts c2("Sara", "Ali", "01101234567");  // Uses defaults
 */

/*
 * GETTER METHODS:
 * ===============
 * string Get_FirstName() const;
 * string Get_LastName() const;
 * string Get_Phone_Number() const;
 * string Get_Company() const;
 * Contactgroup Get_Group() const;
 * 
 * EXAMPLE:
 *   cout << c1.Get_FirstName() << endl;  // Prints: Ahmed
 *   cout << c1.Get_Phone_Number() << endl;  // Prints: 01001234567
 */

/*
 * SETTER METHODS:
 * ===============
 * void SET_FirstName(const string &var);
 * void SET_LastName(const string &var);
 * void SET_Phone_Number(const string &var);
 * void SET_Company(const string &var);
 * void SET_Group(const string &var);  // String converted to enum
 * 
 * EXAMPLE:
 *   c1.SET_LastName("Mohamed");
 *   c1.SET_Company("Microsoft");
 *   c1.SET_Group("2");  // Converts to Contactgroup::FAMILY
 */

/*
 * DISPLAY METHOD:
 * ===============
 * void Print_ContactData() const;
 *   - Prints contact info to console
 * 
 * OUTPUT FORMAT:
 *   Name : Ahmed Hassan
 *   Phone number : 01001234567
 *   Company : Google
 */

/*
 * OPERATORS:
 * ==========
 * bool operator<(const Contacts &obj) const;
 *   - Compares first names alphabetically
 *   - Used for sorting
 * 
 * EXAMPLE:
 *   Contacts c1("Ahmed", ...);
 *   Contacts c2("Ziad", ...);
 *   if (c1 < c2) cout << "Ahmed comes before Ziad" << endl;
 */

// =====================================================
// CONTACT GROUP ENUM VALUES
// =====================================================

/*
 * Contactgroup::DEFAULT   (0)   - Default group
 * Contactgroup::COWORKERS (1)   - Work colleagues
 * Contactgroup::FAMILY    (2)   - Family members
 * Contactgroup::FRIENDS   (3)   - Friends
 * 
 * USAGE:
 *   Contactgroup myGroup = Contactgroup::FRIENDS;
 *   int groupValue = static_cast<int>(myGroup);  // Gets numeric value
 */

// =====================================================
// CONTACT_STORE_CLASS - PUBLIC API
// =====================================================

/*
 * MANAGEMENT METHODS:
 * ====================
 * 
 * 1. ADD CONTACT
 *    -----------
 *    void Add_contact(Contacts &&contact);
 * 
 *    EXAMPLE:
 *      Contact_store_class store;
 *      store.Add_contact(Contacts("Ahmed", "Hassan", "01001234567", 
 *                                 "Google", Contactgroup::COWORKERS));
 *    
 *    OUTPUT:
 *      Contact has been added...
 * 
 * 
 * 2. SEARCH BY NAME
 *    ---------------
 *    Contacts* Search_by_Name(const string &name, bool WhichName);
 * 
 *    Parameters:
 *      - name: Name to search for
 *      - WhichName: false = search FirstName, true = search LastName
 * 
 *    Return:
 *      - Pointer to first matching Contact (or nullptr if not found)
 * 
 *    EXAMPLES:
 *      // Search by first name
 *      Contacts* c = store.Search_by_Name("Ahmed", false);
 *      if (c != nullptr) cout << c->Get_Phone_Number() << endl;
 * 
 *      // Search by last name
 *      Contacts* c = store.Search_by_Name("Hassan", true);
 *      if (c == nullptr) cout << "Not found" << endl;
 * 
 *    NOTE: Pointer becomes invalid after calling Add_contact()
 * 
 * 
 * 3. REMOVE BY NAME
 *    ---------------
 *    void Remove_by_Name(const string &name, bool WhichName);
 * 
 *    Parameters:
 *      - name: Name of contact to remove
 *      - WhichName: false = remove by FirstName, true = remove by LastName
 * 
 *    EXAMPLES:
 *      // Remove by first name
 *      store.Remove_by_Name("Ahmed", false);
 *      
 *      // Remove by last name
 *      store.Remove_by_Name("Hassan", true);
 * 
 *    OUTPUT:
 *      Contact was deleted..
 *      OR
 *      This name was not found in your contact book...
 */

/*
 * DISPLAY METHODS:
 * =================
 * 
 * 1. DISPLAY ALL
 *    -----------
 *    void DisplayAll() const;
 * 
 *    Shows all contacts in formatted output
 * 
 *    EXAMPLE:
 *      store.DisplayAll();
 * 
 *    OUTPUT:
 *      ==============================
 *      Name : Ahmed Hassan
 *      Phone number : 01001234567
 *      Company : Google
 *      
 *      Name : Sara Ali
 *      ...
 *      ==============================
 * 
 * 
 * 2. DISPLAY BY GROUP
 *    -----------------
 *    void DisplayByGroup(Contactgroup group) const;
 * 
 *    Shows only contacts in specified group
 * 
 *    EXAMPLE:
 *      store.DisplayByGroup(Contactgroup::FAMILY);
 * 
 *    OUTPUT:
 *      ==============================
 *      Contacts in Group 2:
 *      Name : Fatima Mohamed
 *      Phone number : 01101234567
 *      Company : Google
 *      ==============================
 */

/*
 * SORTING METHOD:
 * ================
 * 
 * void Sort_By_A_D_Name(bool orderFlag);
 * 
 * Sorts contacts by first name and displays them
 * 
 * Parameters:
 *   - orderFlag: true = Ascending (A-Z)
 *   - orderFlag: false = Descending (Z-A)
 * 
 * EXAMPLES:
 *   store.Sort_By_A_D_Name(true);   // A-Z order
 *   store.Sort_By_A_D_Name(false);  // Z-A order
 * 
 * NOTE: Automatically calls DisplayAll() after sorting
 */

/*
 * FILE I/O METHODS:
 * ==================
 * 
 * 1. LOAD CONTACTS
 *    ---------------
 *    void Load_all_contacts();
 * 
 *    Loads contacts from CSV file
 *    File path: ./Contact-APP/utilities/Phonebook.csv
 * 
 *    CSV Format:
 *      FirstName,LastName,PhoneNumber,Company,GroupNumber
 * 
 *    EXAMPLE:
 *      store.Load_all_contacts();
 *    
 *    BEHAVIOR:
 *      - Creates file if it doesn't exist
 *      - Creates directory if needed
 *      - Parses CSV and loads contacts
 * 
 *    REQUIREMENTS:
 *      - Directory must be writable
 *      - CSV must be in correct format
 * 
 * 
 * 2. SAVE CONTACTS
 *    ---------------
 *    void Save_all_contacts();
 * 
 *    Saves all contacts to CSV file
 * 
 *    EXAMPLE:
 *      store.Add_contact(Contacts(...));
 *      store.Save_all_contacts();
 * 
 *    OUTPUT:
 *      file ./Contact-APP/utilities/Phonebook.csv is saved
 * 
 *    NOTE: Overwrites existing file
 */

// =====================================================
// COMMON USAGE PATTERNS
// =====================================================

/*
 * PATTERN 1: Create and add a contact
 * ====================================
 * Contact_store_class store;
 * store.Add_contact(Contacts("Ahmed", "Hassan", "01001234567", 
 *                           "Google", Contactgroup::COWORKERS));
 * store.DisplayAll();
 */

/*
 * PATTERN 2: Search and modify
 * =============================
 * Contacts* contact = store.Search_by_Name("Ahmed", false);
 * if (contact != nullptr) {
 *     contact->SET_Phone_Number("01101234567");
 *     contact->SET_Company("Microsoft");
 * }
 */

/*
 * PATTERN 3: Remove a contact
 * ============================
 * store.Remove_by_Name("Ahmed", false);  // By first name
 * // OR
 * store.Remove_by_Name("Hassan", true);  // By last name
 */

/*
 * PATTERN 4: Sort and display
 * ============================
 * store.Sort_By_A_D_Name(true);   // Sorts and displays
 */

/*
 * PATTERN 5: Filter by group
 * ===========================
 * store.DisplayByGroup(Contactgroup::FAMILY);
 */

/*
 * PATTERN 6: Complete workflow
 * =============================
 * Contact_store_class phonebook;
 * 
 * // Add contacts
 * phonebook.Add_contact(Contacts("Ahmed", "Hassan", "01001234567", "Google", 
 *                               Contactgroup::COWORKERS));
 * phonebook.Add_contact(Contacts("Fatima", "Mohamed", "01101234567", "Microsoft",
 *                               Contactgroup::FAMILY));
 * 
 * // Display
 * phonebook.DisplayAll();
 * 
 * // Search
 * Contacts* c = phonebook.Search_by_Name("Ahmed", false);
 * if (c) cout << "Found: " << c->Get_Phone_Number() << endl;
 * 
 * // Sort
 * phonebook.Sort_By_A_D_Name(true);
 * 
 * // Remove
 * phonebook.Remove_by_Name("Fatima", false);
 * 
 * // Save
 * phonebook.Save_all_contacts();
 */

// =====================================================
// IMPORTANT NOTES
// =====================================================

/*
 * 1. POINTER VALIDITY
 *    - Search_by_Name() returns a pointer to internal vector element
 *    - This pointer becomes INVALID after calling Add_contact()
 *    - Best practice: Use pointer immediately, don't store it
 * 
 * 2. SEARCH BEHAVIOR
 *    - Search returns FIRST match only
 *    - If multiple contacts have same name, only first is returned
 *    - Case-sensitive: "Ahmed" ≠ "ahmed"
 * 
 * 3. REMOVE BEHAVIOR
 *    - Removes FIRST match only
 *    - If duplicates exist, use LastName search to remove specific one
 * 
 * 4. SORTING
 *    - Sorts by FIRST NAME only
 *    - Uses alphabetical comparison
 *    - Automatically displays result
 * 
 * 5. CSV FILE FORMAT
 *    - Comma-separated values
 *    - Each line: FirstName,LastName,Phone,Company,GroupNumber
 *    - GroupNumber: 0=DEFAULT, 1=COWORKERS, 2=FAMILY, 3=FRIENDS
 *    - Example: Ahmed,Hassan,01001234567,Google,1
 * 
 * 6. DEFAULT VALUES
 *    - Company: "NA" (if not specified)
 *    - Group: Contactgroup::DEFAULT (if not specified)
 */

// =====================================================
// ERROR HANDLING
// =====================================================

/*
 * SEARCH NOT FOUND:
 *   Contacts* c = store.Search_by_Name("John", false);
 *   if (c == nullptr) {
 *       cout << "Contact not found" << endl;
 *   }
 * 
 * REMOVE NOT FOUND:
 *   Output: "This name was not found in your contact book..."
 * 
 * FILE I/O ERRORS:
 *   - Load failures are caught and printed to cerr
 *   - Save failures are caught and printed to cerr
 *   - Program continues even if file operations fail
 */

// =====================================================
// COMPILATION COMMAND
// =====================================================

/*
 * Quick compile all:
 * 
 * g++ -std=c++17 -Wall -Wextra \
 *     Contact_Class/Contacts.cpp \
 *     Contact_store_Class/Contact_store_class.cpp \
 *     integration_tests.cpp \
 *     -o integration_tests && ./integration_tests
 */

// =====================================================
// STATUS: READY FOR UI INTEGRATION
// =====================================================

/*
 * ✓ All classes fully functional
 * ✓ All critical bugs fixed
 * ✓ Comprehensive testing in place
 * ✓ API documented
 * ✓ Ready for Operation class and UI implementation
 */
