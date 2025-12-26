#include <iostream>
#include <cmath>
#include <unordered_map>
#include <vector>
#include <algorithm>
#include <limits>
#include <string>
#include <sstream>
#include <unordered_set>
#include <array>
#include <format>
#include <memory>
using namespace std;
std::array<int,5> mohy{1,2,5,4,67};
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

class student
{
private:
    std::string First_name;
    std::string Last_name;
    int age,standard;
public:
    student();
    ~student();
    void set_age(int &objage);
    void set_Firstname(std::string &name);
    void set_Lastname(std::string &name);
    void set_stand(int &stdrd);
    int getage()const;
    int getstand()const;
    std::string getfirst()const;
    std::string getlast()const;
    std::string to_string();

};
student::student()
{}
student::~student()
{}
int student::getage()const
{
    return this->age;
}
void student::set_age(int &objage)
{
    age = objage;
}   
void student::set_stand(int &stdrd)
{
    standard = stdrd;
}
int student::getstand()const
{
    return this->standard;
}
void student::set_Firstname(std::string &name)
{
    First_name = name;
}
void student::set_Lastname(std::string &name)
{
    Last_name = name;
}
std::string student::getfirst()const
{
    return this->First_name;
}
std::string student::getlast()const
{
    return this->Last_name;
}
std::string student::to_string()
{
     
    return std::to_string(this->age) + ','+ this->First_name +','+ this->Last_name + ','+ std::to_string(this->standard);
    // return std::format("{},{},{},{}",age,First_name,Last_name,standard);
}
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


class Solution_container
{
public:
    int maxArea(vector<int>& height) {
        int area{0},leftwall{0};
        int rightwall =height.size()-1;
        while(leftwall < rightwall)
        {
            int y_axis = min(height[leftwall],height[rightwall]);
            int x_axis = rightwall -leftwall;
            int temparea = x_axis *y_axis;
            area  = max(temparea, area);
            if(height[leftwall] <height[rightwall])
            {
                ++leftwall;
            }
            else
            {
                --rightwall ;
            }
        }

        return area;
    }
};

class Solution_commonPrefix
{
public:
    string longestCommonPrefix(vector<string>& strs)
    {
        if(strs.empty())
        {
            return "";
        }
        std::string firststring = strs[0];
        for(int i=0 ; i <strs.size();i++)
        {
            while(strs[i].find(firststring))
            {
                // firststring = firststring.substr(0,firststring.size()-1);
                firststring.pop_back();
                if(firststring.empty())
                {
                    return "";
                }
            }
        }
        return firststring;
    }
};
class Solution_reportspam {
public:
    // bool reportSpam(vector<string>& message, vector<string>& bannedWords)
    // {
    //     int counter{0};
    //     while(!(message.empty()))
    //     {
    //         if(find(bannedWords.begin(),bannedWords.end(),message[message.size()-1]) != bannedWords.end())
    //         {
    //             counter++;
    //         }
    //         message.pop_back();
    //         if(counter>=2)
    //         {
    //             return true;
    //         }
    //     }
    //     return false;
    // }
    bool reportSpam(vector<string>& message, vector<string>& bannedWords)
    {
        int count{0};
        std::unordered_set<string> bannedset(bannedWords.begin(),bannedWords.end());
        for(const auto &word : message)
        {
            if(bannedset.count(word) && ++count >=2)
            {
                return true;
            }
        }
        return false;
    }

};


int max_of_four(int a, int b, int c, int d) 
{
    int max{};
    std::array<int,4> array{a,b,c,d};
    auto itr = max_element(array.begin(),array.end());
    std::cout<< *(itr)<<std::endl;
    for(auto &x : array)
    {
      max =  x > max ?  x : max ; 
    }
    return max;
}
void manipulate(int *a , int *b)
{
    int temp{};
    temp = *(a) + *(b);
    *(b) = abs(*(a) - *(b));
    *a = temp;
}   
void variable_sized_queries()
{
       int vectormembers{},quernum{};
    std::vector<std::vector<int>> bigVEC{};
    std::cin>>vectormembers>>quernum;
    for(int rows =0 ;rows<vectormembers; rows++)
    {
        int ColumnNum{};
        std::cin>>ColumnNum;
        std::vector<int> tempvector;        
        for(int columns = 0 ; columns< ColumnNum ; columns++)
        {
            int temp{};
            std::cin>>temp;
            tempvector.push_back(temp);
            
        }
        bigVEC.push_back(tempvector);
    }
    for(int que = 0 ; que<quernum ; que++)
    {
        int row,col;
        std::cin>>row>>col;
        std::cout<<bigVEC[row][col]<<std::endl;
    }
    for(auto x :bigVEC)
    {
        for(auto y : x)
        {
            std::cout<<y<<',';
        }
        std::cout<<'\n';
    }
}

struct Workshop{
    int starttime = 0 , duration = 0, endtime = 0;
    
    Workshop(int _startime, int _duration){
        starttime = _startime;
        duration = _duration;
        endtime = _startime + _duration;
    }
    
};

struct Available_Workshops{
    int len = 0;
    vector<Workshop> workshops;
    
    Available_Workshops(int _len, vector<Workshop> _workshops){
        len=_len;
        workshops=_workshops;
    }

};

Available_Workshops* initialize(int* startime, int* duration, int n){
    vector<Workshop> workshops;
        
    for (int i = 0; i<n; i++) {
        workshops.emplace_back(startime[i], duration[i]);      
    }
        
    return new Available_Workshops(n, workshops);
}

