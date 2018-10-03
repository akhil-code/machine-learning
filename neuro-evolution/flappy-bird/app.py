import pygame

from attrib import Bird, Color, Pipe, Screen


def main():
    # initialize game screen
    screen, clock, bird, pipes = Screen.initialize()
    Screen.loop(screen, clock, bird, pipes)

if __name__ == '__main__':
    main()
    pygame.quit()
