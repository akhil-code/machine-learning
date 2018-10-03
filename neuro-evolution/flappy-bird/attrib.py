from numpy import random
from math import floor
import pygame

def do_overlap(rect1, rect2):
    l1, r1 = rect1.topleft, rect1.bottomright
    l2, r2 = rect2.topleft, rect2.bottomright
    # condition to not overlap
    if r1[0] < l2[0] or r2[0] < l1[0]:
        return False
    if r2[1] < l1[1] or r1[1] < l2[1]:
        return False

    return True

class Color:
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    WHITE = (255,255,255)
    YELLOW = (255,255,0)
    BLACK = (0,0,0)

class Screen:
    WIDTH = 640             # width of screen
    HEIGHT = 480            # height of screen
    FRAME_RATE = 120        # FPS
    FRAMES = 0              # counts number of frames elapsed
    TITLE = 'Flappy bird'   # Window Title
    EXIT = False            # Flag to exit the game
    GAME_OVER = False       # Flag to denote if it's game over
    ICON_PATH = 'res/icon.jpg'

    # initializes required objects required for game
    def initialize():
        pygame.init()

        # screen parameters
        icon = pygame.image.load(Screen.ICON_PATH)
        pygame.display.set_icon(icon)
        pygame.display.set_caption(Screen.TITLE)
        screen = pygame.display.set_mode(Screen.get_dimensions())
        
        # reference clock
        clock = pygame.time.Clock()
        
        # initializing game objects
        bird = Bird()
        pipes = []

        return screen, clock, bird, pipes

    def get_dimensions():
        return (Screen.WIDTH, Screen.HEIGHT)
    
    def draw_screen(screen, bird, pipes):
        Screen.FRAMES += 1
        screen.fill(Color.BLACK)

        # draw bird
        pygame.draw.circle(screen, Color.WHITE, bird.get_center(), bird.radius)

        for pipe in pipes:
            upper_rect, lower_rect = pipe.get_pipe_rects()
            pygame.draw.rect(screen, Color.WHITE, upper_rect)
            pygame.draw.rect(screen, Color.WHITE, lower_rect)
        
        # update whole screen
        pygame.display.update()
    
    def update_objects(bird, pipes):
        if len(pipes) > 0:
            # add new pipe if possible
            last_pipe = pipes[-1]
            if last_pipe.posx + Pipe.width + Pipe.space_between_pipes < Screen.WIDTH:
                pipes.append(Pipe())

            # remove first pipe if it stripes away from screen
            first_pipe = pipes[0]
            if first_pipe.posx + Pipe.width < 0:
                del pipes[0]
        else:
            # add new pipe
            pipes.append(Pipe())

        # update each of pipe object
        for pipe in pipes:
            pipe.update() 
                   
        # update bird object
        bird.update()

        # check if bird hits the pipes
        for pipe in pipes:
            upper_rect, lower_rect = pipe.get_pipe_rects()
            bird_rect = bird.get_rect()
            if do_overlap(bird_rect, upper_rect) or do_overlap(bird_rect, lower_rect):
                Screen.GAME_OVER = True 

    def loop(screen, clock, bird, pipes):
        while not Screen.EXIT:
            # objects updated for each frame
            Screen.update_objects(bird, pipes)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Screen.EXIT = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        bird.fly()
            if Screen.GAME_OVER:
                print("game over")
            Screen.draw_screen(screen, bird, pipes)
            clock.tick(Screen.FRAME_RATE)


class Bird:
    ANIMATION_RATE = 5      # animates for every 5 elapsed frames
    def __init__(self):
        self.radius = 15
        self.width = self.radius*2
        self.height = self.radius*2
        self.posx = 0
        self.posy = 0
        # gravitation parameters
        self.velocity = 0
        self.gravity = 0.08

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
            # updating position and velocity based on equations of motion
            self.posy += floor((u*t) + (0.5*(a*t*t)))
            self.velocity = u + a*t
            # if bird goes above the screen
            if self.posy < 0:
                self.posy = 0
            # if it goes below the screen
            elif self.posy + self.height > Screen.HEIGHT:
                self.posy = Screen.HEIGHT - self.height
            # stores the instant, when updated
            self.last_update = Screen.FRAMES
    
    def fly(self):
        self.velocity = -3      # impulsive velocity in upward direction
    
    def get_rect(self):
        return pygame.rect.Rect(self.posx, self.posy, self.width, self.height)


class Pipe:
    gap_width = 125             # vertical gap between two pipes
    width = 30                  # width of each pipe
    space_between_pipes = 350   # space between two adjacent pipes
    stepx = 5                   # pipes move in x direction by 5px
    ANIMATION_RATE = 5          # animates after every 5th frame

    def __init__(self):
        # space between two vertical pipes is denoted as gap
        self.gap_start = random.randint(0, high=Screen.HEIGHT - Pipe.gap_width)
        self.gap_end = self.gap_start + Pipe.gap_width
        self.posx = Screen.WIDTH
        # stores the latest instant when updated
        self.last_update = 0
    
    def update(self):
        t = Screen.FRAMES - self.last_update
        if t > Pipe.ANIMATION_RATE:
            self.posx -= Pipe.stepx
            self.last_update = Screen.FRAMES
    
    def get_pipe_rects(self):
        # upper pipe
        pipe_position = (self.posx, 0)
        pipe_dimensions = (self.width, self.gap_start)
        upper_rect = pygame.Rect(pipe_position, pipe_dimensions)
        
        # lower pipe
        pipe_position = (self.posx, self.gap_end)
        pipe_dimensions = (self.width, Screen.HEIGHT - self.gap_end)
        lower_rect = pygame.Rect(pipe_position, pipe_dimensions)

        return upper_rect, lower_rect


