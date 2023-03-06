---
D key: Enter/Exit Debug Mode
S key: Skip Trial
Space key: Next Frame
Up Arrow Key: Speed up frame by 100
Down Arrow Key: Slow down frame by 100
---

## Check out my Website
https://www.aidenwchang.com/


## How to run the code

Clone the github repository, install and activate python venv.

Run the code typing in:
```
python3 learn.py
```

Once the snake program is launched, you can adjust the frame rate of the snake with the up and down arrow keys.

### Debug Mode
If you press the 'D' key, you will enter debug mode. This allows you to see graphically what the weight values of each possible moves are. The red colored value will indicate the direction the snake chose for the next move.

Pressing the 'D' key one more time will exit debug mode.

Press the 'S' key to skip one trial. A trial is defined to be 10,000 frames or until the snake dies.

Press the space bar to allow the snake to move one frame. 

On the terminal, the current feature values will be displayed followed by a dashed line.
| Command | Description |
| --- | --- |
| foodLeft | Food is on the left side of snake |
| foodRight | Food is on the right side of the snake |
| foodDown | Food is on the down side of the snake |
| foodUp | Food is on the up side of the snake |
| dangerDown | the snake will die if it travels one block below |
| dangerUp | the snake will die if it travels one block above |
| dangerLeft | the snake will die if it travels one block to the left |
| dangerRight | the snake will die if it travels one block to the right |


## About the Project
The snake AI uses Reinforcement Learning to solve the most optimal way to play snake.

The AI uses Q algorithm to solve the problem. 

There are 4 actions that the AI can take. "up", "down", "left", or "right". Depending on if the body size > 1, this could be limited to 3 actions.

A "state" in this problem is defined to be the x,y coordinates of the head, length of the snake, x,y coordinates of the food, and the snake body.

Given that the food is randomly generated across the screen(besides the first iteration so the snake can learn quickly that eating the food gives a good reward). There are too many possible states to visit. Therefore instead of saving and trying to visit all possible states, approximate Q learning will be used. 

For actual rewards, two methodes were tested. 

1. Reward for every closer block to the fruit.
    - Reward for eating fruit: 10
    - Reward for being in a new state closer to the fruit compared to the previous state: 1
    - Reward for being in a new state further to the fruit compared to the previous state: -1
    - Reward for dying: -1000

The idea was to try to get the snake always moving towards the fruit, but it ended up determening that dying might be worth more than going around its long tail in later stages.

2. Reward for only the fruit.
    - Reward for eating fruit: 10
    - Reward for dying: -1000
    - Any other reward: 0

The idea was to try to get the snake to prioritize staying alive, giving it no negative feedback when it takes the long way around.

### The algorithm:
With a probability of $\epsilon$(default 0.2), the snake will take a random legal action. This value will decrease as the number of trials increase.

With a probability of $\epsilon$, the snake will choose its next move from the following algorithm.
$\sqrt{3x-1}+(1+x)^2$

With the 

Issues resolved:
    - The code has an epsilon value that acts as a probability of the snake to make a random move with the purpose of exploring new states. This causes an issue in later stages, so an epsilon value of each trial is determined to be epsilon = max_epsilon/trial. This decreases randomness as our trials increase
    - The fruit spawned in the snake body causing the snake to crash into itself


