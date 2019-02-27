import pygame
import time
import random

#needs to be here
pygame.init()

#define some colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#set width and height
display_width = 1000
display_height = 1000

#initialize window
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Dungeon Game')

#load in the image of our hero
character = pygame.image.load('racecar.png')
car_width = 73 #width of the image

#initialize clock
clock = pygame.time.Clock()

def platform(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def character_update(x, y):
    #put the image on the screen
    gameDisplay.blit(character, (x,y))

def game_loop():
    #character starting position
    x = (display_width * 0.45) #do this to get correct centering
    y = (display_height * 0.45)

    gameExit = False

    #variables for controllign the sprite
    x_change = 0
    y_change = 0

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
                elif event.key == pygame.K_DOWN:
                    y_change = 5
                elif event.key == pygame.K_UP:
                    y_change = -5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0


        #update the x position of the car
        x += x_change
        y += y_change

        #do this above car --> draws things in order
        gameDisplay.fill(white)

        #draw platforms
        platform(100, 100, 100, 100, red)

        #move the character
        character_update(x, y)

        #collision detection with walls
        if x > display_width - car_width or x < 0:
            pygame.quit()
            quit()

            #TODO: Figure out collisions

        #move the incoming blocks around
        # if thing_starty > display_height:
        #     thing_starty = 0 - thing_height
        #     thing_startx = random.randrange(0, display_width)
        #
        # #handle crashes with objects
        # #check if there is y crossover
        # if y < thing_starty + thing_height:
        #     print('y crossover')
        #
        #     #are we anywhere within the boundaries of x
        #     if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
        #         print('x crossover')
        #         pygame.quit()
        #         quit()

        #pygame.display.flip()  --> always just updates entire surface
        pygame.display.update() #can use an argument to update small things

        #number is frames per second
        clock.tick(60)

#run the game loop
game_loop()

#stops pygame from running
pygame.quit()
