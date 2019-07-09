

class ActionList:
    '''Class that represents actions available to an acutator'''

    def __init__(self):
        self._actions = []

    def __len__(self):
        return len(self._actions)

    def __getitem__(self, position):
        return self._actions[position]

    def __call__(self, func):
        '''
        NOTE: I do NOT need to use functools.wraps for this.
        This is because functools.wraps will not actually
        register the function until it is called.
        It also appears that not using functools.wraps
        (in this case) does NOT result in any name-mangling
        problems.
        '''
        print('registered {}'.format(func.__name__))
        self._actions.append(func)
        return func


# global list of actions
actions = ActionList()
