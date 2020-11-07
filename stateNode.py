import numpy as np
import gym


class State_Node(object):

    def __init__(self, action, obs, reward, done, parent):

        self.state = obs
        self.action = action  # action is the action taken to reach this state
        self.done = done
        self.reward = reward

        self.children: [State_Node] = set()
        self.children_action = set()
        self.visited = False
        self.fully_expanded = False
        self.parent = parent

        self.N = 0
        self.Q = 0

    # Probably need to change this later
    def add_visit_times(self):
        self.N += 1

    def update_simulation_result(self, q):
        self.Q += q

    def add_child_node(self, child_node):
        self.children.add(child_node)
        self.children_action.add(child_node.action)

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
















