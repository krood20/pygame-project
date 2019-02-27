import pygame
import time
import random

#needs to be here
pygame.init()

#set width and height
display_width = 800
display_height = 600

#define some colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#initialize window
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Racing Game')

#initialize clock
clock = pygame.time.Clock()

#load in the car image
carImg = pygame.image.load('racecar.png')
car_width = 73 #width of the image


def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

#function for displaying the car
def car(x, y):
    #put the image on the screen
    gameDisplay.blit(carImg, (x,y))

#get the text objects for a given font
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#display a message to the screen
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)

    #text surface and the actual text
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    #update the display
    pygame.display.update()

    time.sleep(2)

    game_loop()

def crash():
    message_display('You crashed!')

def game_loop():
    #car starting position
    x = (display_width * 0.45) #do this to get correct centering
    y = (display_height * 0.8)

    gameExit = False

    #variables for controllign the car
    x_change = 0

    #putting an object on screen
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100

    #event loop
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #stops pygame from running
                pygame.quit()
                quit()

            #check for keystrokes
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        #update the x position of the car
        x += x_change

        #do this above car --> draws things in order
        gameDisplay.fill(white)

        #things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, black)

        #move the rectangle closer to us
        thing_starty += thing_speed

        #move the car
        car(x, y)

        #collision detection with walls
        if x > display_width - car_width or x < 0:
            crash()

        #move the incoming blocks around
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)

        #handle crashes with objects
        #check if there is y crossover
        if y < thing_starty + thing_height:
            print('y crossover')

            #are we anywhere within the boundaries of x
            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                print('x crossover')
                crash()

        #pygame.display.flip()  --> always just updates entire surface
        pygame.display.update() #can use an argument to update small things

        #number is frames per second
        clock.tick(60)

#run the game loop
game_loop()

#stops pygame from running
pygame.quit()
