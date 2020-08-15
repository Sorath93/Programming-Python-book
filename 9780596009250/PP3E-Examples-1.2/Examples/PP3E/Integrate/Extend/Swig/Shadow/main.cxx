#include "iostream.h"
#include "number.h"

main()
{
    Number *num;
    num = new Number(1);            // make a C++ class instance
    num->add(4);                    // call its methods
    num->display();
    num->sub(2); 
    num->display();
    cout << num->square() << endl;

    num->data = 99;                 // set C++ data member
    cout << num->data << endl;      // fetch C++ data member
    num->display();
    cout << num << endl;            // print raw instance ptr
    delete num;                     // run destructor
}
