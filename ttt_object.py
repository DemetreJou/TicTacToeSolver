class TicTacToe:

    def __init__(self):
        # flattened view, each row appeneded to each other from top to bottom
        # X always goes first
        self.state = '         '
        self.player = 'X'
        self.winner = None

    def allowed_moves(self) -> list:
        """
        Adds self.player to every open space on the board
        :return: a list of possible states from current state
        :rtype: list
        """
        states = []
        for i in range(len(self.state)):
            if self.state[i] == ' ':
                states.append(self.state[:i] + self.player + self.state[i+1:])
        return states

    def make_move(self, next_state):
        """
        Moves the current board state to the given next_state
        updates the current player
        :param next_state: the state of the next move
        :type next_state: ttt_object
        """
        if self.winner:
            raise(Exception("Game already has a winner, cannot make a move on an ended game"))
        if not self.__valid_move(next_state):
            raise(Exception("Can't make move from {} to {}".format(self.state, next_state)))
        # next_state is valid
        self.state = next_state
        self.winner = self.find_winner(self.state)
        # changes the currret player
        if self.winner:
            self.player = None
        elif self.player == "X":
            self.player = 'O'
        else:
            self.player = 'X'

    def playable(self):
        """
        :return: if the game is still playable, i.e not over and moves left
        :rtype: bool
        """
        return not self.winner and any(self.allowed_moves())

    def find_winner(self, state):
        """
        :param state: the given state of the game
        :return: the winner of the game
        :rtype: string
        """
        winner = None
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                 (0, 3, 6), (1, 4, 7), (2, 5, 8),
                 (0, 4, 8), (2, 4, 6)
                 ]
        for line in lines:
            line_state = state[line[0]] + state[line[1]] + state[line[2]]
            if line_state == 'XXX':
                winner = 'X'
            elif line_state == 'OOO':
                winner = 'O'

        return winner

    def __valid_move(self, next_state):
        """
        :return: if a state is valid from current state
        :rtype: bool
        """
        allowed_moves = self.allowed_moves()
        if any(state == next_state for state in allowed_moves):
            return True
        return False

    def __str__(self):
        s = self.state
        print('     {} | {} | {} '.format(s[0], s[1], s[2]))
        print('    -----------')
        print('     {} | {} | {} '.format(s[3], s[4], s[5]))
        print('    -----------')
        print('     {} | {} | {} '.format(s[6], s[7], s[8]))
