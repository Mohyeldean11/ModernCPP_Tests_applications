#include "Integer_m.hpp"

//default constructor
Integer::Integer(/* args */)
:m_ptr(new int (0))
{
    std::cout << "Integer()"<<std::endl;
}
//paramaterized const
Integer::Integer(int value)
:m_ptr(new int(value))
{
    std::cout << "Integer(int value)"<<std::endl;

}

//move constructor
Integer::Integer( Integer &&obj)
{
    m_ptr = obj.m_ptr;
    obj.m_ptr = nullptr;
    std::cout << "Integer(Integer &&obj)"<<std::endl;

}
//copy constructor
Integer::Integer(const Integer &obj)
{
    m_ptr = new int(*obj.m_ptr);
    std::cout << "Integer(const Integer &obj)"<<std::endl;

}
int Integer::Get_value()const
{
    return *(m_ptr);
}
void Integer::Set_value(int value)
{
    *(m_ptr) = value;
}

//destructor
Integer::~Integer()
{
    std::cout << "~Integer()"<<std::endl;
}


//operator overloading

Integer & Integer::operator++()
{
    ++(*m_ptr);
    return *(this);
}

bool Integer::operator==(const Integer &obj)const
{
    return *(obj.m_ptr) == *(m_ptr);
}
//copy assignment
Integer & Integer::operator=(const Integer &obj)
{
    if(this != &obj)
    {
        delete m_ptr;
        m_ptr = new int(*(obj.m_ptr));
    }
    return *this;
}
//move assignment 
Integer & Integer::operator=(Integer &&obj)
{
    if(this != &obj)
    {
        delete m_ptr;
        m_ptr = new int(*obj.m_ptr);
        obj.m_ptr = nullptr ;  
    }
    return *this;
}
Integer Integer::operator+(const Integer &obj)const
{
    Integer temp;
    *(temp.m_ptr) =*(this->m_ptr) + *(obj.m_ptr);
    return temp;
}

Integer Integer::operator-(const Integer &obj)const
{
    Integer temp;
    *(temp.m_ptr) = *(m_ptr) - *(obj.m_ptr);
    return temp;
}

std::ostream & operator << (std::ostream & out , const Integer &obj)
{
    out << *(obj.m_ptr);
    return out;
}
std::istream & operator >>(std::istream &in ,Integer &obj)
{
    int x ;
    in >> x;
    obj.Set_value(x);
    return in;
}
//adding x + Integer
Integer operator +(int x , const Integer &obj)
{
    Integer Temp;
    Temp.Set_value(x + obj.Get_value());
    return Temp;
}



