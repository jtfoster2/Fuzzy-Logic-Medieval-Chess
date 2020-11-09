#!/user/bin/env python3
"""
Group: 4A
Topic: Distributed Chess AI
Group Members: John Foster, Jordan Gibbons, Ian Gregoire, Mina Hanna, Leonel Hernandez, John Hurd, and Rafael Quarles
File Name: AI.py
Project Area: AI
File Description: This file contains a class used to define objects representative of the AI "corps."Development of those classes will begin shortly
"""
from Backend import LegalMoveGen
from Backend import ChessEngine
import random
class Corp():
    mode = 'advance' #sets whether AI will advance, attack, or retreat
    gs = 0
    vmov = 0
    color = 0
    pieces = []
    moves = []
    captures = []
    op_caps = []
    opposing = []
    best_capture = 0
    best_move = 0
    corp = -1

    def __init__(self, gs, color, corp):
        self.color = color
        self.gs = gs
        self.vmov = LegalMoveGen.VariantLegalMoveGen(gs)
        self.corp = corp
        if self.color == 1:
            if self.corp == 0:
                self.pieces = self.gs.treg.blackCorpL
            elif self.corp == 1:
                self.pieces = self.gs.treg.blackCorpC
            else:
                self.pieces = self.gs.treg.blackCorpR

            for piece in self.gs.treg.whiteCorpL:
                self.opposing.append(piece)
            for piece in self.gs.treg.whiteCorpC:
                self.opposing.append(piece)
            for piece in self.gs.treg.whiteCorpR:
                self.opposing.append(piece)


        else:
            if self.corp == 0:
                self.pieces = self.gs.treg.whiteCorpL
            elif self.corp == 1:
                self.pieces = self.gs.treg.whiteCorpC
            else:
                self.pieces = self.gs.treg.whiteCorpR

            for piece in self.gs.treg.blackCorpL:
                self.opposing.append(piece)
            for piece in self.gs.treg.blackCorpC:
                self.opposing.append(piece)
            for piece in self.gs.treg.blackCorpR:
                self.opposing.append(piece)

        for piece in self.pieces:
            if piece not in self.gs.taken_pieces:
                self.vmov.generate(self.locate(piece)[0],self.locate(piece)[1])
                for move in self.vmov.legal_moves:
                    self.moves.append((self.locate(piece),move))
                for location in self.vmov.legal_attacks:
                    self.captures.append((piece,self.identify(location)))
            self.vmov.clearGenerated()

        self.clear()
 
    #returns the row and column of piece
    def locate(self, piece):
        icount = 0
        jcount = 0
        for i in range(0,8):
            for j in range(0,8):
                if piece == self.gs.board[i][j]:
                    return (i,j)

    #returns a piece at a location
    def identify(self, tup):
        return self.gs.board[tup[0]][tup[1]]

    #returns a list of all possible moves, captures, and attacker-defender pairs
    def allMoves(self):
        for piece in self.pieces:
            if piece not in self.gs.taken_pieces:
                self.vmov.generate(self.locate(piece)[0],self.locate(piece)[1])
                for move in self.vmov.legal_moves:
                    self.moves.append((self.locate(piece),move))
                for location in self.vmov.legal_attacks:
                    self.captures.append((piece,self.identify(location)))
            self.vmov.clearGenerated()
        for move in self.moves:
            print("Move: " + self.identify(move[0]) + " to " + str(move[1]))
        for move in self.captures:
            print("Capture: " +str(move[0]) + " takes " + str(move[1]))
    
    #returns a priority number for pieces (how important the piece is)
    def evaluate(self, piece):
        if piece[1] == "K":
            return 5
        if piece[1] == "B":
            return 4
        if piece[1] == "Q":
            return 3
        if piece[1] == "N":
            return 2
        if piece[1] == "R":
            return 1
        if piece[1] == "P":
            return 0

    #chooses best capture
    def bestCapture(self):
        best = ('ZZZ', 'YYY')
        best_ranked = (5, 0)
        best_diff = -6
        best_attack_diff = 6
        if len(self.captures)>0:
            for pair in self.captures:
                pair_ranked = (self.evaluate(pair[0]), self.evaluate(pair[1]))
                diff = pair_ranked[1] - pair_ranked[0]

                #uses weak pieces to attack equal or strong pieces in advance mode
                if self.mode != "attack":
                    if diff >= best_diff:
                        if self.mode == "retreat":
                            if pair[0] == "R": #only archers attack while retreating
                                best = pair
                                best_ranked = pair_ranked
                                best_diff = diff
                            else:
                                pass
                        else:    
                            best = pair
                            best_ranked = pair_ranked
                            best_diff = diff
                
                #uses strong pieces to attack equal or weaker pieces in attack mode
                if self.mode == "attack":
                    if diff <= best_attack_diff:
                        best = pair 
                        best_ranked = pair_ranked
                        best_attack_diff = diff
              

            move = ChessEngine.Move(self.locate(best[0]), self.locate(best[1]),self.gs.board)
            self.best_capture = move
            print("Best Capture: " + self.identify((self.best_capture.startRow,self.best_capture.startCol)) + " takes " +self.identify((self.best_capture.endRow,self.best_capture.endCol)))

        else:
            self.best_capture = 0

    #chooses best non-capture move
    def bestMove(self):
        
        #finds furthest forward move of most powerful piece excluding leaders 70 percent of the time and including bishops 30 percent of the time
        if self.mode=='attack':
            pass
        #finds furthest forward move 30 percent of the time and furthest safe move 70 percent of the time. Does not allow unsafe moves by leaders
        #70 30 rule also enables 2 AIs to actually attack each other. Otherwise, the AIs would never go into vulnerable places.
        if self.mode == 'advance':
            pass
        #finds either the furthest backward movement or the furthest backward movement of the most vulnerable piece
        if self.mode =='retreat':
            pass
            #compute currently vunerable pieces
            for piece in self.opposing:
                self.vmov.generate(self.locate(piece)[0],self.locate(piece)[1])
                for location in self.vmov.legal_attacks:
                    self.op_caps.append((piece,self.identify(location)))
                self.vmov.clearGenerated()

        #always have king escape vunerability by pieces more powerful th an archers
        #find vunerable pieces
        for piece in self.opposing:
            self.vmov.generate(self.locate(piece)[0],self.locate(piece)[1])
            for location in self.vmov.legal_attacks:
                self.op_caps.append((piece,self.identify(location)))
            self.vmov.clearGenerated()
        
        for pair in self.op_caps:
            if pair[1][1] == 'K' and self.evaluate(pair[0]) > 1:
                pass #make king run away

    #updates pieces on the board and changes mode accordingly
    def strategize(self): #attack means focus on captures. Advance means an equal focus on captures and advancing pieces forwards. Retreat means a focus on archer captures and moving pieces backwards
        #updates pieces
        if self.color == 1:
            if self.corp == 0:
                self.pieces = self.gs.treg.blackCorpL
            elif self.corp == 1:
                self.pieces = self.gs.treg.blackCorpC
            else:
                self.pieces = self.gs.treg.blackCorpR

            for piece in self.gs.treg.whiteCorpL:
                self.opposing.append(piece)
            for piece in self.gs.treg.whiteCorpC:
                self.opposing.append(piece)
            for piece in self.gs.treg.whiteCorpR:
                self.opposing.append(piece)


        else:
            if self.corp == 0:
                self.pieces = self.gs.treg.whiteCorpL
            elif self.corp == 1:
                self.pieces = self.gs.treg.whiteCorpC
            else:
                self.pieces = self.gs.treg.whiteCorpR

            for piece in self.gs.treg.blackCorpL:
                self.opposing.append(piece)
            for piece in self.gs.treg.blackCorpC:
                self.opposing.append(piece)
            for piece in self.gs.treg.blackCorpR:
                self.opposing.append(piece)

        #changes mode
        num_of_white_dead = 0
        num_of_black_dead = 0
        for piece in self.gs.taken_pieces:
            if piece[0] == "w":
                num_of_white_dead = num_of_white_dead + 1
            if piece[0] == "b":
                num_of_black_dead = num_of_black_dead + 1
        diff = num_of_white_dead - num_of_black_dead

        #if AI is white
        if self.color == 0:
            if diff >1:
                self.mode ="retreat"
            if diff <= 1 and diff >= -1 or ("wR1" in self.gs.taken_pieces and "wR2" in self.gs.taken_pieces):
                self.mode = "advance"
            if diff < -1:
                self.mode = "attack"

        #if AI is black
        if self.color == 1:
            if diff <-1:
                self.mode ="retreat"
            if diff >= -1 and diff <= 1 or ("bR1" in self.gs.taken_pieces and "bR2" in self.gs.taken_pieces):
                self.mode = "advance"
            if diff > 1:
                self.mode = "attack"

        print("Current Corps: " + str(self.corp))
        print("Pieces: " + str(self.pieces))
        print("Current Mode: " + self.mode)
    def move(self):
        #sets percentage variable
        percentage = random.randint(0,100)

        #executes if in attack mode
        if self.mode == 'attack':
             
            #move handling
            if percentage <=70 and self.best_capture != 0:
                self.gs.treg.attack = 1
                roll = random.randint(1, 6)
                if self.vmov.knight_special_attack == True and self.evaluate(self.best_capture.pieceMoved) == 2:
                    roll = roll - 1
                    self.vmov.knight_special_attack = False
                if self.gs.validate_capture(self.gs.getPiece(self.best_capture.startRow, self.best_capture.startCol), self.gs.getPiece(self.best_capture.endRow, self.best_capture.endCol), roll, self.gs.treg.Movable(self.best_capture.pieceMoved)):

                    if self.best_capture.moveCompleted == True: #if move is successful
                        print(self.best_capture.getChessNotation())  # prints move log entry
                    self.gs.makeMove(self.best_capture)  # makes move

                elif self.best_capture.pieceMoved == "wN1" and self.gs.treg.wN1Flag == False:
                    self.gs.treg.wN1Flag = True
                elif self.best_capture.pieceMoved == "wN2" and self.gs.treg.wN2Flag == False:
                    self.gs.treg.wN2Flag = True
                elif self.best_capture.pieceMoved == "bN1" and self.gs.treg.bN1Flag == False:
                    self.gs.treg.bN1Flag = True
                elif self.best_capture.pieceMoved == "bN2" and self.gs.treg.bN2Flag == False:
                    self.gs.treg.bN2Flag = True
                
            elif self.best_move !=0:
                self.gs.treg.attack = 0
                self.gs.makeMove(self.best_move)  # makes move
                if self.best_move.moveCompleted == True: #if move is successful
                    print(self.best_move.getChessNotation())  # prints move log entry
                if self.evaluate(self.best_move.pieceMoved) == 2:
                    self.vmov.knight_special_attack = True  # indicator that if knight attacks after moving, dice roll is decreased by one


            #flag setting
            if self.color == 0:
                if self.corp == 0:
                    self.gs.treg.whiteLeftMoveFlag = True
                elif self.corp == 1:
                    self.gs.treg.whiteCenterMoveFlag = True
                else:
                    self.gs.treg.whiteRightMoveFlag = True
            if self.color == 1:
                if self.corp == 0:
                    self.gs.treg.blackLeftMoveFlag = True
                elif self.corp == 1:
                    self.gs.treg.blackCenterMoveFlag = True
                else:
                    self.gs.treg.blackRightMoveFlag = True

            #turn switching
            if self.gs.treg.currentTurn == 0:
                leaders = self.gs.treg.leadersW
            else:
                leaders = self.gs.treg.leadersB
            if self.gs.treg.turnMoveCount() == leaders:
                print("Move limit reached, End turn")
                self.gs.treg.turnSwap()
                print("New Turn: ", self.gs.treg.currentTurn )

        #executes if in advance mode
        elif self.mode == 'advance':

            #move handling
            if percentage <= 80 and self.best_capture != 0:
                self.gs.treg.attack = 1
                roll = random.randint(1, 6)
                if self.vmov.knight_special_attack == True and self.evaluate(self.best_capture.pieceMoved) == 2:
                    roll = roll - 1
                    self.vmov.knight_special_attack = False
                if self.gs.validate_capture(self.gs.getPiece(self.best_capture.startRow, self.best_capture.startCol), self.gs.getPiece(self.best_capture.endRow, self.best_capture.endCol), roll, self.gs.treg.Movable(self.best_capture.pieceMoved)):
    
                    if self.best_capture.moveCompleted == True: #if move is successful
                        print(self.best_capture.getChessNotation())  # prints move log entry
                    self.gs.makeMove(self.best_capture)  # makes move
    
                elif self.best_capture.pieceMoved == "wN1" and self.gs.treg.wN1Flag == False:
                    self.gs.treg.wN1Flag = True
                elif self.best_capture.pieceMoved == "wN2" and self.gs.treg.wN2Flag == False:
                    self.gs.treg.wN2Flag = True
                elif self.best_capture.pieceMoved == "bN1" and self.gs.treg.bN1Flag == False:
                    self.gs.treg.bN1Flag = True
                elif self.best_capture.pieceMoved == "bN2" and self.gs.treg.bN2Flag == False:
                    self.gs.treg.bN2Flag = True


            elif self.best_move !=0:
                self.gs.treg.attack = 0
                self.gs.makeMove(self.best_move)  # makes move
                if self.best_move.moveCompleted == True: #if move is successful
                    print(self.best_move.getChessNotation())  # prints move log entry
                if self.evaluate(self.best_move.pieceMoved) == 2:
                    self.vmov.knight_special_attack = True  # indicator that if knight attacks after moving, dice roll is decreased by one


            #flag setting
            if self.color == 0:
                if self.corp == 0:
                    self.gs.treg.whiteLeftMoveFlag = True
                elif self.corp == 1:
                    self.gs.treg.whiteCenterMoveFlag = True
                else:
                    self.gs.treg.whiteRightMoveFlag = True
            if self.color == 1:
                if self.corp == 0:
                    self.gs.treg.blackLeftMoveFlag = True
                elif self.corp == 1:
                    self.gs.treg.blackCenterMoveFlag = True
                else:
                    self.gs.treg.blackRightMoveFlag = True
            
            #turn switching
            if self.gs.treg.currentTurn == 0:
                leaders = self.gs.treg.leadersW
            else:
                leaders = self.gs.treg.leadersB
            if self.gs.treg.turnMoveCount() == leaders:
                print("Move limit reached, End turn")
                self.gs.treg.turnSwap()
                print("New Turn: ", self.gs.treg.currentTurn )

        #executes if in retreat mode
        elif self.mode == 'retreat':

            #move handling
            if percentage <=20 and self.best_capture != 0:
                self.gs.treg.attack = 1
                roll = random.randint(1, 6)
                if self.vmov.knight_special_attack == True and self.evaluate(self.best_capture.pieceMoved) == 2:
                    roll = roll - 1
                    self.vmov.knight_special_attack = False
                if self.gs.validate_capture(self.gs.getPiece(self.best_capture.startRow, self.best_capture.startCol), self.gs.getPiece(self.best_capture.endRow, self.best_capture.endCol), roll, self.gs.treg.Movable(self.best_capture.pieceMoved)):

                    if self.best_capture.moveCompleted == True: #if move is successful
                        print(self.best_capture.getChessNotation())  # prints move log entry
                    self.gs.makeMove(self.best_capture)  # makes move

                elif self.best_capture.pieceMoved == "wN1" and self.gs.treg.wN1Flag == False:
                    self.gs.treg.wN1Flag = True
                elif self.best_capture.pieceMoved == "wN2" and self.gs.treg.wN2Flag == False:
                    self.gs.treg.wN2Flag = True
                elif self.best_capture.pieceMoved == "bN1" and self.gs.treg.bN1Flag == False:
                    self.gs.treg.bN1Flag = True
                elif self.best_capture.pieceMoved == "bN2" and self.gs.treg.bN2Flag == False:
                    self.gs.treg.bN2Flag = True



            elif self.best_move !=0:
                self.gs.treg.attack = 0
                self.gs.makeMove(self.best_move)  # makes move
                if self.best_move.moveCompleted == True: #if move is successful
                    print(self.best_move.getChessNotation())  # prints move log entry
                if self.evaluate(self.best_move.pieceMoved) == 2:
                    self.vmov.knight_special_attack = True  # indicator that if knight attacks after moving, dice roll is decreased by one

        
            #flag setting
            if self.color == 0:
                if self.corp == 0:
                    self.gs.treg.whiteLeftMoveFlag = True
                elif self.corp == 1:
                    self.gs.treg.whiteCenterMoveFlag = True
                else:
                    self.gs.treg.whiteRightMoveFlag = True
            if self.color == 1:
                if self.corp == 0:
                    self.gs.treg.blackLeftMoveFlag = True
                elif self.corp == 1:
                    self.gs.treg.blackCenterMoveFlag = True
                else:
                    self.gs.treg.blackRightMoveFlag = True

            #turn switching
            if self.gs.treg.currentTurn == 0:
                    leaders = self.gs.treg.leadersW
            else:
                    leaders = self.gs.treg.leadersB
            if self.gs.treg.turnMoveCount() == leaders:
                print("Move limit reached, End turn")
                self.gs.treg.turnSwap()
                print("New Turn: ", self.gs.treg.currentTurn )


    #clears values after a move
    def clear(self):
        self.moves = []
        self.captures = []
        self.opposing = []
        self.op_caps = []
        self.best_capture = 0
        self.best_move = 0

    #executes method sequence required to make a move
    def step(self):
        if len(self.pieces)>0:
            self.strategize()
            self.allMoves()
            self.bestMove()
            self.bestCapture()
            self.move()
            self.clear()
        else:
            self.strategize()
            self.move()


