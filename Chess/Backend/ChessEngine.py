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

from Backend import TurnRegulator
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

        self.treg = TurnRegulator.TurnRegulator()
        self.moveLog = []
        self.movedPieces = []
        self.taken_pieces =[]
        self.alive_white_leaders = ["wB1", "wK", "wB2"]
        self.alive_black_leaders = ["bB1", "bK", "bB2"]
    #moves pieces and logs moves
    def makeMove(self, move):
        self.movecomplete = False

        #complete move
        if ((self.treg.currentTurn == 0 and move.pieceMoved[0] == "w") or (self.treg.currentTurn == 1 and move.pieceMoved[0] == "b")):
            if self.getPiece(move.startRow, move.startCol) !=2 or self.getPiece(move.endRow, move.endCol) == 0:

                move.moveCompleted = True 
                self.board[move.startRow][move.startCol] = "---"
                if self.board[move.endRow][move.endCol] != "---":
                    self.taken_pieces.append(self.board[move.endRow][move.endCol])
                self.board[move.endRow][move.endCol] = move.pieceMoved
                self.moveLog.append(move)  # log the move to potentially display it later
                if move.pieceMoved not in self.movedPieces:
                    self.movedPieces.append(move.pieceMoved)
            else:
                move.moveCompleted = True
                self.taken_pieces.append(self.board[move.endRow][move.endCol])
                self.board[move.endRow][move.endCol] = "---"
                self.board[move.startRow][move.startCol] = move.pieceMoved
                if move.pieceMoved not in self.movedPieces:
                    self.movedPieces.append(move.pieceMoved)
            self.regroup()
            #Update Corps Move Flags
            if move.pieceMoved in self.treg.whiteCorpL:
                self.treg.whiteLeftMoveFlag = True
            if move.pieceMoved in self.treg.whiteCorpC:
                self.treg.whiteCenterMoveFlag = True
            if move.pieceMoved in self.treg.whiteCorpR:
                self.treg.whiteRightMoveFlag = True
            if move.pieceMoved in self.treg.blackCorpL:
                self.treg.blackLeftMoveFlag = True
            if move.pieceMoved in self.treg.blackCorpC:
                self.treg.blackCenterMoveFlag = True
            if move.pieceMoved in self.treg.blackCorpR:
                self.treg.blackRightMoveFlag = True
            
            if move.pieceMoved == "wN1" and self.treg.attack == 0:
                self.treg.wN1Flag = False
            if move.pieceMoved == "wN2" and self.treg.attack == 0:
                self.treg.wN2Flag = False
            if move.pieceMoved == "bN1" and self.treg.attack == 0:
                self.treg.bN1Flag = False
            if move.pieceMoved == "bN2" and self.treg.attack == 0:
                self.treg.bN2Flag = False


            if self.treg.currentTurn == 0:
                leaders = self.treg.leadersW
            else:
                leaders = self.treg.leadersB
            if self.treg.turnMoveCount() == leaders:
                print("Move limit reached, End turn")
                self.treg.turnSwap()
                print("New Turn: ", self.treg.currentTurn )
    
    def regroup(self):
        for piece in self.taken_pieces:
            if piece in self.alive_white_leaders:
                self.alive_white_leaders.remove(piece)
            if piece in self.alive_black_leaders:
                self.alive_black_leaders.remove(piece)

        self.treg.leadersW = len(self.alive_white_leaders)
        self.treg.leadersB = len(self.alive_black_leaders)
        
        if "wB1" in self.taken_pieces and len(self.treg.whiteCorpL) != 0:
            for piece in self.treg.whiteCorpL:
                self.treg.whiteCorpC.append(piece)
            self.treg.whiteCorpL.clear()
        if "wB2" in self.taken_pieces and len(self.treg.whiteCorpR) != 0:
            for piece in self.treg.whiteCorpR:
                self.treg.whiteCorpC.append(piece)
            self.treg.whiteCorpR.clear()
        if "bB1" in self.taken_pieces and len(self.treg.blackCorpL) != 0:
            for piece in self.treg.blackCorpL:
                self.treg.blackCorpC.append(piece)
            self.treg.blackCorpL.clear()
        if "bB2" in self.taken_pieces and len(self.treg.blackCorpR) != 0:
            for piece in self.treg.blackCorpR:
                self.treg.blackCorpC.append(piece)
            self.treg.blackCorpR.clear()

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

    # function for die roll, returns true if defending piece is captured
    def validate_capture(self, attacker, defender, roll, move_valid):
        if move_valid == False:
            print("Corp Already Moved")
            self.treg.hudCapture = 3
            return False
        else:
            capture = False
            self.treg.hudDice = roll

            if roll == 6:
                capture = True

            if roll == 5:
                if (attacker >= 4) or (attacker == 3 and defender < 5) or (attacker == 2 and defender != 2) or (attacker == 1 and (defender == 4 or defender == 1)):
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
            if roll == 1:
                if attacker == 6 and defender == 1:
                    capture = True
                else:
                    capture = False

            if capture == True:
                print("Capture Successful")
                # UI hud capture
                self.treg.hudCapture = 1
            else:
                print("Capture Failed")
                # UI hud capture
                self.treg.hudCapture = 2
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
