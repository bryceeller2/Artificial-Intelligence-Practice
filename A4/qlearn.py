### import random
import sys
import random

DEFAULT_STATE = '       | ###  -| # #  +| # ####|       '

class Action:

    def __init__(self, name, dx, dy):
        self.name = name
        self.dx = dx
        self.dy = dy


ACTIONS = [
    Action('UP', 0, -1),
    Action('RIGHT', +1, 0),
    Action('DOWN', 0, +1),
    Action('LEFT', -1, 0)
]


class State:

    def __init__(self, env, x, y):
        self.env = env
        self.x = x
        self.y = y

    def clone(self):
        return State(self.env, self.x, self.y)

    def is_legal(self, action):
        cell = self.env.get(self.x + action.dx, self.y + action.dy)
        return cell is not None and cell in ' +-'
    
    def legal_actions(self, actions):
        legal = []
        for action in actions:
            if self.is_legal(action):
                legal.append(action)
        return legal
    
    def reward(self):
        cell = self.env.get(self.x, self.y)
        if cell is None:
            return None
        elif cell == '+':
            return +10
        elif cell == '-':
            return -10
        else:
            return 0

    def at_end(self):
        return self.reward() != 0

    def execute(self, action):
        self.x += action.dx
        self.y += action.dy
        return self

    def __str__(self):
        tmp = self.env.get(self.x, self.y)
        self.env.put(self.x, self.y, 'A')
        s = ' ' + ('-' * self.env.x_size) + '\n'
        for y in range(self.env.y_size):
            s += '|' + ''.join(self.env.row(y)) + '|\n'
        s += ' ' + ('-' * self.env.x_size)
        self.env.put(self.x, self.y, tmp)
        return s


class Env:

    def __init__(self, string):
        self.grid = [list(line) for line in string.split('|')]
        self.x_size = len(self.grid[0])
        self.y_size = len(self.grid)

    def get(self, x, y):
        if x >= 0 and x < self.x_size and y >= 0 and y < self.y_size:
            return self.grid[y][x]
        else:
            return None

    def put(self, x, y, val):
        if x >= 0 and x < self.x_size and y >= 0 and y < self.y_size:
            self.grid[y][x] = val

    def row(self, y):
        return self.grid[y]

    def random_state(self):
        x = random.randrange(0, self.x_size)
        y = random.randrange(0, self.y_size)
        while self.get(x, y) != ' ':
            x = random.randrange(0, self.x_size)
            y = random.randrange(0, self.y_size)
        return State(self, x, y)


class QTable:

    def __init__(self, env, actions):
        xSize = env.x_size
        ySize = env.y_size
        self.env = env
        self.actions = actions
        self.table = []
        for x in range(xSize):
            row = []
            for y in range(ySize):
                row.append([0,0,0,0])
            self.table.append(row)
        

    def get_q(self, state, action):
        # return the value of the q table for the given state, action
        index = ACTIONS.index(action)
        x = state.x
        y = state.y
        
        q = self.table[x][y][index]
        return q

    def get_q_row(self, state):
        # return the row of q table corresponding to the given state
        x = state.x
        y = state.y
        return self.table[x][y]

    def set_q(self, state, action, val):
        # set the value of the q table for the given state, action
        index = ACTIONS.index(action)
        x = state.x
        y = state.y
        
        self.table[x][y][index] = val
        return True

    def learn_episode(self, alpha=.1, gamma=.9):
        # with the given alpha and gamma values,
        # from a random initial state,
        # consider a random legal action, execute that action,
        # compute the reward, and update the q table for (state, action).
        # repeat until an end state is reached (thus completing the episode)
        # also print the state at each state
        
        env = self.env
        state = env.random_state()
        end = False
        
        while not end:
            print(state)
            legalActions = state.legal_actions(ACTIONS)
            action = legalActions[random.randint(0,len(legalActions)-1)]

            oldQ = self.get_q(state,action)
            oldState = state.clone()

            state.execute(action)
            reward = state.reward()
            if reward is not None and reward is not 0:
                end=True
            row = self.get_q_row(state)
            maxA = max(row)

            q = ((1-alpha)*oldQ) + (alpha*(reward+(gamma*maxA)))
            self.set_q(oldState, action, q)
    
    def learn(self, episodes, alpha=.1, gamma=.9):
        for i in range(episodes):
            self.learn_episode(alpha, gamma)
    
    def invertArray(self, arr):
        result = []
        for i in range(len(arr[0])):
            newRow = []
            for row in arr:
                newRow.append(row[i])
            result.append(newRow)
        return result
    
    def __str__(self):
        # return a string for the q table as described in the assignment
        result = ""
        actionIndex=0
        
        invertedTable = self.invertArray(self.table)
        
        for action in ACTIONS:
            result+= action.name + "\n"
            for row in invertedTable:
                for box in row:
                    if box[actionIndex] != 0:
                        result += str(round(box[actionIndex],2))
                    else:
                        result += "----"
                    result +="\t"
                result += "\n"
            actionIndex+=1
        return result
    

        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        env = Env(DEFAULT_STATE)
        
        if cmd == 'learn':
            qt = QTable(env, ACTIONS)
            qt.learn(100)
            print(qt)

#     env = Env(DEFAULT_STATE)
#     qt = QTable(env, ACTIONS)
#     qt.learn(100)
#     print(qt)
