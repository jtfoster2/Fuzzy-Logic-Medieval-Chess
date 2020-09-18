#!/usr/bin/env python3
"""
This class is responsible for storing all the information about current state of chess game.
It will also be responsible for valid moves at the current state.
Also keep move log.
"""

class GameState():
    def __init__(self):
        # board is 8x8 2d list, each element of list has 2 characters.
        # the first character represents the color of the piece, 'b' or 'w'
        # the second character represents te type of piece, 'K', 'Q', 'B', 'N', 'R', or 'P'
        # '--' represents an empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move to potentially display it later
        self.whiteToMove = not self.whiteToMove  # swap players
    
    #returns an integer representing the piece in a given space
    def getPiece(self, row, col):
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

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
