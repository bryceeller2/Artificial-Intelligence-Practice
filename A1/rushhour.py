import sys

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
        
    def Clone(self):
        newBoard = Board()
        newBoard.fromArr(self.arr)
        return newBoard
    
    def done(self):
        if(self.arr[2][5] == 'x'):
            return True
        else:
            return False

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
                    newBoard = self.Clone()
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
                    newBoard = self.Clone()
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
                    newBoard = self.Clone()
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
                    newBoard = self.Clone()
                    for j in range(i):
                        newBoard.moveCar(targetCar.letter, "down")
                    boardList.append(newBoard)
                    i+=1
        return boardList

command = sys.argv[1]

if len(sys.argv)>2:
    
    command2 = sys.argv[2]
    if (command=="print"):
        board = Board()
        board.fromStr(command2)
        board.printBoard()

    elif command=="next":
        board = Board()
        board.fromStr(command2)
        for c in board.carsList:
            boards = board.next_for_car(c.letter)
            for a in boards:
                a.printBoard()
                
    elif command=="done":
        board = Board()
        board.fromStr(command2)
        print(board.done())
    else:
        print("please enter commands \"print\", \"done\", or \"next\".")
        
else:        
    if command=="print":
        test1 = "  o aa|  o   |xxo   |ppp  q|     q|     q"
        board = Board()
        board.fromStr(test1)
        board.printBoard()

    elif command=="done":
        test1 = "  o aa|  o   |xxo   |ppp  q|     q|     q" 
        board = Board()
        board.fromStr(test1)
        print(board.done())

    elif command=="next":
        test1 = "  o aa|  o   |xxo   |ppp  q|     q|     q" 
        board = Board()
        board.fromStr(test1)
        for c in board.carsList:
            boards = board.next_for_car(c.letter)
            for a in boards:
                a.printBoard()
    else:
        print("please enter commands \"print\", \"done\", or \"next\".")

#End state test string
#test2 = "  o aa|  o   |  o xx|ppp  q|     q|     q"
