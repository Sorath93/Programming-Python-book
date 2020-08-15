# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _number

def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name) or (name == "thisown"):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


class Number(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Number, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Number, name)
    def __repr__(self):
        return "<%s.%s; proxy of C++ Number instance at %s>" % (self.__class__.__module__, self.__class__.__name__, self.this,)
    def __init__(self, *args):
        _swig_setattr(self, Number, 'this', _number.new_Number(*args))
        _swig_setattr(self, Number, 'thisown', 1)
    def __del__(self, destroy=_number.delete_Number):
        try:
            if self.thisown: destroy(self)
        except: pass

    def add(*args): return _number.Number_add(*args)
    def sub(*args): return _number.Number_sub(*args)
    def square(*args): return _number.Number_square(*args)
    def display(*args): return _number.Number_display(*args)
    __swig_setmethods__["data"] = _number.Number_data_set
    __swig_getmethods__["data"] = _number.Number_data_get
    if _newclass:data = property(_number.Number_data_get, _number.Number_data_set)

class NumberPtr(Number):
    def __init__(self, this):
        _swig_setattr(self, Number, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, Number, 'thisown', 0)
        _swig_setattr(self, Number,self.__class__,Number)
_number.Number_swigregister(NumberPtr)


