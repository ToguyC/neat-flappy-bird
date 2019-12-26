import pygame, os

class Bird:
    IMGS = [
        pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bird1.png'))),
        pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bird2.png'))),
        pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bird3.png')))
    ]
    MAX_ROTATION = 25 # Maximum bird tilt (in deg)
    ROT_VEL = 20 # How much the bird will rorate
    ANIMATION_TIME = 5 # How long the whole animation will durate

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0 # Current image index
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5 # Set it negative bcs the origin is in the upper-left corner
        self.tick_count = 0 # How much time ellapsed after the previous jump
        self.height = self.y
    
    def move(self):
        self.tick_count += 1

        d = (self.vel * self.tick_count) + (1.5 * (self.tick_count**2)) # Simulate the "gravity"

        if d >= 16: # Maximum speed
            d = 16
        
        # TODO tester ce que la valeur fait une fois le "jeu" fait
        if d < 0:
            d -= 2
        
        self.y += d

        if d < 0 or self.y < self.height + 50: # Y value to begin the bird tilt animation
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
        
    def show(self, win):
        self.img_count += 1
        
        # Change the bird image based on frame count (ANIMATION_TIME)
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        if self.tilt <= -80: # If the bird is almost pointing downward, just set the image
            self.img = self.IMGS[1]

        rotated_image = pygame.transform.rotate(self.img, self.tilt) # Rotate the image on the upper-left corner
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center) # Move the rotation point to the center of the image
        win.blit(rotated_image, new_rect.topleft)
        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)