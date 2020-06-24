import torch
from torch import nn, optim

torch.manual_seed(0)

model = nn.Sequential(nn.Linear(14, 128), nn.ReLU(),
                      nn.Linear(128, 128), nn.ReLU(),
                      nn.Linear(128, 128), nn.ReLU(),
                      nn.Linear(128, 1)
                     )
model.load_state_dict(torch.load("train1000.pth"))

loss_fn = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.0001)

endgame_x = torch.Tensor([[0, 0, 0, 0, 0, 0, x, 0, 0, 0, 0, 0, 0, 48-x] for x in range(49)])
endgame_y = torch.Tensor([[x] for x in range(-24, 25)])

loss = 1
epoch = 0
while loss > 0.01:
    epoch += 1

    y_pred = model(endgame_x)
    loss = loss_fn(y_pred, endgame_y)

    if epoch % 10 == 9:
        print(f"epoch {epoch} loss {loss}")

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

print(model(endgame_x))

# torch.save(model.state_dict(), "endgame.pth")