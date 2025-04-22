"""
Abheek Tuladhar
Period 4 - HCP
Snake Game
Simple snake game in pygame
"""

import pygame, sys, random, turtle
from pygame import mixer

def askColumnRows():
    sc = turtle.Screen()
    sc.setup(1, 1)

    while True:
        try:
            rows = int(turtle.textinput("Rows", "How many rows do you want?"))
            columns = int(turtle.textinput("Columns", "How many columns do you want?"))
            break
        except ValueError:
            continue

    return rows, columns

#board size
numRows, numCols = askColumnRows()

pygame.init()
mixer.init()

# Set up drawing surface
WIDTH = 700
HEIGHT = WIDTH
size=(WIDTH, HEIGHT)
surface = pygame.display.set_mode(size)

rowH = HEIGHT/numRows
colW = WIDTH/numCols

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
appleSound = pygame.mixer.Sound("snakeMusic/apple.wav")
gameoverSound = pygame.mixer.Sound("snakeMusic/gameover.mp3")

appleSound.set_volume(0.1)

leftSound = pygame.mixer.Sound("snakeMusic/moveSounds/left.wav")
rightSound = pygame.mixer.Sound("snakeMusic/moveSounds/right.wav")
upSound = pygame.mixer.Sound("snakeMusic/moveSounds/up.wav")
downSound = pygame.mixer.Sound("snakeMusic/moveSounds/down.wav")

clock = pygame.time.Clock()

def subtractCells(loc1, loc2):
    """
    returns the difference between two [row,col] locations as a list

    Parameters:
    -----------
    loc1: list
        The first location
    loc2: list
        The second location

    Returns:
    --------
    The difference between the two locations
    """

    return [loc1[0] - loc2[0], loc1[1] - loc2[1]]


def addCells(loc1, loc2):
    """
    returns the sum of two [row,col] locations as a list

    Parameters:
    -----------
    loc1: list
        The first location
    loc2: list
        The second location

    Returns:
    --------
    The sum of the two locations
    """

    return [loc1[0] + loc2[0], loc1[1] + loc2[1]]


def show_message(words, font_name, size, x, y, color, bg=None, hover=False):
    """
    Credit to programming mentor, Valerie Klosky

    Parameters:
    -----------
    words : str
        The text to be displayed.
    font_name : str
        The name of the font to use.
    size : int
        The size of the font.
    x : int
        The x-coordinate of the center of the text.
    y : int
        The y-coordinate of the center of the text.
    color : tuple
        The RGB color of the text.
    bg : tuple, optional
        The RGB background color of the text. Defaults to None.
    hover : bool, optional
        Whether to change the text color on hover. Defaults to False.

    Returns:
    --------
    text_bounds : Rect
        The bounding box of the text.
    """

    font = pygame.font.SysFont(font_name, size, True, False)
    text_image = font.render(words, True, color, bg)
    text_bounds = text_image.get_rect()  #bounding box of the text image
    text_bounds.center = (x, y)  #center text within the bounding box

    #find position of mouse pointer
    mouse_pos = pygame.mouse.get_pos()  #returns (x,y) of mouse location

    if text_bounds.collidepoint(mouse_pos) and bg != None and hover:
        #Regenerate the image on hover
        text_image = font.render(words, True, bg, color)  #swap bg and text color

    surface.blit(text_image, text_bounds)    #render on screen
    return text_bounds                      #bounding box returned for collision detection


