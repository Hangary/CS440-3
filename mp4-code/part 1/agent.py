import numpy as np
import utils
import random


class Agent:
    
    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = Ne # used in exploration function
        self.C = C
        self.gamma = gamma

        # Create the Q and N Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()

        #last state
        self.s
        #last action
        self.a

    def train(self):
        self._train = True
        
    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self,model_path):
        utils.save(model_path, self.Q)

    # Load the trained model for evaluation
    def load_model(self,model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    def act(self, state, points, dead):
        '''
        :param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: the index of action. 0,1,2,3 indicates up,down,left,right separately

        TODO: write your function here.
        Return the index of action the snake needs to take, according to the state and points known from environment.
        Tips: you need to discretize the state to the state space defined on the webpage first.
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the 480x480 board)

        '''
        # training
        if self.train:
            # updating
            cur_s = state_index(state)
            last_Q_value = self.Q[self.s][self.a]
            update_value = last_Q_value + alpha(self) * (reward(self, dead) + self.gamma * max(self.Q[cur_s])  - last_Q_value)
            self.Q[self.s][self.a] = update_value # update Q-table!

            # action
            max_v = -float("inf")
            cur_a = 0
            for i in range (3, -1, -1):
                if self.N[cur_s][i] < self.Ne:
                    cur_a = i
                    break

                if self.Q[cur_s][i] > max_v:
                    max_v = v
                    cur_a = i 
            self.s = cur_s
            self.a = cur_a       
        # testing
        else:
    
    def alpha(self):
        return self.C/(self.C+self.N[self.s][self.a])

    def reward(self, dead):
        if dead:
            return -1
        elif self.state[0] == self.state[3] and self.state[1] == self.state[4]:  # snake eats food
            return 1
        else:
            return -0.1

    def state_index(state):
        adjoining_wall_x = 0
        adjoining_wall_y = 0
        food_dir_x = 0
        food_dir_y = 0
        adjoining_body_top = 0
        adjoining_body_bottom = 0
        adjoining_body_left = 0
        adjoining_body_right = 0

        if state.snake_head_x == 40:
            adjoining_wall_x = 1
        elif state.snake_head_x == 520:
            adjoining_wall_x = 2
        
        if state.snake_head_y == 40:
            adjoining_wall_y = 1
        elif state.snake_head_y == 520:
            adjoining_wall_y = 2
        
        if state.food_x < state.snake_head_x:
            food_dir_x = 1
        elif state.food_x > state.snake_head_x:
            food_dir_x = 2

        if state.food_y < state.snake_head_y:
            food_dir_y = 1
        elif state.food_y > state.snake_head_y:
            food_dir_y = 2

        for x,y in state.snake_body:
            if state.snake_head_x == x + 40:
                adjoining_body_left = 1
            if state.snake_head_x == x - 40:
                adjoining_body_right = 1
            if state.snake_head_y == y - 40:
                adjoining_body_top = 1
            if state.snake_head_y == y + 40:
                adjoining_body_bottom = 1
        
        return (adjoining_wall_x, adjoining_wall_y, food_dir_x, food_dir_y, adjoining_body_top, 
        adjoining_body_bottom, adjoining_body_left, adjoining_body_right)