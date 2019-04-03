#Mouse_collisions example

self.sound = pygame.mixer.Sound( "gong.wav" )


def play_sound( self ):
    self.sound.play()


def set_image( self, filename = None ):
        if(filename != None ):

            self.image = pygame.image.load(filename)

            self.rect = self.image.get_rect()

    


    #Drawing block sprites
    block_group = pygame.sprite.Group()
    #1
    a_block = Block()

    #Replacing the block with an image
    a_block.set_image( "brick.png" )
    a_block.set_position( window_width/2-150, window_height/2-100 )

    #2
    another_block = Block( red )
    another_block.set_position( window_width/2, window_height/2+80 )

    #3
    more_block = Block( blue, 300, 20 )
    more_block.set_position( window_width/2, window_height/2+200 )

    #Adding blocks to group and drawing group
    block_group.add( more_block, another_block, a_block )




    # if you want to play sound
    #a_block.play_sound()



    collidable_objects = pygame.sprite.Group()
    collidable_objects.add( more_block, another_block )


        #final drawing of everything
        clock.tick( frames_per__second )

        window.fill( white )
        #Collision detection

        a_block.update( collidable_objects, event )
        event = None
        
        if ( pygame.sprite.collide_rect( a_block, another_block ) ):
            set_message("There is a collision!" )
        else:
            set_message( "" )
        #Message
        if ( message != previous_message ):
            set_message( message )
        
        #Drawing message
        window.blit( message, ( window_width/2 - message.get_rect().width/2, window_height/2 - 100 ))

        block_group.draw( window )
        
        pygame.display.update()


        set_message( "" )


        
    def change_speed( self, hspeed, vspeed ):
        self.hspeed += hspeed
        self.vspeed += vspeed


        def set_image( self, filename = None ):
        if ( filename != None):

            self.image = pygame.image.load( filename ).convert()
            self.set_properties()


    #Redering text
    font = pygame.font.SysFont( "Times New Roman", 30 )
