import pygame
import time
import random
import math
from util import State

CONTROLS = False


class Snake:
    def __init__(self, dis, height, width, size) -> None:
        self.size = size
        self.dis = dis
        self.height = height
        self.width = width

    def reset(self) -> State:
        foodx = round(random.randrange(0, self.width-self.size) / self.size) * self.size 
        foody = round(random.randrange(0, self.width-self.size) / self.size) * self.size
        self.dis.fill("black")
        state = State(300, 300, 1, foodx, foody, [])
        return state

    
    def collide(self, head, state):
        #add tail check later
        if head in state.snake_list[:-1]:
            return True

        if state.x < 0 or state.x > self.width-self.size or state.y<0 or state.y > self.height-self.size:
            # print("crashing")
            return True 
        
        return False
    

    
    def choices(self, state, action):
        moves = {"up":[0,-self.size], "down":[0,self.size], "left":[-self.size,0], "right":[self.size,0]} #up, down left, right
        if action not in moves:
            print("Invalid action")
            exit(0)
        reward = 0
        move = moves[action]
        temp_x = state.x + move[0]
        temp_y = state.y + move[1]
        new_state = State(temp_x, temp_y, state.length, state.foodx, state.foody, state.snake_list)
        if self.collide([temp_x,temp_y],state):
            # new_state = State
            return None, -1
        if temp_x == state.foodx and temp_y == state.foody:
            reward = 1
            new_state.length += 1
            state.foodx = round(random.randrange(0, self.width-self.size) / self.size) * self.size
            state.foody = round(random.randrange(0, self.width-self.size) / self.size) * self.size

        if temp_x < 0 or temp_x > self.width-self.size or temp_y<0 or temp_y > self.height-self.size or [temp_x, temp_y] in state.snake_list[:-1]:
            reward = -1


        return new_state, reward              
    


    def draw(self, state, trial):

        blue=(0,0,255)
        red=(255,0,0)  
        white = (255, 255, 255) 
        score_font = pygame.font.SysFont("comicsansms", 35)
        mesg = score_font.render(f"Trial: {trial}", True, white)

        snake_Head = []
        snake_Head.append(state.x)
        snake_Head.append(state.y)
        state.snake_list.append(snake_Head)
        if len(state.snake_list) > state.length:
            del state.snake_list[0]

        self.dis.fill("black")
        self.dis.blit(mesg, [0, 0])
        for x,y in state.snake_list:
            pygame.draw.rect(self.dis,blue,[x,y,self.size,self.size])
        pygame.draw.rect(self.dis,red,[state.foodx,state.foody,self.size,self.size])
        pygame.display.update()
    
