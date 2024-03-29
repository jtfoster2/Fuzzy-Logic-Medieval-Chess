#!/usr/bin/env python3
"""
Class: Senior Project
Group: 4A
Topic: Distributed Chess AI
Group Members: John Foster, Jordan Gibbons, Ian Gregoire, Mina Hanna, Leonel Hernandez, John Hurd, and Raf
ael Quarles
File Name: LegalMoveGen.py
Project Area: Back End
File Description: This file contains the legal move generator. It generates a list of legal moves for a piece.
"""
class LegalMoveGen():
    legal_moves = [] #put tuples for legal spaces (row,col) in here
    piece_type = -1 #1:pawn, 2:rook, 3:knight, 4:bishop, 5:queen, 6:king
    piece_color = -1 #0:white, 1:black
    parent = 0#gamestate for utility functions
    diagonal_is_en_passant = -1 #indicates en passant captures so pieces can be manually cleared from the board
    #sets the gamestate that will use the generator
    def __init__(self, parent):
        self.parent = parent
    
    #Generates a list of legal moves for the current piece and places them in legal_moves
    def generate(self, row, col):

        #get type and color of selected piece
        self.piece_type = self.parent.getPiece(row,col)
        self.piece_color= self.parent.getColor(row,col)

        #black pawn move handling 
        if self.piece_type == 1 and self.piece_color == 1: #pawns only move forward, so a distinction must be made between black and white pawns
            
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
            if self.enPassantCapture(row,col) == 1:
                if self.parent.getPiece(row+1,col+1)==0:
                    self.diagonal_is_en_passant = 1
                    self.legal_moves.append((row+1,col+1))
            if self.enPassantCapture(row,col) == 0:
                if self.parent.getPiece(row+1,col-1)==0:
                    self.diagonal_is_en_passant = 0
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
            if self.enPassantCapture(row,col) == 1:
                if self.parent.getPiece(row-1,col+1)==0:
                    self.diagonal_is_en_passant = 1
                    self.legal_moves.append((row-1,col+1))
            if self.enPassantCapture(row,col) == 0:
                if self.parent.getPiece(row-1,col-1)==0:
                    self.diagonal_is_en_passant = 0
                    self.legal_moves.append((row-1,col-1))


        #rook move handling
        if self.piece_type == 2:

            #upward movement (All directions are from the point of view of white pieces. Up and down are reversed for black pieces)
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

    #checks if a move is contained in the legal move list
    def isLegal(self,row,col):
        if (row,col) in self.legal_moves:
            return True
        else:
            return False

    #clears all generated information (so the generator can be used again next move)
    def clearGenerated(self):
        self.legal_moves = []
        self.piece_type = -1
        self.piece_color = -1
        self.diagonal_is_en_passant = -1

    #boolean function, returns true if a double jump is legal for a piece at the given coordinates
    def pawnDoubleJump(self, row, col):
        legal = False
        if self.parent.getPiece(row, col) == 1: #checks that the piece is a pawn

            if self.hasMoved(row, col) == False:#checks if the pawn has moved

                #checks that the spaces to be traversed are empty for a black pawn
                if self.parent.getPiece(row + 1, col) == 0 and self.parent.getPiece(row + 2, col) == 0 and self.parent.getColor(row,col) == 1:
                    legal = True
                
                #checks that the spaces to be traversed are empty for a white pawn
                if self.parent.getPiece(row-1,col)==0 and self.parent.getPiece(row-2,col)==0 and self.parent.getColor(row,col)==0:
                    legal = True

        return legal

    #returns -1 if no en passant is legal for the piece, 0 if taking the piece to the left via en passant is legal, and 1 for the piece on the right
    def enPassantCapture(self, row, col):

        #black piece is capturing white piece
        if self.parent.getPiece(row,col) == 1 and self.parent.getColor(row,col) == 1 and row==4: #check that the piece is a black pawn on its 5th rank
            #take piece to the left (on board)
            if self.parent.getPiece(row, col-1)==1 and self.parent.getColor(row,col-1)==0: #checks that piece directly left is a white pawn
                if self.parent.moveLog[-1].endRow == row and self.parent.moveLog[-1].endCol == col-1: #checks that the white pawn moved last
                    if self.parent.moveLog[-1].startRow == row+2 and self.parent.moveLog[-1].startCol == col-1: #checks that last move was a double jump
                        return 0
            #take piece to the right (on board)
            if self.parent.getPiece(row, col+1)==1 and self.parent.getColor(row,col+1)==0: #checks that piece directly left is a white pawn
                if self.parent.moveLog[-1].endRow == row and self.parent.moveLog[-1].endCol == col+1: #checks that the white pawn moved last
                    if self.parent.moveLog[-1].startRow == row+2 and self.parent.moveLog[-1].startCol == col+1: #checks that last move was a double jump
                        return 1
            return -1

        #white piece is capturing black piece
        if self.parent.getPiece(row,col) == 1 and self.parent.getColor(row,col) == 0 and row==3: #check that the piece is a white pawn on its 5th rank
            #take piece to the left (on board)
            if self.parent.getPiece(row, col-1)==1 and self.parent.getColor(row,col-1)==1: #checks that piece directly left is a black pawn
                if self.parent.moveLog[-1].endRow == row and self.parent.moveLog[-1].endCol == col-1: #checks that the black pawn moved last
                    if self.parent.moveLog[-1].startRow == row-2 and self.parent.moveLog[-1].startCol == col-1: #checks that last move was a double jump
                        return 0
            #take piece to the right (on board)
            if self.parent.getPiece(row, col+1)==1 and self.parent.getColor(row,col+1)==1: #checks that piece directly left is a black pawn
                if self.parent.moveLog[-1].endRow == row and self.parent.moveLog[-1].endCol == col+1: #checks that the black pawn moved last
                    if self.parent.moveLog[-1].startRow == row-2 and self.parent.moveLog[-1].startCol == col+1: #checks that last move was a double jump
                        return 1
            return -1



    #boolean function, returns true if queen side castling is legal for the piece (king) at the given coordinates
    def queenSideCastle(self,row,col):
        pass #write later
    
    #boolean function, returns true if king side castling is legal for the piece (king) at the given coordinates
    def kingSideCastle(self,row,col):
        pass #write later

    # boolean function, returns true when piece that was at the given location at start of game has been moved or captured
    def hasMoved(self, row, col):
        moved = False
        for x in self.parent.moveLog:#iterates through move log
            if (x.startRow == row and x.startCol == col) or (x.endRow == row and x.endCol == col): #checks that the piece has not moved
                moved = True
        return moved


