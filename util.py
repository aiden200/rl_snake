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
    def getQ(self, state: State, action: Any) -> float:
        score = 0
        featureValues, debug_values = self.featureExtractor(state, action, self.height, self.width, self.size)
        for f, v in featureValues:
            score += self.weights[f] * v
        return score, debug_values

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state: State, debug, iterations) -> Any:
        self.numIters += 1
        moves = {"up":[0,-self.size], "down":[0,self.size], "left":[-self.size,0], "right":[self.size,0]}
        actions = []
        debug_list = []
        explorationProb = self.explorationProb / iterations #decreasing randomness as we go
        for key in moves:
            delta_vals = moves[key]
            # if state.snake_list:
                # print([state.x + delta_vals[0],state.y + delta_vals[1]], state.snake_list)
            if len(state.snake_list) > 1 and [state.x + delta_vals[0],state.y + delta_vals[1]] == state.snake_list[-2]:
                continue
            actions.append(key)
        # print(actions)
        chosen_action = None
        debug_bit = None
        if random.random() < explorationProb:
            chosen_action = random.choice(actions)
        else:
            # random.shuffle(actions)
            if debug:
                debug_list = [(self.getQ(state, action)[0], action) for action in actions]
            chosen_action_list = max((self.getQ(state, action)[0], action, self.getQ(state, action)[1]) for action in actions)
            debug_bit = chosen_action_list[2]
            chosen_action = chosen_action_list[1]
        return chosen_action, debug_list, debug_bit

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

        featureValues, debug_values = self.featureExtractor(state, action, self.height, self.width, self.size)
        max_action_value = float('-inf')
        for new_action in self.actions:
            temp_value, debug_values = self.getQ(newState, new_action)
            if temp_value > max_action_value:
                max_action_value = temp_value

        value, debug_values = self.getQ(state, action)
        difference = reward + self.discount*max_action_value - value

        alpha = self.getStepSize()
        for f, v in featureValues:
            self.weights[f] += alpha*difference*v


def featureExtractor(state: State, action, height, width, size):
    features = []
    temp_x = state.x
    temp_y = state.y
    wall_feature = False
    abs_distance_to_fruit = False
    direction_to_fruit = False
    state_features = True

    if wall_feature:
        # distance to left wall, how big the tail is, action maybe you need location?
        features.append(Feature(featureKey=('leftWall', temp_x, action), featureValue=1))
        # distance to right wall, how big the tail is, action
        features.append(Feature(featureKey=('rightWall', width-size-temp_x, action), featureValue=1))
        # distance to top wall, how big the tail is, action
        features.append(Feature(featureKey=('topWall', temp_y, action), featureValue=1))
        # distance to bottom wall, how big the tail is, action
        features.append(Feature(featureKey=('bottomWall', height-size-temp_y, action), featureValue=1))

    if abs_distance_to_fruit:
        #distance to fruit, action
        food_distance = 1
        if abs(temp_y-state.foody) + abs(temp_x-state.foodx) != 0:
            food_distance = 1/(abs(temp_y-state.foody) + abs(temp_x-state.foodx))
        # food_distance = 1/(abs(temp_y-state.foody) + abs(temp_x-state.foodx))
        features.append(Feature(featureKey=('distance_to_food', food_distance, action), featureValue=3))

    if direction_to_fruit:
        #distance to left food
        features.append(Feature(featureKey=('leftFood', temp_x-state.foodx, action), featureValue=1))
        #distance to right food
        features.append(Feature(featureKey=('rightFood', state.foodx-temp_x, action), featureValue=1))
        #distance to top food
        features.append(Feature(featureKey=('topFood', state.foody-temp_y, action), featureValue=1))
        #distance to bottom food
        features.append(Feature(featureKey=('bottomFood', temp_y-state.foody, action), featureValue=1))


    #maybe how close the head is to the body?

    # distance_to_wall = min(temp_x, width-size-temp_x, temp_y, height-size-temp_y)
    # features.append(Feature(featureKey=('distance_to_wall', distance_to_wall, action), featureValue=1))



    # #abs horizontal distance to food, action maybe you need location?
    # features.append(Feature(featureKey=('horiDirectionFood', state.foodx - temp_x, action), featureValue=1))

    # #abs vertical distance to food, action
    # features.append(Feature(featureKey=('vertDirectionFood', state.foody-temp_y, action), featureValue=1))





    #where head is compared to the rest of snake tail
    # if state.snake_list:
    #     features.append(Feature(featureKey=('headPosition', (temp_x,temp_y), tuple(state.snake_list[-1]),action), featureValue=-1))

    #score
    # features.append(Feature(featureKey=('current_score', state.length, action), featureValue=1))

    #I think this will decide best option reletive to wall
    # features.append(Feature(featureKey=('in_wall', (temp_x, temp_y), action), featureValue=1))



    # food_distance = 1
    # if abs(temp_y-state.foody) != 0:
    #     food_distance = 1/(abs(temp_y-state.foody))
    # features.append(Feature(featureKey=('distance_to_foody', food_distance, action), featureValue=3))
    # food_distance = 1
    # if abs(temp_x-state.foodx) != 0:
    #     food_distance = 1/(abs(temp_x-state.foodx))
    # features.append(Feature(featureKey=('distance_to_foodx', food_distance, action), featureValue=3))




    '''
    Some ideas
    if the snake is in the wall, put it at 0? Since it doesnt want to crash
    '''

    bit = None
    debug_bit = []
    if state_features:
        #if snake is right of food
        if state.x > state.foodx:
            bit = 1
        else:
            bit = 0
        features.append(Feature(featureKey=('foodRight', action), featureValue=bit))
        debug_bit.append(bit)
        #if snake is left of food
        if state.x < state.foodx:
            bit = 1
        else:
            bit = 0
        features.append(Feature(featureKey=('foodLeft', action), featureValue=bit))
        debug_bit.append(bit)
        #if snake is up of food
        if state.y < state.foody:
            bit = 1
        else:
            bit = 0
        features.append(Feature(featureKey=('foodUp', action), featureValue=bit))
        debug_bit.append(bit)
        #if snake is down of food
        if state.y > state.foody:
            bit = 1
        else:
            bit = 0
        features.append(Feature(featureKey=('foodDown', action), featureValue=bit))
        debug_bit.append(bit)
        

        #danger up
        if state.y == 0 or [state.x, state.y - size] in state.snake_list[:-1]:
            bit = 1
        else:
            bit = 0
        features.append(Feature(featureKey=('dangerUp', action), featureValue=bit))
        debug_bit.append(bit)
        #danger down
        if state.y == height-size or [state.x, state.y + size] in state.snake_list[:-1]:
            bit = 1
        else:
            bit = 0
        features.append(Feature(featureKey=('dangerDown', action), featureValue=bit))
        debug_bit.append(bit)
        #danger left
        if state.x == 0 or [state.x - size, state.y] in state.snake_list[:-1]:
            bit = 1
        else:
            bit = 0
        features.append(Feature(featureKey=('dangerLeft', action), featureValue=bit))
        debug_bit.append(bit)
        #danger right
        if state.x == width-size or [state.x + size, state.y] in state.snake_list[:-1]:
            bit = 1
        else:
            bit = 0
        features.append(Feature(featureKey=('dangerRight', action), featureValue=bit))
        debug_bit.append(bit)




    return features, debug_bit
