import os 
import sys
import random
import argparse
from MCTS import mcts
from connect_board import connect4_system, vs_mode, strategy_random


random.seed(11)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--teban', type=str, default='gote', choices=["sente", "gote"])
    args = parser.parse_args() 

    teban = args.teban
    if teban == "gote":
        palyer_strategy_dict = {"player_1":[mcts, {"turn_player": "player_1", "playout_num":1000, "ucb_const":1.2}], "player_2": None}
    else:
        palyer_strategy_dict = {"player_1":None, "player_2": [mcts, {"turn_player": "player_2", "playout_num":1000, "ucb_const":1.2}]}

    # palyer_strategy_dict = {"player_1":[strategy_random, {}], "player_2": None}


    conect_board = connect4_system()
    winner = vs_mode(conect_board, palyer_strategy_dict)
