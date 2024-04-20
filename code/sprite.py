from typing import Any
import pygame

class Sprite(pygame.sprite.Sprite): #creates sprite objects for tiles, etc
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf #surf is from surf in tmx_map setup()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-self.rect.height *0.3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos,direction,surf,groups):
        super().__init__(groups)

        self.image = surf #passed the surf from the class
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = pos)
        
        #float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = direction #passed the direction from the class
        self.speed = 400

    def update(self,dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x),round(self.pos.y))