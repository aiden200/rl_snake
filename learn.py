from learning_snake import Snake
from util import QLearningAlgorithm, featureExtractor
import pygame




def simulate(display, height, width, numTrials=50, maxIterations=10000):
    actions = ["up","down","left","right"]
    discount = 1 # what is this
    size = 30
    qlearn = QLearningAlgorithm(actions, discount, featureExtractor, height, width, size)
    snake = Snake(display, height, width, size)
    total_rewards = []

    for trial in range(numTrials):
        state = snake.reset()
        totalDiscount = 1 #future
        trial_reward = 0
        for _ in range(maxIterations):
            action = qlearn.getAction(state)
            new_state, reward = snake.choices(state, action)
            if new_state == None:
                qlearn.incorporateFeedback(state, action, -1, None)
                print("crashed")
                break

            qlearn.incorporateFeedback(state, action, reward, new_state)
            trial_reward += totalDiscount * reward
            totalDiscount *= discount
            state = new_state
            snake.draw(new_state, trial)
        total_rewards.append(trial_reward)
    
    return total_rewards
            



def learn():
    height = 600
    width = 600
    pygame.init()
    dis=pygame.display.set_mode((height,width))
    pygame.display.set_caption('Reinforcement Learning Snake')
    total_reward = simulate(dis,height,width)
    print(total_reward)
    pygame.quit()
    quit()

learn()