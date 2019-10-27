import sys
import math
import random

class Path:

    def __init__(self):
        self.boards=[]
    
    def setBoards(self, boards):
        self.boards = boards
    
    def add(self, board):
        self.boards.append(board)
    
    def clone(self):
        newPath = Path()
        newPath.setBoards(self.boards.copy())
        return newPath
    
    def last(self):
        if len(self.boards) >= 1:
            return self.boards[len(self.boards)-1]
        else:
            return None
        
    def pop(self):
        return self.boards.pop()
    
    def printPath(self):
        #Each line will have six boards
        for i in range(math.ceil(len(self.boards)/6)):
            #Each board has eight rows
            for k in range(8):
                #print boards 0-5,6-11,etc
                for board in self.boards[i*6:((i+1)*6)]:
                    arr = board.getPrintableBoard()
                    print(arr[k], end=" ")
                print()
            print()

class Car:
    
    def __init__(self, letter):
        self.letter = letter
        self.coords = []
        self.orientation=None

class Board:
    
    def __init__(self):
        self.arr=[]
    
    def fromArr(self, arr):
        self.arr=arr
        self.carsList = self.getCarList()
        
    def fromStr(self, s):
        arr=[]
        arr.append(s[0:6])
        arr.append(s[7:13])
        arr.append(s[14:20])
        arr.append(s[21:27])
        arr.append(s[28:34])
        arr.append(s[35:41])
        self.arr = arr
        self.carsList = self.getCarList()
        
    def clone(self):
        newBoard = Board()
        newBoard.fromArr(self.arr)
        return newBoard
    
    def done(self):
        if(self.arr[2][5] == 'x'):
            return True
        else:
            return False
        
    def getPrintableBoard(self):
        arr = []
        arr.append(" ------ ")
        for i in range(6):
            if i is not 2:
                arr.append("|" +"".join(self.arr[i]) +"|")
            else:
                arr.append("|" +"".join(self.arr[i]) +" ")
        arr.append(" ------ ")
        return arr
    
    def printBoard(self):
        print(" ------ ")
        for row in range(len(self.arr)):
            print("|", end="")
            for space in self.arr[row]:
                print(space, end="")
            if row is not 2:
                print("|", end="")
            print("")
        print(" ------ ")
        return "Board Printed"
    
    def refreshBoard(self):
        carsList = self.carsList
        
        newBoard = []
        for i in range(6):
            newRow = []
            for j in range(6):
                newRow.append(" ")
            newBoard.append(newRow)
        
        for car in carsList:
            for coord in car.coords:
                newBoard[coord[1]][coord[0]] = car.letter
                
        self.arr = newBoard
    
    def getCarList(self):
        
        boardArrays = self.arr
        carsList=[]

        for i in range(6):
            for j in range(6):
                #First check to see if a space is occupied
                if boardArrays[i][j] is not ' ':
                    seen=False
                    for car in carsList:
                        if car.letter == boardArrays[i][j]:
                            seen = True
                            car.coords.append([j,i])
                            break
                    if not seen:
                        car = Car(boardArrays[i][j])
                        car.coords.append([j,i])
                        carsList.append(car)
                        
        for car in carsList:
            pos1 = car.coords[0]
            pos2 = car.coords[1]
            
            if (pos1[1] - pos2[1] == 0):
                car.orientation = "H"
            elif (pos1[0] - pos2[0] == 0):
                car.orientation = "V"
            else:
                raise Exception("Car Orientation error")
        return carsList
#         for car in carsList:
#             print("CAR: " +car.letter)
#             print("COORDS: " +str(car.coords))

    def moveCar(self, car, direction):
        for i in range(len(self.carsList)):
            if self.carsList[i].letter == car:
                for j in range(len(self.carsList[i].coords)):
                    if direction == "up" or direction == "north":
                        self.carsList[i].coords[j][1]-=1
                    if direction == "down" or direction == "south":
                        self.carsList[i].coords[j][1]+=1
                    if direction == "left" or direction == "west":
                        self.carsList[i].coords[j][0]-=1
                    if direction == "right" or direction == "east":
                        self.carsList[i].coords[j][0]+=1
        self.refreshBoard()
    
    def next_for_car(self,car):
        cars = self.carsList
        targetCar=None
        boardList=[]
        for c in cars:
            if c.letter == car:
                targetCar = c
        if targetCar==None:
            raise exception("no car found in next_for_car")
            
        end1 = targetCar.coords[0]
        end2 = targetCar.coords[len(targetCar.coords)-1]
        
        if targetCar.orientation == 'H':
            #left
            empty = True
            i=1
            while empty == True:
                leftCoord = [end1[0]-i, end1[1]]
                for c in cars:
                    for coord in c.coords:
                        if coord == leftCoord or leftCoord[0]<0:
                            empty = False
                if empty:
                    newBoard = self.clone()
                    for j in range(i):
                        newBoard.moveCar(targetCar.letter, "left")
                    boardList.append(newBoard)
                    i+=1
            #right
            empty = True
            i=1
            while empty == True:
                rightCoord = [end2[0]+i, end2[1]]
                for c in cars:
                    for coord in c.coords:
                        if coord == rightCoord or rightCoord[0]>5:
                            empty = False
                if empty:
                    newBoard = self.clone()
                    for j in range(i):
                        newBoard.moveCar(targetCar.letter, "right")
                    boardList.append(newBoard)
                    i+=1
        elif targetCar.orientation == 'V':
            #up
            empty = True
            i=1
            while empty == True:
                upCoord = [end1[0], end1[1]-i]
                for c in cars:
                    for coord in c.coords:
                        if coord == upCoord or upCoord[1] < 0:
                            empty = False
                if empty:
                    newBoard = self.clone()
                    for j in range(i):
                        newBoard.moveCar(targetCar.letter, "up")
                    boardList.append(newBoard)
                    i+=1
            #down
            empty = True
            i=1
            while empty == True:
                downCoord = [end2[0], end2[1]+i]
                for c in cars:
                    for coord in c.coords:
                        if coord == downCoord or downCoord[1]>5:
                            empty = False
                if empty:
                    newBoard = self.clone()
                    for j in range(i):
                        newBoard.moveCar(targetCar.letter, "down")
                    boardList.append(newBoard)
                    i+=1
        return boardList
    
    def getNextBoards(self):
        allBoards=[]
        for c in self.carsList:
            boards = self.next_for_car(c.letter)
            for a in boards:
                allBoards.append(a)
        return allBoards
    
    def printNextBoards(self):
        allBoards = self.getNextBoards()
        
        for i in range(8):
            for board in allBoards:
                arr = board.getPrintableBoard()
                print(arr[i], end=" ")
            print()
            
    def getPath(self):
        boards = []
        board = self        
        boards.append(board)
        while board.parent is not None:
            board = board.parent
            boards.append(board)
        
        path = Path()
        for board in reversed(boards):
            path.add(board)
        return path
        
    def randomWalk(self, n=10):
        i=1
        path = Path()
        path.add(self)
        while i<n and path.last().done() == False:
            currentBoard = path.last()
            nextBoards = currentBoard.getNextBoards()
            boardChoice = nextBoards[random.randint(0,len(nextBoards)-1)]
            path.add(boardChoice)
            i+=1
        return path
