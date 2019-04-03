import pygame
import time
import random

#File which contains colors
from colors import *

#Start with the classes
class Player( pygame.sprite.Sprite ):
    #Initializing the sprites
    def __init__( self, color=blue, width = 32, height = 48 ):

        super( Player, self ).__init__()

        #self.image = pygame.Surface(( width, height))
        #self.image.fill( color )

        self.image = pygame.image.load("racecar.png").convert()

        self.set_properties()

        self.hspeed = 0
        self.vspeed = 0

        self.level = None

    #setting properties; origin
    def set_properties( self ):
        self.rect = self.image.get_rect()
        self.origin_x = self.rect.centerx
        self.origin_y = self.rect.centery

        self.speed = 5

        #setting position of sprites

    def set_position( self, x, y ):
        self.rect.x = x - self.origin_x
        self.rect.y = y - self.origin_y

    def set_level( self, level ):
        self.level = level
        self.set_position( level.player_start_x, level.player_start_y)

    #Collisions
    def update( self, collidable = pygame.sprite.Group(), event = None ):

        self.experience_gravity()

        self.rect.x += self.hspeed

        collision_list = pygame.sprite.spritecollide( self, collidable, False )

        for collided_object in collision_list:
            if ( self.hspeed > 0 ):
                #Right direction
                self.rect.right = collided_object.rect.left

            elif ( self.hspeed < 0 ):
                #left direction
                self.rect.left = collided_object.rect.right

        self.rect.y += self.vspeed

        collision_list = pygame.sprite.spritecollide( self, collidable, False )

        for collided_object in collision_list:
            if ( self.vspeed > 0 ):
                #Down direction
                self.rect.bottom = collided_object.rect.top
                self.vspeed = 0

            elif ( self.vspeed < 0 ):
                #Up direction
                self.rect.top = collided_object.rect.bottom
                self.vspeed = 0

        if not ( event == None ):
            if ( event.type == pygame.KEYDOWN ):
                if ( event.key == pygame.K_LEFT ):
                    self.hspeed = -self.speed

                if ( event.key == pygame.K_RIGHT ):
                    self.hspeed = self.speed
                #makes sure block only jumps once
                if ( event.key == pygame.K_UP ):
                    if ( len(collision_list) == 1 ):
                        self.vspeed = -( self.speed )*2

            if ( event.type == pygame.KEYUP ):
                if ( event.key == pygame.K_LEFT ):
                    if ( self.hspeed < 0 ): self.hspeed = 0
                if ( event.key == pygame.K_RIGHT ):
                    if ( self.hspeed > 0 ): self.hspeed = 0


                if ( event.key == pygame.K_UP ):
                    #if ( self.vspeed != 0 ): self.vspeed = 0
                    #comment this out if you want box to jump full height each time
                    pass
                if ( event.key == pygame.K_DOWN ):
                    #if ( self.vspeed != 0 ): self.vspeed = 0
                    #comment this out if you want box to jump full height each time
                    pass


    def experience_gravity( self, gravity = .35 ):
        #GRAVITY
        if ( self.vspeed == 0 ): self.vspeed = 1
        else: self.vspeed += gravity

class Block( pygame.sprite.Sprite ):
#Initializing the sprites
    def __init__( self, x, y, width, height, color = blue):

        super( Block, self ).__init__()

        if( width < 0):
            x += width
            width = abs( width )
        if (height < 0):
            y += height
            height = abs( height )

        self.image = pygame.Surface(( width, height))
        self.image.fill( color )

        self.rect = self.image.get_rect()
        #Comment in if you want to use origin functionality

        #self.origin_x = self.rect.centerx
        #self.origin_y = self.rect.centery

        self.rect.x = x #- self.origin_x
        self.rect.y = y #- self.origin_y


    def set_message( text ):
        global message, previous_message
        message = font.render( text, True, black, white )
        previous_message = message

