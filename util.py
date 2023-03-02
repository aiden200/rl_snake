from typing import List, Tuple, Dict, Any, Optional, NamedTuple, Callable
from typing import List, Callable, Tuple, Any
from collections import defaultdict
import random
import math


Feature = NamedTuple('Feature', [('featureKey', Tuple), ('featureValue', int)])

class State:
    def __init__(self, x, y, length, foodx, foody, snake_list) -> None:
        self.x = x
        self.y = y
        self.length = length
        self.foodx = foodx
        self.foody = foody
        self.snake_list = snake_list


############################################################
# Performs Q-learning. 
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm():
    def __init__(self, actions: List, discount: float, featureExtractor: Callable,  height, width, size, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0
        self.height = height
        self.width = width
        self.size = size

    # Return the Q function associated with the weights and features
    def getQ(self, state: Tuple, action: Any) -> float:
        score = 0
        for f, v in self.featureExtractor(state, action, self.height, self.width, self.size):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state: Tuple) -> Any:
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions)
        else:
            random.shuffle(self.actions)
            return max((self.getQ(state, action), action) for action in self.actions)[1]

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

        featureValues = self.featureExtractor(state, action, self.height, self.width, self.size)
        max_action_value = float('-inf')
        for new_action in self.actions:
            temp_value = self.getQ(newState, new_action)
            if temp_value > max_action_value:
                max_action_value = temp_value

        difference = reward + self.discount*max_action_value - self.getQ(state, action)

        alpha = self.getStepSize()
        for f, v in featureValues:
            self.weights[f] += alpha*difference*v


def featureExtractor(state: State, action, height, width, size):
    features = []
    temp_x = state.x
    temp_y = state.y


    # #distance to left wall, how big the tail is, action maybe you need location?
    # features.append(Feature(featureKey=('leftWall', temp_x, action), featureValue=1))

    # #distance to right wall, how big the tail is, action
    # features.append(Feature(featureKey=('rightWall', width-size-temp_x, action), featureValue=1))

    # #distance to top wall, how big the tail is, action
    # features.append(Feature(featureKey=('topWall', temp_y, action), featureValue=1))

    # #distance to bottom wall, how big the tail is, action
    # features.append(Feature(featureKey=('bottomWall', height-size-temp_y, action), featureValue=1))

    #maybe how close the head is to the body?

    distance_to_wall = min(temp_x, width-size-temp_x, temp_y, height-size-temp_y)
    features.append(Feature(featureKey=('distance_to_wall', distance_to_wall, action), featureValue=1))

    #distance to fruit, action
    food_distance = 1
    if abs(temp_y-state.foody) + abs(temp_x-state.foodx) != 0:
        food_distance = 1/(abs(temp_y-state.foody) + abs(temp_x-state.foodx))
    # food_distance = 1/(abs(temp_y-state.foody) + abs(temp_x-state.foodx))

    features.append(Feature(featureKey=('bottomWall', food_distance, action), featureValue=5))

    features.append(Feature(featureKey=('current_score', state.length, action), featureValue=5))
    return features
