import pygame
import sys
import random
from time import sleep

padWidth = 480   # width of game screen
padHeight = 640  # height of game screen
rockimg = ['rock01.png','rock02.png','rock03.png','rock04.png','rock05.png',
         'rock06.png','rock07.png','rock08.png','rock09.png','rock10.png',
         'rock11.png','rock12.png','rock13.png','rock14.png','rock15.png',
         'rock16.png','rock17.png','rock18.png','rock19.png','rock20.png',
         'rock21.png','rock22.png','rock23.png','rock24.png','rock25.png',
         'rock26.png','rock27.png','rock28.png','rock29.png','rock30.png']

def score(count):  # this counts the score, missile hit
    global gamePad  # global enables all variables to be read in other functions
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('Number Destroyed: ' + str(count), True, (255,255,255)) # RGB
    gamePad.blit(text, (10,0))
                       
def missed(count):  # this counts missed rocks
    global gamaPad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('Number missed: ' + str(count), True, (255,0,0)) # RGB (only red)
    gamePad.blit(text, (300,0))

def message(text):  # this shows the text message on the screen
    global gamePad, gameovermusic
    textfont = pygame.font.Font('NanumGothic.ttf', 50)
    text = textfont.render(text, True, (255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()  
    pygame.mixer.music.stop()   # stops the background sound for gameover sound
    gameovermusic.play()   # play gameover sound
    sleep(2)   # stop the game for two seconds
    pygame.mixer.music.play(-1)  # play the background sound again
    rungame()

def crash():  # gives message of flight destroyed
    global gamePad
    message('Flight Destroyed!!')

def gameover():  # gives messgage of game over
    global gamePad
    message('Game Over..')
    
def initGame(): # this function initialize the game. It starts over from the beginning
    global gamePad, clock, background, flight, missile, explosion, explosionmusic, gameovermusic, missilemusic
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption("Shooting Game")  # name of game
    background = pygame.image.load('background.png')  # pygame.image.load brings all images
    flight = pygame.image.load('fighter.png')
    missile = pygame.image.load('missile.png')
    explosion = pygame.image.load('explosion.png')
    pygame.mixer.music.load('music.wav') # background sound
    pygame.mixer.music.play(-1)  # play background sound
    missilemusic = pygame.mixer.Sound('missile.wav') # missile sound
    gameovermusic = pygame.mixer.Sound('gameover.wav') # gameover sound
    clock = pygame.time.Clock()
    
def drawobject(obj, x, y):  # it draws objects need in game play
    global gamePad
    gamePad.blit(obj, (x,y)) # blit(background, (x,y)) it is the position inside the window

def rungame(): # this function execute the whole game process
    global gamepad, clock, background, flight, missile, explosion, explosionmusic, gameovermusic, missilemusic

    flightsize = flight.get_rect().size  # the size of the flight
    flightWidth = flightsize[0]
    flightHeight = flightsize[1]

    x = padWidth * 0.45  # it decides the position of the flight
    y = padHeight * 0.9
    flighterX = 0
    flighterY = 0 # starting location of the flight
    missileXY = []
    
    rock = pygame.image.load(random.choice(rockimg)) # ramdomly bring the image of rocks
    rocksize = rock.get_rect().size  # size of rock
    rockwidth = rocksize[0]
    rockheight = rocksize[1]
    
    rockX = random.randrange(0, padWidth - rockwidth) # starting location of rock
    rockY = 0
    rockspeed = 2  # speed of rock

    hit = False
    hitcount = 0
    rockpassed = 0
                 
    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]: # this enables the game to be shut down
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]: # goes 5 left when left button pressed
                if event.key == pygame.K_LEFT:
                    flighterX -= 5

                elif event.key == pygame.K_RIGHT: # goes 5 right when right button pressed
                    flighterX += 5    

                elif event.key == pygame.K_SPACE: # shoots missile when space button pressed
                    missilemusic.play()  # plays missile shooting music
                    missileX = x + flightWidth/2
                    missileY = y - flightHeight
                    missileXY.append([missileX, missileY])

                elif event.key == pygame.K_UP: # goes five up when up button pressed
                    flighterY -= 5

                elif event.key == pygame.K_DOWN: # goes five down when down button pressed
                    flighterY += 5

            if event.type in [pygame.KEYUP]:  # take hand off from keybord, the flight will stop
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    flighterX = 0
                elif event.key == pygame.K_UP:
                    flighterY = 0
                elif event.key == pygame.K_DOWN:
                    flighterY = 0
                    
        drawobject(background, 0,0)
        
        y += flighterY
        x += flighterX
        if x < 0:  # when x becomes negative, the flight will go out of screen
            x = 0   # set x == 0 to prevent it to be out of screen
        elif x > padWidth - flightWidth:  # it serves the same purpose as above
            x = padWidth - flightWidth  # it is the maximum position of the flight to the right

        if y < 0:   # These if and elif statement prevent the flight not going outside of the screen top and bottom
            y = 0
        elif y > padHeight - flightHeight:
            y = padHeight - flightHeight

        if y <= rockY + rockheight:
            if(rockX >= x and rockX <= x + flightWidth) or \
                     (rockX + rockwidth >= x + flightWidth and rockX + rockwidth <= x + flightWidth):
                crash()
        
        drawobject(flight, x, y)

        if len(missileXY) != 0:
               for i, bxy in enumerate(missileXY):  # repeat missile element, multiple missiles needed
                   bxy[1] -= 10  # missile goes 10 up along y axis
                   missileXY[i][1] = bxy[1]

                   if bxy[1] < rockY:  
                       if bxy[0] > rockX and bxy[0] < rockX + rockwidth:  # this checks if the missile hit the rock or not
                           missileXY.remove(bxy) # remove the rock when it is hit
                           hit = True   # change the hit as True from False
                           hitcount += 1  # count if missile hit the rock

                   if bxy[1] <= 0:  # if missile goes out of the screen
                       try:
                           missileXY.remove(bxy) # remove the missile
                       except:
                            pass

        if len(missileXY) != 0:
               for bx, by in missileXY:
                   drawobject(missile, bx, by)

        score(hitcount)

        rockY += rockspeed # rock goes to down from the top

        if rockY >= padHeight: # this is when the rock hit the bottom of the screen (player missed the rock)
            rock = pygame.image.load(random.choice(rockimg)) # load random lock image again
            rocksize = rock.get_rect().size
            rockwidth = rocksize[0]
            rockheight = rocksize[1]
            rockX = random.randrange(0, padWidth - rockwidth)
            rockY = 0
            rockpassed += 1

        if rockpassed == 5:  # if 5 rocks are missied, it is gameover
            gameover()

        missed(rockpassed)

        if hit:  # when hit becomes true
            drawobject(explosion, rockX, rockY) # draw the explosion image to enhance the game experience
            rock = pygame.image.load(random.choice(rockimg)) # then the load random rock image
            rocksize = rock.get_rect().size
            rockwidth = rocksize[0]
            rockheight = rocksize[1]
            rockX = random.randrange(0, padWidth - rockwidth)
            rockY = 0
            hit = False  # change the hit to False again

            rockspeed += 0.3 # increase the speed if rock is hit
            if rockspeed >= 10:
                rockspeed == 10  # maximum speed of rock

        drawobject(rock, rockX, rockY)
            

        pygame.display.update()  
        
        clock.tick(60) # FPS
    pygame.quit() # quit pygame

initGame()
rungame()
