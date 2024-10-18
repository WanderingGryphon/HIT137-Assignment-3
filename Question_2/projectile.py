import pygame
import os

class Projectile:
    def __init__(self, x, y, direction):
        # Initialize projectile attributes
        self.x = x
        self.y = y - 20  # Adjust y position for projectile origin
        self.direction = 1  # Default direction
        self.vel = 10 * direction  # Velocity based on direction
        self.width = 30
        self.height = 30
        # Load projectile images
        self.images = [pygame.image.load(os.path.join('images', f'Bullet_00{i}.png')) for i in range(1, 2)]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def update_image(self):
        # Update projectile image for animation
        self.image_index = (self.image_index + 1) % len(self.images)
        self.image = self.images[self.image_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
