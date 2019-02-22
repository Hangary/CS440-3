from time import sleep
from math import inf
from random import randint

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True

        self.twoInARowMax = [['X','X','_'],['X','_','X'],['_','X','X']]
        self.twoInARowMin = [['O','O','_'],['O','_','O'],['_','O','O']]
        self.twoInARowBlockMin = [['O','O','X'],['O','X','O'],['X','O','O']]
        self.twoInARowBlockMax = [['X','X','O'],['X','O','X'],['O','X','X']]
        self.winMax = ['X','X','X']
        self.winMin = ['O','O','O']
        self.ownagent = 0

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')

    def max_scoreOneBoard(self, row, column):
        """
        row, column: top left corner
        First rule: If the offensive agent wins (form three-in-a-row), set the utility score to be 10000.
        Second rule: For each local board, count the number of two-in-a-row without the third spot taken by
        the opposing player (unblocked two-in-a-row). For each unblocked two-in-a-row, increment the utility
        score by 500. For each local board, count the number of places in which you have prevented the opponent
        player forming two-in-a-row (two-in-a-row of opponent player but with the third spot taken by offensive agent).
        For each prevention, increment the utility score by 100.
        Third rule: For each corner taken by the offensive agent, increment the utility score by 30.
        """
        count_R2 = 0
        board = self.board
        for i in range(3):
            list_temp1 = [board[i+row][0+column], board[i+row][1+column], board[i+row][2+column]]
            list_temp2 = [board[0+row][i+column], board[1+row][i+column], board[2+row][i+column]]
            if list_temp1 == self.winMax or list_temp2 == self.winMax:
                return 10000
            if list_temp1 in self.twoInARowMax:
                count_R2 += 500
            elif list_temp1 in self.twoInARowBlockMin:
                count_R2 += 100
            if list_temp2 in self.twoInARowMax:
                count_R2 += 500
            elif list_temp2 in self.twoInARowBlockMin:
                count_R2 += 100
        list_temp1 = [board[row][column], board[row+1][column+1], board[row+2][column+2]]
        list_temp2 = [board[row][column+2], board[row+1][column+1], board[row+2][column]]
        if list_temp1 == self.winMax or list_temp2 == self.winMax:
            return 10000
        if list_temp1 in self.twoInARowMax:
            count_R2 += 500
        elif list_temp1 in self.twoInARowBlockMin:
            count_R2 += 100
        if list_temp2 in self.twoInARowMax:
            count_R2 += 500
        elif list_temp2 in self.twoInARowBlockMin:
            count_R2 += 100
        return count_R2

    def min_scoreOneBoard(self, row, column):
        """
        row, column: top left corner
        First rule: If the defensive agent wins (forms three-in-a-row), set the utility score to be -10000.
        Second rule: For each local board, count the number of two-in-a-row without the third spot taken by
        the opponent player. For each two-in-a-row, decrement the utility score by 100. For each local board,
        count the number of prevention of opponent player forming two-in-a-row (two-in-a-row of opponent player
        but with the third spot taken by defensive agent). For each prevention, decrement the utility score by 500.
        Third rule: For each corner taken by defensive agent, decrement the utility score by 30.
        """
        count_R2 = 0
        board = self.board
        for i in range(3):
            list_temp1 = [board[i+row][0+column], board[i+row][1+column], board[i+row][2+column]]
            list_temp2 = [board[0+row][i+column], board[1+row][i+column], board[2+row][i+column]]
            if list_temp1 == self.winMin or list_temp2 == self.winMin:
                return -10000
            if list_temp1 in self.twoInARowMin:
                count_R2 -= 100
            elif list_temp1 in self.twoInARowBlockMax:
                count_R2 -= 500
            if list_temp2 in self.twoInARowMin:
                count_R2 -= 100
            elif list_temp2 in self.twoInARowBlockMax:
                count_R2 -= 500
        list_temp1 = [board[row][column], board[row+1][column+1], board[row+2][column+2]]
        list_temp2 = [board[row][column+2], board[row+1][column+1], board[row+2][column]]
        if list_temp1 == self.winMin or list_temp2 == self.winMin:
            return -10000
        if list_temp1 in self.twoInARowMin:
            count_R2 -= 100
        elif list_temp1 in self.twoInARowBlockMax:
            count_R2 -= 500
        if list_temp2 in self.twoInARowMin:
            count_R2 -= 100
        elif list_temp2 in self.twoInARowBlockMax:
            count_R2 -= 500
        if count_R2 < 0:
            rule2 = 1
        return count_R2

    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score = 0
        if isMax:
            for x in self.globalIdx:
                row, column = x
                s= self.max_scoreOneBoard(row, column)
                score += s
                if score >= 10000:
                    return 10000
        else:
            for x in self.globalIdx:
                row, column = x
                if self.ownagent == 0:
                    s= self.min_scoreOneBoard(row, column)
                else:
                    s= self.Designed_scoreOneBoard(row, column)
                score += s
                if score <= -10000:
                    return -10000
        if score == 0:
            if isMax:
                for x in self.globalIdx:
                    row, column = x
                    if self.board[row][column] == self.maxPlayer:
                        score += 30
                    if self.board[row+2][column] == self.maxPlayer:
                        score += 30
                    if self.board[row][column+2] == self.maxPlayer:
                        score += 30
                    if self.board[row+2][column+2] == self.maxPlayer:
                        score += 30
            else:
                 for x in self.globalIdx:
                     row, column = x
                     if self.board[row][column] == self.minPlayer:
                         score -= 30
                     if self.board[row+2][column] == self.minPlayer:
                         score -= 30
                     if self.board[row][column+2] == self.minPlayer:
                         score -= 30
                     if self.board[row+2][column+2] == self.minPlayer:
                         score -= 30
        return score

    def Designed_scoreOneBoard(self, row, column):
        count_R2 = 0
        board = self.board
        for i in range(3):
            list_temp1 = [board[i+row][0+column], board[i+row][1+column], board[i+row][2+column]]
            list_temp2 = [board[0+row][i+column], board[1+row][i+column], board[2+row][i+column]]
            if list_temp1 == self.winMax or list_temp2 == self.winMax:
                return 10000
            if list_temp1 == self.winMin or list_temp2 == self.winMin:
                return -10000
            if list_temp1 in self.twoInARowMax:
                count_R2 += 250
            elif list_temp1 in self.twoInARowBlockMin:
                count_R2 += 50
            elif list_temp1 in self.twoInARowMin:
                count_R2 -= 500
            elif list_temp1 in self.twoInARowBlockMax:
                count_R2 -= 100
            if list_temp2 in self.twoInARowMax:
                count_R2 += 250
            elif list_temp2 in self.twoInARowBlockMin:
                count_R2 += 50
            elif list_temp2 in self.twoInARowMin:
                count_R2 -= 500
            elif list_temp2 in self.twoInARowBlockMax:
                count_R2 -= 100
        list_temp1 = [board[row][column], board[row+1][column+1], board[row+2][column+2]]
        list_temp2 = [board[row][column+2], board[row+1][column+1], board[row+2][column]]
        if list_temp1 == self.winMax or list_temp2 == self.winMax:
            return 10000
        if list_temp1 == self.winMin or list_temp2 == self.winMin:
            return -10000
        if list_temp1 in self.twoInARowMax:
            count_R2 += 250
        elif list_temp1 in self.twoInARowBlockMin:
            count_R2 += 50
        elif list_temp1 in self.twoInARowMin:
            count_R2 -= 500
        elif list_temp1 in self.twoInARowBlockMax:
            count_R2 -= 100
        if list_temp2 in self.twoInARowMax:
            count_R2 += 250
        elif list_temp2 in self.twoInARowBlockMin:
            count_R2 += 50
        elif list_temp2 in self.twoInARowMin:
            count_R2 -= 500
        elif list_temp2 in self.twoInARowBlockMax:
            count_R2 -= 100
        return count_R2

    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        score = 0
        for x in self.globalIdx:
            row, column = x
            s= self.Designed_scoreOneBoard(row, column)
            score += s
            if score <= -10000:
                return -10000
            if score >= 10000:
                return 10000
        if score == 0:
            for x in self.globalIdx:
                row, column = x
                if self.board[row][column] == self.minPlayer:
                    score -= 30
                if self.board[row+2][column] == self.minPlayer:
                    score -= 30
                if self.board[row][column+2] == self.minPlayer:
                    score -= 30
                if self.board[row+2][column+2] == self.minPlayer:
                    score -= 30
        return score


    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == '_':
                    return True
        return False

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        score = self.evaluatePredifined(True)
        if score == 10000:
            return 1
        score = self.evaluatePredifined(False)
        if score == -10000:
            return -1
        return 0

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        self.expandedNodes += 1
        if isMax:
            bestValue = -100000
        else:
            bestValue = 100000
        if depth == self.maxDepth:
            return self.evaluatePredifined(not isMax)
        row, column = self.globalIdx[currBoardIdx]
        iffull = 1
        for i in range(3):
            for j in range(3):
                if self.board[i+row][j+column] == '_':
                    iffull = 0
                    if isMax:
                        self.board[i+row][j+column] = self.maxPlayer
                        bestValue = max(self.alphabeta(depth+1, i*3+j, alpha, beta, not isMax), bestValue)
                        self.board[i+row][j+column] = '_'
                        if bestValue >= beta:
                            return bestValue
                        alpha = max(alpha, bestValue)
                    else:
                        self.board[i+row][j+column] = self.minPlayer
                        bestValue = min(self.alphabeta(depth+1, i*3+j, alpha, beta, not isMax), bestValue)
                        self.board[i+row][j+column] = '_'
                        if bestValue <= alpha:
                            return bestValue
                        beta = min(beta, bestValue)

        if iffull == 1:
            for x in self.globalIdx:
                row, column = x
                for i in range(3):
                    for j in range(3):
                        if self.board[i][j] == '_':
                            if isMax:
                                self.board[i+row][j+column] = self.maxPlayer
                                bestValue = max(self.alphabeta(depth+1, i*3+j, alpha, beta, not isMax), bestValue)
                                self.board[i+row][j+column] = '_'
                                if bestValue >= beta:
                                    return bestValue
                                alpha = max(alpha, bestValue)
                            else:
                                self.board[i+row][j+column] = self.minPlayer
                                bestValue = min(self.alphabeta(depth+1, i*3+j, alpha, beta, not isMax), bestValue)
                                self.board[i+row][j+column] = '_'
                                if bestValue <= alpha:
                                    return bestValue
                                beta = min(beta, bestValue)
        return bestValue


    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have

        Minimax(node) =
         Utility(node) if node is terminal
         max action Minimax(Succ(node, action)) if player = MAX
         min action Minimax(Succ(node, action)) if player = MIN
        """
        #YOUR CODE HERE
        self.expandedNodes += 1
        if isMax:
            bestValue = -100000
        else:
            bestValue = 100000
        if depth == self.maxDepth:
            return self.evaluatePredifined(not isMax)
        row, column = self.globalIdx[currBoardIdx]
        iffull = 1
        for i in range(3):
            for j in range(3):
                if self.board[i+row][j+column] == '_':
                    iffull = 0
                    if isMax:
                        self.board[i+row][j+column] = self.maxPlayer
                        bestValue = max(self.minimax(depth+1, i*3+j, not isMax), bestValue)
                        self.board[i+row][j+column] = '_'
                    else:
                        self.board[i+row][j+column] = self.minPlayer
                        bestValue = min(self.minimax(depth+1, i*3+j, not isMax), bestValue)
                        self.board[i+row][j+column] = '_'
        if iffull == 1:
            for x in self.globalIdx:
                row, column = x
                for i in range(3):
                    for j in range(3):
                        if self.board[i][j] == '_':
                            if isMax:
                                self.board[i+row][j+column] = self.maxPlayer
                                bestValue = max(self.minimax(depth+1, i*3+j, not isMax), bestValue)
                                self.board[i+row][j+column] = '_'
                            else:
                                self.board[i+row][j+column] = self.minPlayer
                                bestValue = min(self.minimax(depth+1, i*3+j, not isMax), bestValue)
                                self.board[i+row][j+column] = '_'
        return bestValue

    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        expandedNodes =[]
        winner=0
        nextisMax = maxFirst
        row, column = self.globalIdx[self.startBoardIdx]
        count = 0
        while count < 81:
            alpha = -100000
            beta = 100000
            count += 1
            if nextisMax:
                cur_score = -100000
            else:
                cur_score = 100000
            cur_step = (-1, -1)
            board_index = -1
            self.expandedNodes = 0
            for i in range(3):
                for j in range(3):
                    if self.board[i+row][j+column] == '_':
                        if nextisMax:
                            self.board[i+row][j+column] = self.maxPlayer
                            if isMinimaxOffensive:
                                score = self.minimax(1, i*3+j,0)
                            else:
                                score = self.alphabeta(1, i*3+j, alpha, beta, 0)
                        else:
                            self.board[i+row][j+column] = self.minPlayer
                            if isMinimaxDefensive:
                                score = self.minimax(1, i*3+j, 1)
                            else:
                                score = self.alphabeta(1, i*3+j, alpha, beta, 1)
                        self.board[i+row][j+column] = '_'
                        if nextisMax:
                            if score > cur_score:
                                cur_score = score
                                cur_step = ((i+row), (j+column))
                                board_index = i*3+j
                                alpha = max(alpha, cur_score)
                        else:
                            if score < cur_score:
                                cur_score = score
                                cur_step = ((i+row), (j+column))
                                board_index = i*3+j
                                beta = min(beta, cur_score)
            bestMove.append(cur_step)
            bestValue.append(cur_score)
            expandedNodes.append(self.expandedNodes)
            row, column = cur_step
            if nextisMax:
                self.board[row][column] = self.maxPlayer
            else:
                self.board[row][column] = self.minPlayer
            gameBoards.append(self.board.copy())
            row, column = self.globalIdx[board_index]
            winner = self.checkWinner()
            self.printGameBoard()
            print(nextisMax)
            print(cur_score)
            nextisMax = not nextisMax
            if winner != 0:
                print(winner)
                return gameBoards, bestMove, expandedNodes, bestValue, winner
        return gameBoards, bestMove, expandedNodes, bestValue, winner



    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        self.ownagent = 1
        maxFirst = randint(0,1)
        if maxFirst == 1:
            print("predifined offensive agent First!")
        else:
            print("own agent First!")
        gameBoards, bestMove, expandedNodes, bestValue, winner = self.playGamePredifinedAgent(maxFirst,False,False)
        return gameBoards, bestMove, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        self.ownagent = 1
        while 1:
            try:
                maxFirst = int(input("Enter a number: 0 for agent first, 1 for human first "))
            except:
                print("invalid")
                continue
            if maxFirst == 0 or maxFirst == 1:
                break
            print("invalid")
        bestMove=[]
        gameBoards=[]
        winner=0
        nextisMax = maxFirst
        row, column = self.globalIdx[self.startBoardIdx]
        count = 0
        if nextisMax:
            count += 1
            while 1:
                try:
                    board_index = int(input("choose board (0~8): "))
                except:
                    print("invalid")
                    continue
                row, column = self.globalIdx[board_index]
                inp = input("Enter next step in local board (0,0 to 2,2): a,b ")
                il = inp.split(',')
                try:
                    i = int(il[0])
                    j = int(il[1])
                except:
                    print("invalid")
                    continue
                if self.board[i+row][j+column] == '_':
                    self.board[i+row][j+column] = self.maxPlayer
                    cur_step = ((i+row), (j+column))
                    board_index = i*3+j
                    bestMove.append(cur_step)
                    gameBoards.append(self.board.copy())
                    row, column = self.globalIdx[board_index]
                    self.printGameBoard()
                    break
                print("invalid")
        nextisMax = 0
        while count < 81:
            alpha = -100000
            beta = 100000
            count += 1
            if nextisMax:
                cur_score = -100000
            else:
                cur_score = 100000
            cur_step = (-1, -1)
            board_index = -1
            self.expandedNodes = 0
            if not nextisMax:
                for i in range(3):
                    for j in range(3):
                        if self.board[i+row][j+column] == '_':
                            self.board[i+row][j+column] = self.minPlayer
                            score = self.alphabeta(1, i*3+j, alpha, beta, 1)
                            self.board[i+row][j+column] = '_'
                            if score < cur_score:
                                cur_score = score
                                cur_step = ((i+row), (j+column))
                                board_index = i*3+j
                                beta = min(beta, cur_score)
                bestMove.append(cur_step)
                a,b = cur_step
                self.board[a][b] = self.minPlayer
                print("agent: " + str(cur_step))
            else:
                while 1:
                    inp = input("Enter next step in local board (0,0 to 2,2): a,b ")
                    il = inp.split(',')
                    try:
                        i = int(il[0])
                        j = int(il[1])
                    except:
                        print("invalid")
                        continue
                    if self.board[i+row][j+column] == '_':
                        self.board[i+row][j+column] = self.maxPlayer
                        cur_step = ((i+row), (j+column))
                        board_index = i*3+j
                        bestMove.append(cur_step)
                        break
                    print("invalid")
            gameBoards.append(self.board.copy())
            row, column = self.globalIdx[board_index]
            winner = self.checkWinner()
            self.printGameBoard()
            nextisMax = not nextisMax
            print("you are in board " + str(board_index))
            if winner != 0:
                print(winner)
                return gameBoards, bestMove, winner
        return gameBoards, bestMove, winner

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    #gameBoards, bestMove, bestValue, winner=uttt.playGameReflexAgent()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(0,1,1)
    print(bestMove)
    print(expandedNodes)
    #gameBoards, bestMove, winner = uttt.playGameHuman()
    #gameBoards, bestMove, winner = uttt.playGameYourAgent()
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
