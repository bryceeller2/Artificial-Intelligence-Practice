import math
import random
import sys
import time

CONNECT = 3
COLS = 4
ROWS = 3
EMPTY = ' '
TIE = 'TIE'

class Connect3Board:
    def __init__(self, string=None):
        if string is not None:
            self.b = [list(line) for line in string.split('|')]
        else:
            self.b = [list(EMPTY * ROWS) for i in range(COLS)]

    def compact_string(self):
        return '|'.join([''.join(row) for row in self.b])

    def clone(self):
        return Connect3Board(self.compact_string())

    def get(self, i, j):
        return self.b[i][j] if i >= 0 and i < COLS and j >= 0 and j < ROWS else None

    def row(self, j):
        return [self.get(i, j) for i in range(COLS)]

    def put(self, i, j, val):
        self.b[i][j] = val
        return self

    def empties(self):
        return self.compact_string().count(EMPTY)

    def first_empty(self, i):
        j = ROWS - 1
        if self.get(i, j) != EMPTY:
            return None
        while j >= 0 and self.get(i, j) == EMPTY:
            j -= 1
        return j+1
    
    def place(self, i, label):
        j = self.first_empty(i)
        if j is not None:
            self.put(i, j, label)
        return self

    def equals(self, board):
        return self.compact_string() == board.compact_string()
    
    def next(self, label):
        boards = []
        for i in range(COLS):
            j = self.first_empty(i)
            if j is not None:
                board = self.clone()
                board.put(i, j, label)
                boards.append(board)
        return boards
    
    def _winner_test(self, label, i, j, di, dj):
        for _ in range(CONNECT-1):
            i += di
            j += dj
            if self.get(i, j) != label:
                return False
        return True
    
    def getNextTurn(self):
        xCount = 0
        oCount = 0
        for row in self.b:
            for char in row:
                if char == 'X':
                    xCount+=1
                if char == 'O':
                    oCount+=1
                    
        if xCount >  oCount:
            return 'O'
        else:
            return 'X'
    
    def winner(self):
        for i in range(COLS):
            for j in range(ROWS):
                label = self.get(i, j)
                if label != EMPTY:
                    if self._winner_test(label, i, j, +1, 0) \
                            or self._winner_test(label, i, j, 0, +1) \
                            or self._winner_test(label, i, j, +1, +1) \
                            or self._winner_test(label, i, j, -1, +1):
                        return label
        return TIE if self.empties() == 0 else None
    
    def utility(self,label):
        util=0
        player = label
        if self.winner() is label:
            return 999999999
        for i in range(COLS):
            for j in range(ROWS):
                label = self.get(i,j)
                if label is player:
                    if self.get(i,j+1) is player \
                            or self.get(i+1,j) is player \
                            or self.get(i+1,j+1) is player \
                            or self.get(i-1,j+1) is player:
                        util+=1
        return util
                        

    def __str__(self):
        return stringify_boards([self])
    
class Game:
    def __init__(self, board = Connect3Board()):
        self.board = board
        self.moves = [board]
        self.player1 = RandomPlayer('X')
        self.player2 = RandomPlayer('O')
    
    def playerMove(self, player):
        currentBoard = self.moves[-1]
        newMove = player.makeMove(currentBoard)
        self.moves.append(newMove)
        return newMove
    
    def playGame(self):
        currentBoard = self.moves[-1]
        currentPlayer = self.player1
        
        while currentBoard.winner() is None:
            currentBoard = self.playerMove(currentPlayer)
            if currentPlayer is self.player1:
                currentPlayer = self.player2
            else:
                currentPlayer = self.player1
        
        return currentBoard.winner()
            
def stringify_boards(boards):
    if len(boards) > 6:
        return stringify_boards(boards[0:6]) + '\n' + stringify_boards(boards[6:])
    else:
        s = ' '.join([' ' + ('-' * COLS) +' '] * len(boards)) + '\n'
        for j in range(ROWS):
            rows = []
            for board in boards:
                rows.append('|' + ''.join(board.row(ROWS-1-j)) + '|')
            s += ' '.join(rows) + '\n'
        s += ' '.join([' ' + ('-' * COLS) +' '] * len(boards))
        return s

class Player:
    def __init__(self, label):
        self.label = label

class RandomPlayer(Player):
    def makeMove(self, board):
        moves = board.next(self.label)
        moveCount = len(moves)
        move = moves[random.randint(0,moveCount-1)]
        return move
    
