import reversi
import numpy as np

class Player:
    def __init__(self):
        pass

    def select(self, game, board, color):
        return None

class StdInput(Player):
    def __init__(self):
        super().__init__()

    def select(self, game, board, color):
        if len(game.puttableCells(board, color)) == 0:
            return None
        return self.ask(game, board, color)

    def ask(self, game, board, color):
        print("you are", "X" if color == reversi.BLACK else "O")
        while True:
            s = input("input position (ex. A3):")
            if len(s) == 2:
                y = "ABCDEFGH".find(s[0])
                x = "12345678".find(s[1])
                if game.canPut(board, color, (x, y)):
                    return (x, y)
                else:
                    print("Can't put there'")

class RandomUniform(Player):
    def __init__(self):
        super().__init__()

    def select(self, game, board, color):
        return self.selectRandomly(game, board, color)

    def selectRandomly(self, game, board, color):
        cells = game.puttableCells(board, color)
        if len(cells) == 0:
            return None
        else:
            np.random.shuffle(cells)
            return cells[0]

class RandomMTS(Player):
    def __init__(self, playoutNum=100, maxDepth=-1, dumpNodes=False):
        super().__init__()
        self.playoutNum = playoutNum
        self.maxDepth = maxDepth
        self.dumpNodes = dumpNodes

    def select(self, game, board, color):
        return self.searchAndSelect(game, board, color, self.playoutNum, self.maxDepth)

    def searchAndSelect(self, game, board, color, playoutNum, maxDepth):
        rootNode = MTSNode(game, None, board, color, maxDepth)
        for i in range(playoutNum):
            node = rootNode

            while len(node.puttables) == 0 and len(node.children) > 0:
                node = node.selectNode()

            if len(node.puttables) > 0:
                node = node.expandChild()

            win = self.playout(game, node.board, node.color)
            node.backpropagate(win)
        if self.dumpNodes:
            rootNode.dump()
        return rootNode.selectMove()
  
    def playout(self, game, board, color):
        board = np.copy(board)
        while True:
            puttables = game.puttableCells(board, color)
            np.random.shuffle(puttables)
            p = puttables[0] if len(puttables) > 0 else None
            if p is None:
                color = -color
                if not game.canPut(board, color):
                    break
                continue
            board = game.put(board, color, p)
            color = -color
        return game.judge(board)


class MTSNode:
    def __init__(self, game, parent, board, color, maxDepth=-1, move = None):
        self.game = game
        self.parent = parent

        self.board = board
        self.color = color

        self.move = move
        self.maxDepth = maxDepth

        if maxDepth == 0:
            self.puttables = []
        else:
            self.puttables = game.puttableCells(self.board, self.color)
            if len(self.puttables) == 0: # when pass
                self.color = -color
                self.puttables = game.puttableCells(self.board, self.color)
        
        self.children = []
        
        # number of wins of oppent(=-self.color)
        self.opponentTotalWins = 0
        self.totalPlayouts = 0

    def expandChild(self):
        np.random.shuffle(self.puttables)
        move = self.puttables.pop()
        board = self.game.put(self.board, self.color, move)
        child = MTSNode(self.game, self, board, -self.color, self.maxDepth-1, move)
        self.children.append(child)
        return child

    def selectNode(self):
        max = -9999
        ret = None
        for child in self.children:
            ucb = self.ucb(child)
            if max <= ucb:
                max = ucb
                ret = child
        return ret

    def selectMove(self):
        if not self.parent is None:
            raise Exception("selectMove is only for rootNode.")
        if len(self.children)==0 and len(self.puttables)==0:
            return None
        else:
            ret = None
            max = -10000
            for c in self.children:
                score = c.opponentTotalWins / c.totalPlayouts
                if score >= max:
                    ret = c
                    max = score
            return ret.move

    def ucb(self, child):
        c = 1
        return child.opponentTotalWins / child.totalPlayouts \
                + c * np.sqrt(np.log(self.totalPlayouts) / child.totalPlayouts)

    def playout(self):
        win = self.game.playout(self.board, self.color)
        self.backpropagate(win)

    def backpropagate(self, win):
        node = self
        while not node is None:
            if node.color == -win:
                node.opponentTotalWins += 1
            node.totalPlayouts += 1
            node = node.parent

    def getRootNode(self):
        node = self
        while not node.parent is None:
            node = node.parent
        return node

    def printRoute(self):
        node = self
        while not node.parent is None:
            print(node.move, end="<-")
            node = node.parent
            print("")

    def dump(self, ucb=0, pad=0):
        print("- "*pad, end="")
        print("{0}:{1} ucb:{2:5f} playouts:{3}".format(
            "BLACK" if self.color == reversi.BLACK else "WHITE",
            self.move,
            ucb,
            self.totalPlayouts))
        for c in self.children:
            u = self.ucb(c)
            c.dump(u,pad+1)