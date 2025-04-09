"""
Abheek Tuladhar
Period 4 - HCP
Snake Game
Simple snake game in pygame
"""

import pygame, sys,random

pygame.init()

#board size
numRows = 20
numCols = 20

#Set up drawing surface
WIDTH = 650
HEIGHT = 650
size=(WIDTH, HEIGHT)
surface = pygame.display.set_mode(size)

rowH = (HEIGHT)/numRows
colW = (WIDTH)/numCols

#set window title bar
pygame.display.set_caption("Snake")

#Color constants
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED =   (255,  0,  0)
GREEN = (  0,255,  0)
BLUE =  (  0,  0,255)
LTGRAY = (200,200,200)
LAWN = (170, 215, 81)
LAWN2 =(162, 209, 73)

#load & size images
appleImg = pygame.transform.scale(pygame.image.load("snakeGraphics/apple.png").convert_alpha(),(colW, rowH))

#head- 4 directions
headUp = pygame.transform.scale(pygame.image.load("snakeGraphics/head_up.png").convert_alpha(),(colW, rowH))
headDown = pygame.transform.scale(pygame.image.load("snakeGraphics/head_down.png").convert_alpha(),(colW, rowH))
headLeft = pygame.transform.scale(pygame.image.load("snakeGraphics/head_left.png").convert_alpha(),(colW, rowH))
headRight = pygame.transform.scale(pygame.image.load("snakeGraphics/head_right.png").convert_alpha(),(colW, rowH))

#tail- 4 directions
tailUp = pygame.transform.scale(pygame.image.load("snakeGraphics/tail_up.png").convert_alpha(),(colW, rowH))
tailDown = pygame.transform.scale(pygame.image.load("snakeGraphics/tail_down.png").convert_alpha(),(colW, rowH))
tailLeft = pygame.transform.scale(pygame.image.load("snakeGraphics/tail_left.png").convert_alpha(),(colW, rowH))
tailRight = pygame.transform.scale(pygame.image.load("snakeGraphics/tail_right.png").convert_alpha(),(colW, rowH))

#body- 6 options

bodyBL = pygame.transform.scale(pygame.image.load("snakeGraphics/body_BL.png").convert_alpha(),(colW, rowH))
bodyBR = pygame.transform.scale(pygame.image.load("snakeGraphics/body_BR.png").convert_alpha(),(colW, rowH))
bodyTL = pygame.transform.scale(pygame.image.load("snakeGraphics/body_TL.png").convert_alpha(),(colW, rowH))
bodyTR = pygame.transform.scale(pygame.image.load("snakeGraphics/body_TR.png").convert_alpha(),(colW, rowH))
bodyHorz = pygame.transform.scale(pygame.image.load("snakeGraphics/body_horizontal.png").convert_alpha(),(colW, rowH))
bodyVert = pygame.transform.scale(pygame.image.load("snakeGraphics/body_vertical.png").convert_alpha(),(colW, rowH))

clock = pygame.time.Clock()

def subtractCells(loc1, loc2):
    '''
    returns the difference between two [row,col] locations as a list
    '''
    return [loc1[0] - loc2[0], loc1[1] - loc2[1]]



def addCells(loc1, loc2):
    '''
    returns the sum of two [row,col] locations as a list
    '''
    return [loc1[0] + loc2[0], loc1[1] + loc2[1]]


def showMessage(words, size, font, x, y, color, bg = None):
    '''
    blits text on the view centered at [x,y]
    returns Rect of bounding box
    '''
    text_font = pygame.font.SysFont(font, size, True, False)
    text = text_font.render(words, True, color, bg)
    textBounds = text.get_rect()
    textBounds.center = (x, y)
    surface.blit(text, textBounds)
    return textBounds


def drawSnake(snake, headDirection):
    '''
    blits all parts of the snake in the view
    '''
    for i in snake:
        #surface.blit(pygame.Rect((i[1] * colW, i[0] * rowH, colW, rowH)), (i[1] * colW, i[0] * rowH))
        pygame.draw.rect(surface, RED, (i[1] * colW, i[0] * rowH, colW, rowH))
    #head
    pygame.draw.rect(surface, BLACK, (snake[0][1] * colW, snake[0][0] * rowH, colW, rowH))

    #tail if snake length>1


    #body if snake length>2   -->check class notes for algorithm

    return 42


def drawScreen(gameOver, foodLoc, snake, headDirection):
    '''
    draws the view
    '''
    x = 0
    y = 0

    #draw checkerboard
    for row in range(numRows):
        for col in range(numCols):
            if (row + col) % 2 == 0:
                pygame.draw.rect(surface, LAWN, (x, y, colW, rowH))
            else:
                pygame.draw.rect(surface, LAWN2, (x, y, colW, rowH))
            x += colW
        x = 0
        y += rowH

    #draw food
    surface.blit(appleImg, (foodLoc[1] * colW, foodLoc[0] * rowH))

    drawSnake(snake, headDirection)


def placeFood(snake):
    '''
    returns a valid [row,col] location for the food
    post: location is not part of the snake
    '''
    while True:
        foodLocation = [random.randint(0, numRows - 1), random.randint(0, numCols - 1)]
        if foodLocation not in snake:
            break
    return foodLocation


def moveSnake(snake,direction,foodLocation):
    '''
    Moves the snake once in the direction specified
    returns two values
    - whether/not the game is over
    - foodLocation (which may/may not change)
    '''
    head = snake[0]
    newhead = addCells(head, direction)
    snake.insert(0, newhead)
    snake.pop()


    return False, foodLocation  #game is not over, food may have moved


#----------Main Program Loop ----------
def main():
    gameOver = False
    UP = [-1, 0]
    DOWN = [1, 0]
    LEFT = [0, -1]
    RIGHT = [0, 1]

    #use for testing
    snake =[
        [5,10],
        [5,9],
        [5,8],
        [4,8],
        [3,8],
        [3,9],
        [2,9]
    ]

    foodLocation = placeFood(snake)
    currentDirection = RIGHT

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    currentDirection = UP
                elif event.key == pygame.K_DOWN:
                    currentDirection = DOWN
                elif event.key == pygame.K_LEFT:
                    currentDirection = LEFT
                elif event.key == pygame.K_RIGHT:
                    currentDirection = RIGHT


        surface.fill(LAWN)
        drawScreen(gameOver, foodLocation, snake, currentDirection)
        gameOver, foodLocation = moveSnake(snake, currentDirection, foodLocation)

        pygame.display.update()
        clock.tick(10)
main()
