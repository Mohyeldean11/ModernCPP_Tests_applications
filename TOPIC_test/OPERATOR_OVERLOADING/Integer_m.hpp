#pragma once
#include <iostream>
#include <stdlib.h>
#include <memory>

class Integer
{
private:
    /* data */
    int *m_ptr ;
public:
    //default constructor
    Integer(/* args */);
    //paramaterized constructor
    Integer(int x);
    //move constructor
    Integer( Integer &&obj);
    //copy constructor
    Integer(const Integer &obj);
    //getter
    int Get_value()const;
    //setter
    void Set_value(int x);
    //destructor
    ~Integer();

    //add overloading 
    Integer operator +(const Integer &obj)const;
    //subtract overloading
    Integer operator -(const Integer &obj)const;
    //pre_increment overloading
    Integer & operator ++();
    //if equal
    bool operator ==(const Integer &obj)const;
    //copy operator 
    Integer & operator =(const Integer &obj);
    //move operator
    Integer & operator =(Integer &&obj);
    friend std::ostream & operator << (std::ostream & out , const Integer &obj);

};
//adding x + Integer
Integer operator +(int x , const Integer &obj);


std::istream & operator >>(std::istream &in ,Integer &obj);


