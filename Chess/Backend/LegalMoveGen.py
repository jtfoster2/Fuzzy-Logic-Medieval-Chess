#!/usr/bin/env python3
"""
This is the legal move generator. This generates a list of legal moves for a piece.
"""
class MoveGen():
    moves = []
    legal_moves = []
    piece_type = -1 #1:pawn, 2:rook, 3:knight, 4:bishop, 5:queen, 6:king
    piece_color = -1 #0:white, 1:black

    def __init__(self, parent):
        self.parent = parent

    def generate(self, row, col):
        piece_type = self.parent.getPiece(row,col)
        

    # boolean function, returns true if a double jump is legal for the pawn at the given coordinates
    def pawnDoubleJump(self, row, col):
        legal = False
        if self.parent.getPiece(row, col) == 1:

            if self.hasMoved(row, row) == False:

                if (self.parent.getPiece((row - 1), col) == 0) and (self.parent.getPiece((row - 2), col) == 0):
                    legal = True

        return legal

    # boolean function, returns true if an en passe capture is legal for the pawn at the given coordinates
    def enPassantCapture(self, row, col):
        legal = False
        lastmove = self.parent.moveLog[-1] #check last move made
        if (self.parent.getPiece(row, col + 1) == 1) or (self.parent.getPiece(row, col - 1) == 1) :
            if (lastmove.startRow == (row + 2)) and ((lastmove.startCol == (col + 1)) or (lastmove.startCol == (col - 1))):
                if (lastmove.endRow == row) and ((lastmove.endCol == (col + 1)) or (lastmove.endCol == (col -1))):
                    legal = True

        return legal

    # boolean function, returns true when piece that was at the given location at start of game has been moved or captured

    def hasMoved(self, row, col):
        moved = False
        for x in self.parent.moveLog:
            if (x.startRow == row and x.startCol == col) or (x.endRow == row and x.endCol == col):
                moved = True
        return moved
