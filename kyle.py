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
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 255)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

block_color = (53, 115, 255)

#initialize window
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Racing Game')

#initialize clock
clock = pygame.time.Clock()

#load in the car image
carImg = pygame.image.load('racecar.png')
car_width = 73 #width of the image



def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


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

#put in the message, x and y of start position
#width and height for rectangle
#inactive color and active color
def button(msg, x, y, w, h, ic, ac, action=None):
    #get our mouse position and the clicks
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    #xcoord + width < mouse[0] > xcoord and same for y boundaries
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        # pygame.draw.rect(gameDisplay, bright_red, (550, 450, 100, 50))
        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def quit_game():
    pygame.quit()
    quit()

#start screen --> use this to do pause screen
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 115)

        #text surface and the actual text
        TextSurf, TextRect = text_objects("A bit racey", largeText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("QUIT", 550, 450, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)



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
    thing_speed = 4
    thing_width = 100
    thing_height = 100

    #count for the number of things dodged
    dodged = 0

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
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        
        #move the car
        car(x, y)
        things_dodged(dodged)

        #collision detection with walls
        if x > display_width - car_width or x < 0:
            crash()

        #move the incoming blocks around
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_count += 1
            #thing_speed += 1 #if you want to make it faster over time
            #thing_width += (dodged * 1.2) #to make it wider over time


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

#game intro
game_intro()

#run the game loop
game_loop()

#stops pygame from running
pygame.quit()
