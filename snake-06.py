


from pygame import mixer
# import serial
import random, pygame, sys, os
from pygame.locals import *
startImg = pygame.image.load('start08.png')
gameOverImg = pygame.image.load('gameOver06.png')
newHighScoreImg = pygame.image.load('newHighScore06.png')

FPS = 8
# WINDOWWIDTH = 1410
# WINDOWHEIGHT = 1020
WINDOWWIDTH = 600
WINDOWHEIGHT = 570
CELLSIZE = 30
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

contents = None

# ser = serial.Serial('/dev/cu.usbmodem1421', 9600)



#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   31,   232) #BACKGROUND
RED       = ( 250,  207,  60) #APPLE
GREEN     = ( 250,  207,  60)   #SNAKE
DARKGREEN = ( 250,  207,  60)  #SNAKE OUTLINE
DARKGRAY  = (  0,   31,   232)#GRID LINES
REDRED  = ( 255,  0,  0)  # APPLE REALLY
YELLOW  = ( 250,  225,  60)  #YELLOW
GREENGREEN  = ( 0,  204,  0)  #GREEN
BGCOLOR =   BLACK
score_file_path = 'scorefile.txt'

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)
    BASICFONT = pygame.font.Font('arial.ttf', 55)
    pygame.display.set_caption('ITP BANK')

    showStartScreen()
    while True:
        score = runGame()

        if score:
            saveScore(score)
        showGameOverScreen(score)



def saveScore(score):
    score = score * 20
    if os.path.exists(score_file_path):
        with open(score_file_path, 'r') as score_file:
            contents = score_file.read()
            contents = contents.replace("\n", "")
    else:
        contents = None
    if not contents:
        prev_high_score = 0
    else:
        prev_high_score = int(contents)
    if (score > prev_high_score):
        with open(score_file_path, 'w') as score_file:
            score_file.write(str(score))
            print "saved new high score: {}".format(score)
            # gameOverFont = pygame.font.Font('arial.ttf', 50)
            # gameSurf = gameOverFont.render(u'\u2605NEW HIGH SCORE!\u2605', True, YELLOW)
            # gameSurf = gameOverFont.render('$$NEW HIGH SCORE$$', True, GREENGREEN)
            # gameRect = gameSurf.get_rect()
            # gameRect.midtop = (WINDOWWIDTH / 2, 310)

            DISPLAYSURF.blit(newHighScoreImg,(0,0))



def runGame():

    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                    pygame.mixer.music.load('beep2.wav')
                    pygame.mixer.music.play(0)
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                    pygame.mixer.music.load('beep2.wav')
                    pygame.mixer.music.play(0)
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                    pygame.mixer.music.load('beep2.wav')
                    pygame.mixer.music.play(0)
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                    pygame.mixer.music.load('beep2.wav')
                    pygame.mixer.music.play(0)
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            score = len(wormCoords) - 3
            return score # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                score = len(wormCoords) - 3
                return score # game over

        # check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        else:
            del wormCoords[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        score = len(wormCoords) - 3
        drawScore(score)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
    pressKeySurf = pygame.font.Font('arial.ttf', 36).render('Press 2 to play.', True, YELLOW)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 250, WINDOWHEIGHT - 42)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)



def arrowMsg():
    arrowSurf = BASICFONT.render(u'2= \u2191 5= \u2193 4= \u2190 6= \u2192', True, YELLOW)
    arrowRect = arrowSurf.get_rect()
    arrowRect.topleft = (WINDOWWIDTH - 1280, WINDOWHEIGHT - 75)
    # DISPLAYSURF.blit(arrowSurf, arrowRect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyDownEvents = pygame.event.get(KEYDOWN)

    if len(keyDownEvents) != 0:
        pygame.mixer.music.load('beep2.wav')
        pygame.mixer.music.play(0)


    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key





def showStartScreen():

    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(startImg,(0,0))


    drawPressKeyMsg()

    arrowMsg()

    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return



def terminate():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen(score):
    pygame.mixer.music.load('errorTone3.wav')
    pygame.mixer.music.play(0)



    gameOverFont = pygame.font.Font('arial.ttf', 150)
    gameSurf = gameOverFont.render('GAME', True, YELLOW)
    overSurf = gameOverFont.render('OVER', True, YELLOW)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height - 20)

    # DISPLAYSURF.blit(gameSurf, gameRect)
    # DISPLAYSURF.blit(overSurf, overRect)
    DISPLAYSURF.blit(gameOverImg,(0,0))


    if os.path.exists(score_file_path):
        with open(score_file_path, 'r') as score_file:
            contents = score_file.read()

    highScoreFont = pygame.font.Font('arial.ttf', 60)
    highScoreSurf = highScoreFont.render('HIGH SCORE: $%s' % (contents), True, YELLOW)
    highScoreRect = highScoreSurf.get_rect()
    highScoreRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT - 116)
    DISPLAYSURF.blit(highScoreSurf, highScoreRect)



    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue


    count = 80099

    while count > 0:
        count-= 1
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return


    showStartScreen()

def drawScore(score):
    scoreSurf = pygame.font.Font('arial.ttf', 38).render('Score: $%s' % (score * 20), True, YELLOW)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 230, 5)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)


# pygame.draw.rect(screen, color, (x,y,width,height), thickness)

# pygame.draw.circle(screen, color, (x,y), radius, thickness)

    # pygame.draw.rect(DISPLAYSURF, REDRED, appleRect)

    # hiddenRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    # pygame.draw.rect(DISPLAYSURF, REDRED, hiddenRect)
    pygame.draw.circle(DISPLAYSURF, YELLOW, (x+15,y+15), CELLSIZE - 20, 0)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
