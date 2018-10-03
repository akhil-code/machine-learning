from numpy import random
from math import floor
import pygame

class Color:
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    WHITE = (255,255,255)
    YELLOW = (255,255,0)
    BLACK = (0,0,0)

class Screen:
    WIDTH = 640
    HEIGHT = 480
    FRAME_RATE = 120
    FRAMES = 0              # counts number of frames elapsed
    TITLE = 'Flappy bird'
    EXIT = False
    GAME_OVER = False

    def initialize():
        pygame.init()
        pygame.display.set_caption(Screen.TITLE)
        screen = pygame.display.set_mode(Screen.get_dimensions())

        Pipe.pipes_on_screen = floor(Screen.WIDTH/(Pipe.width+Pipe.space_between_pipes))
        print(Pipe.pipes_on_screen)

        return screen

    def get_dimensions():
        return (Screen.WIDTH, Screen.HEIGHT)
    
    def draw_screen(screen, bird, pipes):
        Screen.FRAMES += 1
        screen.fill(Color.BLACK)

        for pipe in pipes:
            # draw bird
            pygame.draw.circle(screen, Color.WHITE, bird.get_center(), bird.radius)
            # draw upper pipe
            pipe_position = (pipe.posx, 0)
            pipe_dimensions = (pipe.width, pipe.gap_start)
            rect = pygame.Rect(pipe_position, pipe_dimensions)
            pygame.draw.rect(screen, Color.WHITE, rect)
            # draw lower pipe
            pipe_position = (pipe.posx, pipe.gap_end)
            pipe_dimensions = (pipe.width, Screen.HEIGHT - pipe.gap_end)
            rect = pygame.Rect(pipe_position, pipe_dimensions)
            pygame.draw.rect(screen, Color.WHITE, rect)
        # update whole screen
        pygame.display.update()
    
    def update_objects(bird, pipes):
        
        if len(pipes) == 0:
            pipes.append(Pipe())
        else:
            # add new pipe if possible
            last_pipe = pipes[-1]
            if last_pipe.posx + Pipe.width + Pipe.space_between_pipes < Screen.WIDTH:
                pipes.append(Pipe())
            
            # remove first pipe if it stripes away from screen
            first_pipe = pipes[0]
            if first_pipe.posx + Pipe.width < 0:
                del pipes[0]

        for pipe in pipes:
            pipe.update()        

        bird.update()


class Bird:
    ANIMATION_RATE = 5      # animates for every 5 elapsed frames
    def __init__(self):
        self.radius = 15
        self.width = self.radius*2
        self.height = self.radius*2
        self.posx = 0
        self.posy = 0

        self.velocity = 0
        self.gravity = 0.05

        self.last_update = 0

    def get_center(self):
        x = self.posx + self.radius
        y = self.posy + self.radius
        return (x,y)
    
    def update(self):
        t = Screen.FRAMES - self.last_update
        if t > Bird.ANIMATION_RATE:
            u = self.velocity
            a = self.gravity
            s = self.posy

            self.posy += floor((u*t) + (0.5*(a*t*t)))
            self.velocity = u + a*t
            if self.posy < 0:
                self.posy = 0
            elif self.posy + self.height > Screen.HEIGHT:
                self.posy = Screen.HEIGHT - self.height
            
            
            self.last_update = Screen.FRAMES
    
    def fly(self):
        self.velocity = -2


class Pipe:
    gap_width = 100
    width = 30
    space_between_pipes = 350
    pipes_on_screen = None
    stepx = 5
    ANIMATION_RATE = 5

    def __init__(self):
        self.gap_start = random.randint(0, high=Screen.HEIGHT - Pipe.gap_width)
        self.gap_end = self.gap_start + Pipe.gap_width
        self.posx = Screen.WIDTH
        self.last_update = 0
    
    def update(self):
        t = Screen.FRAMES - self.last_update
        if t > Pipe.ANIMATION_RATE:
            self.posx -= Pipe.stepx
            self.last_update = Screen.FRAMES


