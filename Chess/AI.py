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
    vulnerable = []
    opposing = []
    best_capture = 0
    best_move = 0
    corp = -1

    def __init__(self, gs, color, corp):
        self.color = color
        self.gs = gs
        self.vmov = LegalMoveGen.VariantLegalMoveGen(gs)
        self.corp = corp
        if self.color == 0:
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

    
    #absorbs another corp
    def absorb(self, corp):
        for piece in corp.pieces:
            self.pieces.append(piece)
        corp.pieces.clear()
    
    #returns the row and column of piece in the corp
    def locate(self, piece):
        if piece in self.pieces:
            icount = 0
            jcount = 0
            for i in self.gs.board:
                for j in i:
                    if j == piece:
                        return (icount, jcount)
                    jcount = jcount + 1
                icount = icount + 1

    #returns a piece at a location
    def identify(self, tup):
        return self.gs.board[tup[0]][tup[1]]

    #returns a list of all possible moves, captures, and attacker-defender pairs
    def allMoves(self):
        for piece in self.pieces:
            self.vmov.generate(self.locate(piece)[0],self.locate(piece)[1])
            for move in self.vmov.legal_moves:
                self.moves.append(move)
            for attack in self.vmov.legal_attacks:
                self.captures.append(attack)
            for location in self.captures:
                self.vulnerable.append((piece,self.identify(location)))
        print(self.captures) 

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

    #chooses best capture and sets best_capture method of evaluting may change
    def bestCapture(self):
        best = ('ZZZ', 'YYY')
        best_ranked = (5, 0)
        best_diff = -6
        for pair in self.vulnerable:
            pair_ranked = (self.evaluate(pair[0]), self.evaluate(pair[1]))
            diff = pair_ranked[1] - pair_ranked[0]
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
        if best_diff != -6:
            move = ChessEngine.Move(self.locate(best[0]), self.locate(best[1]),self.gs.board)
            self.best_capture = move
        else:
            self.best_capture = 0
    #chooses best non-capture move
    def bestMove(self):
        if self.mode=='attack':
            pass #replace this with a heuristic calculation for the furthest forward move that does not place the piece in range of an attack other than one by an archer. Prioritize moves by pawns, knights, and the queeen
        if self.mode == 'advance':
            pass #replace this with a heuristic calculation for the furthest forward move that does not place the piece in range of an attack other than one by an archer. prioritize moves by less important piecesother than archers.
        if self.mode =='retreat':
            pass #replace this with a heuristic calculation for the furthest backward move that does not place the piece in range of attacks. Prioritize moves that escape vunerability

    #changes mode
    def strategize(self): #attack means focus on captures. Advance means an equal focus on captures and advancing pieces forwards. Retreat means a focus on archer captures and moving pieces backwards
        #updates pieces
        if self.color == 0:
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

        if self.color == 0:
            if diff >2:
                self.mode =="retreat"
            if diff <= 2 and diff >= 0 or ("wR1" in self.gs.taken_pieces and "wR2" in self.gs.taken_pieces):
                self.mode == "advance"
            if diff < 0:
                self.mode == "attack"
        
        if self.color == 1:
            if diff <-2:
                self.mode =="retreat"
            if diff >= -2 and diff <= 0 or ("bR1" in self.gs.taken_pieces and "bR2" in self.gs.taken_pieces):
                self.mode == "advance"
            if diff > 0:
                self.mode == "attack"
    
    def move(self):
        percentage = random.randint(0,100)
        if self.mode == 'attack':
            if percentage <=70 and self.best_capture != 0:
                self.gs.makeMove(best_capture)
            elif self.best_move !=0:
                self.gs.makeMove(best_move) 
            elif self.color == 0:
                if self.corp == 0:
                    self.gs.treg.whiteLeftMoveFlag = True
                elif self.corp == 1:
                    self.gs.treg.whiteCenterMoveFlag = True
                else:
                    self.gs.treg.whiteRightMoveFlag = True
            elif self.color == 1:
                if self.corp == 0:
                    self.gs.treg.blackLeftMoveFlag = True
                elif self.corp == 1:
                    self.gs.treg.blackCenterMoveFlag = True
                else:
                    self.gs.treg.blackRightMoveFlag = True

            if self.gs.treg.currentTurn == 0:
                leaders = self.gs.treg.leadersW
            else:
                leaders = self.gs.treg.leadersB
            if self.gs.treg.turnMoveCount() == leaders:
                print("Move limit reached, End turn")
                self.gs.treg.turnSwap()
                print("New Turn: ", self.gs.treg.currentTurn )


        elif self.mode == 'advance':
            if percentage <= 50 and self.best_capture != 0:
                self.gs.makeMove(best_capture)
            elif self.best_move !=0:
                self.gs.makeMove(best_move)
            elif self.color == 0:
                if self.corp == 0:
                    self.gs.treg.whiteLeftMoveFlag = True
                elif self.corp == 1:
                    self.gs.treg.whiteCenterMoveFlag = True
                else:
                    self.gs.treg.whiteRightMoveFlag = True
            elif self.color == 1:
                if self.corp == 0:
                    self.gs.treg.blackLeftMoveFlag = True
                elif self.corp == 1:
                    self.gs.treg.blackCenterMoveFlag = True
                else:
                    self.gs.treg.blackRightMoveFlag = True
            if self.gs.treg.currentTurn == 0:
                leaders = self.gs.treg.leadersW
            else:
                leaders = self.gs.treg.leadersB
            if self.gs.treg.turnMoveCount() == leaders:
                print("Move limit reached, End turn")
                self.gs.treg.turnSwap()
                print("New Turn: ", self.gs.treg.currentTurn )


        elif self.mode == 'retreat':
            if percentage <=20 and self.best_capture != 0:
                self.gs.makeMove(best_capture)
            elif self.best_move !=0:
                self.gs.makeMove(best_move)
            elif self.color == 0:
                if self.corp == 0:
                    self.gs.treg.whiteLeftMoveFlag = True
                elif self.corp == 1:
                    self.gs.treg.whiteCenterMoveFlag = True
                else:
                    self.gs.treg.whiteRightMoveFlag = True
            elif self.color == 1:
                if self.corp == 0:
                    self.gs.treg.blackLeftMoveFlag = True
                elif self.corp == 1:
                    self.gs.treg.blackCenterMoveFlag = True
                else:
                    self.gs.treg.blackRightMoveFlag = True

            if self.gs.treg.currentTurn == 0:
                    leaders = self.gs.treg.leadersW
            else:
                    leaders = self.gs.treg.leadersB
            if self.gs.treg.turnMoveCount() == leaders:
                print("Move limit reached, End turn")
                self.gs.treg.turnSwap()
                print("New Turn: ", self.gs.treg.currentTurn )


    #clears 
    def clear(self):
        self.moves = []
        self.captures = []
        self.vulnerable = []
        self.opposing = []
        self.best_capture = 0
        self.best_move = 0

    def step(self,gs):
        self.strategize(gs)
        self.allMoves()
        self.bestMove()
        self.bestCapture()
        self.move()
        self.clear()


