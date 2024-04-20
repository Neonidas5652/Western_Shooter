import pygame
from entity import Entity
from pathlib import Path
from pygame.math import Vector2 as v2

class Monster:
    def get_player_distance_direction(self):#gets distance and direction from monster to player
        enemy_pos = v2(self.rect.center) 
        player_pos = v2(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()#magnitude changes vector to distance
        
        if distance !=0: #needed if no collision of enemy and player
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = v2()
        return (distance,direction) #lets you get distance and direction by calling the method

    def face_player(self):
        distance, direction = self.get_player_distance_direction()

        if distance < self.notice_radius:
            if -0.5 < direction.y < 0.5: #if within notice radius
                if direction.x < 0: # player to the left
                    self.status = "left_idle"
                elif direction.x > 0: # player to the right
                    self.status = "right_idle"
            else:
                if direction.y < 0: #player to the top
                    self.status = "up_idle"
                elif direction.y > 0: #player to the bottom
                    self.status = "down_idle"

    def walk_to_player(self):
        distance, direction = self.get_player_distance_direction()
        if self.attack_radius < distance < self.walk_radius: #if inside radius, starts walking to player but if inside attack radius, stops moving so can attack
            self.direction = direction
            self.status = self.status.split("_")[0]
        else:
            self.direction = v2() #stops movement outside of radius


class Coffin(Entity, Monster):
    def __init__(self, pos, groups, collision_sprites,player):
        super().__init__(pos, groups, collision_sprites)
        #overwrites speed from parent Entity
        self.speed = 150

        #player interactions
        self.player = player #sets the actual player to the "player" parameter for interactions between the two
        self.notice_radius = 550
        self.walk_radius = 400
        self.attack_radius = 70

    def attack(self):
        distance = self.get_player_distance_direction()[0] #index 0 is the distance
        if distance < self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0
        
        if self.attacking:
            self.status = self.status.split("_")[0] + "_attack"
    
    def animate(self,dt):
        current_animation = self.animations[self.status] #current animation is set to status
        
        #damages player
        if int(self.frame_index) == 4 and self.attacking:
            if self.get_player_distance_direction()[0] < self.attack_radius:
                self.player.damage()
        
        self.frame_index += 10 * dt #cycles through frames, image files at dt for consistency
        if self.frame_index >= len(current_animation): #if frame index greater than length of amount of status images
           self.frame_index = 0 #reset frame index to 0 to restart animation
           if self.attacking: 
               self.attacking = False #resets attacking after attacking

        self.image = current_animation[int(self.frame_index)] #sets the image to the current status, and file image in that status
        self.mask = pygame.mask.from_surface(self.image)

    def take_damage(self):
        if self.health <= 0:
            self.kill()

    def update(self,dt):
        self.face_player()
        self.walk_to_player()
        self.move(dt) #move from parent Entity class

        self.attack()
        self.take_damage()
        self.vulnerability_timer()
        self.animate(dt)
        self.blink()

    def import_assets(self): #imports images for coffin
        root_dir = Path(f'../graphics/monster/coffin')
        self.animations = {}
        for path in root_dir.iterdir():
            # print(path)
            self.animations[str(path).split('\\')[-1]] = [pygame.image.load(file).convert_alpha() for file in Path(path).iterdir() if file.is_file()]

class Cactus(Entity, Monster):
    def __init__(self, pos, groups, collision_sprites,player,create_bullet):
        super().__init__(pos, groups, collision_sprites)
        self.player = player
        #overwrites speed from parent Entity
        self.speed = 100

        #player interactions
        self.player = player #sets the actual player to the "player" parameter for interactions between the two
        self.notice_radius = 600
        self.walk_radius = 500
        self.attack_radius = 350

        self.create_bullet = create_bullet
        self.bullet_shot = False

    def import_assets(self): #imports images for cactus
        root_dir = Path(f'../graphics/monster/cactus')
        self.animations = {}
        for path in root_dir.iterdir():
            # print(path)
            self.animations[str(path).split('\\')[-1]] = [pygame.image.load(file).convert_alpha() for file in Path(path).iterdir() if file.is_file()]
    
    def attack(self):
        distance = self.get_player_distance_direction()[0] #index 0 is the distance
        if distance < self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0
            self.bullet_shot = False
        
        if self.attacking:
            self.status = self.status.split("_")[0] + "_attack"

    def animate(self,dt): #animate triggers attack and damage so can't be shared, attacks at different file images
        current_animation = self.animations[self.status] #current animation is set to status
        
        
        if int(self.frame_index) == 6 and self.attacking and not self.bullet_shot: #creates bullet at proper file image of attacking
           direction = self.get_player_distance_direction()[1]
           pos = self.rect.center + direction * 80
           self.create_bullet(pos,direction)
           self.bullet_shot = True
        
        self.frame_index += 10 * dt #cycles through frames, image files at dt for consistency
        if self.frame_index >= len(current_animation): #if frame index greater than length of amount of status images
           self.frame_index = 0 #reset frame index to 0 to restart animation
           if self.attacking: 
               self.attacking = False #resets attacking after attacking
        
    

        self.image = current_animation[int(self.frame_index)] #sets the image to the current status, and file image in that status
        self.mask = pygame.mask.from_surface(self.image)

    def take_damage(self):
        if self.health <= 0:
            self.kill()

    def update(self,dt):
        self.face_player()
        self.walk_to_player()
        self.move(dt) #move from parent Entity class
        self.attack()
        self.take_damage()
        self.vulnerability_timer()
        self.animate(dt)
        self.blink()
