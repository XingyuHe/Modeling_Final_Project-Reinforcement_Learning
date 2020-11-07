from gameState import GameState
import numpy as np
import networkx as nx


class MonteCarloTreeSearch(object):

    def __init__(self, player, root_GameState, utc_explore_parameter):

        self.node_counter = 0
        self.root_GameState = root_GameState
        self.action_space = self.root_GameState.action_space()
        self.UTC_explore_parameter = utc_explore_parameter
        self.searchTimes = 100

        self.digraph = nx.DiGraph()
        self.digraph.add_node(self.node_counter, Q=0, N=0, uct=0, expanded=False, GameState=self.root_GameState)
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
            if selected_node == None:
                break
            print('================ ( expansion ) ================')
            expand_node = self.expand(selected_node)
            print('================ ( simulation ) ================')
            result = self.simulate(expand_node)
            print('================ ( backpropagation ) ================')
            self.backpropagate(expand_node, result)

    def select_UTC_policy(self, node_index):

        children = self.digraph.successors(node_index)

        child_index_max = None
        utc_max = 0
        n_parent = self.digraph.nodes[node_index]["N"]

        turn = self.digraph.nodes[node_index]["GameState"].turn()

        for child_index in children:
            # In case that I select a game state that is a terminal state
            if self.digraph.nodes[child_index]["GameState"].done == False:
                q_child = self.digraph.nodes[child_index]["Q"]
                n_child = self.digraph.nodes[child_index]["N"]

                if turn == self.player:
                    utc = q_child / n_child + self.UTC_explore_parameter * np.sqrt(np.log(n_parent) / n_child)
                else:
                    utc = 1 - q_child / n_child

                self.digraph.nodes[child_index]['uct'] = utc
                if utc > utc_max:
                    child_index_max = child_index
                    utc_max = utc

        return child_index_max

    def add_new_node(self, node_index, action):

        curr_gameState = self.digraph.nodes[node_index]["GameState"]
        child_gameState = curr_gameState.step(action)
        self.digraph.add_node(self.node_counter, Q=0, N=0, uct=0, expanded=False, GameState=child_gameState)
        self.digraph.add_edge(node_index, self.node_counter, action=action)
        child_node_index = self.node_counter
        self.node_counter += 1

        return child_node_index

    def select(self, node_index):

        # If the node is not fully expanded, select the node to expand
        if not self.digraph.nodes[node_index]['expanded']:
            print("Selected node index: {}".format(node_index))
            return node_index
        # Otherwise proceed traversal by finding the node that maximizes the UTC
        else:
            selected_node_index = self.select_UTC_policy(node_index)
            if selected_node_index == None:
                print("A terminal node is selected")
                return None
            else:
                return self.select(selected_node_index)


    def expand(self, node_index):

        # If the node is not fully expanded, then choose one of the action to create a
        # new child node
        curr_node = self.digraph.nodes[node_index]
        curr_gameState = curr_node["GameState"]

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

        chosen_action = np.random.choice(list(unvisited_actions))

        child_node_index = self.add_new_node(node_index, chosen_action)
        print('Expanded child node index: {}'.format(child_node_index))

        if len(self.digraph.edges(node_index)) == len(legal_moves):
            self.digraph.nodes[node_index]['expanded'] = True
            print('Node is expanded')

        return child_node_index

    @staticmethod
    def simulate_policy(gameState: GameState):
        # This is a weak simulation policy
        return np.random.choice(list(gameState.legal_moves))

    def simulate(self, node_index):

        curr_gameState = self.digraph.nodes[node_index]["GameState"]
        while not curr_gameState.winner():

            # print(curr_gameState.winner)
            action = self.simulate_policy(curr_gameState)
            curr_gameState = curr_gameState.step(action)

        if curr_gameState.winner() == self.player:
            return 1

        else:
            return 0

    def backpropagate(self, node_index, reward):

        def backpropagate_sub_fn(curr_node_index, result):
            self.digraph.nodes[curr_node_index]['N'] += 1
            self.digraph.nodes[curr_node_index]['Q'] += result
            print('Updating to N={} and Q={}:\n{}'.format(self.digraph.nodes[curr_node_index]['N'],
                                                          self.digraph.nodes[curr_node_index]['Q'],
                                                          self.digraph.nodes[curr_node_index]['GameState']))

        for curr_node_index in self.digraph.predecessors(node_index):
            backpropagate_sub_fn(curr_node_index, reward)

        backpropagate_sub_fn(node_index, reward)
