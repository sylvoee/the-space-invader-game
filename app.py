
import pygame
import sys
import random


pygame.init()

screen_width = 800
screen_height = 600

cols = 5
rows = 9

# last time alien bullet ws shot 
last_alien_shot = pygame.time.get_ticks()

screen = pygame.display.set_mode((screen_width, screen_height - 10))
clock = pygame.time.Clock()


# calss spaceship
class Spaceship(pygame.sprite.Sprite):
    
    # making a constructor
    def __init__(self, position):
        # it give a clearer of the class methods
        super().__init__()
        
         #getting image
        self.image = pygame.image.load('img/sprite.svg')
        self.image = pygame.transform.smoothscale(self.image,(100, 100))
        self.rect = self.image.get_rect(center = position)
        # variable for last time short
        self.last_shot = pygame.time.get_ticks()
             

     # draw on the screen
   
       
       # get player input 
    def get_input(self):
          self.time_now = pygame.time.get_ticks()
          
          # event keys
          keys = pygame.key.get_pressed()

          if keys[pygame.K_LEFT] and self.rect.left > 0:
               self.rect.left = self.rect.left - 3

          if keys[pygame.K_RIGHT] and self.rect.right < 800:
               self.rect.left += 3     

               # short input
          if keys[pygame.K_SPACE] and self.time_now - self.last_shot > 500 :
               bullet = Bullet(self.rect.centerx, self.rect.top)
               bullet_group.add(bullet)
               
               # update the time the bullet was shot
               self.last_shot = self.time_now
        
          
     # fire up all the codes or functions  and overiding the update method           
    def update(self): 
          self.get_input()
        
        
        
 
  # making a bullet class
class Bullet(pygame.sprite.Sprite):

     # making a constructor
     def __init__(self, x,y):
          # it give a clearer of the class methods
          super().__init__()
          
          #getting image
          self.image = pygame.image.load('img/sprite.svg')
          self.image = pygame.transform.smoothscale(self.image,(10, 20))
          self.rect = self.image.get_rect()
          self.rect.center = [x, y]
          
     def bullet_kill_aliens(self):
          # killing the aliens from the bullet of the sprite
          if pygame.sprite.spritecollide(self, alien_group, True):
               # after shooting destroy the bullet
               self.kill()           
               
     
     def update(self):
          # make the bullet move upward at a speed of  5
          self.rect.y -=5
          
          # make the bullet disappear when it goes off the screen
          if self.rect.y < 0:
               self.kill() 
               
          # call the function kill bullet
          self.bullet_kill_aliens()     
          
           
         
 
 
  # making a Aliens class
class Aliens(pygame.sprite.Sprite):

     # making a constructor
     def __init__(self, x,y):
          # it give a clearer of the class methods
          super().__init__()
          
          #getting image
          self.image = pygame.image.load('img/tropy.png')
          self.image = pygame.transform.smoothscale(self.image,(30, 30))
          self.rect = self.image.get_rect()
          self.rect.center = [x, y]
          self.counter = 0
      
     def move_side(self):
          self.rect.x -= 1
          # self.rect.y += 0.25
          if(self.rect.left <= 0):
               self.rect.x = 675
               self.rect.x += 1
     
     def update(self):
          self.move_side()
          
          
          
# Making a Aliens Bullet class
class Aliens_Bullet(pygame.sprite.Sprite):
     # making a constructor
     def __init__(self, x,y):
          # it give a clearer of the class methods
          super().__init__()
          
          #getting image
          self.image = pygame.image.load('img/bullet.png')
          self.image = pygame.transform.smoothscale(self.image,(30, 30))
          self.rect = self.image.get_rect()
          self.rect.center = [x, y]
          
      # function that kills the sprite    
     def bullet_kill_sprite(self):
          if  pygame.sprite.spritecollide(self, spaceship_group, True):
               # make the bullet disappear
               self.kill()      
        
     
     def update(self):
          self.rect.y += 3
          if self.rect.top > screen_height:
               self.kill()
          
          self.bullet_kill_sprite()      
               
                      
    
          
          
 
         
        
        
#  instance of the the class Spaceship
spaceship_group  = pygame.sprite.Group() 
spaceship = Spaceship((screen_width/2, screen_height - 100))
spaceship_group.add(spaceship) 


# Making an instance of the bullet and sprite group
bullet_group = pygame.sprite.Group() 
# bullet = Bullet() 


#  instance of the the class Aliens
alien_group  = pygame.sprite.Group() 

#  instance of the the class Aliens Bullet
alien_bullet_group  = pygame.sprite.Group() 


# Creatiing  Aliens 
def create_aliens():
     for row in range(rows):
          for col in range(cols):
               alien = Aliens(115 + row * 70, 45 + col * 50 )
               alien_group.add(alien) 
     
create_aliens()             




while True:
     #  gmae backeground
     screen.fill((00, 11, 11))      
     
     # settinh time interval for alien shooting
     time_now_alien_bullet = pygame.time.get_ticks()
      
      # limit the amount of bullet that will be released
     if time_now_alien_bullet -  last_alien_shot  > 1000 and len(alien_bullet_group) < 4:
          attacking_alien = random.choice(alien_group.sprites())
          # making instance of alien bullet
          alien_bullet = Aliens_Bullet(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
          alien_bullet_group.add(alien_bullet)
          last_alien_shot = last_alien_shot
          
     
     
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
               
      
     # Draw on the screen)
     spaceship_group.draw(screen)
     
     #drw bullet
     bullet_group.draw(screen) 
     
     # draw the aliens
     alien_group.draw(screen)
    # update aliens
     alien_group.update()
     
      # update Alien Bullet
     alien_bullet_group.update()
     
      # draw the alien bullet on the screen
     alien_bullet_group.draw(screen)
    
    
     # spaceship_group.draw(screen)
     spaceship.update()
     # bullet updated as a group
     bullet_group.update()
     
     pygame.display.update()
     clock.tick(60)