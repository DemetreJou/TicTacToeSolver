"""
Agent used to train tic tac toe using reinforcement learning
"""
import csv
import random
import numpy as np
from itertools import groupby


class Agent:
    """
    let's get this bread
    """
    def __init__(self, game_class, epsilon=0.1, alpha=0.5, value_player='X'):
        # dict has keys of moves and values of q-learning values
        self.V = dict()
        self.NewGame = game_class
        self.epsilon = epsilon
        self.alpha = alpha
        self.value_player = value_player

    def state_value(self, game_state):
        return self.V.get(game_state, 0.0)

    def learn_game(self, num_episodes=1000):
        """
        runs the training num_episodes amount of times
        """
        for episode in range(num_episodes):
            self.learn_from_episode()

    def learn_from_episode(self):
        game = self.NewGame()
        # _ is used to capture the second value returned from learn_select_move
        # the first value is used in other functions
        _, move = self.learn_select_move(game)
        while move:
            move = self.learn_from_move(game, move)

    def learn_from_move(self, game, move):
        """
        Basic generic Q-learning formula to 'learn'
        """
        game.make_move(move)
        r = self.__reward(game)
        td_target = r
        next_state_value = 0.0
        selected_next_move = None
        if game.playable():
            best_next_move, selected_next_move = self.learn_select_move(game)
            next_state_value = self.state_value(best_next_move)

        current_state_value = self.state_value(move)
        td_target = r + next_state_value
        self.V[move] = current_state_value + self.alpha * (td_target - current_state_value)
        return selected_next_move

    def learn_select_move(self, game):
        """
        Decides whether it needs to min or max based on who's playing
        Then picks a move
        """
        allowed_state_values = self.__state_values(game.allowed_moves())
        if game.player == self.value_player:
            best_move = self.__argmax_V(allowed_state_values)
        else:
            best_move = self.__argmin_V(allowed_state_values)

        selected_move = best_move
        if random.random() < self.epsilon:
            selected_move = self.__random_V(allowed_state_values)

        return (best_move, selected_move)

    # NOTE!
    # learn select move is used when learning
    # play select move is used after it's been trained when playing a real game

    def play_select_move(self, game):
        """
        Picks a highest value move out of all possible moves
        """
        allowed_state_values = self.__state_values(game.allowed_moves())
        if game.player == self.value_player:
            return self.__argmax_V(allowed_state_values)
        else:
            return self.__argmin_V(allowed_state_values)

    def demo_game(self, verbose=False):
        """
        visualization of an example game with different levels of detail
        """
        game = self.NewGame()
        t = 0
        while game.playable():
            if verbose:
                print(" \nTurn {}\n".format(t))
                game.print_board()
            move = self.play_select_move(game)
            game.make_move(move)
            t += 1
        if verbose:
            print(" \nTurn {}\n".format(t))
            game.print_board()
        if game.winner:
            if verbose:
                print("\n{} is the winner!".format(game.winner))
            return game.winner
        else:
            if verbose:
                print("\nIt's a draw!")
            return '-'

    def interactive_game(self, agent_player='X'):
        """
        plays a game against the AI
        """
        game = self.NewGame()
        t = 0
        while game.playable():
            print(" \nTurn {}\n".format(t))
            game.print_board()
            if game.player == agent_player:
                move = self.play_select_move(game)
                game.make_move(move)
            else:
                move = self.__request_human_move(game)
                game.make_move(move)
            t += 1

        print(" \nTurn {}\n".format(t))
        game.print_board()

        if game.winner:
            print("\n{} is the winner!".format(game.winner))
            return game.winner
        print("\nIt's a draw!")
        return '-'

    def round_V(self):
        """
        After training, this makes action selection random from equally-good choices
        """
        for k in self.V.keys():
            self.V[k] = round(self.V[k], 1)

    def save_v_table(self):
        """
        Stores all the states + values to read
        """
        with open('state_values.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['State', 'Value'])
            all_states = list(self.V.keys())
            all_states.sort()
            for state in all_states:
                writer.writerow([state, self.V[state]])

    def __state_values(self, game_states):
        return dict((state, self.state_value(state)) for state in game_states)

    def __argmax_V(self, state_values):
        max_V = max(state_values.values())
        chosen_state = random.choice([state for state, v in state_values.items() if v == max_V])
        return chosen_state

    def __argmin_V(self, state_values):
        min_V = min(state_values.values())
        chosen_state = random.choice([state for state, v in state_values.items() if v == min_V])
        return chosen_state

    def __random_V(self, state_values):
        """
        choses random from all possible moves
        """
        return random.choice(list(state_values.keys()))

    def __reward(self, game):
        """
        This sets the rewards, can set tie to 0.5 to match other games like chess
        """
        if game.winner == self.value_player:
            return 1.0
        elif game.winner:
            return -1.0
        else:
            return 0.0

    def __request_human_move(self, game):
        allowed_moves = [i + 1 for i in range(9) if game.state[i] == ' ']
        human_move = None
        while not human_move:
            idx = int(input('Choose move for {}, from {} : '.format(game.player, allowed_moves)))
            if any([i == idx for i in allowed_moves]):
                human_move = game.state[:idx - 1] + game.player + game.state[idx:]
        return human_move


# TODO: refactor to create a manager of sorts
# Move all the gameplay code into a new file
# use this a future backend to a web app?
