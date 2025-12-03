#include <iostream>
#include <cmath>
#include <unordered_map>
#include <vector>
#include <algorithm>
#include <limits>
#include <string>
#include <sstream>
using namespace std;
class Solution {
public:
       bool areNumbersAscending(string s) 
    {
        std::string token;
        std::stringstream ss(s);
        int prevNum{-1};
        while (ss >> token)
        {
            if (isdigit(token[0]))
            {
                int num = stoi(token);
                if(num > prevNum)
                {
                    prevNum = num;
                }
                else
                {
                    return false;
                }
                cout << "Extracted: " << num << " | Previous: " << prevNum << endl;
            }
        }
        return true;
    }
};


class Solution_myAtoi
{
public:
    int myAtoi(string s)
        {
        int i = 0;
        int n = s.length();
        
        // Step 1: Skip leading whitespace
        while (i < n && s[i] == ' ') {
            i++;
        }
        
        // Step 2: Determine the sign
        int sign = 1;
        if (i < n && (s[i] == '-' || s[i] == '+')) {
            if (s[i] == '-') {
                sign = -1;
            }
            i++;
        }
        
        // Step 3: Convert digits, handling overflow
        long long result = 0;
        while (i < n && isdigit(s[i])) {
            int digit = s[i] - '0';
            result = result * 10 + digit;
            
            // Step 4: Handle overflow for positive numbers
            if (result > std::numeric_limits<int>::max()) {
                return sign == 1 ? std::numeric_limits<int>::max() : std::numeric_limits<int>::min();
            }
            
            i++;
        }
        
        result *= sign;
        
        // Step 4: Clamp to 32-bit signed integer range
        if (result < std::numeric_limits<int>::min())
        {
            return std::numeric_limits<int>::min();
        }
        if (result > std::numeric_limits<int>::max())
        {
            return std::numeric_limits<int>::max();
        }
        
        return (int)result;
    }

    int myAtoi_map(string s)
    {
        // Create a map for digit validation and conversion
        unordered_map<char, int> digitMap;
        digitMap['0'] = 0;
        digitMap['1'] = 1;
        digitMap['2'] = 2;
        digitMap['3'] = 3;
        digitMap['4'] = 4;
        digitMap['5'] = 5;
        digitMap['6'] = 6;
        digitMap['7'] = 7;
        digitMap['8'] = 8;
        digitMap['9'] = 9;

        int i = 0;
        int n = s.length();
        signed long result = 0;
        bool negFlag = false;
        // bool signFound = false;  // Track if we've already found a sign

        // Step 1: Skip leading whitespace
        while (i < n && s[i] == ' ') {
            i++;
        }

        // Step 2: Check for sign character
        if (i < n && (s[i] == '-' || s[i] == '+')) {
            if (s[i] == '-') {
                negFlag = true;
            }
            // signFound = true;
            i++;
        }

        // Step 3: Convert digits
        while (i < n) {
            auto itr = digitMap.find(s[i]);

            // If character is a digit, add it to result
            if (digitMap.end() != itr) {
                int digit = itr->second;
                result = result * 10 + digit;

                // Check overflow before it gets out of hand
                if (negFlag && (-result) < numeric_limits<int>::min()) {
                    return numeric_limits<int>::min();
                }
                if (!negFlag && result > numeric_limits<int>::max()) {
                    return numeric_limits<int>::max();
                }
            } 
            // If not a digit, stop processing
            else {
                break;
            }
            i++;
        }

        // Step 4: Apply sign and return
        result = negFlag ? -result : result;
        return static_cast<int>(result);
    }
};


class Solution_palindrome {
public:
    int getDigitCount(int x) {
        if (x == 0) return 1;
        return static_cast<int>(log10(x)) + 1;
    }

    int getnumber(int x, int pos) {
        return (x / static_cast<int>(pow(10, pos))) % 10;
    }

    std::string isPalindrome(int x) {
        if (x < 0) return "false";

        int count = getDigitCount(x);
        int left = count - 1;
        int right = 0;

        while (right < left) {
            if (getnumber(x, right) != getnumber(x, left)) {
                return "false";
            }
            right++;
            left--;
        }
        return "true";
    }
};

class Solution_roman {
public:
    int romanToInt(string s) {
        // Create map of Roman numerals to integer values
        unordered_map<char, int> roman = {
            {'I', 1},
            {'V', 5},
            {'X', 10},
            {'L', 50},
            {'C', 100},
            {'D', 500},
            {'M', 1000}
        };
        
        int sum{0},n{0};
        while(n <static_cast<int>(s.length()))
        {
            // std::cout << roman[s[n]]<<endl;
            if(roman[s[n]] >= roman[s[n+1]])
                sum += roman[s[n]];
            else
                sum -= roman[s[n]];
            n++;
        }  
        return sum;
    }
};

class Solution_reverse {
public:
    int reverse(int x) 
    {
        signed long long result{0};
        while(x != 0)
        {
            result = result*10 + x%10;
            x= x/10; 
        }
        return (abs(result) >= std::numeric_limits<int>::max()) ?  0 : static_cast<int>(result);
    }
};


//Definition for singly-linked list.
struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution_Linked_list_merge {
public:
    
    ListNode* mergeTwo_unsorted_linked_Lists(ListNode* list1, ListNode* list2)
    {
        vector<int> result;
        while(!(list1))
        {
            result.push_back(list1->val);
            list1 = list1->next;
        }
        while(!(list2))
        {
            result.push_back(list2->val);
            list2 = list2->next;
        }
        sort(result.begin(), result.end());
        if(result.empty()) 
            return nullptr;
        
        ListNode *head = new ListNode(result[0]);
        ListNode *current = head;
        for (auto x : result)
        {
            current->next = new ListNode(x);
            current = current->next;
        }
        return head;
    }
    // Method 2: Optimal solution (without extra space)
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        // Create a dummy node to simplify logic
        ListNode dummy(0);
        ListNode* tail = &dummy;
        
        // Merge while both lists have nodes
        while(list1 != nullptr && list2 != nullptr) {
            if(list1->val <= list2->val) {
                tail->next = list1;
                list1 = list1->next;
            } else {
                tail->next = list2;
                list2 = list2->next;
            }
            tail = tail->next;
        }
        
        // Attach remaining nodes
        if(list1 != nullptr) {
            tail->next = list1;
        } else {
            tail->next = list2;
        }
        
        return dummy.next;
    }
};


int main()
{
    // Create a dynamic array using new. Example: allocate 5 ints.
    // size_t n = 5;
    // int *ptr = new int[n];
    // for (size_t i = 0; i < n; ++i)
    //     ptr[i] = static_cast<int>(i) + 1; // fill the array with 1..5
    // auto x{3.4}, y{33.223};
    // std::cout << "Add(x,y) = " << Add(x,y) << std::endl;
    // std::cout << "ArraySum(ptr, n) = " << ArraySum(ptr, n) << std::endl;
    // // Free the dynamically allocated array
    // delete [] ptr;
    //Solution_palindrome s1;
    // Solution_roman s2;
    //std::cout<< s1.isPalindrome(1123)<<std::endl;
    // std::cout <<s2.romanToInt("x")<<std::endl;
    // cout<<s2.romanToInt("LVIII")<<endl;
    // Solution_myAtoi myatoi_dummy;
    // cout << myatoi_dummy.myAtoi_map("-042");
    // Solution Trial;
    // cout <<Trial.areNumbersAscending("hello world 5 x 5");
    Solution sol;
    sol.areNumbersAscending("hello 55 hello 55");
    return 0;
}