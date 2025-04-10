"""
Abheek Tuladhar
Period 4 - HCP
Snake Game
Simple snake game in pygame
"""

import pygame, sys,random
from pygame import mixer

pygame.init()
mixer.init()

#board size
numRows = 20
numCols = 20

#Set up drawing surface
WIDTH = 640
HEIGHT = WIDTH
size=(WIDTH, HEIGHT)
surface = pygame.display.set_mode(size)

rowH = (HEIGHT)/numRows
colW = (WIDTH)/numCols

#set window title bar
pygame.display.set_caption("Snake")

#Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED =   (255, 0, 0)
LAWN =  (170, 215, 81)
LAWN2 = (162, 209, 73)

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

#load sound effects
appleSound = pygame.mixer.Sound("apple.wav")
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
    UP = [-1, 0]
    DOWN = [1, 0]
    LEFT = [0, -1]
    RIGHT = [0, 1]
    tail = snake[1:]

    #head
    if headDirection == UP:
        surface.blit(headUp, (snake[0][1] * colW, snake[0][0] * rowH))
    elif headDirection == DOWN:
        surface.blit(headDown, (snake[0][1] * colW, snake[0][0] * rowH))
    elif headDirection == LEFT:
        surface.blit(headLeft, (snake[0][1] * colW, snake[0][0] * rowH))
    elif headDirection == RIGHT:
        surface.blit(headRight, (snake[0][1] * colW, snake[0][0] * rowH))

    #Body: WIP
    for i in snake[1:]:
        pygame.draw.rect(surface, RED, (i[1] * colW, i[0] * rowH, colW, rowH))

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

    drawSnake(snake, headDirection)

    #draw food
    surface.blit(appleImg, (foodLoc[1] * colW, foodLoc[0] * rowH))

    if gameOver:
        showMessage("Game Over", 96, "Consolas", WIDTH/2, HEIGHT/2, BLACK, WHITE)
        showMessage("Total Length: " + str(len(snake)), 48, "Consolas", WIDTH/2, HEIGHT/2 + 70, BLACK, WHITE)

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

    if head in snake[1:]:
        return True, foodLocation

    if head[0] < 0 or head[0] >= numRows or head[1] < 0 or head[1] >= numCols:
        return True, foodLocation

    if foodLocation == head:
        snake.insert(0, head)
        foodLocation = placeFood(snake)
        appleSound.play()
        pygame.mixer.music.stop()


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

    snake = [
        [10, 10],
        [10, 9],
        [10, 8]
    ]

    foodLocation = placeFood(snake)
    currentDirection = RIGHT

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not gameOver:
                if currentDirection != DOWN and event.key == pygame.K_UP:
                    currentDirection = UP
                elif currentDirection != UP and event.key == pygame.K_DOWN:
                    currentDirection = DOWN
                elif currentDirection != RIGHT and event.key == pygame.K_LEFT:
                    currentDirection = LEFT
                elif currentDirection != LEFT and event.key == pygame.K_RIGHT:
                    currentDirection = RIGHT

        surface.fill(LAWN)
        drawScreen(gameOver, foodLocation, snake, currentDirection)
        gameOver, foodLocation = moveSnake(snake, currentDirection, foodLocation)

        pygame.display.update()
        clock.tick(10)

main()