def drawSnake(snake, headDirection):
    """
    blits all parts of the snake in the view

    Parameters:
    -----------
    snake: list
        The snake
    headDirection: list
        The direction of the head

    Returns:
    --------
    None
    """

    UP = [-1, 0]
    DOWN = [1, 0]
    LEFT = [0, -1]
    RIGHT = [0, 1]

    #head
    if headDirection == UP:
        surface.blit(headUp, (snake[0][1] * colW, snake[0][0] * rowH))
    elif headDirection == DOWN:
        surface.blit(headDown, (snake[0][1] * colW, snake[0][0] * rowH))
    elif headDirection == LEFT:
        surface.blit(headLeft, (snake[0][1] * colW, snake[0][0] * rowH))
    elif headDirection == RIGHT:
        surface.blit(headRight, (snake[0][1] * colW, snake[0][0] * rowH))

    #body
    for i in range(1, len(snake)-1):
        prev = snake[i-1]
        curr = snake[i]
        next = snake[i+1]
        prev_to_curr = subtractCells(curr, prev)
        curr_to_next = subtractCells(next, curr)

        if prev_to_curr == UP and curr_to_next == LEFT:
            surface.blit(bodyTR, (curr[1] * colW, curr[0] * rowH))
        elif prev_to_curr == UP and curr_to_next == RIGHT:
            surface.blit(bodyTL, (curr[1] * colW, curr[0] * rowH))
        elif prev_to_curr == UP and curr_to_next == UP:
            surface.blit(bodyVert, (curr[1] * colW, curr[0] * rowH))

        elif prev_to_curr == DOWN and curr_to_next == LEFT:
            surface.blit(bodyBR, (curr[1] * colW, curr[0] * rowH))
        elif prev_to_curr == DOWN and curr_to_next == RIGHT:
            surface.blit(bodyBL, (curr[1] * colW, curr[0] * rowH))
        elif prev_to_curr == DOWN and curr_to_next == DOWN:
            surface.blit(bodyVert, (curr[1] * colW, curr[0] * rowH))

        elif prev_to_curr == LEFT and curr_to_next == UP:
            surface.blit(bodyBL, (curr[1] * colW, curr[0] * rowH))
        elif prev_to_curr == LEFT and curr_to_next == DOWN:
            surface.blit(bodyTL, (curr[1] * colW, curr[0] * rowH))
        elif prev_to_curr == LEFT and curr_to_next == LEFT:
            surface.blit(bodyHorz, (curr[1] * colW, curr[0] * rowH))

        elif prev_to_curr == RIGHT and curr_to_next == UP:
            surface.blit(bodyBR, (curr[1] * colW, curr[0] * rowH))
        elif prev_to_curr == RIGHT and curr_to_next == DOWN:
            surface.blit(bodyTR, (curr[1] * colW, curr[0] * rowH))
        elif prev_to_curr == RIGHT and curr_to_next == RIGHT:
            surface.blit(bodyHorz, (curr[1] * colW, curr[0] * rowH))

    #tail
    if len(snake) > 1:
        tail = snake[-1]
        prev = snake[-2]
        tail_direction = subtractCells(tail, prev)

        if tail_direction == UP:
            surface.blit(tailUp, (tail[1] * colW, tail[0] * rowH))
        elif tail_direction == DOWN:
            surface.blit(tailDown, (tail[1] * colW, tail[0] * rowH))
        elif tail_direction == LEFT:
            surface.blit(tailLeft, (tail[1] * colW, tail[0] * rowH))
        elif tail_direction == RIGHT:
            surface.blit(tailRight, (tail[1] * colW, tail[0] * rowH))


def drawScreen(gameOver, foodLocations, snake, headDirection):
    """
    draws the view

    Parameters:
    -----------
    gameOver: bool
        Whether the game is over
    foodLocations: list
        The locations of the food
    snake: list
        The snake
    headDirection: list
        The direction of the head

    Returns:
    --------
    None
    """

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

    show_message(str(len(snake)), "Consolas", 40, 30, 20, BLACK, WHITE)

    #draw all food
    for foodLoc in foodLocations:
        surface.blit(appleImg, (foodLoc[1] * colW, foodLoc[0] * rowH))

    if gameOver:
        show_message("Game Over", "Consolas", 96, WIDTH/2, HEIGHT/2, BLACK, WHITE)
        show_message("Total Length: " + str(len(snake)), "Consolas", 40, WIDTH/2, HEIGHT/2 + 70, BLACK, WHITE)
        show_message("Press Space to Play Again", "Consolas", 40, WIDTH/2, HEIGHT/2 + 120, BLACK, WHITE)


