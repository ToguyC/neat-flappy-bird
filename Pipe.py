import pygame, os, random

class Pipe:
    GAP = 200
    VEL = 5 # Moving speed
    PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'pipe.png')))

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0

        self.PIPE_BOTTOM = self.PIPE_IMG
        self.PIPE_TOP = pygame.transform.flip(self.PIPE_IMG, False, True)
        
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height() # Get the top height of the gap
        self.bottom = self.height + self.GAP # Get the bottom height of the gap

    def move(self):
        self.x -= self.VEL

    def show(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # How far away the pipe masks and the bird mask are
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset) # If not colliding, return None
        t_point = bird_mask.overlap(top_mask, top_offset) # If not colliding, return None

        if t_point or b_point:
            return True
        else:
            return False
