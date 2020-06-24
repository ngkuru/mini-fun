import random

class End:
    pass

class Mancala(object):
    def __init__(self):
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.turn = 0
        self.ended = False

        self.history = [self.board.copy()]

    def move(self, a):
        assert not self.end(), "This game is over."
        assert self.valid(a), "Can't play on an empty hole."

        places = ((0, 6), (7, 13))
        # My/opponent first/store
        myf, mys = places[self.turn]
        opf, ops = places[(self.turn + 1) % 2]   
        
        pos = myf + a
        peb = self.board[pos]

        # Empty the starting hole and distribute pebbles
        # one in every hole except opponent's store
        self.board[pos] = 0
        # If only one pebble, start from next
        if peb == 1:
            pos = (pos + 1) % 14
        while peb > 0:
            if pos != ops:
                self.board[pos] += 1
                peb -= 1
            if peb > 0:
                pos = (pos + 1) % 14

        # If we don't end on our store, switch turn
        if pos != mys:
            self.turn = (self.turn + 1) % 2

        # If we end on a singleton in our side, take both sides
        if myf <= pos and pos < mys and self.board[pos] == 1:
            # Find the gap and add from the store to find across
            gap = mys - pos
            across = (mys + gap) % 14
            # Put all pebbles from pos and across to store
            self.board[mys] += self.board[pos] + self.board[across]
            self.board[pos], self.board[across] = 0, 0

        # If we end on an even in the opposite side, take the pebbles
        if opf <= pos and pos < opf and self.board[pos] % 2 == 0 :
            self.board[mys] += self.board[pos]
            self.board[pos] = 0

        # Check for endgame
        self.final()

        # Append to history
        entry = self.board.copy() if self.turn == 0 else self.board[7:] + self.board[:7]
        self.history.append(entry)

    def sim(self, a):
        new = Mancala()
        new.board = self.board.copy()
        new.turn = self.turn
        new.move(a)
        return new.board, new.turn

    def valid(self, a):
        places = ((0, 6), (7, 13))
        # My/opponent first/store
        myf, mys = places[self.turn]
        opf, ops = places[(self.turn + 1) % 2]   
        
        pos = myf + a
        peb = self.board[pos]
        return peb > 0 # Can't play on an empty hole.

    def final(self):
        # Zero/one first/store
        zf, zs = 0, 6
        of, os = 7, 13

        # Calculate number of pebbles
        zp = 0
        for pos in range(zf, zs):
            zp += self.board[pos]
        # If zero pebbles, take the opponent's pebbles and end
        if zp == 0:
            for pos in range(of, os):
                self.board[zs] += self.board[pos]
                self.board[pos] = 0
            self.ended = True

        # Calculate number of pebbles
        op = 0
        for pos in range(of, os):
            op += self.board[pos]
        # If zero pebbles, take the opponent's pebbles and end
        if op == 0:
            for pos in range(zf, zs):
                self.board[os] += self.board[pos]
                self.board[pos] = 0
            self.ended = True

    def end(self):
        return self.ended

    def printBoard(self):
        # Zero/one first/store
        zf, zs = 0, 6
        of, os = 7, 13

        print("  ", end=" ")
        for pos in range(os-1, of-1, -1):
            print(f"{self.board[pos]:2d}", end=" ")
        print()
        
        print(f"{self.board[os]:2d}                   {self.board[zs]:2d}")

        print("  ", end=" ")
        for pos in range(zf, zs):
            print(f"{self.board[pos]:2d}", end=" ")
        print()
        print()

# if __name__ == "__main__":
#     game = Mancala()
#     while not game.end():
#         game.printBoard()
        
#         if game.turn == 0:
#             move = int(input(f"Oyuncu {game.turn + 1} hamle yap: "))
#             game.move(move-1)
#         else:
#             print(f"Oyuncu {game.turn + 1} hamle yapiyor")
#             while True:
#                 move = random.randint(0, 5)
#                 try:
#                     game.move(move)
#                     break
#                 except:
#                     pass
#         print()
#     print(f"Son skor {game.board[6]} - {game.board[13]}")