def howManyApples():
    """
    Asks the user how many apples will be on the screen at a time
    Returns the number of apples selected (1, 3, or 5)

    Parameters:
    -----------
    None

    Returns:
    --------
    int
        The number of apples selected
    """
    choosing = True

    while choosing:
        surface.fill(LAWN)

        #Draw title
        show_message("How many apples?", "Consolas", 64, WIDTH/2, HEIGHT/4, BLACK, WHITE)

        #Draw buttons
        button1 = show_message("1 Apple", "Consolas", 48, WIDTH/2, HEIGHT/2 - 50, BLACK, WHITE, True)
        button3 = show_message("3 Apples", "Consolas", 48, WIDTH/2, HEIGHT/2, BLACK, WHITE, True)
        button5 = show_message("5 Apples", "Consolas", 48, WIDTH/2, HEIGHT/2 + 50, BLACK, WHITE, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button1.collidepoint(mouse_pos):
                    return 1
                elif button3.collidepoint(mouse_pos):
                    return 3
                elif button5.collidepoint(mouse_pos):
                    return 5

        pygame.display.update()
        clock.tick(60)


def placeFood(snake, existingFood):
    """
    returns a valid [row,col] location for the food
    that is not in the snake or in existing food locations

    Parameters:
    -----------
    snake: list
        The snake
    existingFood: list
        The locations of the existing food

    Returns:
    --------
    list : foodLocation
        The location of the food
    """

    while True:
        foodLocation = [random.randint(0, numRows - 1), random.randint(0, numCols - 1)]
        if foodLocation not in snake and foodLocation not in existingFood and foodLocation not in [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]:
            break

    return foodLocation


def moveSnake(snake, direction, foodLocations, targetApples):
    """
    Moves the snake once in the direction specified
    returns two values
    - whether/not the game is over
    - list of food locations

    Parameters:
    -----------
    snake: list
        The snake
    direction: list
        The direction of the snake
    foodLocations: list
        The locations of the food
    targetApples: int
        The number of apples to be on the screen

    Returns:
    --------
    bool:
        Whether the game is over
    list : foodLocations
        The locations of the food
    """

    head = snake[0]

    #Check if the new position would be out of bounds
    newhead = addCells(head, direction)
    if newhead[0] < 0 or newhead[0] >= numRows or newhead[1] < 0 or newhead[1] >= numCols:
        return True, foodLocations

    if newhead in snake[1:]:
        return True, foodLocations

    if newhead in foodLocations:
        foodLocations.remove(newhead)  #Remove eaten apple
        if len(foodLocations) < targetApples:  #Add new apple if below target
            foodLocations.append(placeFood(snake, foodLocations))
        appleSound.play()
        pygame.mixer.music.stop()
        #Don't pop the tail when eating an apple to make the snake grow
        snake.insert(0, newhead)

    else:
        #Normal movement - add new head and remove tail
        snake.insert(0, newhead)
        snake.pop()

    return False, foodLocations


def main():
    """
    The main function, where all the action happens

    Parameters:
    -----------
    None

    Returns:
    --------
    None
    """

    gameOver = False
    gameOverSound = False
    UP = [-1, 0]
    DOWN = [1, 0]
    LEFT = [0, -1]
    RIGHT = [0, 1]

    #Get number of apples from user
    targetApples = howManyApples()

    #Starting snake
    snake = [
        [numRows//2, numCols//2]
    ]

    #Initialize multiple food locations
    foodLocations = []
    for _ in range(targetApples):
        foodLocations.append(placeFood(snake, foodLocations))

    currentDirection = RIGHT

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not gameOver:
                #Prevent moving in the opposite direction
                if event.key == pygame.K_UP and currentDirection != DOWN:
                    if currentDirection != UP:  #Only play sound if direction changes
                        upSound.play()
                    currentDirection = UP
                elif event.key == pygame.K_DOWN and currentDirection != UP:
                    if currentDirection != DOWN:  #Only play sound if direction changes
                        downSound.play()
                    currentDirection = DOWN
                elif event.key == pygame.K_LEFT and currentDirection != RIGHT:
                    if currentDirection != LEFT:  #Only play sound if direction changes
                        leftSound.play()
                    currentDirection = LEFT
                elif event.key == pygame.K_RIGHT and currentDirection != LEFT:
                    if currentDirection != RIGHT:  #Only play sound if direction changes
                        rightSound.play()
                    currentDirection = RIGHT

            elif event.type == pygame.KEYDOWN and gameOver:
                if event.key == pygame.K_SPACE:
                    #Restart all game variables
                    gameOver = False
                    gameOverSound = False

                    #Get new number of apples
                    targetApples = howManyApples()

                    #Starting snake
                    snake = [
                        [numRows//2, numCols//2]
                    ]
                    #Initialize multiple food locations
                    foodLocations = []
                    for _ in range(targetApples):
                        foodLocations.append(placeFood(snake, foodLocations))

                    currentDirection = RIGHT

        surface.fill(LAWN)
        drawScreen(gameOver, foodLocations, snake, currentDirection)

        if not gameOver:
            gameOver, foodLocations = moveSnake(snake, currentDirection, foodLocations, targetApples)

        if gameOver and not gameOverSound:
            gameoverSound.play()
            gameOverSound = True

        pygame.display.update()
        clock.tick(10)

main()
