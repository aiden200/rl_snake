from typing import List, Tuple, Dict, Any, Optional, NamedTuple, Callable
from typing import List, Callable, Tuple, Any
from collections import defaultdict
import random
import math


Feature = NamedTuple('Feature', [('featureKey', Tuple), ('featureValue', int)])

class State:
    def __init__(self, delta_x, delta_y, reward) -> None:
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.reward = reward


############################################################
# Performs Q-learning. 
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm():
    def __init__(self, actions: Callable, discount: float, featureExtractor: Callable, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state: Tuple, action: Any) -> float:
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state: Tuple) -> Any:
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self) -> float:
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state: State, action: Any, reward: int, newState: State) -> None:

        if newState == None:
            # s is terminal
            return

        featureValues = self.featureExtractor(state, action)
        max_action_value = float('-inf')
        for new_action in self.actions(newState):
            temp_value = self.getQ(newState, new_action)
            if temp_value > max_action_value:
                max_action_value = temp_value

        difference = reward + self.discount*max_action_value - self.getQ(state, action)

        alpha = self.getStepSize()
        for f, v in featureValues:
            self.weights[f] += alpha*difference*v
