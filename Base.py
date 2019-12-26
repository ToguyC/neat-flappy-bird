import pygame, os

class Base:
    VEL = 5
    BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'base.png')))
    WIDHT = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDHT

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # Move the image behind the previous image if the (x + widht) value goes out of the screen
        if self.x1 + self.WIDHT < 0:
            self.x1 = self.x2 + self.WIDHT

        if self.x2 + self.WIDHT < 0:
            self.x2 = self.x1 + self.WIDHT

    def show(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))