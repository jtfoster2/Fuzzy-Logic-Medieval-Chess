#!/usr/bin/env python3
"""
Class: Senior Project
Group: 4A
Topic: Distributed Chess AI
Group Members: John Foster, Jordan Gibbons, Ian Gregoire, Mina Hanna, Leonel Hernandez, John Hurd, and Rafael Quarles
File Name: ChessMain.py
Project Area: Front End
File Description: This file draws the board and integrates the chess engine to the GUI
"""

#import pygame
import pygame as p

#import backend files
from Backend import ChessEngine #facilitates piece movement
from Backend import LegalMoveGen #generates legal moves

#set game properties
WIDTH = HEIGHT = 1600 #size of window
DIMENSION = 8 
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #frames per second
IMAGES = {}

#loads images for use on board
def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Backend/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: we can access an image by saying 'IMAGES['wP']'


#main function
def main():
    #initialize pygame and window infomration
    p.init()
    p.display.set_caption('Python Chess Game')
    screen = p.display.set_mode((WIDTH, HEIGHT))

    #set clock and fill screen
    clock = p.time.Clock() 
    screen.fill(p.Color("white"))

    #initialize backend
    gs = ChessEngine.GameState()
    mov = LegalMoveGen.LegalMoveGen(gs)
    loadImages()  # only do this once, before while loop
    running = True

    #initialize variables used to log clicks
    sqSelected = ()  # no square is selected initially, keeps track of last click of user ( tuple:(row, col))
    playerClicks = []  # keeps track of player clicks( two tuples: [(x,y), (x,y)])
    while running: 
        #handles clicks
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):  # the user clicked same square twice
                    sqSelected = ()  # deselect
                    mov.clearGenerated() #clear generated legal moves
                    playerClicks = []  # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks
                if len(playerClicks) == 2:  # after second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    if gs.getPiece(playerClicks[0][0], playerClicks[0][1])!=0: #makes sure an empty square is not set to be moved
                        mov.generate(playerClicks[0][0], playerClicks[0][1]) #generates legal moves
                        if  mov.isLegal(playerClicks[1][0],playerClicks[1][1]) == True: #disallows illegal moves
                            print(move.getChessNotation()) #prints move log entry
                            gs.makeMove(move) #makes move
                            #handles piece removal during en passant capture
                            if mov.diagonal_is_en_passant == 1 and playerClicks[1][1] == playerClicks[0][1]+1:
                                gs.board[playerClicks[0][0]][playerClicks[1][1]] = "--"
                            if mov.diagonal_is_en_passant == 0 and playerClicks[1][1] == playerClicks[0][1]-1:
                                gs.board[playerClicks[0][0]][playerClicks[1][1]] = "--"
                        else:
                            print("ERROR: Move Not Legal") #error message for illegal moves
                    mov.clearGenerated() #clear generated legal moves
                    sqSelected = ()  #reset user clicks
                    playerClicks = []#clear player clicks
        
        #draw board
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


#function for drawing board
def drawGameState(screen, gs):
    drawBoard(screen)  # draw squares on the board
    # add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board)  # draw pieces on top of those squares


#function for drawing grid on board
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("dark grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

#places pieces on board based on current game state
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
