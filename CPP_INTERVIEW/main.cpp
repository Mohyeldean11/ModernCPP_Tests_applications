#include <memory>
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1,vector<int>& nums2)
    {
        
        double result{0};
        nums1.insert(nums1.end(),nums2.begin(),nums2.end());
        sort(nums1.begin(),nums1.end());
        // for(auto x : nums1)
        // {
        //     cout<< x<<",";
        // }
        // if(nums1.size() % 2 == 0)
        // {
        //     result =  ((static_cast<double>(nums1[nums1.size()/2])) + (static_cast<double>(nums1[(nums1.size()/2)-1])))/2; 
        //     return result;
        // }
        (nums1.size()%2 ==0) ?  result =  ((static_cast<double>(nums1[nums1.size()/2])) + (static_cast<double>(nums1[(nums1.size()/2)-1])))/2 : result = nums1[nums1.size()/2]; 
        // else
        // {
        //     result = nums1[nums1.size()/2]; 
        //     return result;

        // }
        // // std::cout << nums1 << std::endl;
        // cout<<" '\n' the median is = ";
        return   result;
        
    }
};


int main()
{
    vector<int> mohy1{1,4,21};
    vector<int> mohy2{12,42,};

    Solution s1;
    cout<< s1.findMedianSortedArrays(mohy1,mohy2)<< endl;
    return 0 ;
}