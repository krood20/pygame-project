
import pygame

if __name__ == '__main__':

    pygame.init()
    blue1 = (65,164,255)

    window_size = width, height = 1250, 700
    window = pygame.display.set_mode(window_size)

    white = pygame.Color(255,255,255)
    red = pygame.Color(255,0,0)
    black = pygame.Color(0,0,0)


    clock = pygame.time.Clock()
    fps = 60

    to_draw = []

    draw_start_box = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = mouse_x, mouse_y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = mouse_pos
                draw_start_box = True

            if event.type == pygame.MOUSEBUTTONUP:
                final_pos = mouse_pos
                draw_start_box = False

                rect = pygame.Rect(pos, (final_pos[0]-pos[0], final_pos[1]-pos[1]))
                rect.normalize()

                to_draw += [ rect ]


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for platform in to_draw:
                        print'['+str(platform).split('(')[1].split(')')[0]+', black],'

                if event.key == pygame.K_BACKSPACE:
                    to_draw.pop()



        window.fill(white)
        if draw_start_box:
            pygame.draw.rect(window,red,pygame.Rect(pos,(mouse_pos[0]-pos[0], mouse_pos[1]-pos[1])))

        for item in to_draw:
            pygame.draw.rect(window, black, item)


        pygame.display.update()

        clock.tick(fps)
    pygame.quit()
