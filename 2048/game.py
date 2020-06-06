import numpy as np
import random

def collapse(v, dir):
    prior = [x for x in v if x != 0]
    posterior = []
    score = 0

    if dir == 0:
        i = 0
        while i < len(prior):
            if i == len(prior) - 1 or prior[i] != prior[i+1]:
                posterior.append(prior[i])
                i += 1
            else:
                posterior.append(prior[i] * 2)
                score += prior[i] * 2
                i += 2
        
        while len(posterior) < 4:
            posterior.append(0)
        return posterior, score
    else:
        i = len(prior) - 1
        while i >= 0:
            if i == 0 or prior[i] != prior[i-1]:
                posterior.append(prior[i])
                i -= 1
            else:
                posterior.append(prior[i] * 2)
                score = prior[i] * 2
                i -= 2
        
        while len(posterior) < 4:
            posterior.append(0)    
        return posterior[::-1], score

def up(board):
    score = 0
    for i in range(4):
        board[:, i], partial_score = collapse(board[:, i], 0)
        score += partial_score
    return score

def down(board):
    score = 0
    for i in range(4):
        board[:, i], partial_score = collapse(board[:, i], 1)
        score += partial_score
    return score

def left(board):
    score = 0
    for i in range(4):
        board[i, :], partial_score = collapse(board[i, :], 0)
        score += partial_score
    return score

def right(board):
    score = 0
    for i in range(4):
        board[i, :], partial_score = collapse(board[i, :], 1)
        score += partial_score
    return score

def playable(board):
    inp = board.copy()
    
    for func in (up, down, left, right):
        func(inp)
        if (inp != board).any():
            return True
    return False

def generate_number(board):
    empty = np.where(board == 0)
    index = random.randint(0, len(empty[0]) - 1)
    place = empty[0][index], empty[1][index]
    board[place] = 2 if random.uniform(0, 1) < 0.9 else 4

def play():
    board = np.zeros((4, 4), dtype=int)
    moves = {"up":up, "down":down, "left":left, "right":right}
    score = 0

    while True:
        generate_number(board)
        print(f"Score: {score}")
        print(board)
        print()
        if not playable(board):
            break

        old = board.copy()

        move = input("Pick a move: ")
        while move not in moves:
            move = input("Please pick a valid move: ")
        partial_score = moves[move](board)

        while (old == board).all() or move not in moves:
            move = input("Please pick a valid move: ")
            partial_score = moves[move](board)

        score += partial_score
        print()

    print(f"Final score: {score}")

def state(board):
    return(tuple(board.view(-1)))
