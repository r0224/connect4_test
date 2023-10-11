import math
import os
import sys
import copy
import numpy as np
from connect_board import connect4_system, vs_mode, strategy_random


class Node:
    def __init__(self, state, board, choiced, parent=None):
        # 手番情報をいれる。
        self.state = state
        # board 情報を入れる。
        self.board = board
        # 子ノードのリスト
        self.children = [] 
        # 親ノード
        self.parent = parent
        # 親からの手のindex
        self.choiced = choiced
        # 初期値は0 （0で割るのを避けるために、小さい値をいれておく）
        self.visits = 0.000001
        self.value = 0.000001


def compute_uct1(node, total, const=1):
    if total != 0:
        return node.value/node.visits + const * math.sqrt(2 * math.log(total) / node.visits)
    else :
        return 0

def choose_node_by_ucb(node_list, number, ucb_const=1):
    uct1_list = [compute_uct1(node, number, ucb_const) for node in node_list]
    argmax = np.argmax(np.array(uct1_list))
    return node_list[argmax]

def result2value(winner, turn_player):
    if winner == "draw":
        value = 0.5
    elif winner == turn_player:
        value = 1.0
    else:
        value = 0
    return value

def mcts(conect_board, turn_player, playout_num=5000, threshold=10, ucb_const=1, win_value=1, draw_value=-0.5, lose_value=0):
    # 初期化
    print("Computer is now thinking", end="")

    node_tree = []
    root_node_list = []
    legal_choice_list = conect_board.can_choice()
    for choice in legal_choice_list:
        # 一手進めたボードをルートノードとして保存。
        child = copy.deepcopy(conect_board)
        child.one_move(choice, turn_player)
        node = Node(connect4_system.next_player(turn_player), child.board_data, choiced=choice)
        root_node_list.append(node)

    # ここからプレイアウトを繰り返す。
    for number in range(playout_num):
        if number % 100 == 0:
            print(".", end="", flush=True)

        # 展開済のみ木を辿る
        k = 0
        while True:
            if k == 0:
                node_list = root_node_list
            choiced_node = choose_node_by_ucb(node_list, number, ucb_const) # この関数は書け！！
            if len(choiced_node.children) == 0:
                break
            else:
                node_list = choiced_node.children
            k+=1
        # for x in root_node_list:
        #     print(x.__dict__)

        # ここからランダムに打つ
        choiced_node_tmp = copy.deepcopy(choiced_node.board)
        next_player = choiced_node.state
        winner = vs_mode(
                            connect4_system(choiced_node_tmp), 
                            {"player_1":[strategy_random, {}], "player_2": [strategy_random, {}]},
                            next_player,
                            display = False
                        )
        
        # 勝敗に応じて自身のノードの値更新、親ノードに伝播
        value = result2value(winner, turn_player)
        update_node = choiced_node
        while True:
            update_node.value += value
            update_node.visits += 1
            if update_node.parent is None:
                break
            else :
                update_node = update_node.parent

        # ゲーム木の展開
        if choiced_node.visits >= threshold:
            board_tmp = choiced_node.board
            conect_board_tmp = connect4_system(board_tmp)
            legal_choice_list = conect_board_tmp.can_choice()
            for choice in legal_choice_list:
                child = copy.deepcopy(conect_board_tmp)
                child.one_move(choice, choiced_node.state)
                node = Node(connect4_system.next_player(choiced_node.state), child.board_data, choiced=choice, parent=choiced_node)
                choiced_node.children.append(node)

    print(".")
    # １手目の試行回数を表示。
    for y in root_node_list:
        print(y.visits)
    root_node_list = sorted(root_node_list, key=lambda x: x.visits, reverse=True)

    return root_node_list[0].choiced

if __name__ == "__main__":

    conect_board = connect4_system()
    print(mcts(conect_board, "player_1"))