#facilitates legal move generation for the chess variant
class VariantLegalMoveGen():
    legal_moves = [] #put tuples for legal moves (row,col) in here
    legal_attacks = [] #put tuples for legal attacks (row,col) in here
    piece_type = -1 #1:pawn, 2:rook, 3:knight, 4:bishop, 5:queen, 6:king
    piece_color = -1 #0:white, 1:black
    parent = 0#gamestate for utility functions
    knight_special_attack = False #indicates whether 1 should be subtracted from the dice role due to a combined move and attack by a knight

    #sets the gamestate that will use the generator
    def __init__(self, parent):
        self.parent = parent

    #Generates a list of legal moves for the current piece and places them in legal_moves
    def generate(self, row, col):

        #get type and color of selected piece
        self.piece_type = self.parent.getPiece(row,col)
        self.piece_color= self.parent.getColor(row,col)
        
        #Royalty Move Handling
        if self.piece_type == 5 or self.piece_type == 6:
 
            #upward movement
            for i in range(1,4):
                if self.parent.getPiece(row+i,col) == 0:
                    self.legal_moves.append((row+i,col))
                elif self.parent.getPiece(row+i,col) != -1:
                    break
            
            #downward movement
            for i in range(1,4):
                if self.parent.getPiece(row-i,col) == 0:
                    self.legal_moves.append((row-i,col))
                elif self.parent.getPiece(row-i,col) != -1:
                    break
            
            #right movement
            for i in range(1,4):
                if self.parent.getPiece(row,col+i) == 0:
                    self.legal_moves.append((row,col+i))
                elif self.parent.getPiece(row,col+i) != -1:
                    break
            
            #left movement
            for i in range(1,4):
                if self.parent.getPiece(row,col-i) == 0:
                    self.legal_moves.append((row,col-i))
                elif self.parent.getPiece(row,col-i) != -1:
                    break
            
            #upward right movement
            for i in range(1,4):
                if self.parent.getPiece(row+i,col+i) == 0:
                    self.legal_moves.append((row+i,col+i))
                elif self.parent.getPiece(row+i,col+i) != -1:
                    break
            
            #upward left movement
            for i in range(1,4):
                if self.parent.getPiece(row+i,col-i) == 0:
                    self.legal_moves.append((row+i,col-i))
                elif self.parent.getPiece(row+i,col-i) != -1:
                    break
            
            #downward right movement
            for i in range(1,4):
                if self.parent.getPiece(row-i,col+i) == 0:
                    self.legal_moves.append((row-i,col+i))
                elif self.parent.getPiece(row-i,col+i) != -1:
                    break
            
            #downward left movement
            for i in range(1,4):
                if self.parent.getPiece(row-i,col-i) == 0:
                    self.legal_moves.append((row-i,col-i))
                elif self.parent.getPiece(row-i,col-i) != -1:
                    break

            #attacks
            if self.parent.getPiece(row-1,col) != 0 and self.parent.getPiece(row-1,col) != -1 and self.parent.getColor(row-1,col) != self.piece_color:
                self.legal_attacks.append((row-1,col))

            if self.parent.getPiece(row+1,col) != 0 and self.parent.getPiece(row+1,col) != -1 and self.parent.getColor(row+1,col) != self.piece_color:
                self.legal_attacks.append((row+1,col))
            
            if self.parent.getPiece(row,col-1) != 0 and self.parent.getPiece(row,col-1) != -1 and self.parent.getColor(row,col-1) != self.piece_color:
                self.legal_attacks.append((row,col-1))

            if self.parent.getPiece(row,col+1) != 0 and self.parent.getPiece(row,col+1) != -1 and self.parent.getColor(row,col+1) != self.piece_color:
                self.legal_attacks.append((row,col+1))

            if self.parent.getPiece(row-1,col+1) != 0 and self.parent.getPiece(row-1,col+1) != -1 and self.parent.getColor(row-1,col+1) != self.piece_color:
                self.legal_attacks.append((row-1,col+1))

            if self.parent.getPiece(row-1,col-1) != 0 and self.parent.getPiece(row-1,col-1) != -1 and self.parent.getColor(row-1,col-1) != self.piece_color:
                self.legal_attacks.append((row-1,col-1))

            if self.parent.getPiece(row+1,col+1) != 0 and self.parent.getPiece(row+1,col+1) != -1 and self.parent.getColor(row+1,col+1) != self.piece_color:
                self.legal_attacks.append((row+1,col+1))
            
            if self.parent.getPiece(row+1,col-1) != 0 and self.parent.getPiece(row+1,col-1) != -1 and self.parent.getColor(row+1,col-1) != self.piece_color:
                self.legal_attacks.append((row+1,col-1))

        #knight move handling
        if self.piece_type == 3:

            #upward movement
            for i in range(1,6):
                if self.parent.getPiece(row+i,col) == 0:
                    self.legal_moves.append((row+i,col))
                elif self.parent.getPiece(row+i,col) != -1:
                    break
            
            #downward movement
            for i in range(1,6):
                if self.parent.getPiece(row-i,col) == 0:
                    self.legal_moves.append((row-i,col))
                elif self.parent.getPiece(row-i,col) != -1:
                    break
            
            #right movement
            for i in range(1,6):
                if self.parent.getPiece(row,col+i) == 0:
                    self.legal_moves.append((row,col+i))
                elif self.parent.getPiece(row,col+i) != -1:
                    break
            
            #left movement
            for i in range(1,6):
                if self.parent.getPiece(row,col-i) == 0:
                    self.legal_moves.append((row,col-i))
                elif self.parent.getPiece(row,col-i) != -1:
                    break
            
            #upward right movement
            for i in range(1,6):
                if self.parent.getPiece(row+i,col+i) == 0:
                    self.legal_moves.append((row+i,col+i))
                elif self.parent.getPiece(row+i,col+i) != -1:
                    break
            
            #upward left movement
            for i in range(1,6):
                if self.parent.getPiece(row+i,col-i) == 0:
                    self.legal_moves.append((row+i,col-i))
                elif self.parent.getPiece(row+i,col-i) != -1:
                    break
            
            #downward right movement
            for i in range(1,6):
                if self.parent.getPiece(row-i,col+i) == 0:
                    self.legal_moves.append((row-i,col+i))
                elif self.parent.getPiece(row-i,col+i) != -1:
                    break
            
            #downward left movement
            for i in range(1,6):
                if self.parent.getPiece(row-i,col-i) == 0:
                    self.legal_moves.append((row-i,col-i))
                elif self.parent.getPiece(row-i,col-i) != -1:
                    break

            #attacks
            if self.parent.getPiece(row-1,col) != 0 and self.parent.getPiece(row-1,col) != -1 and self.parent.getColor(row-1,col) != self.piece_color:
                self.legal_attacks.append((row-1,col))

            if self.parent.getPiece(row+1,col) != 0 and self.parent.getPiece(row+1,col) != -1 and self.parent.getColor(row+1,col) != self.piece_color:
                self.legal_attacks.append((row+1,col))
            
            if self.parent.getPiece(row,col-1) != 0 and self.parent.getPiece(row,col-1) != -1 and self.parent.getColor(row,col-1) != self.piece_color:
                self.legal_attacks.append((row,col-1))

            if self.parent.getPiece(row,col+1) != 0 and self.parent.getPiece(row,col+1) != -1 and self.parent.getColor(row,col+1) != self.piece_color:
                self.legal_attacks.append((row,col+1))

            if self.parent.getPiece(row-1,col+1) != 0 and self.parent.getPiece(row-1,col+1) != -1 and self.parent.getColor(row-1,col+1) != self.piece_color:
                self.legal_attacks.append((row-1,col+1))

            if self.parent.getPiece(row-1,col-1) != 0 and self.parent.getPiece(row-1,col-1) != -1 and self.parent.getColor(row-1,col-1) != self.piece_color:
                self.legal_attacks.append((row-1,col-1))

            if self.parent.getPiece(row+1,col+1) != 0 and self.parent.getPiece(row+1,col+1) != -1 and self.parent.getColor(row+1,col+1) != self.piece_color:
                self.legal_attacks.append((row+1,col+1))
            
            if self.parent.getPiece(row+1,col-1) != 0 and self.parent.getPiece(row+1,col-1) != -1 and self.parent.getColor(row+1,col-1) != self.piece_color:
                self.legal_attacks.append((row+1,col-1))



        #infantry move handling
        if self.piece_type == 1 or self.piece_type == 4:

            #black infantry
            if self.piece_color == 1:
            
                #forward
                if self.parent.getPiece(row+1,col)==0:
                    self.legal_moves.append((row+1,col))
                elif self.parent.getPiece(row+1,col)!=-1and self.parent.getColor(row+1,col) != self.piece_color:
                    self.legal_attacks.append((row+1,col))
            
                #forward and right
                if self.parent.getPiece(row+1,col+1)==0:
                    self.legal_moves.append((row+1,col+1))
                elif self.parent.getPiece(row+1,col+1) != -1 and self.parent.getColor(row+1,col+1) != self.piece_color:
                    self.legal_attacks.append((row+1,col+1))

                #forward and left
                if self.parent.getPiece(row+1,col-1) == 0:
                    self.legal_moves.append((row+1,col-1))
                elif self.parent.getPiece(row+1,col-1) != -1 and self.parent.getColor(row+1,col-1) != self.piece_color:
                    self.legal_attacks.append((row+1,col-1))

            #white infantry
            if self.piece_color == 0:

                #forward
                if self.parent.getPiece(row-1,col)==0:
                    self.legal_moves.append((row-1,col))
                elif self.parent.getPiece(row-1,col)!=-1 and self.parent.getColor(row-1,col) != self.piece_color:
                    self.legal_attacks.append((row-1,col))

                #forward and right
                if self.parent.getPiece(row-1,col+1)==0:
                    self.legal_moves.append((row-1,col+1))
                elif self.parent.getPiece(row-1,col+1) != -1 and self.parent.getColor(row-1,col+1) != self.piece_color:
                    self.legal_attacks.append((row-1,col+1))

                #forward and left
                if self.parent.getPiece(row-1,col-1) == 0:
                    self.legal_moves.append((row-1,col-1))
                elif self.parent.getPiece(row-1,col-1) != -1 and self.parent.getColor(row-1,col-1) != self.piece_color:
                    self.legal_attacks.append((row-1,col-1))

        
        #archers
        if self.piece_type == 2:
            
            #moves
            if self.parent.getPiece(row-1,col)==0:
                    self.legal_moves.append((row-1,col))

            if self.parent.getPiece(row+1,col)==0:
                    self.legal_moves.append((row+1,col))
            
            if self.parent.getPiece(row,col+1)==0:
                    self.legal_moves.append((row,col+1))

            if self.parent.getPiece(row,col-1)==0:
                    self.legal_moves.append((row,col-1))
            
            if self.parent.getPiece(row-1,col+1)==0:
                    self.legal_moves.append((row-1,col+1))

            if self.parent.getPiece(row-1,col-1)==0:
                    self.legal_moves.append((row-1,col-1))
            
            if self.parent.getPiece(row+1,col+1)==0:
                    self.legal_moves.append((row+1,col+1))

            if self.parent.getPiece(row+1,col-1)==0:
                    self.legal_moves.append((row+1,col-1))

            #attacks
            loop_start_row = row - 3
            loop_start_col = col - 3
            for i in range(0,7):
                for j in range(0,7):
                    if self.parent.getPiece(loop_start_row + i, loop_start_col +j) != 0 and self.parent.getPiece(loop_start_row + i, loop_start_col +j) != -1 and self.parent.getColor(loop_start_row + i, loop_start_col +j) != self.piece_color:
                        self.legal_attacks.append((loop_start_row + i, loop_start_col + j))

    #checks if a move is contained in the legal move list
    def isLegalMove(self,row,col):
        if (row,col) in self.legal_moves:
            return True
        else:
            return False

    #checks if a move is contained in the legal move list
    def isLegalAttack(self,row,col):
        if (row,col) in self.legal_attacks:
            return True
        else:
            return False


    #clears all generated information (so the generator can be used again next move)
    def clearGenerated(self):
        self.legal_moves = []
        self.legal_attacks = []
        self.piece_type = -1
        self.piece_color = -1
        self.knight_special_attack = False


