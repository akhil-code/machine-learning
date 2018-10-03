import pygame

from attrib import Bird, Color, Pipe, Screen


def main():
    # initialize game screen
    screen = Screen.initialize()
    
    # reference clock
    clock = pygame.time.Clock()

    # initializing game objects
    bird = Bird()
    pipes = []

    while not Screen.EXIT:
        # objects updated for each frame
        Screen.update_objects(bird, pipes)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Screen.EXIT = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    bird.fly()

        Screen.draw_screen(screen, bird, pipes)
        clock.tick(Screen.FRAME_RATE)


if __name__ == '__main__':
    main()
    pygame.quit()
