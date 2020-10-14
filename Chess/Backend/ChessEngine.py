#!/usr/bin/env python3

"""
Class: Senior Project
Group: 4A
Topic: Distributed Chess AI
Group Members: John Foster, Jordan Gibbons, Ian Gregoire, Mina Hanna, Leonel Hernandez, John Hurd, and Raf
ael Quarles
File Name: ChessEngine.py
Project Area: Back End
File Description: This file is responsible for storing all the information about current state of chess game. It also contains code for the move log and utility functions for gathering information about a piece ata given location.
"""

#Expresses state of game
#global turn variable
currentTurn = 0 # 0=white, 1=black
class GameState():

    def __init__(self):
        # board is 8x8 2d list, each element of list has 2 characters.
        # the first character represents the color of the piece, 'b' or 'w'
        # the second character represents te type of piece, 'K', 'Q', 'B', 'N', 'R', or 'P'
        # the third character represents the number of that piece for each side, "1", "2", "3", etc...
        # '---' represents an empty space
        self.board = [
            ["bR1", "bN1", "bB1",  "bQ",  "bK", "bB2", "bN2", "bR2"],
            ["bP1", "bP2", "bP3", "bP4", "bP5", "bP6", "bP7", "bP8"],
            ["---", "---", "---", "---", "---", "---", "---", "---"],
            ["---", "---", "---", "---", "---", "---", "---", "---"],
            ["---", "---", "---", "---", "---", "---", "---", "---"],
            ["---", "---", "---", "---", "---", "---", "---", "---"],
            ["wP1", "wP2", "wP3", "wP4", "wP5", "wP6", "wP7", "wP8"],
            ["wR1", "wN1", "wB1",  "wQ",  "wK", "wB2", "wN2", "wR2"]]

        self.whiteToMove = True
        self.moveLog = []
        self.movedPieces = []
        
        #TURN REGULATION
        #separate pieces into corps, make flags for each's movement per turn
        self.whiteCorpL = ["wB1", "wN1", "wP1", "wP2", "wP3"]
        self.whiteLeftMoveFlag = False
        self.whiteCorpC = ["wK", "wQ", "wR1", "wR2", "wP4", "wP5"]
        self.whiteCenterMoveFlag = False
        self.whiteCorpR = ["wB2", "wN2", "wP6", "wP7", "wP8"]
        self.whiteRightMoveFlag = False


        self.blackCorpL = ["bB1", "bN1", "bP1", "bP2", "bP3"]
        self.blackLeftMoveFlag = False
        self.blackCorpC = ["bK", "bQ", "bR1", "bR2", "bP4", "bP5"]
        self.blackCenterMoveFlag = False
        self.blackCorpR = ["bB2", "bN2", "bP6", "bP7", "bP8"]
        self.blackRightMoveFlag = False

    #returns amount of corps that have used their moves for the turn
    def turnMoveCount(self):
        global currentTurn
        count = 0

        if currentTurn == 0:
            if self.whiteLeftMoveFlag == True:
                count += 1
            if self.whiteCenterMoveFlag == True:
                count+= 1
            if self.whiteRightMoveFlag == True:
                count+= 1
        if currentTurn == 1:
            if self.blackLeftMoveFlag == True:
                count += 1
            if self.blackCenterMoveFlag == True:
                count += 1
            if self.blackRightMoveFlag == True:
                count += 1
        return count

    #Switches the turn
    def turnSwap(self):
        global currentTurn
        self.whiteToMove = not self.whiteToMove

        if currentTurn == 0:
            currentTurn = 1
            print("current turn (in method): ", currentTurn)
            self.whiteLeftMoveFlag = False
            self.whiteCenterMoveFlag = False
            self.whiteRightMoveFlag = False
        elif currentTurn == 1:
            currentTurn = 0
            self.blackLeftMoveFlag = False
            self.blackCenterMoveFlag = False
            self.blackRightMoveFlag = False

        print("turn complete, swapping sides")
        return currentTurn


    #moves pieces and logs moves
    def makeMove(self, move):
        global currentTurn

        self.movecomplete = False

        #limit each corp to one move per turn (aside from knights)
        if (move.pieceMoved in self.whiteCorpL) and (self.whiteLeftMoveFlag == True) and (move.pieceMoved[0:2] != "wN"):
            print("Error: White left Corp has already moved this turn")
            return
        if (move.pieceMoved in self.whiteCorpC) and (self.whiteCenterMoveFlag == True) and (move.pieceMoved[0:2] != "wN"):
            print("Error: White center Corp has already moved this turn")
            return
        if (move.pieceMoved in self.whiteCorpR) and (self.whiteRightMoveFlag == True) and (move.pieceMoved[0:2] != "wN"):
            print("Error: White right Corp has already moved this turn")
            return
        if (move.pieceMoved in self.blackCorpL) and (self.blackLeftMoveFlag == True) and (move.pieceMoved[0:2] != "bN"):
            print("Error: Black left Corp has already moved this turn")
            return
        if (move.pieceMoved in self.blackCorpC) and (self.blackCenterMoveFlag == True) and (move.pieceMoved[0:2] != "bN"):
            print("Error: Black center Corp has already moved this turn")
            return
        if (move.pieceMoved in self.blackCorpR) and (self.blackRightMoveFlag == True) and (move.pieceMoved[0:2] != "bN"):
            print("Error: Black right Corp has already moved this turn")
            return

        #complete move
        elif (currentTurn == 0 and move.pieceMoved[0] == "w") or (currentTurn == 1 and move.pieceMoved[0] == "b"):
            move.moveCompleted = True
            self.board[move.startRow][move.startCol] = "---"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)  # log the move to potentially display it later
            if move.pieceMoved not in self.movedPieces:
                self.movedPieces.append(move.pieceMoved)

            #Update Corps Move Flags
            if move.pieceMoved[1:2] != "N":    #exclude knights

                if move.pieceMoved in self.whiteCorpL:
                    self.whiteLeftMoveFlag = True
                if move.pieceMoved in self.whiteCorpC:
                    self.whiteCenterMoveFlag = True
                if move.pieceMoved in self.whiteCorpR:
                    self.whiteRightMoveFlag = True
                if move.pieceMoved in self.blackCorpL:
                    self.blackLeftMoveFlag = True
                if move.pieceMoved in self.blackCorpC:
                    self.blackCenterMoveFlag = True
                if move.pieceMoved in self.blackCorpR:
                    self.blackRightMoveFlag = True

            if self.turnMoveCount() == 3:
                print("Move limit reached, End turn")
                self.turnSwap()
                print("New Turn: ", currentTurn )

        
    #returns an integer representing the piece in a given space
    def getPiece(self, row, col):
        if row > 7 or row < 0 or col > 7 or col < 0:
            return -1
        piece = self.board[row][col]
        kind = -1 #0:empty, 1:pawn, 2:rook, 3:knight, 4:bishop, 5:queen, 6:king
        if piece[1] == "-":
            kind = 0
        elif piece[1]=="P":
            kind = 1
        elif piece[1]=="R":
            kind = 2
        elif piece[1]=="N":
            kind = 3
        elif piece[1]=="B":
            kind = 4
        elif piece[1]=="Q":
            kind = 5
        else:
            kind = 6
        return kind
    
    #returns an integer representing the color of a piece
    def getColor(self, row, col):
        if row > 7 or row < 0 or col > 7 or col < 0:
            return -1
        piece = self.board[row][col]
        color = -1 #0:white, 1:black
        if self.getPiece(row,col) == 0:
            pass
        elif piece[0] == "w":
            color = 0
        else:
            color = 1
        return color
    #returns an integer representing the current active player.
    def getTurnstate(self):
        global currentTurn
        turn = -1 # 0:White, 1:Black
        if currentTurn == 0:
            turn = 0
        if currentTurn == 1:
            turn = 1
        return turn
    
    #function for die roll, returns true if defending piece is captured
    def validate_capture(self, attacker, defender, roll):
        capture = False

        if roll == 6:
            capture = True

        if roll == 5:
            if (attacker >= 4) or (attacker == 3 and defender < 5) or (attacker == 2 and defender != 2) or (
                    attacker == 1 and (defender == 4 or defender == 1)):
                capture = True

        if roll == 4:
            if (attacker >= 5 and defender != 2) or (attacker == 4 and (defender == 4 or defender == 1)) or (
                    attacker == 3 and defender <= 4 and defender != 2) or (attacker == 2 and defender >= 5) or (
                    attacker == 1 and defender == 1):
                capture = True

        if roll == 3:
            if defender == 1 and attacker >= 3:
                capture = True

        if roll == 2:
            if defender == 1 and (attacker >= 5 or attacker == 3):
                capture = True
        
        if capture == True:
            print("Capture Successful")
        else:
            print("Capture Failed")
        return capture

#used to express information about a move
class Move():
    # chess rank file notation
    # maps key to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveCompleted = False #flips true when move is successfully completed

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
