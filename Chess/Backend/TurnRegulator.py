#!/usr/bin/env python3

"""
Class: Senior Project
Group: 4A
Topic: Distributed Chess AI
Group Members: John Foster, Jordan Gibbons, Ian Gregoire, Mina Hanna, Leonel Hernandez, John Hurd, and Raf
ael Quarles
File Name: TurnRegulator.py
Project Area: Back End
File Description: This file is responsible for regulating turns in the Chess Variant
"""
class TurnRegulator():

    #separate pieces into corps, make flags for each's movement per turn
    whiteCorpL = ["wB1", "wN1", "wP1", "wP2", "wP3"]
    whiteLeftMoveFlag = False
    whiteCorpC = ["wK", "wQ", "wR1", "wR2", "wP4", "wP5"]
    whiteCenterMoveFlag = False
    whiteCorpR = ["wB2", "wN2", "wP6", "wP7", "wP8"]
    whiteRightMoveFlag = False

    blackCorpL = ["bB1", "bN1", "bP1", "bP2", "bP3"]
    blackLeftMoveFlag = False
    blackCorpC = ["bK", "bQ", "bR1", "bR2", "bP4", "bP5"]
    blackCenterMoveFlag = False
    blackCorpR = ["bB2", "bN2", "bP6", "bP7", "bP8"]
    blackRightMoveFlag = False
    
    wN1Flag = True
    wN2Flag = True
    bN1Flag = True
    bN2Flag = True
    currentTurn = 0
    leadersW = 3
    leadersB = 3
    attack = 0

    hudCapture = 0

    #returns amount of corps that have used their moves for the turn
    def turnMoveCount(self):
        count = 0

        if self.currentTurn == 0:
            if self.whiteLeftMoveFlag == True:
                count += 1
            if self.whiteCenterMoveFlag == True:
                count+= 1
            if self.whiteRightMoveFlag == True:
                count+= 1
        if self.currentTurn == 1:
            if self.blackLeftMoveFlag == True:
                count += 1
            if self.blackCenterMoveFlag == True:
                count += 1
            if self.blackRightMoveFlag == True:
                count += 1
        return count

    #Switches the turn
    def turnSwap(self):

        if self.currentTurn == 0:
            self.whiteLeftMoveFlag = False
            self.whiteCenterMoveFlag = False
            self.whiteRightMoveFlag = False
            self.currentTurn = 1
            self.hudCapture = 0
            print("current turn (in method): ", self.currentTurn)
        elif self.currentTurn == 1:
            self.blackLeftMoveFlag = False
            self.blackCenterMoveFlag = False
            self.blackRightMoveFlag = False
            self.currentTurn = 0
            self.hudCapture = 0
            print("current turn (in method): ", self.currentTurn)
        print("turn complete, swapping sides")
    
    def getCorps(self, piece):
        if piece in self.whiteCorpL:
            return 0
        elif piece in self.whiteCorpC:
            return 1
        elif piece in self.whiteCorpR:
            return 2
        elif piece in self.blackCorpL:
            return 3
        elif piece in self.blackCorpC:
            return 4
        elif piece in self.blackCorpR:
            return 5
        else:
            print("ERROR: Not a Piece!")
            return -1

    def Movable(self, piece):
        corp = self.getCorps(piece)
        available = []

        if self.whiteLeftMoveFlag == False:
            available.append(0)
        if self.whiteCenterMoveFlag == False:
            available.append(1)
        if self.whiteRightMoveFlag == False:
            available.append(2)
        if self.blackLeftMoveFlag == False:
            available.append(3)
        if self.blackCenterMoveFlag == False:
            available.append(4)
        if self.blackRightMoveFlag == False:
            available.append(5)
        
        if corp in available:
            return True
        elif piece == "wN1" and self.wN1Flag == False:
            self.wN1Flag = True
            if self.attack == 1:
                return True
        elif piece == "wN2" and self.wN2Flag == False:
            self.wN2Flag = True
            if self.attack == 1:
                return True
        elif piece == "bN1" and self.bN1Flag == False:
            self.bN1Flag = True
            if self.attack == 1:
                return True
        elif piece == "bN2" and self.bN2Flag == False:
            self.bN2Flag = True
            if self.attack == 1:
                return True
        else:
            return False
    

