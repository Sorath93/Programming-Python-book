from number import Number       # use C++ class in Python (shadow class)
                                # runs same tests as main.cxx C++ file
num = Number(1)                 # make a C++ class object in Python
num.add(4)                      # call its methods from Python 
num.display()                   # num saves the C++ 'this' pointer
num.sub(2)
num.display()
res = num.square()              # converted c++ return value
print res

num.data = 99                   # set C++ data member, generated __setattr__ 
print num.data                  # get C++ data member, generated __getattr__ 
num.display()
print num                       # runs repr in shadow/proxy class
del num                         # runs C++ destructor automatically
