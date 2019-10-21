#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 22:25:23 2019

@author: mandroid6
"""
import numpy as np

# movements
FORWARD = 1
BACKWARD = -1
NO_MOVE = 0

# rotation/turning
TURN_LEFT = -1
TURN_RIGHT = 1
TURN_ZERO = 0

# cardinal directions for heading
UPWARDS = [11, 0, 1]
DOWNWARDS = [5, 6, 7]
RIGHTWARDS = [2, 3, 4]
LEFTWARDS = [8, 9, 10]

class state():
    
    def __init__(self, shape):
        
        self.L = shape[0]
        self.W = shape[1]
        
        states = []
        
        for i in range(0,self.L):
            for j in range(0, self.W):
                for heading in range(0,12):
                    states.append((i, j, heading))
                    
                    
        stateSize = len(states)
        print("stateSize = ", stateSize)
        
        
        actions = []
        
        for movement in [FORWARD, BACKWARD, NO_MOVE]:
            if movement != NO_MOVE:
                for turning in [TURN_LEFT, TURN_RIGHT, TURN_ZERO]:
                    actions.append((movement, turning))
                    
            else:
                actions.append((movement, TURN_ZERO))
                
        actionSpace = len(actions)
        print("action space = ", actionSpace)
        
            
    
    def find_transition_prob(self, state, action, next_state, pe=0):
        
        
        P_head = self.create_heading_prob()
        
        P = {}
        if action[0] == FORWARD:
            for move_direction in P_head[state[2]]:
                x = state[0] + move_direction[0][0]
                x_result = x if (x<= self.L-1 and x >=0) else state[0]
                
                y = s[1] + move_direction[0][1]
                y_result = y if (y<= self.W-1 and y>=0) else state[1]
               
                head_result = (move_direction[1] + action[1]) % 12
                
                P[(x_result, y_result, head_result)] = move_direction[2]

                if move_direction[2] != 0.0:
                    P[move_direction[2]] = (x_result, y_result, head_result)
                
                
        elif action[0] == BACKWARD:
            for move_direction in P_head[state[2]]:
                x = state[0] - move_direction[0][0]
                x_result = x if (x<= self.L-1 and x >=0) else state[0]
                
                y = s[1] - move_direction[0][1]
                y_result = y if (y<= self.W-1 and y>=0) else state[1]
               
                head_result = (move_direction[1] + action[1]) % 12
                
                P[(x_result, y_result, head_result)] = move_direction[2]
                
                if move_direction[2] != 0.0:
                    P[move_direction[2]] = (x_result, y_result, head_result)
                
        else:
            # taking no action
            P[state] = 1
            
            
        if next_state in P.keys():
            return P[next_state]
        else:
            return 0.0
        
        
    def predict_next_state(self, state, action, pe=0):
        
        
        P_head = self.create_heading_prob()
        
        P = {}
        if action[0] == FORWARD:
            for move_direction in P_head[state[2]]:
                x = state[0] + move_direction[0][0]
                x_result = x if (x<= self.L-1 and x >=0) else state[0]
                
                y = s[1] + move_direction[0][1]
                y_result = y if (y<= self.W-1 and y>=0) else state[1]
               
                head_result = (move_direction[1] + action[1]) % 12
                
                if move_direction[2] != 0.0:
                    P[move_direction[2]] = (x_result, y_result, head_result)
                
                
        elif action[0] == BACKWARD:
            for move_direction in P_head[state[2]]:
                x = state[0] - move_direction[0][0]
                x_result = x if (x<= self.L-1 and x >=0) else state[0]
                
                y = s[1] - move_direction[0][1]
                y_result = y if (y<= self.W-1 and y>=0) else state[1]
               
                head_result = (move_direction[1] + action[1]) % 12
                
                if move_direction[2] != 0.0:
                    P[move_direction[2]] = (x_result, y_result, head_result)
                
        else:
            # taking no action
            P[state] = 1
            
            
        
        return P
        
    
    def reward(state):
        
        if not ((0<=state[0] < 7) and (0<=state[1] < 7)):
            raise ValueError('The state is not of size L = W = 8')
        if (state[0] == 5) and (state[1] == 6):
            reward =  1
        elif (state[0] in [0, 7]) or (state[1] in [0, 7]):
            reward = -100
        elif (state[0] == 3) and (state[1] in [4, 5, 6]):
            reward = -10
            
        else:
            reward = 0
            
        return reward
        
    
    
    

    def create_heading_prob(self):
        P_head = {}
        
        for i in range(0, 12):
            head_plus = i + 1
            head_minus = i - 1
            
            if i in UPWARDS:
                P_head[i] = [([0, 1], i, 1 - 2*pe)]
                
                if head_plus in RIGHTWARDS:
                    P_head[i].append(([1, 0], (12+head_plus)%12, pe))
                        
                else:
                    P_head[i].append(([0, 1], (12+head_plus)%12, pe))
                    
                if head_minus in LEFTWARDS:
                    P_head[i].append(([-1, 0], (12 +head_minus)%12, pe))
                    
                else:
                    P_head[i].append(([0, 1], (12 +head_minus)%12, pe))
                    
                    
                    
            elif i in RIGHTWARDS:
                P_head[i] = [([1, 0], i, 1- 2*pe)]
                
                if head_plus in DOWNWARDS:
                    P_head[i].append(([0, -1], head_plus, pe))
                
                else:
                    P_head[i].append(([1, 0], head_plus, pe))
                   
                if head_minus in UPWARDS:
                    P_head[i].append(([0, 1], head_minus, pe))
                
                else:
                    P_head[i].append(([1, 0], head_minus, pe))
                   
            elif i in DOWNWARDS:
                P_head[i] = [([0, -1], i, 1- 2*pe)]
                
                if head_plus in LEFTWARDS:
                    P_head[i].append(([-1, 0], head_plus, pe))
                 
                else:
                    P_head[i].append(([0, -1], head_plus, pe))
                    
                if head_minus in RIGHTWARDS:
                    P_head[i].append(([1, 0], head_minus, pe))
                   
                else:
                    P_head[i].append(([0, -1], head_minus, pe))
                    
            elif i in LEFTWARDS:
                P_head[i] = [([-1, 0], i, 1- 2*pe)]
                
                if head_plus in UPWARDS:
                    P_head[i].append(([0, 1], head_plus, pe))
                    
                else:
                    P_head[i].append(([-1, 0], head_plus, pe))
                    
                        
                if head_minus in DOWNWARDS:
                    P_head[i].append(([0, -1], head_minus, pe))
              
                else:
                    P_head[i].append(([-1, 0], head_minus, pe))
                    
                    
        return P_head