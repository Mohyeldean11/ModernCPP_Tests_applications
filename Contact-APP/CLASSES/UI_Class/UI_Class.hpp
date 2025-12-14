#ifndef UI_CLASS_HPP
#define UI_CLASS_HPP

#include "./../Contact_store_Class/Contact_store_class.hpp"



class UI_Class
{
private:
    Contact_store_class MainContactOBJ;
    /* data */
   

public:
    UI_Class();
    ~UI_Class();

    void Operate();    
    void Preview_Menu(const MainMenuOptions &&chosedMenu);
    void Display_Menu(const DisplayMenuOptions &&movedOption);
    void Contact_Menu();
    void Another_DB();
    static MainMenuOptions GetMenuInput();
    static DisplayMenuOptions GetDisplayMenuInput();
    static ContactMenuOptions GetContactMenuInput();
    
};

#endif 