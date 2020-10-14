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
import random

#import backend files
from Backend import ChessEngine #facilitates piece movement
from Backend import LegalMoveGen #generates legal moves

#set game properties
WIDTH = 1000
HEIGHT = 600 #size of window
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #frames per second
IMAGES = {}
black = (0,0,0)
grey = (200,200,200)
dark_grey = (130,130,130)

#initialize game
p.init()
p.display.set_caption('Python Chess Game')
screen = p.display.set_mode((int(WIDTH), HEIGHT))

#set clock and fill screen
clock = p.time.Clock()
screen.fill(p.Color("white"))

#loads images for use on board
def loadImages():
    imgs = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6']
    for img in imgs:
        IMAGES[img] = p.transform.scale(p.image.load("Backend/images/" + img + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: we can access an image by saying 'IMAGES['wP']'



#main function
def main():
    menuScreen()

#button function
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = p.mouse.get_pos()
    click = p.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        p.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        p.draw.rect(screen, ic,(x,y,w,h))

    smallText = p.font.SysFont('Backend/fonts/8-BIT WONDER.ttf', 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( int(x+(w/2)), int(y+(h/2)) )
    screen.blit(textSurf, textRect)

#menu function
def menuScreen():

    menu = True

    while menu:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                quit()

        screen.fill(p.Color("white"))

        image1 = p.image.load('Backend/images/bK.png')
        image2 = p.image.load('Backend/images/bQ.png')
        screen.blit(image1, (int(WIDTH / 2 - 200),50))
        screen.blit(image2, (int(WIDTH / 2 ),50))

        largeText = p.font.Font('Backend/fonts/8-BIT WONDER.ttf', 55)
        TextSurf, TextRect = text_objects("Chess AI", largeText)
        TextRect.center = (int(WIDTH / 2), int(HEIGHT / 2 + 30))
        screen.blit(TextSurf, TextRect)

        button("PLAY",int(WIDTH/2 - 150),450,100,50,dark_grey,grey,chessGame)
        button("RULES",int(WIDTH/2 + 50),450,100,50,dark_grey,grey,infoScreen)

        clock.tick(MAX_FPS)
        p.display.flip()


#displays rules in the game
def infoScreen():

    info = True

    while info:
        for e in p.event.get():
            #print(e)
            if e.type == p.QUIT:
                p.quit()
                quit()

        screen.fill(p.Color("white"))
        largeText = p.font.Font('Backend/fonts/8-BIT WONDER.ttf', 55)
        smallText = p.font.Font('Backend/fonts/8-BIT WONDER.ttf', 15)

        TextSurf, TextRect = text_objects("RULES", largeText)
        TextRect.center = (int(WIDTH / 2), 100)
        screen.blit(TextSurf, TextRect)

        TextSurf, TextRect = text_objects("Will add rules here soon", smallText)
        TextRect.center = (int(WIDTH / 2 ), 200)
        screen.blit(TextSurf, TextRect)

        TextSurf, TextRect = text_objects("--------------------------------------------", smallText)
        TextRect.center = (int(WIDTH / 2 ), 160)
        screen.blit(TextSurf, TextRect)


        button("PLAY",int(WIDTH/2 - 150),500,100,50,dark_grey,grey,chessGame)
        button("MENU",int(WIDTH/2 + 50),500,100,50,dark_grey,grey,menuScreen)

        p.display.flip()


#initialize backend (10/12/2020 edit: moved outside of chessGame function to save gamesstate when leaving mid game)
gs = ChessEngine.GameState()
mov = LegalMoveGen.LegalMoveGen(gs)
vmov = LegalMoveGen.VariantLegalMoveGen(gs)

global movesMade

#game play function
def chessGame():
    attack_array = []
    valid_array = []

    movesMade = 0

    # initialize backend (moved up)
    #gs = ChessEngine.GameState()
    #mov = LegalMoveGen.LegalMoveGen(gs)
    #vmov = LegalMoveGen.VariantLegalMoveGen(gs)

    #initialize variables used to log clicks
    sqSelected = ()  # no square is selected initially, keeps track of last click of user ( tuple:(row, col))
    playerClicks = []  # keeps track of player clicks( two tuples: [(x,y), (x,y)])

    loadImages()  # only do this once, before while loop
    running = True

    while running == True:
        # handles clicks
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                quit()
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col) or location > (600,600): #or movesMade >= 3:  # the user clicked same square twice / or is outside te board/  (or is out of turns)
                    sqSelected = ()  # deselect
                    vmov.clearGenerated()  # clear generated legal moves
                    playerClicks = []  # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks  #vmov.generate(sqSelected)
                    vmov.generate(row, col)
                    attack_array = vmov.legal_attacks
                    valid_array = vmov.legal_moves
                    print("The new legal :" + str(valid_array))
                if len(playerClicks) == 2:  # after second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    if gs.getPiece(playerClicks[0][0], playerClicks[0][1]) != 0:  # makes sure an empty square is not set to be moved
                        vmov.generate(playerClicks[0][0], playerClicks[0][1])  # generates legal moves
                        if vmov.isLegalMove(playerClicks[1][0], playerClicks[1][1]) == True:  # checks if legal move
                            gs.makeMove(move)  # makes move
                            if move.moveCompleted == True: #if move is successful
                                print(move.getChessNotation())  # prints move log entry
                            if vmov.piece_type == 3:
                                vmov.knight_special_attack = True  # indicator that if knight attacks after moving, dice roll is decreased by one

                            # tracks number of moves made after move piece
                            if move.moveCompleted == True:
                                movesMade += 1 # add 1 move
                                print("Move number:" + str(movesMade))

                        elif vmov.isLegalAttack(playerClicks[1][0], playerClicks[1][1]) == True:  # checks if legal attack
                            roll = random.randint(1, 6)
                            if vmov.knight_special_attack == True and vmov.piece_type == 3:
                                roll = roll - 1
                                vmov.knight_special_attack = False
                            if gs.validate_capture(vmov.piece_type, gs.getPiece(playerClicks[1][0], playerClicks[1][1]), roll):
                                if vmov.piece_type != 2:
                                    if move.moveCompleted == True: #if move is successful
                                        print(move.getChessNotation())  # prints move log entry
                                    gs.makeMove(move)  # makes move
                                else:
                                    gs.board[playerClicks[1][0]][playerClicks[1][1]] = "--"

                            # tracks number of moves made after attack
                            if move.moveCompleted == True:
                                movesMade += 1  # add 1 move
                                print("Move number:" + str(movesMade))
                        else:
                            print("ERROR: Move Not Legal")  # error message for illegal moves

                    sqSelected = ()  # reset user clicks
                    playerClicks = []  # clear player clicks
                    vmov.clearGenerated()  # clear generated legal moves
            elif e.type == p.KEYDOWN:
                if e.key == p.K_u: #undo move if 'u' is pressed
                    gs.undoMove()
                    movesMade -= 1


        # draw board
        drawGameState(screen, gs, valid_array, attack_array, sqSelected)

        p.display.flip()



#function for drawing board
def drawGameState(screen, gs, validMoves, attackMoves, sqSelected):
    drawBoard(screen)  # draw squares on the board
    # add in piece highlighting or move suggestions (later)
    highlightedMoves(screen, gs, validMoves, attackMoves, sqSelected)
    drawPieces(screen, gs.board)  # draw pieces on top of those squares
    drawHud(screen)

#handles UI screen located right of the board
def drawHud(screen):
    #init area and bg color
    hudSize = p.Rect(600,0,400,600)
    p.draw.rect(screen, p.Color("gainsboro"),hudSize)

    medText = p.font.Font('Backend/fonts/8-BIT WONDER.ttf', 20)
    smallText = p.font.Font('Backend/fonts/8-BIT WONDER.ttf', 12)

    #handle display of captured pieces
    screen.blit(p.transform.scale(IMAGES['bK'], (50, 50)), (600, 10))
    screen.blit(p.transform.scale(IMAGES['bQ'], (50, 50)), (600, 60))
    screen.blit(p.transform.scale(IMAGES['bR'], (50, 50)), (600, 110))
    screen.blit(p.transform.scale(IMAGES['bR'], (50, 50)), (600, 160))
    screen.blit(p.transform.scale(IMAGES['bN'], (50, 50)), (600, 210))
    screen.blit(p.transform.scale(IMAGES['bN'], (50, 50)), (600, 260))
    screen.blit(p.transform.scale(IMAGES['bB'], (50, 50)), (600, 310))
    screen.blit(p.transform.scale(IMAGES['bB'], (50, 50)), (600, 360))

    screen.blit(p.transform.scale(IMAGES['bP'], (50, 50)), (640, 10))
    screen.blit(p.transform.scale(IMAGES['bP'], (50, 50)), (640, 60))
    screen.blit(p.transform.scale(IMAGES['bP'], (50, 50)), (640, 110))
    screen.blit(p.transform.scale(IMAGES['bP'], (50, 50)), (640, 160))
    screen.blit(p.transform.scale(IMAGES['bP'], (50, 50)), (640, 210))
    screen.blit(p.transform.scale(IMAGES['bP'], (50, 50)), (640, 260))
    screen.blit(p.transform.scale(IMAGES['bP'], (50, 50)), (640, 310))
    screen.blit(p.transform.scale(IMAGES['bP'], (50, 50)), (640, 360))

    screen.blit(p.transform.scale(IMAGES['wK'], (50, 50)), (680, 10))
    screen.blit(p.transform.scale(IMAGES['wQ'], (50, 50)), (680, 60))
    screen.blit(p.transform.scale(IMAGES['wR'], (50, 50)), (680, 110))
    screen.blit(p.transform.scale(IMAGES['wR'], (50, 50)), (680, 160))
    screen.blit(p.transform.scale(IMAGES['wN'], (50, 50)), (680, 210))
    screen.blit(p.transform.scale(IMAGES['wN'], (50, 50)), (680, 260))
    screen.blit(p.transform.scale(IMAGES['wB'], (50, 50)), (680, 310))
    screen.blit(p.transform.scale(IMAGES['wB'], (50, 50)), (680, 360))

    screen.blit(p.transform.scale(IMAGES['wP'], (50, 50)), (720, 10))
    screen.blit(p.transform.scale(IMAGES['wP'], (50, 50)), (720, 60))
    screen.blit(p.transform.scale(IMAGES['wP'], (50, 50)), (720, 110))
    screen.blit(p.transform.scale(IMAGES['wP'], (50, 50)), (720, 160))
    screen.blit(p.transform.scale(IMAGES['wP'], (50, 50)), (720, 210))
    screen.blit(p.transform.scale(IMAGES['wP'], (50, 50)), (720, 260))
    screen.blit(p.transform.scale(IMAGES['wP'], (50, 50)), (720, 310))
    screen.blit(p.transform.scale(IMAGES['wP'], (50, 50)), (720, 360))

    # handle display of dice roll
    screen.blit(p.transform.scale(IMAGES['d1'], (75, 75)), (785, 15))


    #buttons
    button("MENU", 890, 10, 100, 50, dark_grey, grey, menuScreen)
    button("RULES", 890, 70, 100, 50, dark_grey, grey, infoScreen)
    button("QUIT", 890, 130, 100, 50, dark_grey, grey, quit)
    button("END TURN", 775, 360, 200, 50, p.Color("lightgreen"), p.Color("brown1"), main)

    #capture failed/ succeeded
    p.draw.rect(screen, p.Color("black"), (610, 440, 380, 75), 4)
    TextSurf, TextRect = text_objects("Capture Failed", medText)
    TextRect.center = (800, 480)
    screen.blit(TextSurf, TextRect)
    #TextSurf, TextRect = text_objects("Capture Succeeded", medText)
    #TextRect.center = (800, 480)
    #screen.blit(TextSurf, TextRect)

    #turn indicator
    p.draw.rect(screen, p.Color("black"), (610, 515, 380, 75), 4)
    TextSurf, TextRect = text_objects("Turns Left", medText)
    TextRect.center = (800, 540)
    screen.blit(TextSurf, TextRect)
    TextSurf, TextRect = text_objects("Left Corp", smallText)
    TextRect.center = (680, 570)
    screen.blit(TextSurf, TextRect)
    TextSurf, TextRect = text_objects("King Corp", smallText)
    TextRect.center = (805, 570)
    screen.blit(TextSurf, TextRect)
    TextSurf, TextRect = text_objects("Right Corp", smallText)
    TextRect.center = (930, 570)
    screen.blit(TextSurf, TextRect)

    #cross out turn indicator
    #p.draw.rect(screen, p.Color("red"), (625, 570, 110, 2))
    p.draw.rect(screen, p.Color("red"), (750, 570, 110, 2))
    #p.draw.rect(screen, p.Color("red"), (875, 570, 110, 2))

    #visual dice being rolled ?



#function for drawing grid on board
def drawBoard(screen):
    screen.fill(p.Color("white"))
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
            if piece != "---":  # not an empty square
                screen.blit(IMAGES[piece[0:2]], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlightedMoves(screen, gs, validMoves, attackMoves, sqSelected):
    #validMoves = [(1,6),(2,6)]
    # print("Valid moves : " + str(validMoves))
    # print("sqSelected : " + str(sqSelected))

    if sqSelected != ():
        r, c = sqSelected
        s = p.Surface((SQ_SIZE, SQ_SIZE))   # Created a square with the dimensions provided
        s.set_alpha(30)     # The method is responsible for adding transparency effect
        s.fill(p.Color('green'))    # Responsible for highlighting the current square as transparent green
        screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
        highlight(screen, gs, validMoves, "yellow")
        highlight(screen, gs, attackMoves, "red")


def highlight(screen, gs, moves, color):
    if moves !=[]:
        a = p.Surface((SQ_SIZE, SQ_SIZE))
        a.set_alpha(80)
        a.fill(p.Color(color))
        for item in moves:  # Loops through the array to highlight the valid moves provided as an array
            row, column = item
            screen.blit(a, (column * SQ_SIZE, row * SQ_SIZE))


def text_objects(text, font):
    textSurface = font.render(text, True, p.Color("black"))
    return textSurface, textSurface.get_rect()


if __name__ == "__main__":
    main()