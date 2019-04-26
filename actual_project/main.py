import pygame
import time
import random

#TODO:

#File which contains colors
from colors import *


##GLOBAL VARS

#needs to be here
pygame.init()

#set width and height
display_width = 1250
display_height = 1000

#initialize window
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Dungeon Game')

#initialize clock
clock = pygame.time.Clock()

#set the fps
frames_per_second = 60

class Spritesheet:
    #utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        #get an image out of a larger spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        #resize the image
        image = pygame.transform.scale(image, (width//2, height//2))
        return image


#TODO: clean this up, put classes in a different file
char_spritesheet = Spritesheet("spritesheet_jumper.png")
platform_spritesheet = Spritesheet("./../abstract_platformer/Spritesheet/spritesheet_tiles.png")

#Start with the classes
class Player( pygame.sprite.Sprite ):
    #Initializing the sprites
    def __init__( self, color=blue, width = 32, height = 48 ):

        super( Player, self ).__init__()

        #self.image = pygame.Surface(( width, height))
        #self.image.fill( color )

        #sprite animations
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]

        #self.image = pygame.image.load("btjump.gif").convert()

        self.set_properties()

        self.hspeed = 0
        self.vspeed = 0

        self.level = None


    #this is used for getting the sprite images
    #TODO: Do the same for background
    def load_images(self):
        self.standing_frames = [char_spritesheet.get_image(614, 1063, 120, 191),
                                char_spritesheet.get_image(690, 406, 120, 201),
                                ]

        #take out background black color
        for frame in self.standing_frames:
            frame.set_colorkey(black)

        self.walking_frames_r = [char_spritesheet.get_image(678, 860, 120, 201),
                                 char_spritesheet.get_image(692, 1458, 120, 207),
                                ]

        self.walking_frames_l = []

        #walking frame l is just r but flipped
        for frame in self.walking_frames_r:
                frame.set_colorkey(black)
                self.walking_frames_l.append(pygame.transform.flip(frame, True, False))

        #add in the jump frame
        self.jump_frame = char_spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(black)

    def get_position(self):
        return (self.rect.centerx, self.rect.centery)


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
    def update( self, collidable = pygame.sprite.Group(), event=None ):
        #run sprite animations
        self.animate()

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

        #TODO: Fix this loop so that it will automatically update and put player at top without needing another button press *******
        if not ( event == None):
            if ( event.type == pygame.KEYDOWN ):
                if ( event.key == pygame.K_LEFT ):
                    self.hspeed = -self.speed

                if ( event.key == pygame.K_RIGHT ):
                    self.hspeed = self.speed
                #makes sure block only jumps once TODO: Double jumping
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

    #figure out better name for this later
    def animate(self):
        #get the current time --> # of ticks since game started
        now = pygame.time.get_ticks()

        #set walking variable to true if we are moving horizontally
        if self.hspeed != 0:
            self.walking = True
        else:
            self.walking = False

        #show walk animations
        #TODO: Figure out why the sideways walking animation isnt working
        if self.walking:
            #check if it is time to update
            if now - self.last_update > 200: #number is the # milliseconds between updating frmaes --> more frames of animation, lower number
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                #bottom = self.rect.bottom

                #if our hspeed is positive, we are moving to the right, otherwise left
                if self.hspeed>0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]

                #self.rect.bottom = bottom

        #show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]

                #make the bunny standing on the floor
                # bottom = self.rect.bottom
                # self.image = self.standing_frames[self.current_frame]
                # self.rect = self.image.get_rect()
                # self.rect.bottom = bottom


class Block( pygame.sprite.Sprite ):
#Initializing the sprites TODO: Change the color attribute to the type of block
    def __init__( self, x, y, platform_number):
        #for platform number, 0 is top platform, 1 is middle, 2 is bottom --> TODO: add in more types later

        super( Block, self ).__init__()

        # if( width < 0):
        #     x += width
        #     width = abs( width )
        # if (height < 0):
        #     y += height
        #     height = abs( height )


        #just black blocks
        # self.image = pygame.Surface(( width, height))
        # self.image.fill( color )

        #using spritesheet images --> load in all of the blocks
        #TODO: Paser xml file to grab specific sprites
        images = [  platform_spritesheet.get_image(390, 650, 64, 64), #top/side platform --> bluetile_
                    platform_spritesheet.get_image(325, 130, 64, 50), #middle platform --> bluetile_05
                    platform_spritesheet.get_image(390, 520, 64, 64)  #bottom platform
                ]
        self.image = images[platform_number] #can use this to pick different platforms
        self.image.set_colorkey(black)
        #TODO:scale the images so they will be slightly larger

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
        # if ( self.player_object.rect.y <= self.up_viewbox ):
        #     view_difference = self.up_viewbox - self.player_object.rect.y
        #     self.player_object.rect.y = self.up_viewbox
        #     self.shift_world( 0, view_difference )
        # #down viewbox
        # if ( self.player_object.rect.y >= self.down_viewbox ):
        #     view_difference = self.down_viewbox - self.player_object.rect.y
        #     self.player_object.rect.y = self.down_viewbox
        #     self.shift_world( 0, view_difference )


