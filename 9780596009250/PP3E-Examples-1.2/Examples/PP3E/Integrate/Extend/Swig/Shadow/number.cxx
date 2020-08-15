///////////////////////////////////////////////////////////////
// implement a c++ class, to be used from Python code or not;
// caveat: cout and print usually both work, but I ran into
// an issue on cygwin that prompted printf due to lack of time
///////////////////////////////////////////////////////////////

#include "number.h"
#include "stdio.h"                       // versus #include "iostream.h"

Number::Number(int start) { 
    data = start;                        // python print goes to stdout
    printf("Number: %d\n", data);        // cout << "Number: " << data << endl;
} 

Number::~Number() { 
    printf("~Number: %d\n", data);
}

void Number::add(int value) { 
    data += value; 
    printf("add %d\n", value);
}

void Number::sub(int value) { 
    data -= value; 
    printf("sub %d\n", value);
}

int Number::square() { 
    printf("Square = ");
    return data * data; 
}

void Number::display() { 
    printf("Number = %d\n", data);
}
