import functools

class ActionList:
    '''Class that represents actions available to an acutator'''

    def __init__(self):
        self._actions = []

    def __len__(self):
        return len(self._actions)

    def __getitem__(self, position):
        return self._actions[position]

    def register(self, func):
        '''decorator that adds function to _actions'''
        # FIXME using @wraps doesnt work
        # @wraps(func)
        # def wrapper(*args, **kwargs):
        #     print("register")
        #     return func(*args, **kwargs)
        # return wrapper
        print('register')
        self._actions.append(func)
        return func


class Actuator:
    '''Base class for all actuators'''

    def __init__(self):
        # TODO figure out how to refactor
        pass
