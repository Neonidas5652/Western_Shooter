import pygame, sys
from pygame.math import Vector2 as v2
from settings import *
from player import Player
from sprite import Sprite, Bullet
from pytmx.util_pygame import load_pygame #needed to import Tiled info
from monster import Coffin, Cactus
# from debug import debug

#creates camera
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__() #creates it as a normal Group
        self.offset =v2()
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load('../graphics/other/bg.png').convert()
    
    def customize_draw(self,player): #putting player in here makes it not in global scope, modular

        #changing offset vector to follow character movement
        self.offset.x = player.rect.centerx - WINDOW_WIDTH/2 #offset moves all other assets in oppositve direction of player to simulate movement
        self.offset.y = player.rect.centery - WINDOW_HEIGHT/2

        #blit background first so other things drawn on top of it
        self.display_surface.blit(self.bg,-self.offset) #negative offset to move camera correctly
        #blit sprites inside of the group (player)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): #sorted lambda bit creates depth of images
            #sets camera to the sprites in the group (player)
            offset_rect = sprite.image.get_rect(center = sprite.rect.center) #sets offset rect to sprite rect  
            offset_rect.center -= self.offset #moves camera in oppostive of sprite
            self.display_surface.blit(sprite.image,offset_rect) #draws all the sprites (player, etc)

class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption("Wild West Shierff Shootout")
        self.clock = pygame.time.Clock()
        self.bullet_surf = pygame.image.load("../graphics/other/particle.png").convert_alpha()

        #groups
        # self.all_sprites = pygame.sprite.Group()
        self.all_sprites = AllSprites() #does the same as above, after AllSprites class is made to change standard Group
        self.obstacles = pygame.sprite.Group() #group for collisions
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group() #group for monster for collisions, must be passed in lines 90,92 when getting coffin/cactus image info
        
        self.setup() 

    def create_bullet(self,pos,direction):
        Bullet(pos,direction,self.bullet_surf,[self.all_sprites,self.bullets])

    def bullet_collision(self):
        #bullet obstacle collision
        for obstacle in self.obstacles.sprites():
            pygame.sprite.spritecollide(obstacle,self.bullets,True,pygame.sprite.collide_mask)

        #bullet monster collision and damage
        for bullet in self.bullets.sprites():
            sprites = pygame.sprite.spritecollide(bullet,self.monsters,False, pygame.sprite.collide_mask)
            if sprites:
                bullet.kill()
                for sprite in sprites:
                    sprite.damage()


        #bullet player collision and damage
        if pygame.sprite.spritecollide(self.player,self.bullets,True, pygame.sprite.collide_mask):
            self.player.damage()



    def setup(self): #calls in Tiled info
        tmx_map = load_pygame("../data/map.tmx")
        
        #ground tiles
        # for x,y,surf in tmx_map.get_layer_by_name("Cliffs").tiles():
        #     Sprite((x * 64, y * 64),surf,self.all_sprites)

        #objects
        for obj in tmx_map.get_layer_by_name("Objects"): #two groups below, each sprite is in both, for drawing/animation and obstacle collisions
            Sprite((obj.x,obj.y),obj.image,[self.all_sprites,self.obstacles])
            
        #tiles
        for x,y,surf in tmx_map.get_layer_by_name("Fence").tiles(): #calls tile info from "Fence layer" - x,y cords and the surf itself
            Sprite((x * 64, y * 64),surf,[self.all_sprites,self.obstacles]) #multiples x,y by 64 because Tiled tiles are 64 pixels big

        #entities
        for obj in tmx_map.get_layer_by_name("Entities"):
            if obj.name == "Player": #player needs pos, a group its in, and group to collide with
                self.player = Player(
                    pos=(obj.x,obj.y),
                    groups=self.all_sprites, 
                    collision_sprites=self.obstacles,
                    create_bullet = self.create_bullet) #sets player to Player class/Group to call alter in function
            if obj.name == "Coffin":
                Coffin((obj.x,obj.y), [self.all_sprites,self.monsters], self.obstacles, self.player) #self.player here allows Coffin/Cactus to interact with player
            if obj.name == "Cactus":
                Cactus((obj.x,obj.y), [self.all_sprites,self.monsters], self.obstacles, self.player,self.create_bullet)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if True:
                    pygame.mouse.set_visible(False)
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        pygame.quit()
                        sys.exit()

            dt = self.clock.tick() / 1000 
            #update groups
            self.all_sprites.update(dt)
            self.bullet_collision()

            #draw groups
            self.display_surface.fill("black") #draws bg before sprites for clear movement
    
            self.all_sprites.customize_draw(self.player)
            # for sprite in self.monsters.sprites():
            #     pygame.draw.rect(self.display_surface,"green",sprite.rect,1)
          

            pygame.display.update()

if __name__ == '__main__': #checks if the name of the file is "main" to run code, cleaner
    game = Game()
    game.run()