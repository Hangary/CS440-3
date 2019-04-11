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
        self.s = None
        #last action
        self.a = None
        #points
        self.points = 0
        #begin
        self.begin = False

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
        if state[0] == 520 and state[1] == 480:
            print("stop")

        # training
        if self.train:
            # updating
            if self.begin:
                cur_s = self.state_index(state)
                last_Q_value = self.Q[self.s][self.a]
                update_value = last_Q_value + self.alpha() * (self.reward(points, dead) + self.gamma * max(self.Q[cur_s])  - last_Q_value)
                self.Q[self.s][self.a] = round(update_value, 2) # update Q-table!

            # action
            max_v = -float("inf")
            cur_s = self.state_index(state)
            cur_a = 0
            for i in range (3, -1, -1):
                if self.N[cur_s][i] < self.Ne:
                    cur_a = i
                    break

                if self.Q[cur_s][i] > max_v:
                    max_v = self.Q[cur_s][i]
                    cur_a = i 

            print("x,y", state[0], state[1])
            print("Q: ", self.Q[self.s][self.a])
            print("All_Q: ", self.Q[self.s])
            print("N: ",self.N[self.s][self.a])
            print("Points: ", points)
            print("##############")

            self.N[cur_s][cur_a] += 1

            self.s = cur_s
            self.a = cur_a

            self.begin = True

            # print(self.N)
            return cur_a       
        # testing
        else:
            cur_s = self.state_index(state)
            real_a = 0
            max_v = -float("inf")
            for i in range (3, -1, -1):
                if self.Q[cur_s][i] > max_v:
                    max_v = self.Q[cur_s][i]
                    real_a = i 
            return real_a
    
    def alpha(self):
        return self.C/(self.C+self.N[self.s][self.a])

    def reward(self, points, dead):
        if dead:
            return -1
        elif points - self.points > 0:
            self.points = points
            return 1
        else:
            return -0.1

    def state_index(self, state):
        adjoining_wall_x = 0
        adjoining_wall_y = 0
        food_dir_x = 0
        food_dir_y = 0
        adjoining_body_top = 0
        adjoining_body_bottom = 0
        adjoining_body_left = 0
        adjoining_body_right = 0

        snake_head_x = state[0]
        snake_head_y = state[1]
        snake_body = state[2]
        food_x = state[3]
        food_y = state[4]

        if snake_head_x == 40:
            adjoining_wall_x = 1
        elif snake_head_x == 480:
            adjoining_wall_x = 2
        
        if snake_head_y == 40:
            adjoining_wall_y = 1
        elif snake_head_y == 480:
            adjoining_wall_y = 2
        
        if food_x < snake_head_x:
            food_dir_x = 1
        elif food_x > snake_head_x:
            food_dir_x = 2

        if food_y < snake_head_y:
            food_dir_y = 1
        elif food_y > snake_head_y:
            food_dir_y = 2

        for x,y in snake_body:
            if snake_head_x + 40 == x and snake_head_y == y:
                adjoining_body_right = 1
                continue
            if snake_head_x - 40 == x and snake_head_y == y:
                adjoining_body_left = 1
                continue
            if snake_head_y + 40 == y and snake_head_x == x:
                adjoining_body_top = 1
                continue
            if snake_head_y - 40 == y and snake_head_x == x:
                adjoining_body_bottom = 1
                continue
        
        return (adjoining_wall_x, adjoining_wall_y, food_dir_x, food_dir_y, adjoining_body_top, 
        adjoining_body_bottom, adjoining_body_left, adjoining_body_right)