#         if (i<n):
#             print("solved after " +str(i) +" moves!")
#         else:
#             print("not solved :(")
    
    #for each possible move
    #print current path
    #then bfs for that move with the current path
    
    def bfs(self):
        queue = []
        path = Path()
        path.add(self)
        queue.append(path)
        totalBoardsChecked=0
        
        while True:
            currentPath = queue.pop(0)
            currentBoard = currentPath.last()
            for board in currentBoard.getNextBoards():
                totalBoardsChecked+=1
                currentPath.add(board.clone())
                print(totalBoardsChecked)
#                 Uncomment this to run slightly faster
#                 if (totalBoardsChecked%100000 == 0):
#                 2,179,597 paths checked on the test board
                currentPath.printPath()
                if board.done() is False:
                    queue.append(currentPath.clone())
                    currentPath.pop()
                else:
                    print("Successful path found after "+ str(totalBoardsChecked) +" paths searched.")
                    currentPath.printPath()
                    return currentPath
    
    def getEstimate(self):
        i=5
        estimate = 0
        while self.arr[2][i] is not 'x' and estimate < 8:
            estimate+=1
            i-=1
        if estimate < 8:
            return estimate
        else:
            return "BOARD ERROR"
        
    def getLowestF(self, arr):
        lowestVal = arr[0].g + arr[0].h
        lowestBoard = arr[0]
        for board in arr[1:]:
            if (board.g+board.h) < lowestVal:
                lowestVal = board.g+board.h
                lowestBoard = board
        
        return lowestBoard
    
    def aStar(self):
        ready=[]
        closed=[]
        self.g=0
        self.h=self.getEstimate()
        self.parent = None
        ready.append(self)
        paths=1
        while len(ready) is not 0:
            currentBoard = self.getLowestF(ready)
            paths+=1
            currentBoard.getPath().printPath()
            
            if currentBoard.done():
                #6365 paths checked on the test board
                path = currentBoard.getPath()
                print("Successful path found after "+ str(paths) +" paths searched.")
                return path
            else:
                ready.remove(currentBoard)
                closed.append(currentBoard)
                for board in currentBoard.getNextBoards():
                    board.parent = currentBoard
                    board.g = currentBoard.g+1
                    board.h = board.getEstimate()
                    ready.append(board)
        
#TESTING SECTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
# test1 = "  o aa|  o   |xxo   |ppp  q|     q|     q"
# board = Board()
# board.fromStr(test1)
# test1 = "  o   |  o   |xxo   |ppp  q|     q|     q"
# board2 = Board()
# board2.fromStr(test1)
# test1 = "  w   |  w   |  wxx |ppp  q|     q|     q"
# board3 = Board()
# board3.fromStr(test1)

# # path = board.aStar()
# # path.printPath()
# path = board.bfs()
# path.printPath()

#TESTING SECTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

command = sys.argv[1]

if len(sys.argv)>2:
    
    command2 = sys.argv[2]
    if (command=="random"):
        board = Board()
        board.fromStr(command2)
        path = board.randomWalk()
        path.printPath()
        
    elif command=="bfs":
        board = Board()
        board.fromStr(command2)
        path = board.bfs()
        path.printPath()
        
    elif command=="astar":
        board = Board()
        board.fromStr(command2)
        path = board.aStar()
        path.printPath()
        
    else:
        print("please enter commands \"random\", \"bfs\", or \"astar\".")
        
else:        
    if command=="random":
        test1 = "  o aa|  o   |xxo   |ppp  q|     q|     q"
        board = Board()
        board.fromStr(test1)
        path = board.randomWalk()
        path.printPath()

    #Over 2,000,000 paths
    elif command=="bfs":
        test1 = "  o aa|  o   |xxo   |ppp  q|     q|     q" 
        board = Board()
        board.fromStr(test1)
        path = board.bfs()
        path.printPath()

    #6365 paths
    elif command=="astar":
        test1 = "  o aa|  o   |xxo   |ppp  q|     q|     q" 
        board = Board()
        board.fromStr(test1)
        path = board.aStar()
        path.printPath()
        
    else:
        print("please enter commands \"random\", \"bfs\", or \"astar\".")
