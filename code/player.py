import pygame
from pygame.math import Vector2 as v2
from settings import *
from entity import Entity
from pathlib import Path
# from debug import debug

class Player(Entity):
    def __init__(self, pos, groups, collision_sprites, create_bullet):
        super().__init__(pos, groups, collision_sprites)
        self.create_bullet = create_bullet
        self.bullet_shot = False

    def import_assets(self): #imports images for player
        entity = ["player","coffin","cactus"]
        root_dir = Path(f'../graphics/{entity[0]}')
        self.animations = {}
        for path in root_dir.iterdir():
            # print(path)
            self.animations[str(path).split('\\')[-1]] = [pygame.image.load(file).convert_alpha() for file in Path(path).iterdir() if file.is_file()]

    def animate(self,dt): #dt always when moving anything
       current_animation = self.animations[self.status] #current animation is set to status
       
       self.frame_index += 10 * dt #cycles through frames, image files at dt for consistency
       
       if self.frame_index >= len(current_animation): #if frame index greater than length of amount of status images
           self.frame_index = 0 #reset frame index to 0 to restart animation
           if self.attacking: 
               self.attacking = False #resets attacking after attacking
       
       if int(self.frame_index) == 2 and self.attacking and not self.bullet_shot: #creates bullet at proper file image of attacking
           bullet_offset = self.rect.center + self.bullet_direction * 80 #creates bullet to line up with gun, not inside player itself
           self.create_bullet(bullet_offset,self.bullet_direction)
           self.bullet_shot = True
       if self.status == "down_attack" and self.attacking and not self.bullet_shot:
            bullet_offset = self.rect.center + (self.bullet_direction + (-20,80)) #changing vector x,y alligns bullet to the gun when facing up or down
            self.create_bullet(bullet_offset,self.bullet_direction)
            self.bullet_shot = True
       if self.status == "up_attack" and int(self.frame_index) == 2 and not self.bullet_shot:
            bullet_offset = self.rect.center + self.bullet_direction + (30,-40) #alligns bullet to the gun when facing up or down
            self.create_bullet(bullet_offset,self.bullet_direction)
            self.bullet_shot = True 
            
           
       

       self.image = current_animation[int(self.frame_index)] #sets the image to the current status, and file image in that status
       self.mask = pygame.mask.from_surface(self.image)

    def input(self):
        
        keys = pygame.key.get_pressed()
        if not self.attacking: #if not attack, can move
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            else:
                self.direction.x = 0

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.direction = v2() #stops movement when attacking
                self.frame_index = 0 #resets attack animation no matter where moving frame is
                self.bullet_shot = False

                match self.status.split("_")[0]:
                    case "left": self.bullet_direction = v2(-1,0)
                    case "right": self.bullet_direction = v2(1,0)
                    case "up": self.bullet_direction = v2(0,-1)
                    case "down": self.bullet_direction = v2(0,1)
            # print(self.status)

                # self.bullet_direction

    def get_status(self): #necessary for animation
        #idle status
        if self.direction.x == 0 and self.direction.y == 0: #if not moving
            self.status = self.status.split('_')[0] + "_idle" #takes status splits at _ (down_idle), returns only down part then adds idle
        
        if self.attacking: #if attacking
            self.status = self.status.split('_')[0] + "_attack" #takes status, splits at _ (down_idle), returns only down, adds attack

    def update(self,dt):
        self.input()
        self.get_status()
        # debug(self.status)
        self.move(dt)
        self.animate(dt)
        self.blink( )
        # self.collision(None)
        self.vulnerability_timer()
        print(self.health)