import os
import sys
import numpy as np
import math
import os
import copy
import random
import MCTS

random.seed(11)


def next_player(turn_player):
    if turn_player == "player_1":
        return "player_2"
    if turn_player == "player_2":
        return "player_1"


class connect4_system:
    # ボードデータの引数が渡された場合、途中からの状態。
    def __init__(self, board_data = None):
        if board_data is None:
            self.board_data = np.zeros((6,7), int)
        else :
            self.board_data = board_data
        self.player_stone_id = {"player_1": -1, "player_2": 1}
    
    def display(self):
        print(" 0  1  2  3  4  5  6")
        for cols in self.board_data:
            for x in cols:
                if x == self.player_stone_id["player_1"]:
                    print("|o ", end="")
                elif x ==  self.player_stone_id["player_2"]:
                    print("|x ", end="")
                else :
                    print("|  ", end="")
            print("|")
        print("----------------------\n")


    def one_move(self, choice:int, player="player_1"):
        assert (player == "player_1"  or  player == "player_2"), "playerは、player_1 か player_2としてください。"
        while True:
            if choice not in self.can_choice() or self.board_data[0, choice] != 0:
                # 石をおけない。
                return False
            else:
                for i in range(5,-1,-1):
                    if self.board_data[i, choice] == 0:
                        self.board_data[i, choice] =  self.player_stone_id[player]
                        return True


                
    def can_choice(self):
        return [i for i in range(7) if self.board_data[0, i] == 0]

    #自身を端として、右、下、右下、左下方向で4つ石が並んでないかをチェック。
    def check_end_one_place(self, row, col, player=None, num=4):
        right_end = col + num if col + num <= 7 else 7
        down_end = row + num if row + num <= 6 else 6
        left_end = col - num + 1 if col - num + 1 >= 0 else 0
        # 右チェック
        if abs(np.sum(self.board_data[row, col:right_end])) == num:
            return True
        # 下チェック
        if abs(np.sum(self.board_data[row:down_end, col])) == num:
            return True
        # 右下チェック
        if abs(np.sum(np.diag(self.board_data[row:down_end, col:right_end]))) == num:
            return True
        if abs(np.sum(np.diag(np.fliplr(self.board_data[row:down_end, left_end:(col+1)])))) == 4:
            return True
        return False

    def check_victory(self):
        for row in range(6):
            for col in range(7):
                if self.check_end_one_place(row, col):
                    for key, val in self.player_stone_id.items():
                        if val == self.board_data[row,col]:
                            return key
        return 
    
    @classmethod
    def next_player(cls, turn_player):
        if turn_player == "player_1":
            return "player_2"
        if turn_player == "player_2":
            return "player_1"

def strategy_random(conect_board, **args):
    return random.choice(conect_board.can_choice())

def strategy_MCTS(conect_board, UCB_const=1, threshold=10, playout_num=1000):
    return random.choice(conect_board.can_choice())

def vs_mode(conect_board:connect4_system, palyer_strategy_dict, start_player="player_1", display=True):
    # cpu vs cpu
        turn_player = start_player
        while True:
            if display == True:
                conect_board.display()

            # 勝敗判定を一番最初に行う。
            winner = conect_board.check_victory()
            if winner is not None:
                if display == True:
                    conect_board.display()
                    print(f"{winner} is the winner!!")
                return winner
            if len(conect_board.can_choice()) == 0 :
                if display == True:
                    conect_board.display()
                    print("draw!!!")
                return "draw"

            if display == True:
                print(f"{turn_player}'s turn !")
            if palyer_strategy_dict[turn_player] is not None:
                cpu_strategy = palyer_strategy_dict[turn_player][0]
                args = palyer_strategy_dict[turn_player][1]
                player_choice = cpu_strategy(conect_board, **args)
            else:
                player_choice = int(input(f"Choice column 0 ~ 6: \n"))

            if conect_board.one_move(player_choice, player=turn_player):
                turn_player = next_player(turn_player)
            else:
                print("石を置く場所は0~6で指定してね。")



