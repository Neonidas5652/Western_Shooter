import pygame
from pygame.math import Vector2 as v2
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.import_assets() #
        self.status = "down" # Necessary for animation
        self.frame_index = 0 #

        self.image = self.animations[self.status][self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = pos)

        #float based movement
        self.pos = v2(self.rect.center) #starting position should be center of rect
        self.direction = v2()
        self.speed = 300 

        #collisions                    #self.rect.width bit below reduces hitbox slightly from rect so closer collisions
        self.hitbox = self.rect.inflate(-self.rect.width * 0.3,-self.rect.height *0.3) #creates hitbox smaller for damage collisions
        self.collision_sprites = collision_sprites #whatever in parameter above storeed in self.colisions etc
        
        
        #attacking
        self.attacking = False

        #health
        self.health = 3
        self.is_vulnerable = True
        self.hit_time = None

    def blink(self): #creates white mask on the surface of Entities when hit to simulate damage taken
        if not self.is_vulnerable: #if hit and not vulnerable
            if self.wave(): #and during the wave space
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey("black") #blink surface back and forth
                self.image = white_surf

    def wave(self): #makes blink animation
        value = sin(pygame.time.get_ticks()) #sin value go between 1 and -1, but never hitting either
        if value >= 0:
            return True
        else:
            False

    def damage(self):

        if self.is_vulnerable:
            self.health -=1
            self.is_vulnerable = False
            self.hit_time = pygame.time.get_ticks()
    
    def vulnerability_timer(self):
        if not self.is_vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > 400:
                self.is_vulnerable = True

    def move(self,dt):
         #normalize speed when moving diaganal
        if self.direction.magnitude() != 0: #magnitude means length, as in the length of the direction
            self.direction = self.direction.normalize()

        #horizontal movement and collision
        self.pos.x += self.direction.x * self.speed * dt #moves the x pos of image itself, the surface
        self.hitbox.centerx = round(self.pos.x) #collision pos - moves the hitbox center x position by the rounded position of the image
        self.rect.centerx = self.hitbox.centerx #drawing pos - moves the image rect to same pos of hitbox
        # self.mask = pygame.mask.from_surface(self.image)
        self.collision("horizontal") #after movement calls collision and makes it horizontal to have accurate collisons in method below
                                                #COLLISION AND DRAWING MUST BE SAME POS
        

        #vertical movement and collision
        self.pos.y += self.direction.y * self.speed * dt #moves the y pos
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        # self.mask = pygame.mask.from_surface(self.image)
        self.collision("vertical")
    
    def collision(self,direction):
        for sprite in self.collision_sprites.sprites():
            if self.hitbox.colliderect(sprite.hitbox): #if sprite hitbox collides with player hitbox
                if direction == "horizontal":
                    if self.direction.x > 0: #if moving right
                        self.hitbox.right = sprite.hitbox.left #if player hits on right, moves to objects left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx #updates the rect to the hitbox that is moved due to collision
                    # self.mask = pygame.mask.from_surface(self.image)
                    self.pos.x = self.hitbox.centerx #updates pos to the same

                else: #vertical movement
                    if self.direction.y < 0: #moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0: #moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    self.rect.centery = self.hitbox.centery
                    # self.mask = pygame.mask.from_surface(self.image)
                    self.pos.y = self.hitbox.centery