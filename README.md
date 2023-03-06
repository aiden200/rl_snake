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


## Brief technical report