class Level_00( Level ):

    def __init__( self, player_object ):

        super( Level_00, self ).__init__( player_object )
        #Player start
        self.player_start = self.player_start_x, self.player_start_y = (display_width/2,display_height/2)

        #width of the screen at one point --> can use this to do arithmetic and go off level
        x = 1154

        # level = [
        #         #[ x, y, width, height, color ]
        #         [0, 12, 75, 682, black],
        #         [72, 614, 1154, 80, black],
        #         [70, 542, 223, 23, black],
        #         [538, 534, 239, 32, black],
        #         [830, 486, 164, 25, black],
        #         [1037, 431, 162, 32, black],
        #
        #         [1226, 614, 1154, 80, black],
        #         [339 + x, 496, 233, 33, black],
        #         [662 + x, 470, 202, 26, black],
        #         [907 + x, 419, 306, 21, black],
        #         [1193 + x, 116, 16, 304, black],
        #         [1112 + x, 248, 81, 26, black],
        #         [911 + x, 172, 85, 20, black],
        #         [1088 + x, 117, 106, 17, black],
        #         [1028 + x, 339, 71, 19, black],
        #     ]

        #how thick our lines are
        edge_width = 30
        level = [
                #[ x, y, platform_number ] --> commented out parts are width and height
                #top
                [0, 0, 0], #display_width/8, edge_width, 0],
                [display_width/4, 0, 0], # display_width/2, edge_width, 0],
                [display_width*7/8, 0, 0], # display_width/8, edge_width, 0],

                #left side
                [0, 0, 0], #edge_width, display_height/3, 0],
                [0, display_height*2/3, 0], # edge_width, display_height/3, 0],

                #right side
                [display_width-edge_width, 0, 0], # edge_width, display_height/3, 0],
                [display_width-edge_width, display_height*2/3, 0], # edge_width, display_height/3, 0],

                #bottom
                [0, display_height-edge_width, 2], # display_width/8, edge_width, 2],
                [display_width/4, display_height-edge_width, 2], # display_width/2, edge_width, 2],
                [display_width*7/8, display_height-edge_width, 2], # display_width/8, edge_width, 2],

                #middle platforms
                [display_width/8, display_height/2, 1], # display_width/8, edge_width, 1],
                [display_width*3/4, display_height/2, 1], # display_width/8, edge_width, 1],
                [display_width*3.5/8, display_height/2, 1]# display_width/8, edge_width, 1],
            ]

        for block in level:
            block = Block( block[0], block[1], block[2])#, block [3], block [4])
            self.object_list.add( block )


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

        button("GO!", display_width/3, display_height*(0.6), 100, 50, green, bright_green, game_loop)
        button("QUIT", display_width*2/3 - 100, display_height*(0.6), 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)

def game_loop():
    #initialize the player
    active_object_list = pygame.sprite.Group()
    player = Player()

    #character starting position
    x = display_width/2
    y = display_height/2
    player.set_position(x, y)
    active_object_list.add( player )

    #TODO: add in functionality to deal with multiple levels
    #just going to use level 0 as our default
    level_list = []
    level_list.append( Level_00( player ) )

    current_level_number = 0
    current_level = level_list [ current_level_number ]

    player.set_level( current_level )

    #keeps the game window running
    gameExit = True
    event = None

    while(gameExit):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or ( event.type == pygame.KEYDOWN ) and ( event.key == pygame.K_ESCAPE or event.key == pygame.K_q ):
                gameExit = False
                pygame.quit()
                quit()


        #make the level wrap around --> TODO: might need to put this outside event loop --> make its own function
        position = player.get_position()
        #vertical
        if(position[1] > display_height):
            player.set_position(position[0], 0)
        elif(position[1] < 0):
            player.set_position(position[0], display_height)
        #horizontal --> the player.rect.width/2 modifications cause player to be totally off screen
        #TODO: figure out how to make player appear on both sides
        if(position[0] > display_width  + player.rect.width/2):
            player.set_position(0 - player.rect.width/2, position[1])
        elif(position[0] < 0 - player.rect.width/2):
            player.set_position(display_width + player.rect.width/2, position[1])

        # Update Functions
        player.update ( current_level.object_list, event )
        event = None

        current_level.update()

        #Logic Testing
        #current_level.run_viewbox()

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