int CalculateMaxWorkshops(Available_Workshops* ptr){
    int current_end = 0, scheduled = 0;

    vector<Workshop> workshops = ptr->workshops;
    
    sort(workshops.begin(), workshops.end(), [](const Workshop& a, const Workshop& b) {
        return a.endtime < b.endtime;
    });
    
    for (Workshop& w : workshops){
        if (w.starttime >= current_end) {
            scheduled++;
            current_end = w.endtime;
        }
    }
    
    return scheduled;
}
class Solutio_ndups {
public:
    std::vector<int> removeDuplicates(vector<int>& nums)
    {
        std::vector<int> resultV;
        auto itr = nums.begin();
        while(itr!= nums.end() && itr <nums.end())
        {
            if(*itr == *(itr+1))
            {
            }
            else
            {
                resultV.push_back(*itr);
            }
            itr +=1;

        }
        return resultV;
    }
};
class SolutionRemdup {
public:
    int removeDuplicates(vector<int>& nums) {
        if (nums.empty()) return 0;
        
        int k = 1; // Position to place the next unique element
        
        for (int i = 1; i < nums.size(); i++)
        {
            if (nums[i] != nums[i-1])
            {
                nums[k] = nums[i];
                k++;
            }
        }
        
        return k;
    }
};

class Solution_dups {
public:
    int getOnlyDups(vector<int>& nums)
    {
        std::vector<int> resultV;
        for(auto x :nums)
        {
            auto itr = std::find(nums.begin(),nums.end(),x);
            if(itr!= nums.end())
            {
                if(std::find(itr+1,nums.end(),x)!= nums.end())
                {
                    resultV.push_back(x);
                }
                else
                {
                }
            }
        }
     
        return resultV.size();
    }
};

class Solution_otherdup
{
public:
    int removeElement(vector<int>& nums, int val)
    {
        int count = 0;
        for(int i=0; i< nums.size(); ++i)
        {
            if(nums[i]!= val)
            {
                nums[count] = nums[i];
                count++;
            }
            else
            {
                //pass
            }
        }   
       
    }
};

class Person{
protected:
    std::string name;
    int age;
public:
    Person(){}
    virtual ~Person(){}  // Virtual destructor for base class!
    virtual void putdata() const = 0;
    virtual void getdata() = 0;
};

class Professor: public Person{
private:
    int publications;
    int cur_id;
    static int Professor_sequentialid;
public:
    Professor()
    {
        cur_id = ++Professor_sequentialid;  // Assign unique ID
    }
    
    void putdata() const override 
    {
        std::cout << name << ' ' << age << ' ' << publications << ' ' << cur_id << std::endl;
    }
    
    void getdata() override
    {
        std::cin >> name >> age >> publications;
    }
};

class Student: public Person{
private:
    int cur_id;
    int* marks;
    static int Student_sequentialid;
public:
    Student()
    {
        cur_id = ++Student_sequentialid;  // Assign unique ID
        marks = new int[6];
    }
    
    ~Student()
    {
        delete[] marks;  // Clean up memory
    }
    
    void putdata() const override
    {
        int marksum = 0;
        for(int i = 0; i < 6; ++i)
        {
            marksum += marks[i];
        }
        std::cout << name << ' ' << age << ' ' << marksum << ' ' << cur_id << std::endl;
    }
    
    void getdata() override
    {
        std::cin >> name >> age;
        for(int i = 0; i < 6; ++i)
        {
            std::cin >> marks[i];
        }
    }
};

// MUST define static variables
int Professor::Professor_sequentialid = 0;
int Student::Student_sequentialid = 0;

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
    // Solution sol;
    // sol.areNumbersAscending("hello 55 hello 55");
    // Solution_container S1;
    // std::vector<int> Test{1,1};
    // std::cout<<'\n';
    // std::cout<< S1.maxArea(Test)<<std::endl;   
    //std::cout<< max_of_four(1,4,62,212);
    // int *a = new int();
    // int *b = new int();  
    // std::cin>> *(a)>>*(b);
    // manipulate(a,b);
    // std::cout<<a<<endl;
    // std::cout<<b<<endl;
    // for(auto x: mohy)
    // {
    //     std::cout<<x<<'\n';
    // }
    // workshop *Workshops = new workshop[arrsize];
    // int n; // number of workshops
    // cin >> n;
    // // create arrays of unknown size n
    // int* start_time = new int[n];
    // int* duration = new int[n];

    // for(int i=0; i < n; i++){
    //     cin >> start_time[i];
    // }
    // for(int i = 0; i < n; i++){
    //     cin >> duration[i];
    // }

    // Available_Workshops * ptr;
    // ptr = initialize(start_time,duration, n);
    // cout << CalculateMaxWorkshops(ptr) << endl;
    // Solutio_ndups n1;
    // std::vector<int> DummyVec{1,1,2,3,3,5};
    // for(auto x :n1.removeDuplicates(DummyVec))
    // {
    //     std::cout << x <<'\t';
    // }
    int n, val;
    cin>>n; //The number of objects that is going to be created.
    Person *per[n];

    for(int i = 0;i < n;i++){

        cin>>val;
        if(val == 1){
            // If val is 1 current object is of type Professor
            per[i] = new Professor;

        }
        else per[i] = new Student; // Else the current object is of type Student

        per[i]->getdata(); // Get the data from the user.

    }

    for(int i=0;i<n;i++)
        per[i]->putdata(); // Print the required output for each object.

    return 0;
}