from ttt_object import TicTacToe
from q_learning_agent import Agent


agent = Agent(TicTacToe, epsilon=0.1, alpha=1.0)
agent.learn_game(30000)
agent.round_V()
agent.save_v_table()
