#!/usr/bin/env python3
"""
This is the legal move generator. This generates a list of legal moves for a piece.
"""
class MoveGen():
    moves = []
    legal_moves = []
    piece_type = -1 #1:pawn, 2:rook, 3:knight, 4:bishop, 5:queen, 6:king

    def __init__(self, parent):
        self.parent = parent

    def generate(board_x, board_y):
        pass

    # boolean function, returns true if a double jump is legal for the pawn at the given coordinates
    def pawnDoubleJump(self, board_x, board_y):
        legal = False
        if self.parent.getPiece(board_x, board_y) == 1:

            if self.hasMoved(board_x, board_y) == False:

                if (self.parent.getPiece((board_x - 1), board_y) == 0) and (self.parent.getPiece((board_x - 2), board_y) == 0):
                    legal = True

        return legal

    # boolean function, returns true if an en passe capture is legal for the pawn at the given coordinates
    def enPassantCapture(self, board_x, board_y):
        legal = False
        lastmove = self.parent.moveLog[-1] #check last move made
        if (self.parent.getPiece(board_x, board_y + 1) == 1) or (self.parent.getPiece(board_x, board_y - 1) == 1) :
            if (lastmove.startRow == (board_x + 2)) and ((lastmove.startCol == (board_y + 1)) or (lastmove.startCol == (board_y - 1))):
                if (lastmove.endRow == board_x) and ((lastmove.endCol == (board_y + 1)) or (lastmove.endCol == (board_y -1))):
                    legal = True

        return legal

    # boolean function, returns true when piece that was at the given location at start of game has been moved or captured

    def hasMoved(self, board_x, board_y):
        moved = False
        for x in self.parent.moveLog:
            if (x.startRow == board_x and x.startCol == board_y) or (x.endRow == board_x and x.endCol == board_y):
                moved = True
        return moved
