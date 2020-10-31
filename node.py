import numpy as np
import gym

class State_node(object):

    def __init__(self, obs=None, parent=None):

        self.N = 0
        self.Q = 0
        # Probably need to change this later
        self.state = obs
        self.done = False
        self.children: [State_node] = set()
        self.visited = False
        self.fully_expanded = False
        self.parent = None

    def add_visit_times(self):
        self.N += 1

    def update_simulation_result(self, q):
        self.Q += q

    def add_child_node(self, child_node):
        self.children.add(child_node)

    def return_fully_expanded(self):
        if self.fully_expanded:
            return True
        elif not self.children:
            return False
        else:
            for child in self.children:
                if child.return_visited == False:
                    return False
            self.fully_expanded = True
            return True

    def return_children(self):
        return self.children

    def return_visited(self):
        return self.visited

    def return_done(self):
        return self.done

    def update_terminal(self):
        self.done = True
        self.visited = True


class Monte_Carlo_Tree_Search(object):

    def __init__(self, env: gym.wrappers.time_limit.TimeLimit):

        self.root = State_node()
        self.env = env

    def expansion_policy(self, state_node: State_node):

        return self.env.action_space.sample()

    def expand(self, state_node: State_node):

        curr_state_node = State_node
        while curr_state_node.return_done() == False:

            action = self.expansion_policy(state_node)
            obs, reward, done, info = self.env.step(action)

            child_state_node = State_node(obs=obs, parent=curr_state_node)
            curr_state_node.add_child_node(child_state_node)

            if done:
                child_state_node.update_terminal()

            curr_state_node = child_state_node

    def select(self, state_node: State_node):

        while state_node.return_fully_expanded():

            selected_child_node = self.UCT(state_node)
            self.select(selected_child_node)

        ##Pick a node
        # action = self.env.action_space.sample()
        # unvisited_child_state = self.env.step(action=action)

    def backpropagate(self, state_node: State_node, result):

        state_node.update_simulation_result(result)
        state_node.add_visit_times()

        if state_node is not self.root:
            self.backpropagate(state_node.parent, result)















