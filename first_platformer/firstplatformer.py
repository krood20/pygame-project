#File firstplatformer.py

import pygame
import time

#File which contains colors
from colors import *

class Player( pygame.sprite.Sprite ):
    #Initializing the sprites
    def __init__( self, color = blue, width = 32, height = 48 ):

        super( Player, self ).__init__()

        #self.image = pygame.Surface(( width, height))
        #self.image.fill( color )

        self.image = pygame.image.load("btjump.gif").convert()

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

        self.left_viewbox = window_width/2 - window_width/8
        self.right_viewbox = window_width/2 + window_width/10

        #adjust how much you want screen to move
        self.up_viewbox = window_height/5
        self.down_viewbox = window_height/4 + window_height/12


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

class Level_01( Level ):

    def __init__( self, player_object ):

        super( Level_01, self ).__init__( player_object )
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

if(__name__ == "__main__" ):
    pygame.init()
    #Initializing the window
    window_size = window_width, window_height = 750, 600
    window = pygame.display.set_mode( window_size, pygame.RESIZABLE )

    pygame.display.set_caption("Kyle's Game")

    #FPS using clock function
    clock = pygame.time.Clock()
    frames_per_second = 100


    active_object_list = pygame.sprite.Group()
    player = Player()
    player.set_position( 40, 40 )

    active_object_list.add( player )

    level_list = []
    level_list.append( Level_01( player ) )

    current_level_number = 0
    current_level = level_list [ current_level_number ]

    player.set_level( current_level )


    message = previous_message = None

    running = True
    #keeps game window running

    while ( running ):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or ( event.type == pygame.KEYDOWN ) and ( event.key == pygame.K_ESCAPE or event.key == pygame.K_q ):
                running = False


        # Update Functions
        player.update ( current_level.object_list, event )
        event = None

        current_level.update()

        #Logic Testing
        current_level.run_viewbox()

        #Draw Everything
        current_level.draw( window )
        active_object_list.draw( window )


        #Delay Framerate
        clock.tick( frames_per_second )


        #Update Everything
        pygame.display.update()

    pygame.quit()
