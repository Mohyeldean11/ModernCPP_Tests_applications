#include <iostream>

using comparator = bool(*)(int ,int);

//creating a template for the sort function with generalizing the type of the function passed to the sort function along with the size and the return type of the array sent
template <typename T, int size, typename comparator>
void Sort_mohy(T(&arr) [size], comparator comp)
{   
    for(int i = 0 ; i < size-1 ; ++i)
    {
        for(int j = 0 ; j<size-1 ; ++j)
        {
            if(comp(arr[j],arr[j+1]))
            {
                T temp = std::move(arr[j]);
                arr[j] = std::move(arr[j+1]);
                arr[j+1] = std::move(temp);
            }
        }
    }
}
//creating a function to pass it by pointer to function
bool compASC(int x , int y)
{
    return x>y ;
}
bool compDES(int x , int y)
{
    return x<y ;
}

//creating a function object 
struct Comp2
{
    bool operator()(int x , int y)
    {
        return x> y;
    }
};
//creating a lambda
auto myLambda = [](auto x , auto y)->auto
{
    return x+y ;
};


//foreach function
template<typename T , int size ,typename callback>
void ForEach(T (&arr)[size],callback operation)
{
    for(int i = 0 ; i < size ; ++i)
    {
        operation(arr[i]);
    }
}
void oldcode()
{
        Comp2 comp;
    int arr[]{1,4,3,6,13,11,20,9};
    Sort_mohy(arr,compDES);
    for(auto x : arr)
    {
        std::cout << x <<" ";
    }
    std::cout<<"\n";
    Sort_mohy(arr,comp);
    for(auto x : arr)
    {
        // std::cout << x <<std::endl;
        std::cout << x <<" ";

    }    
    std::cout <<"\n"<< myLambda(3.2 , 4)<<std::endl;

}
int main()
{
    Comp2 compASCENDING;
    int arr[]{2,54,1,2,5,8,0,4};
    Sort_mohy(arr,compASCENDING);
    ForEach(arr,[=](auto &x){
        // std::cout<<x<<" "<<std::endl;
        x += 5;
    });
    ForEach(arr,[=](auto x){
        std::cout<<x<<" "<<std::endl;
    });
    return 0;
}