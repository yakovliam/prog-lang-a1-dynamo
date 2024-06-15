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
    # define the dynamic scope
    dyn_scope = DynamicScope()

    def get_size():
        size = -1
        stk = inspect.stack()
        # loop through the stack and get the size
        while stk != []:
            stk.pop()
            size += 1
        return size

    def set_dynamic_local_vars(size):
        # get the stack information
        stack_inf = inspect.stack()
        i = 2

        # loop through the stack and get the local variables
        for _ in range(size - 1):
            frame = stack_inf[i][0]
            free_v = list(frame.f_code.co_freevars)
            local_v = list(frame.f_locals)
            frame_loc_v = frame.f_locals
            i += 1
            vars_to_add = [x for x in local_v if x not in free_v]
            # add the local variables to the dictionary
            for keys in vars_to_add:
                if type(frame_loc_v[keys]) == str:
                    dyn_scope.__setitem__(keys, frame_loc_v[keys])
        return None

    set_dynamic_local_vars(get_size())
    return dyn_scope
