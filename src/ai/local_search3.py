import random
from time import time

from src.constant import ColorConstant, ShapeConstant
from src.model import State, Board

from typing import Tuple, List


class LocalSearch3:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return best_movement

    def countGroupHorizontal(board:Board, row:int, col:int):
        #return number of pieces in a 4 group horizontally
        countPiece = 0
        for i in range (col,col+4):
            if (board[row,i].shape!=ShapeConstant.BLANK):
                countPiece+=1
        return countPiece
    
    def countGroupVertical(board:Board, row:int, col:int):
        #return number of pieces in a 4 group horizontally
        countPiece = 0
        for i in range (row,row+4):
            if (board[i,col].shape!=ShapeConstant.BLANK):
                countPiece+=1
        return countPiece

    def countGroupColorShapeHorizontal(board:Board,color:ColorConstant,shape:ShapeConstant, row:int, col:int):
        #return number of pieces in a group that fits either color or shape
        countPiece = 0
        for i in range (col,col+4):
            if (board[row,i].shape==shape or board[row,i].color==color):
                countPiece+=1
        return countPiece

    def countGroupColorShapeVertical(board:Board,color:ColorConstant,shape:ShapeConstant, row:int, col:int):
        #return number of pieces in a group that fits either color or shape
        countPiece = 0
        for i in range (row,row+4):
            if (board[i,col].shape==shape or board[i,col].color==color):
                countPiece+=1
        return countPiece

    def evaluateGroupHorizontal(state:State,n_player:int, i:int, j:int):
        #return value of group 4 horizontally on position board[i,j]
        currentBoard = state.board
        myPlayer = state.players[n_player]
        enemyPlayer = state.players[(int(not n_player))] #not n_player since n_player can only be 1 or 0 will always refer to the other
        numberOfPiece = LocalSearch3.countGroupHorizontal(currentBoard,i,j)
        countEnemyPiece = LocalSearch3.countGroupColorShapeHorizontal(currentBoard,enemyPlayer.color,enemyPlayer.shape,i,j)
        countPlayerPiece = LocalSearch3.countGroupColorShapeHorizontal(currentBoard,myPlayer.color,myPlayer.shape,i,j)

        if numberOfPiece == 4 :
            #if 4 piece of a group are full
            if countEnemyPiece == 4:
                return -999
            else:
                return +999
        elif numberOfPiece == 3 :
            #3 pieces and 1 empty
            if countEnemyPiece ==3:
                return -999
            elif countPlayerPiece==3:
                return 10
            elif countPlayerPiece==2:
                return 4
        elif numberOfPiece == 2 :
            #2 pieces and 2 empty
            if countEnemyPiece==2:
                return -4
            else:
                return 4

    def evaluateGroupVertical(state:State,n_player:int, i:int, j:int):
        currentBoard = state.board
        myPlayer = state.players[n_player]
        enemyPlayer = state.players[(int(not n_player))] #not n_player since n_player can only be 1 or 0 will always refer to the other
        numberOfPiece = LocalSearch3.countGroupVertical(currentBoard,i,j)
        countEnemyPiece = LocalSearch3.countGroupColorShapeVertical(currentBoard,enemyPlayer.color,enemyPlayer.shape,i,j)
        countPlayerPiece = LocalSearch3.countGroupColorShapeVertical(currentBoard,myPlayer.color,myPlayer.shape,i,j)

        if numberOfPiece == 4 :
            #if 4 piece of a group are full
            if countEnemyPiece == 4:
                return -999
            else:
                return +999
        elif numberOfPiece == 3 :
            #3 pieces and 1 empty
            if countEnemyPiece ==3:
                return -999
            elif countPlayerPiece==3:
                return 10
            elif countPlayerPiece==2:
                return 4
        elif numberOfPiece == 2 :
            #2 pieces and 2 empty
            if countEnemyPiece==2:
                return -4
            else:
                return 4
    
    def stateHeuristic(state:State,n_player:int):
        #function that returns a value of heuristic of a given state
        currentBoard = state.board
        myPlayer = state.players[n_player]
        enemyPlayer = state.players[(int(not n_player))] #not n_player since n_player can only be 1 or 0 will always refer to the other

        state_value = 0
        #check horizontally 1 board
        for i in range (currentBoard.row):
            for j in range (0,currentBoard.col-4):
                state_value+=LocalSearch3.evaluateGroupHorizontal(state,n_player,i,j)
        #check vertically 1 board
        for i in range (currentBoard.col):
            for j in range (0,currentBoard.row-4):
                state_value+=LocalSearch3.evaluateGroupVertical(state,n_player,i,j)
        
