# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:33:55 2020

@author: el comandante
"""

import gym
from gym import spaces

import numpy as np


class CustomTradingEnv(gym.Env):    
    """Minimum Working Example of a Customn Trading Environment for Gym """
    metadata = {'render.modes': ['human']}
    
    def __init__(self, demand, capacity, price_cap):
        super(CustomTradingEnv, self).__init__()   
        
        # Define action and observation space
        # They must be gym.spaces objects    
        # Example when using discrete actions:
        
        # Action Space
        # Should allow a quantity-price bid, both need to be continous with quantity unlimited or limited by capacity and price either unlimited or artifical limit
        
        self.action_space = spaces.Box( low = np.array([0.0, 0.0]), high=np.array([capacity, price_cap]), dtype=np.float32)    # Bid of form (q,p) limited by capacity and price_cap
        
        
        # Observation Space
        # What are the observations?
        self.observation_space = spaces.Box( low = np.array([0.0]), high=np.array([np.inf]), dtype=np.float32) # Unclear, maybe demand?
    
    def step(self, action):
        # Limit sales by demand and pay
        self.current_step += 1
        done = 0
        
        #if self.current_step == 500: # Runtime!
        #    done = 1
        
        sold_quantity = np.clip(action[0], None, demand) # Limits sold quantity to demand
        reward = sold_quantity * action[1]
        self.total_reward += reward
        
        
        self.last_action = action                   #This stores the action to be called via render
        self.last_reward = reward                   #This stores the reward to be called via render
        #print(f'Bid quantity: {action[0]}')
        #print(f'Bid price: {action[1]}')  
        #print(f'Reward: {reward}')  
        
        obs = np.array([0.0])
        
        return obs, reward, done, {} #Attention this returns are important! They need to be defined properly. Observation, Reward, Done, Info!

    def reset(self):
        # Reset the state of the environment to an initial state
        self.total_reward = 0
        self.current_step = 0
        self.last_action = np.array([0.0, 0.0])
        self.last_reward = 0
        
        obs = np.array([0.0])
        #done = 0
        
        return obs
    
    def render(self, mode='human', close=False):
        # Render the environment to the screen
         print(f'\n Step: {self.current_step} \n')
         
         print(f'Bid quantity: {self.last_action[0]}')
         print(f'Bid price: {self.last_action[1]}')  
         print(f'Reward: {self.last_reward}')  
        
         
         print(f'Total Reward: {self.total_reward}')
         #print(self.total_reward)