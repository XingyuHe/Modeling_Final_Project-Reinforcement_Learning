from gameState import GameState
import numpy as np
import networkx as nx


class MonteCarloTreeSearch(object):

    def __init__(self, player, env):

        self.node_counter = 0
        self.root_GameState = GameState(None, None, env)
        self.action_space = self.root_GameState.action_space()
        self.UTC_explore_parameter = 0.01
        self.searchTimes = 100

        self.digraph = nx.DiGraph()

        self.digraph.add_node(self.node_counter, attr_dict={"Q": 0,
                                                            "N": 0,
                                                            'uct': 0,
                                                            'expanded': False,
                                                            'GameState': self.root_GameState})
        self.last_move = None
        self.node_counter += 1
        self.player = player

    def reset_game(self):

        self.last_move = None

    def move(self, starting_state):

        if self.last_move is None:
            return self.MCTS_algorithm(0)
        else:
            pass

    def best_action(self, starting_node_index):

        children = self.digraph.successors(starting_node_index)
        max_value = 0
        max_action = None
        for child_node_index in children:
            value = self.digraph.nodes[child_node_index]["Q"] / self.digraph.nodes[child_node_index]["N"]

            if value > max_value:
                max_value = value
                max_action = self.digraph[starting_node_index][child_node_index]["action"]

        return max_action


    def MCTS_algorithm(self, starting_node_index):

        for _ in range(self.searchTimes):
            print('================ ( selection ) ================')
            selected_node = self.select(starting_node_index)
            print('================ ( expansion ) ================')
            expand_node = self.expand(selected_node)
            print('================ ( simulation ) ================')
            terminal_node, result = self.simulate(expand_node)
            print('================ ( backpropagation ) ================')
            self.backpropagate(terminal_node, result)

    def select_UTC_policy(self, node_index):

        children = self.digraph.successors(node_index)

        child_index_max = 0
        utc_max = 0
        n_parent = self.digraph.nodes[node_index]["N"]

        for child_index in children:
            q_child = self.digraph.nodes[child_index]["Q"]
            n_child = self.digraph.nodes[child_index]["N"]

            utc = q_child / n_child + self.UTC_explore_parameter * np.sqrt(np.log(n_parent) / n_child)

            if utc > utc_max:
                child_index_max = child_index
                utc_max = utc

        return child_index_max

    def add_new_node(self, node_index, action):

        curr_gameState = self.digraph.nodes[node_index]["GameState"]
        child_gameState = curr_gameState.step(action)
        self.digraph.add_node(self.node_counter,
                              attr_dict={"N": 0,
                                         "Q": 0,
                                         "uct": 0,
                                         'expanded': False,
                                         'GameState': child_gameState})
        self.digraph.add_edge(node_index, self.node_counter, attr_dict={'action': action})
        child_node_index = self.node_counter
        self.node_counter += 1

        return child_node_index

    def select(self, node_index):

        # If the node is not fully expanded, select the node to expand
        if not self.digraph.nodes[node_index]['expanded']:
            return node_index
        # Otherwise proceed traversal by finding the node that maximizes the UTC
        else:
            return self.select(self.select_UTC_policy(node_index))

    def expand(self, node_index):

        # If the node is not fully expanded, then choose one of the action to create a
        # new child node
        curr_node = self.digraph.nodes[node_index]
        curr_gameState = curr_node["root_GameState"]

        legal_moves = curr_gameState.legal_moves
        print('Legal moves: {}'.format(legal_moves))

        visited_actions = set()

        for edge in self.digraph.edges(node_index):
            incidentNode1 = edge[0]
            if incidentNode1 == node_index:
                incidentNode2 = edge[1]
                action_taken = self.digraph[incidentNode1][incidentNode2]["action"]
                visited_actions.add(action_taken)

        unvisited_actions = legal_moves - visited_actions
        print('Unvisited moves: {}'.format(unvisited_actions))

        chosen_action = np.random.choice(unvisited_actions)

        child_node_index = self.add_new_node(node_index, chosen_action)

        if len(self.digraph.edges(node_index)) == len(legal_moves):
            self.digraph.nodes[node_index]['expanded'] = True
            print('Node is expanded')

        return child_node_index

    @staticmethod
    def simulate_policy(gameState: GameState):
        # This is a weak simulation policy
        return np.random.choice(gameState.legal_moves)

    def simulate(self, node_index):

        curr_gameState = self.digraph.nodes[node_index]["GameState"]
        while not curr_gameState.winner():

            action = self.simulate_policy(curr_gameState)
            curr_gameState = curr_gameState.step(action)

        if curr_gameState.winner() == self.player:
            return 1

        else:
            return 0

    def backpropagate(self, terminal_node_index, reward):
        curr_node_index = terminal_node_index
        while terminal_node_index != 0:
            self.digraph.nodes[terminal_node_index]['N'] += 1
            self.digraph.nodes[terminal_node_index]['Q'] += reward
            print('Updating to n={} and w={}:\n{}'.format(self.digraph.nodes[curr_node_index]['N'],
                                                          self.digraph.nodes[curr_node_index]['Q'],
                                                          self.digraph.nodes[curr_node_index]['GameState']))
            curr_node_index = self.digraph.predecessors(curr_node_index)[0]