class Level( object ):

    def __init__(self, player_object ):

        self.object_list = pygame.sprite.Group()

        self.player_object = player_object

        self.player_start = self.player_start_x, self.player_start_y = (0,0)

        self.world_shift_x = self.world_shift_y = 0

        self.left_viewbox = display_width/2 - display_width/8
        self.right_viewbox = display_width/2 + display_width/10

        #adjust how much you want screen to move
        self.up_viewbox = display_height/5
        self.down_viewbox = display_height/4 + display_height/12


    def update( self ):

        self.object_list.update()

    def draw( self, window ):

        window.fill( white )

        self.object_list.draw( window )

    def shift_world( self, shift_x, shift_y ):

        self.world_shift_x += shift_x
        self.world_shift_y += shift_y

        for each_object in self.object_list:
            each_object.rect.x += shift_x
            each_object.rect.y += shift_y

    def run_viewbox( self ):
        #left viewbox
        if ( self.player_object.rect.x <= self.left_viewbox ):
            view_difference = self.left_viewbox - self.player_object.rect.x
            self.player_object.rect.x = self.left_viewbox
            self.shift_world( view_difference, 0 )
        #right viewbox
        if ( self.player_object.rect.x >= self.right_viewbox ):
            view_difference = self.right_viewbox - self.player_object.rect.x
            self.player_object.rect.x = self.right_viewbox
            self.shift_world( view_difference, 0 )

        #up viewbox
        if ( self.player_object.rect.y <= self.up_viewbox ):
            view_difference = self.up_viewbox - self.player_object.rect.y
            self.player_object.rect.y = self.up_viewbox
            self.shift_world( 0, view_difference )
        #down viewbox
        if ( self.player_object.rect.y >= self.down_viewbox ):
            view_difference = self.down_viewbox - self.player_object.rect.y
            self.player_object.rect.y = self.down_viewbox
            self.shift_world( 0, view_difference )


class Level_00( Level ):

    def __init__( self, player_object ):

        super( Level_00, self ).__init__( player_object )
        #Player start
        self.player_start = self.player_start_x, self.player_start_y = (100,0)

        x = 1154

        level = [
                #[ x, y, width, height, color ]
                [0, 12, 75, 682, black],
                [72, 614, 1154, 80, black],
                [70, 542, 223, 23, black],
                [538, 534, 239, 32, black],
                [830, 486, 164, 25, black],
                [1037, 431, 162, 32, black],

                [1226, 614, 1154, 80, black],
                [339 + x, 496, 233, 33, black],
                [662 + x, 470, 202, 26, black],
                [907 + x, 419, 306, 21, black],
                [1193 + x, 116, 16, 304, black],
                [1112 + x, 248, 81, 26, black],
                [911 + x, 172, 85, 20, black],
                [1088 + x, 117, 106, 17, black],
                [1028 + x, 339, 71, 19, black],
            ]

        for block in level:
            block = Block( block[0], block[1], block[2], block [3], block [4])
            self.object_list.add( block )




#needs to be here
pygame.init()

#define some colors
# black = (0, 0, 0)
# white = (255, 255, 255)
# red = (255, 0, 0)
# green = (0, 255, 0)
# blue = (0, 0, 255)
#
# bright_red = (255, 0, 0)
# bright_green = (0, 255, 0)

block_color = (53, 115, 255)

#set width and height
display_width = 1000
display_height = 1000

#initialize window
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Dungeon Game')

#load in the image of our hero
# character = pygame.image.load('racecar.png')
# char_width = 73 #width of the image

#initialize clock
clock = pygame.time.Clock()

#set the fps
frames_per_second = 60


# def monsters(thingx, thingy, thingw, thingh, color):
#     pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
#
# def platform(thingx, thingy, thingw, thingh, color):
#     pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

# def character_update(x, y):
#     #put the image on the screen
#     gameDisplay.blit(character, (x,y))

#get the text objects for a given font
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


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
        TextSurf, TextRect = text_objects("Dungeon Master", largeText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!", 150, 600, 100, 50, green, bright_green, game_loop)
        button("QUIT", 550, 600, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)

def game_loop():
    #initialize the player
    active_object_list = pygame.sprite.Group()
    player = Player()

    #character starting position
    x = 500
    y = 500
    player.set_position(x, y)
    active_object_list.add( player )

    #TODO: add in functionality to deal with multiple levels
    #just going to use level 0 as our default
    level_list = []
    level_list.append( Level_00( player ) )

    current_level_number = 0
    current_level = level_list [ current_level_number ]

    player.set_level( current_level )

    #variables for controllign the sprite
    # x_change = 0
    # y_change = 0
    #
    # #putting an object on screen
    # thing_startx = random.randrange(0, display_width)
    # thing_starty = -600
    # thing_speed = 4
    # thing_width = 100
    # thing_height = 100
    #
    # #count for the number of things dodged
    # dodged = 0

    #keeps the game window running
    gameExit = True

    #event loop
    while gameExit:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or ( event.type == pygame.KEYDOWN ) and ( event.key == pygame.K_ESCAPE or event.key == pygame.K_q ):
                gameExit = False


        # Update Functions
        player.update ( current_level.object_list, event )
        event = None

        current_level.update()


        #Logic Testing
        current_level.run_viewbox()


        #Draw Everything
        current_level.draw( gameDisplay )
        active_object_list.draw( gameDisplay )


        #Delay Framerate
        clock.tick( frames_per_second )

        #Update Everything
        #pygame.display.flip()  --> always just updates entire surface
        pygame.display.update() #can use an argument to update small things


#run the start screen
game_intro()

#run the game loop
game_loop()

#stops pygame from running
pygame.quit()
quit()
