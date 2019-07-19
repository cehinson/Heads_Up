
from collections import defaultdict, deque
import random
import numpy as np


class Agent:
    '''
    Base class for other agents
    '''

    def __init__(self, sensors, actuators):
        self.sensors = sensors
        self.actuators = actuators

    def next_action(self):
        raise NotImplementedError


class RandomAgent(Agent):

    def __init__(self, sensors, actuators):
        super().__init__(sensors, actuators)
        self.actions = actuators.actions

    def next_action(self):
        '''Choose next action randomly'''
        return random.choice(self.actions)


class ReinforcementAgent(Agent):
    '''Use reinforcement learning to pick the best next action'''

    def __init__(self, sensors, actuators):
        super().__init__(sensors, actuators)
        self.actions = actuators.actions
        # TODO change to using a pandas dataframe
        # (state, action) --> reward
        self.sar_table = {}
        self.states = deque()  # visited states
        self.actions = deque()  # taken actions
        self.rewards = deque()  # rewards recieved
        # number of times each (state, action) pair has been visited
        self.visit_counter = defaultdict(int)
        # update sar_table at each iteration
        self._train = False

    @property
    def train(self):
        return self._train

    @train.setter
    def train(self, train):
        self._train = train
        print("train is set to {}".format(self._train))

    def to_file(self):
        '''Save to a file'''
        raise NotImplementedError

    @classmethod
    def from_file(cls):
        '''Initialize from file'''
        raise NotImplementedError

    def next_action(self, state, method):
        '''Pick move with highest expected reward'''
        self.states.append(state)

        action = None
        if method == "semi_uniform":
            action = self.semi_uniform_best_action(state)
        elif method == "convergent_suba":
            action = self.convergent_suba(state)
        elif method == "adaptive_suba":
            action = self.adaptive_suba(state)
        elif method == "greedy":
            action = self.greedy_best_action(state)
        else:
            raise Exception("Error : {} is not a valid method".format(method))

        self.actions.append(action)
        return action

    def adaptive_suba(self, state):
        # TODO adaptive version of semi-uniform best action
        raise NotImplementedError

    def convergent_suba(self, state, K=None):
        '''P_best gradually increases as state is explored'''
        if not K:
            K = self.branching_factor * 3
        visit_count = sum([self.visit_counter[(state, a)]
                           for a in self.actions])
        Pb = visit_count / K
        if Pb > 1:
            Pb = 1
        return self.semi_uniform_best_action(state, P_best=Pb)

    def semi_uniform_best_action(self, state, P_best=0.5):
        '''
        Pick action using Semi-Uniform Distributed Exploration:

        P(a) =  (1) : P_best + (1 - P_best)/#Actions -- if a has highest reward
                (2) : (1 - P_best)/#Actions -- otherwise

                Note : P_best = 0 for pure exploration
                       P_best = 1 for pure exploitation
        '''
        # probability to select other action
        P_other = (1 - P_best) / len(self.actions)
        # probability to select action that maximizes reward
        P_max_rew = P_best + P_other

        reward = [self.expected_reward(state, a) for a in self.actions]
        best_action = self.actions[reward.index(max(reward))]

        prob = [P_other if a is not best_action else P_max_rew
                for a in self.actions]
        action_chosen = np.random.choice(self.actions, p=prob)

        self.visit_counter[(state, action_chosen)] += 1
        self.character.move(action_chosen)
        return action_chosen

    def greedy_best_action(self, state):
        '''Pick action with highest expected reward'''
        # shuffle -- will pick random action when there is a tie
        random.shuffle(self.actions)
        reward = [self.expected_reward(state, a) for a in self.actions]
        idx = reward.index(max(reward))
        action_chosen = self.actions[idx]
        self.visit_counter[(state, action_chosen)] += 1
        return action_chosen

    def expected_reward(self, state, action):
        # TODO scale the reward by probability that action will complete
        #  (if we can model this)
        if (state, action) in self.sar_table:
            return self.sar_table[(state, action)]
        else:
            return 0

    def give_reward(self, reward, state, action, discount=0.5, eps=0.01):
        self.rewards.append(reward)
        if self._train:  # update sar map
            # FIXME the reward table needs to be normalized
            self.sar_table[(state, action)] += reward
            prev_state = self.states.pop()
            prev_action = self.states.pop()
            while ((abs(reward) > eps) and prev_state and prev_action):
                reward *= discount
                self.sar_table[(prev_state, prev_action)] += reward
                prev_state = self.states.pop()
                prev_action = self.states.pop()
