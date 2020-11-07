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
            self.vmov.generate(self.locate(piece)[0],self.locate(piece)[1])
            for move in self.vmov.legal_moves:
                self.moves.append((self.locate(piece),move))
            for location in self.vmov.legal_attacks:
                self.captures.append((piece,self.identify(location)))
            self.vmov.clearGenerated()

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
        
        #finds furthest forward move of most powerful piece excluding leaders 60 percent of the time and including leaders 40
        if self.mode=='attack':
            if len(self.moves)>0:
                percentage = random.randint(0,100)

                if percentage <= 60:
                    #finds most powerful movable piece other than leaders
                    pwr_piece = 0
                    for move in self.moves:
                        if self.evaluate(self.identify(move[0])) >= pwr_piece and self.evaluate(self.identify(move[0])) < 4:
                            pwr_piece = self.evaluate(self.identify(move[0]))

                else:
                        #finds most powerful movable piece
                        pwr_piece = 0
                        for move in self.moves:
                            if self.evaluate(self.identify(move[0])) >= pwr_piece:
                                pwr_piece = self.evaluate(self.identify(move[0]))


                #creates list of moves using that type of piece
                possible_moves = []
                for move in self.moves:
                    if self.evaluate(self.identify(move[0])) == pwr_piece:
                        possible_moves.append(move)

                #finds furthest forward move out of the possible moves
                if len(possible_moves)>0:
                    if self.color == 1:
                        max_diff = 0
                        move = 0
                        for possible in possible_moves:
                            diff = possible[1][0] - possible[0][0]
                            if diff >= max_diff:
                                max_diff = diff
                                move = possible
                        if move != 0:
                            self.best_move = ChessEngine.Move(move[0],move[1],self.gs.board)
    
                    if self.color == 0:
                        max_diff = 0
                        move = 0
                        for possible in possible_moves:
                            diff = possible[0][0] - possible[1][0]
                            if diff >= max_diff:
                                max_diff = diff
                                move = possible
                        if move != 0:
                            self.best_move = ChessEngine.Move(move[0],move[1],self.gs.board)


        #finds furthest forward move 40 percent of the time and furthest safe move 60 percent of the time (math favors pawns and knights in the beginning)
        #40 60 rule also enable 2 AIs to actually attack each other. Otherwise, the AIs would never go into vulnerable places.
        if self.mode == 'advance':
            percentage = random.randint(0,100)

            if percentage <=60:
                possible_moves = []

                #find all moves with no adjacent opposing pieces
                if len(self.moves) >0:
                    for move in self.moves:
                        empty_count = 0 #if this ends up at 8, the space has no adjacent opposing pieces
                        end = move[1]
                        for i in range(-1,2):
                            for j in range(-1,2):
                                location = (i,j)
                                if location != (0,0):
                                    if self.color == 1:
                                        if self.identify(location)[0] != 'w':
                                            empty_count = empty_count + 1
                                    if self.color == 0:
                                        if self.identify(location)[0] != 'b':
                                            empty_count = empty_count + 1
                        if empty_count == 8:
                            possible_moves.append(move)
            
            else:
                possible_moves = self.moves
            #find move with biggest row difference
            if len(possible_moves)>0:
                if self.color == 1:
                    max_diff = 0
                    move = 0
                    for possible in possible_moves:
                        diff = possible[1][0] - possible[0][0]
                        if diff >= max_diff:
                            max_diff = diff
                            move = possible
                    if move != 0:
                        self.best_move = ChessEngine.Move(move[0],move[1],self.gs.board)

                if self.color == 0:
                    max_diff = 0
                    move = 0
                    for possible in possible_moves:
                        diff = possible[0][0] - possible[1][0]
                        if diff >= max_diff:
                            max_diff = diff
                            move = possible
                    if move != 0:
                        self.best_move = ChessEngine.Move(move[0],move[1],self.gs.board)

        #finds either the furthest backward movement or the furthest backward movement of the most vulnerable piece
        if self.mode =='retreat':

            #compute currently vunerable pieces
            for piece in self.opposing:
                self.vmov.generate(self.locate(piece)[0],self.locate(piece)[1])
            for location in self.vmov.legal_attacks:
                self.op_caps.append((piece,self.identify(location)))
            self.vmov.clearGenerated()

            #execute if pieces are vulnerable
            if len(self.op_caps) > 0:

                #find opponent's best capture
                for pair in self.op_caps:
                    pair_ranked = (self.evaluate(pair[0]), self.evaluate(pair[1]))
                    diff = pair_ranked[1] - pair_ranked[0]
                    if diff >= best_diff:
                        best = pair
                        best_ranked = pair_ranked
                        best_diff = diff

                #locate most vulnerable piece
                piece_loc = self.locate(best[1])

                #handling for black team
                if self.color == 1:
                    #compute furthest backward movement of most vulnerable piece
                    move_loc = (8,-1)
                    for move in self.moves:
                        if move[1][0] <= move_loc[0] and move[0] == piece_loc:
                            move_loc = move[1]
                    if move_loc[1] != -1:
                        move = ChessEngine.Move(piece_loc, move_loc,self.gs.board)
                        self.best_move = move
                    else:
                        self.best_move = 0
                
                #handling for white team
                if self.color == 0:
                    #compute furthest backward movement of most vulnerable piece
                    move_loc = (-1,-1)
                    for move in self.moves:
                        if move[1][0] >= move_loc[0] and move[0] == piece_loc:
                            move_loc = move[1]
                    if move_loc[1] != -1:
                        move = ChessEngine.Move(piece_loc, move_loc,self.gs.board)
                        self.best_move = move
                    else:
                        self.best_move = 0

            if len(self.op_caps) ==0:

                #find highest level piece in highest rank

                #handling for black team
                if self.color == 1:
                    #find highest rank
                    rank = 0
                    for i in range(0,8):
                        for j in range(0,8):
                            if self.gs.board[i][j][0] == 'b' and j >= rank:
                                rank = j
                    
                    #find highest piece in rank
                    value = -1
                    piece_loc = 0
                    for i in range(0,8):
                        if self.evaluate(self.gs.board[i][rank]) >= value:
                            piece_loc = (i,rank)

                #handling for white team
                if self.color == 0:
                    #find highest rank
                    rank = 8
                    for i in range(0,8):
                        for j in range(0,8):
                            if self.gs.board[i][j][0] == 'w' and j <=rank:
                                rank = j

                    #find highest piece in rank
                    value = -1
                    piece_loc = 0
                    for i in range(0,8):
                        if self.evaluate(self.gs.board[i][rank]) >= value:
                            piece_loc = (i,rank)

                
                #handling for black team
                if self.color == 1:
                    #compute furthest backward movement of most vulnerable piece
                    move_loc = (-1,8)
                    for move in self.moves:
                        if move[1][1] <= move_loc[1] and move[0] == piece_loc:
                            move_loc = move[1]
                    if move_loc[0] != -1:
                        move = ChessEngine.Move(piece_loc, move_loc,self.gs.board)
                        self.best_move = move
                    else:
                        self.best_move = 0

                #handling for white team
                if self.color == 0:
                    #compute furthest backward movement of most vulnerable piece
                    move_loc = (-1,-1)
                    for move in self.moves:
                        if move[1][1] >= move_loc[1] and move[0] == piece_loc:
                            move_loc = move[1]
                    if move_loc[0] != -1:
                        move = ChessEngine.Move(piece_loc, move_loc,self.gs.board)
                        self.best_move = move
                    else:
                        self.best_move = 0

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
            if diff >2:
                self.mode ="retreat"
            if diff <= 2 and diff >= 0 or ("wR1" in self.gs.taken_pieces and "wR2" in self.gs.taken_pieces):
                self.mode = "advance"
            if diff < 0:
                self.mode = "attack"

        #if AI is black
        if self.color == 1:
            if diff <-2:
                self.mode ="retreat"
            if diff >= -2 and diff <= 0 or ("bR1" in self.gs.taken_pieces and "bR2" in self.gs.taken_pieces):
                self.mode = "advance"
            if diff > 0:
                self.mode = "attack"

    def move(self):
        #sets percentage variable
        percentage = random.randint(0,100)

        #executes if in attack mode
        if self.mode == 'attack':
             
            #move handling
            if percentage <=70 and self.best_capture != 0:
                pass #replace with capture logic from main
                
            elif self.best_move !=0:
                pass #replace with move logic from main

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
            if percentage <= 50 and self.best_capture != 0:
                pass

            elif self.best_move !=0:
                pass

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
                pass

            elif self.best_move !=0:
                pass
        
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
        self.strategize()
        self.allMoves()
        self.bestMove()
        self.bestCapture()
        self.move()
        self.clear()