class MinimaxPlayer(Player):
    def minVal(self, board, depth=0):
        if board.winner():
            return board.utility(self.label) * (1-(.01*depth))
        else:
            successors = board.next(board.getNextTurn())
            utilityValues = []
            for board in successors:
                utilityValues.append(self.maxVal(board, depth+1))
            return min(utilityValues)
    
    def maxVal(self, board, depth=0):
        if board.winner():
            return board.utility(self.label) * (1-(.01*depth))
        else:
            successors = board.next(board.getNextTurn())
            utilityValues = []
            for board in successors:
                utilityValues.append(self.minVal(board, depth+1))
            return max(utilityValues)
        
    def getMinimaxMove(self,board,player):
        moves = board.next(player)
        utils = []
        
        for move in moves:
            utils.append(self.minVal(move))
        
        index = utils.index(max(utils))
        return moves[index]
    
    def makeMove(self, board):
        player = self.label
        move = self.getMinimaxMove(board,player)
        return(move)
    
class MinimaxAlphaBetaPlayer(MinimaxPlayer):
    def minVal(self, board, depth=0, localMax=None):
        if board.winner():
            return board.utility(self.label) * (1-(.01*depth))
        else:
            successors = board.next(board.getNextTurn())
            utilityValues = []
            for board in successors:
                if (len(utilityValues) > 0):
                    utilityValue = self.maxVal(board, depth+1, min(utilityValues))
                else:
                    utilityValue = self.maxVal(board, depth+1)
                    
                utilityValues.append(utilityValue)
                if localMax is not None and localMax > utilityValue: #if we find  a smaller value, we dont need to keep looking
                    return min(utilityValues)
                
            return min(utilityValues)
    
    def maxVal(self, board, depth=0, localMin=None):
        if board.winner():
            return board.utility(self.label) * (1-(.01*depth))
        else:
            successors = board.next(board.getNextTurn())
            utilityValues = []
            for board in successors:
                if (len(utilityValues) > 0):
                    utilityValue = self.minVal(board, depth+1, max(utilityValues))
                else:
                    utilityValue = self.minVal(board, depth+1)
                    
                utilityValues.append(utilityValue)
                if localMin is not None and localMin < utilityValue: #if we find  a larger value, we dont need to keep looking
                    return max(utilityValues)
                
            return max(utilityValues)
                    
class Game:
    def __init__(self, player1, player2, board = Connect3Board()):
        self.board = board
        self.moves = [board]
        self.player1 = player1
        self.player2 = player2
    
    def playerMove(self, player):
        currentBoard = self.moves[-1]
        newMove = player.makeMove(currentBoard)
        self.moves.append(newMove)
        return newMove
    
    def playGame(self):
        currentBoard = self.moves[-1]
        
        token = currentBoard.getNextTurn()
        if token == 'X':        
            currentPlayer = self.player1
        else:
            currentPlayer = self.player2
        
        while currentBoard.winner() is None:
            start_time = time.time()
            #Uncomment these lines to run timing tests
#             print(stringify_boards([currentBoard]))
            currentBoard = self.playerMove(currentPlayer)
            
            timeelapsed = time.time() - start_time
#             print("Time elapsed: " +str(timeelapsed))
            if currentPlayer is self.player1:
                currentPlayer = self.player2
            else:
                currentPlayer = self.player1
            start_time = time.time()
        
        return currentBoard.winner()


if __name__ == "__main__":

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        board = Connect3Board()
        if cmd == 'print':
            print(board)
        if cmd == 'next':
            boards = board.next()
            print(stringify_boards(boards))
        if cmd == 'random':
            player1 = RandomPlayer('X')
            player2 = RandomPlayer('O')
            game = Game(player1, player2)
            winner = game.playGame()
            print(stringify_boards(game.moves))
        if cmd == 'minimax':
            player1 = RandomPlayer('X')
            player2 = MinimaxPlayer('O')
            game = Game(player1, player2)
            winner = game.playGame()
            print(stringify_boards(game.moves))
        if cmd == 'alphabeta':
            player1 = RandomPlayer('X')
            player2 = MinimaxAlphaBetaPlayer('O')
            game = Game(player1, player2)
            winner = game.playGame()
            print(stringify_boards(game.moves))
        
    if len(sys.argv) > 2:
        cmd = sys.argv[1]
        board = sys.argv[2]
        board = Connect3Board(board)
        if cmd == 'next':
            token = board.getNextTurn()
            boards = board.next(token)
            print(stringify_boards(boards))
        if cmd == 'random':
            player1 = RandomPlayer('X')
            player2 = RandomPlayer('O')
            game = Game(player1, player2, board)
            winner = game.playGame()
            print(stringify_boards(game.moves))
        
        
#     test = "    |O   |O   |    "
#     test2 =  "   |OXO|OOX|   "
#     board = Connect3Board(test2)
    
#     print(stringify_boards([board]))
#     token = board.getNextTurn()
#     boards = board.next(token)
    
#     print(stringify_boards(boards))

#     player1 = MinimaxAlphaBetaPlayer('X')
#     player2 = RandomPlayer('O')
#     game = Game(player1, player2)
#     winner = game.playGame()
#     print(stringify_boards(game.moves))
    
#     player1 = RandomPlayer('X')
#     player2 = MinimaxPlayer('O')
#     game = Game(player1, player2)
#     winner = game.playGame()
#     print(stringify_boards(game.moves))