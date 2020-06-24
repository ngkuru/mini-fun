import torch
from torch import nn, optim
from game import Mancala
import random

torch.manual_seed(0)

model = nn.Sequential(nn.Linear(14, 128), nn.ReLU(),
                    nn.Linear(128, 128), nn.ReLU(),
                    nn.Linear(128, 128), nn.ReLU(),
                    nn.Linear(128, 1)
                    )

def find_move(mancala, strategy):
    valid = [a for a in range(6) if mancala.valid(a)]
    
    candidates = []
    turns = []
    for a in valid:
        board, turn = mancala.sim(a)
        if turn == 0:
            candidates.append(board)
        else:
            candidates.append(board[7:] + board[:7])
        turns.append(turn)

    candidates = torch.Tensor(candidates)
    turns = torch.Tensor(turns)
    
    mid = model(candidates).view(-1)
    scores = torch.where(turns != mancala.turn, 48-mid, mid)
    
    if strategy == "greedy":
        index = torch.argmax(scores).item()
        return valid[index], scores[index]

    if strategy == "random_walk":
        index = random.randint(0, len(valid)-1)
        return valid[index], scores[index]

    if strategy == "epsilon_greedy":
        if torch.rand(1).item() >= 0.9:
            index = torch.argmax(scores).item()
        else:
            index = random.randint(0, len(valid)-1)
        return valid[index], scores[index]
        
def play(fp_strategy, sp_strategy, verbose=True):
    mancala = Mancala()

    while not mancala.end():
        strategy = fp_strategy if mancala.turn == 0 else sp_strategy
        move, _ = find_move(mancala, strategy)
        mancala.move(move)

    if verbose:
        mancala.printBoard()
    return mancala.history

def train(board, loss_fn=nn.MSELoss(), optimizer=optim.SGD(model.parameters(), lr=0.0001)):
    x = torch.Tensor(board)
    y_pred = model(x)
    
    if x[6] + x[13] == 48:
        y = x[6] - x[13]
    else:
        mancala = Mancala()
        mancala.board = board
        with torch.no_grad():
            _, y = find_move(mancala, "greedy")

    loss = loss_fn(y_pred, y.view(-1))
    # print(y, y_pred, loss)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

if __name__ == "__main__":
    model.load_state_dict(torch.load("model.pth"))

    for epoch in range(1000):
        history = play("epsilon_greedy", "epsilon_greedy", verbose=False)
        history.reverse()
        
        # Can't train for final board
        for board in history:
            train(board)

        print(f"completed epoch {epoch}")

    torch.save(model.state_dict(), "train1000.pth")