#!/usr/bin/env python3
"""
This is the legal move generator. This generates a list of legal moves for a piece.
"""
class LegalMoveGen():
    legal_moves = [] #put tuples for legal spaces (row,col) in here
    piece_type = -1 #1:pawn, 2:rook, 3:knight, 4:bishop, 5:queen, 6:king
    piece_color = -1 #0:white, 1:black
    parent = 0

    def __init__(self, parent):
        self.parent = parent

    def generate(self, row, col):
        #get type and color
        self.piece_type = self.parent.getPiece(row,col)
        self.piece_color= self.parent.getColor(row,col)

        #black pawn move handling
        if self.piece_type == 1 and self.piece_color == 1:
            #double jump handling
            if self.pawnDoubleJump(row,col):
                if self.parent.getPiece(row+2,col)==0:
                    self.legal_moves.append((row+2,col))
            #regular move handling
            if self.parent.getPiece(row+1,col)==0:
                move = (row+1,col)
                self.legal_moves.append(move)
            #capture handling
            if self.parent.getPiece(row+1,col+1)!=0 and self.parent.getPiece(row+1,col+1)!=-1 and self.parent.getColor(row+1,col+1)!=1:
                self.legal_moves.append((row+1,col+1))
            if self.parent.getPiece(row+1,col-1) != 0 and self.parent.getPiece(row+1,col-1)!=-1 and self.parent.getColor(row+1,col-1)!=1:
                self.legal_moves.append((row+1,col-1))
            #en passant capture handling
            if self.enPassantCapture(row,col):
                if self.parent.getPiece(row+1,col+1)==0:
                    self.legal_moves.append((row+1,col+1))
                if self.parent.getPiece(row+1,col-1)==0:
                    self.legal_moves.append((row+1,col-1))

        #white pawn move handling
        if self.piece_type == 1 and self.piece_color == 0:
            #double jump handling
            if self.pawnDoubleJump(row,col):
                if self.parent.getPiece(row-2,col)==0:
                    self.legal_moves.append((row-2,col))
            #regular move handling
            if self.parent.getPiece(row-1,col)==0:
                move = (row-1,col)
                self.legal_moves.append(move)
            #capture handling
            if self.parent.getPiece(row-1,col+1)!=0 and self.parent.getPiece(row-1,col+1)!=-1 and self.parent.getColor(row-1,col+1)!=0:
                self.legal_moves.append((row-1,col+1))
            if self.parent.getPiece(row-1,col-1) != 0 and self.parent.getPiece(row-1,col-1)!=-1 and self.parent.getColor(row-1,col-1)!=0:
                self.legal_moves.append((row-1,col-1))
            #en passant capture handling
            if self.enPassantCapture(row,col):
                if self.parent.getPiece(row-1,col+1)==0:
                    self.legal_moves.append((row-1,col+1))
                if self.parent.getPiece(row-1,col-1)==0:
                    self.legal_moves.append((row-1,col-1))

        #rook move handling
        if self.piece_type == 2:
            #upward movement
            for i in range(1,8):
                if self.parent.getPiece(row+i,col) == 0:
                    self.legal_moves.append((row+i,col))
                elif self.parent.getPiece(row+i,col) != -1:
                    if self.parent.getColor(row+i,col)!=self.piece_color:
                        self.legal_moves.append((row+i,col))
                        break
                    else:
                        break
            #downward movement
            for i in range(1,8):
                if self.parent.getPiece(row-i,col) == 0:
                    self.legal_moves.append((row-i,col))
                elif self.parent.getPiece(row-i,col) != -1:
                    if self.parent.getColor(row-i,col)!=self.piece_color:
                        self.legal_moves.append((row-i,col))
                        break
                    else:
                        break
            #right movement
            for i in range(1,8):
                if self.parent.getPiece(row,col+i) == 0:
                    self.legal_moves.append((row,col+i))
                elif self.parent.getPiece(row,col+i) != -1:
                    if self.parent.getColor(row,col+i)!=self.piece_color:
                        self.legal_moves.append((row,col+i))
                        break
                    else:
                        break
            #left movement
            for i in range(1,8):
                if self.parent.getPiece(row,col-i) == 0:
                    self.legal_moves.append((row,col-i))
                elif self.parent.getPiece(row,col-i) != -1:
                    if self.parent.getColor(row,col-i)!=self.piece_color:
                        self.legal_moves.append((row,col-i))
                        break
                    else:
                        break
        #knight move handling
        if self.piece_type == 3:

            #down two, right one
            if self.parent.getPiece(row+2,col+1)!=-1:
                if self.parent.getPiece(row+2,col+1)==0 or self.parent.getColor(row+2,col+1)!=self.piece_color:
                    self.legal_moves.append((row+2,col+1))
        
            #down two, left one
            if self.parent.getPiece(row+2,col-1)!=-1:
                if self.parent.getPiece(row+2,col-1)==0 or self.parent.getColor(row+2,col-1)!=self.piece_color:
                    self.legal_moves.append((row+2,col-1))

            #up two, right one
            if self.parent.getPiece(row-2,col+1)!=-1:
                if self.parent.getPiece(row-2,col+1)==0 or self.parent.getColor(row-2,col+1)!=self.piece_color:
                    self.legal_moves.append((row-2,col+1))

            #up two, left one
            if self.parent.getPiece(row-2,col-1)!=-1:
                if self.parent.getPiece(row-2,col-1)==0 or self.parent.getColor(row-2,col-1)!=self.piece_color:
                    self.legal_moves.append((row-2,col-1))

            #right two, down one
            if self.parent.getPiece(row+1,col+2)!=-1:
                if self.parent.getPiece(row+1,col+2)==0 or self.parent.getColor(row+1,col+2)!=self.piece_color:
                    self.legal_moves.append((row+1,col+2))

            #right two, up one
            if self.parent.getPiece(row-1,col+2)!=-1:
                if self.parent.getPiece(row-1,col+2)==0 or self.parent.getColor(row-1,col+2)!=self.piece_color:
                    self.legal_moves.append((row-1,col+2))

            #left two, down one
            if self.parent.getPiece(row+1,col-2)!=-1:
                if self.parent.getPiece(row+1,col-2)==0 or self.parent.getColor(row+1,col-2)!=self.piece_color:
                    self.legal_moves.append((row+1,col-2))

            #left two, up one
            if self.parent.getPiece(row-1,col-2)!=-1:
                if self.parent.getPiece(row-1,col-2)==0 or self.parent.getColor(row-1,col-2)!=self.piece_color:
                    self.legal_moves.append((row-1,col-2))


        #bishop move handling
        if self.piece_type == 4:

            #upward right movement
            for i in range(1,8):
                if self.parent.getPiece(row+i,col+i) == 0:
                    self.legal_moves.append((row+i,col+i))
                elif self.parent.getPiece(row+i,col+i) != -1:
                    if self.parent.getColor(row+i,col+i)!=self.piece_color:
                        self.legal_moves.append((row+i,col+i))
                        break
                    else:
                        break
            #upward left movement
            for i in range(1,8):
                if self.parent.getPiece(row+i,col-i) == 0:
                    self.legal_moves.append((row+i,col-i))
                elif self.parent.getPiece(row+i,col-i) != -1:
                    if self.parent.getColor(row+i,col-i)!=self.piece_color:
                        self.legal_moves.append((row+i,col-i))
                        break
                    else:
                        break
            #downward right movement
            for i in range(1,8):
                if self.parent.getPiece(row-i,col+i) == 0:
                    self.legal_moves.append((row-i,col+i))
                elif self.parent.getPiece(row-i,col+i) != -1:
                    if self.parent.getColor(row-i,col+i)!=self.piece_color:
                        self.legal_moves.append((row-i,col+i))
                        break
                    else:
                        break
            #downward left movement
            for i in range(1,8):
                if self.parent.getPiece(row-i,col-i) == 0:
                    self.legal_moves.append((row-i,col-i))
                elif self.parent.getPiece(row-i,col-i) != -1:
                    if self.parent.getColor(row-i,col-i)!=self.piece_color:
                        self.legal_moves.append((row-i,col-i))
                        break
                    else:
                        break

        #queen Move Handling
        if self.piece_type == 5:

            #upward movement
            for i in range(1,8):
                if self.parent.getPiece(row+i,col) == 0:
                    self.legal_moves.append((row+i,col))
                elif self.parent.getPiece(row+i,col) != -1:
                    if self.parent.getColor(row+i,col)!=self.piece_color:
                        self.legal_moves.append((row+i,col))
                        break
                    else:
                        break
            #downward movement
            for i in range(1,8):
                if self.parent.getPiece(row-i,col) == 0:
                    self.legal_moves.append((row-i,col))
                elif self.parent.getPiece(row-i,col) != -1:
                    if self.parent.getColor(row-i,col)!=self.piece_color:
                        self.legal_moves.append((row-i,col))
                        break
                    else:
                        break
            #right movement
            for i in range(1,8):
                if self.parent.getPiece(row,col+i) == 0:
                    self.legal_moves.append((row,col+i))
                elif self.parent.getPiece(row,col+i) != -1:
                    if self.parent.getColor(row,col+i)!=self.piece_color:
                        self.legal_moves.append((row,col+i))
                        break
                    else:
                        break
            #left movement
            for i in range(1,8):
                if self.parent.getPiece(row,col-i) == 0:
                    self.legal_moves.append((row,col-i))
                elif self.parent.getPiece(row,col-i) != -1:
                    if self.parent.getColor(row,col-i)!=self.piece_color:
                        self.legal_moves.append((row,col-i))
                        break
                    else:
                        break
             #upward right movement
            for i in range(1,8):
                if self.parent.getPiece(row+i,col+i) == 0:
                    self.legal_moves.append((row+i,col+i))
                elif self.parent.getPiece(row+i,col+i) != -1:
                    if self.parent.getColor(row+i,col+i)!=self.piece_color:
                        self.legal_moves.append((row+i,col+i))
                        break
                    else:
                        break
            #upward left movement
            for i in range(1,8):
                if self.parent.getPiece(row+i,col-i) == 0:
                    self.legal_moves.append((row+i,col-i))
                elif self.parent.getPiece(row+i,col-i) != -1:
                    if self.parent.getColor(row+i,col-i)!=self.piece_color:
                        self.legal_moves.append((row+i,col-i))
                        break
                    else:
                        break
            #downward right movement
            for i in range(1,8):
                if self.parent.getPiece(row-i,col+i) == 0:
                    self.legal_moves.append((row-i,col+i))
                elif self.parent.getPiece(row-i,col+i) != -1:
                    if self.parent.getColor(row-i,col+i)!=self.piece_color:
                        self.legal_moves.append((row-i,col+i))
                        break
                    else:
                        break
            #downward left movement
            for i in range(1,8):
                if self.parent.getPiece(row-i,col-i) == 0:
                    self.legal_moves.append((row-i,col-i))
                elif self.parent.getPiece(row-i,col-i) != -1:
                    if self.parent.getColor(row-i,col-i)!=self.piece_color:
                        self.legal_moves.append((row-i,col-i))
                        break
                    else:
                        break

        #king move handling
        if self.piece_type == 6:

            #down
            if self.parent.getPiece(row+1,col)!=-1:
                if self.parent.getPiece(row+1,col)==0 or self.parent.getColor(row+1,col)!=self.piece_color:
                    self.legal_moves.append((row+1, col))
            
            #down right
            if self.parent.getPiece(row+1,col+1)!=-1:
                if self.parent.getPiece(row+1,col+1)==0 or self.parent.getColor(row+1,col+1)!=self.piece_color:
                    self.legal_moves.append((row+1, col+1))
            #down left
            if self.parent.getPiece(row+1,col-1)!=-1:
                if self.parent.getPiece(row+1,col-1)==0 or self.parent.getColor(row+1,col-1)!=self.piece_color:
                    self.legal_moves.append((row+1, col-1))

            #up
            if self.parent.getPiece(row-1,col)!=-1:
                if self.parent.getPiece(row-1,col)==0 or self.parent.getColor(row-1,col)!=self.piece_color:
                    self.legal_moves.append((row-1, col))

            #up right
            if self.parent.getPiece(row-1,col+1)!=-1:
                if self.parent.getPiece(row-1,col+1)==0 or self.parent.getColor(row-1,col+1)!=self.piece_color:
                    self.legal_moves.append((row-1, col+1))

            #up left
            if self.parent.getPiece(row-1,col-1)!=-1:
                if self.parent.getPiece(row-1,col-1)==0 or self.parent.getColor(row-1,col-1)!=self.piece_color:
                    self.legal_moves.append((row-1, col-1))

            #right
            if self.parent.getPiece(row,col+1)!=-1:
                if self.parent.getPiece(row,col+1)==0 or self.parent.getColor(row,col+1)!=self.piece_color:
                    self.legal_moves.append((row, col+1))

            #left
            if self.parent.getPiece(row,col-1)!=-1:
                if self.parent.getPiece(row,col-1)==0 or self.parent.getColor(row,col-1)!=self.piece_color:
                    self.legal_moves.append((row, col-1))




    def isLegal(self,row,col):
        if (row,col) in self.legal_moves:
            return True
        else:
            return False

    def clearGenerated(self):
        self.legal_moves = []
        self.piece_type = -1
        self.piece_color = -1

    # boolean function, returns true if a double jump is legal for the pawn at the given coordinates
    def pawnDoubleJump(self, row, col):
        legal = False
        if self.parent.getPiece(row, col) == 1:

            if self.hasMoved(row, col) == False:

                if self.parent.getPiece(row + 1, col) == 0 and self.parent.getPiece(row + 2, col) == 0 and self.parent.getColor(row,col) == 1:
                    legal = True

                if self.parent.getPiece(row-1,col)==0 and self.parent.getPiece(row-2,col)==0 and self.parent.getColor(row,col)==0:
                    legal = True

        return legal

    # boolean function, returns true if an en passe capture is legal for the pawn at the given coordinates
    def enPassantCapture(self, row, col):
        return False #rewrite later to reflect black and white piece differences

    # boolean function, returns true when piece that was at the given location at start of game has been moved or captured

    def hasMoved(self, row, col):
        moved = False
        for x in self.parent.moveLog:
            if (x.startRow == row and x.startCol == col) or (x.endRow == row and x.endCol == col):
                moved = True
        return moved
