import pygame

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

#function for displaying the car
def car(x, y):
    #put the image on the screen
    gameDisplay.blit(carImg, (x,y))

#car starting position
x = (display_width * 0.45) #do this to get correct centering
y = (display_height * 0.8)

crashed = False

#event loop
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    #do this above car --> draws things in order
    gameDisplay.fill(white)

    #move the car
    car(x, y)

    #pygame.display.flip()  --> always just updates entire surface
    pygame.display.update() #can use an argument to update small things

    #number is frames per second
    clock.tick(60)

#stops pygame from running
pygame.quit()
