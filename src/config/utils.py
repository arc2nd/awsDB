#!/usr/bin/env python

# builtin imports
import sys
import json
import pathlib

sys.path.append(str(pathlib.Path(__file__).parents[1]))

# pip imports

# module imports
from config import utils

##
# EXAMPLE OF USE
#   use as a decorator/function wrapper to see if the specified 
#   function exists in the method dict
#   if it does, instead call the value for that method in the 
#   method_dict

#   @CloudAssets.config.utils.check_for_method
##

# More like a config file where we define any methods to be overriden
method_dict = {'example_method': print,
               }


def check_for_method(func):
    """
    A decorator to see if we should substitute the decorated method for another

    Args:
        func: the function that is decorated

    Returns:
        method_wrapper:
    """
    def method_wrapper(*arg, **kwargs):
        if func.func_name in method_dict:
            return method_dict[func.func_name](*arg, **kwargs)
        else:
            return func(*arg, **kwargs)
    return method_wrapper


# declaring a class
class DictionaryObject:
    # constructor
    def __init__(self, dict1):
        self.__dict__.update(dict1)


def dict2obj(in_dict):
    # using json.loads method and passing json.dumps
    # method and custom object hook as arguments
    return json.loads(json.dumps(in_dict), object_hook=DictionaryObject)
