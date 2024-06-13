from ctypes import sizeof
from threading import local
from typing import Dict, Any, Iterator, Optional, Union
from collections import abc
from types import FunctionType
import inspect


class DynamicScope(abc.Mapping):
    def __init__(self):
        self.env: Dict[str, Union[Any, None]] = {}

    def __getitem__(self, key):
        if key in self.env:
            return self.env[key]
        else:
            raise NameError

    def __setitem__(self, key, value):
        if key not in self.env:
            self.env[key] = value
        else:
            return

    def __iter__(self):
        return iter(self.env)

    def __len__(self):
        return len(self.env)


def get_dynamic_re() -> DynamicScope:
    dictionary = DynamicScope()

    def get_size():
        size = -1
        stack = inspect.stack()
        while stack != []:
            stack.pop()
            size += 1
        return size

    def get_locals(size):
        stack_info = inspect.stack()
        i = 2
        for _ in range(size - 1):
            frame = stack_info[i][0]
            freevars = list(frame.f_code.co_freevars)
            localvars = list(frame.f_locals)
            localvars2 = frame.f_locals
            i += 1
            toadd = [x for x in localvars if x not in freevars]
            for keys in toadd:
                if type(localvars2[keys]) == str:
                    dictionary.__setitem__(keys, localvars2[keys])
        return None

    get_locals(get_size())
    return dictionary
