import functools


# NOTE
'''
This currently does not work as intended...
It seems that registering a function will
not happen until the function is actually
called.
'''


class ActionList:
    '''Class that represents actions available to an acutator'''

    def __init__(self):
        self._actions = []

    def __len__(self):
        return len(self._actions)

    def __getitem__(self, position):
        return self._actions[position]

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print('registered {}'.format(func.__name__))
            self._actions.append(func)
            func(*args, **kwargs)
        return wrapper
