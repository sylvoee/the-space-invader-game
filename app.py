
import pygame
import pygame_gui
import sys
import random
import json
import datetime



pygame.init()
      
screen_width = 800
screen_height = 600

obstacle_shot_count = 0

score = 0

latest_score= 0

cols = 5
rows = 9


obstacle_rows = 4
obstacle_cols = 8

game_on = False
bullet_destroy = False

alive = True
stage = 1

pause = False

pygame.display.set_caption('The-Space_invader')


# sounds 
alien_bull_sound = pygame.mixer.Sound('sounds/sniper-rifle-firing-shot-1-39789.mp3')
sprite_bullet = pygame.mixer.Sound('sounds/alien_bullet.mp3')
ob_distroy = pygame.mixer.Sound('sounds/obstacle_destroy.mp3')
game_intro = pygame.mixer.Sound('sounds/game_intro.mp3')

# attacking_alien = None

# MANAGER = pygame_gui.UIManager((screen_width, screen_height))
# text_input  = pygame_gui.elements.UITextEntryLine(relative_rect= ((300, 250), (300, 20)), manager= MANAGER, object_id= "#main_text_entry")


# last time alien bullet ws shot 
last_alien_shot = pygame.time.get_ticks()

# Setting the ready count down
countdown = 4
last_count = pygame.time.get_ticks()
screen = pygame.display.set_mode((screen_width, screen_height - 10))
clock = pygame.time.Clock()


# class spaceship
class Spaceship(pygame.sprite.Sprite):
    
    # making a constructor
    def __init__(self, position):
        # it give a clearer of the class methods
        super().__init__()
        
         #getting image
        self.image = pygame.image.load('img/sprite.svg')
        self.image = pygame.transform.smoothscale(self.image,(30, 50))
        self.rect = self.image.get_rect(center = position)
        # variable for last time short
        self.last_shot = pygame.time.get_ticks()
     
    def reset_spaceship(self):
         self.rect = self.image.get_rect(center = (screen_width/2, screen_height-70))
     
       
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
               # Sound
               alien_bull_sound.play()
               alien_bull_sound.set_volume(0.1)
               
               if bullet_destroy == False:
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    bullet_group.add(bullet)
                    # print(bullet_destroy)   
         
               
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
          self.image = pygame.image.load('img/bullet.svg')
          self.image = pygame.transform.smoothscale(self.image,(10, 20))
          self.rect = self.image.get_rect()
          self.rect.center = [x, y]
         
          
     def bullet_kill_aliens(self):
          # killing the aliens from the bullet of the sprite
          if pygame.sprite.spritecollide(self, alien_group, True):
               sprite_bullet.play()
               global score
               score += 1
              
               # after shooting destroy the bullet
               self.kill()
               
               
     def bullet_kill_ob(self):
          if  pygame.sprite.spritecollide(self, obstacle_group, True):
               self.kill() 
               # make the bullet disappear
               ob_distroy.play()
                   
               
               
     def destroy_alien_bullet(self):
          # killing the aliens from the bullet of the sprite
          if pygame.sprite.spritecollide(self, alien_bullet_group, True):
               self.kill()
               sprite_bullet.play()
                        
               
     
     def update(self):
          # make the bullet move upward at a speed of  5
          self.rect.y -=5 
          
          # make the bullet disappear when it goes off the screen
          if self.rect.y < 0:
               self.kill() 
               
          self.bullet_kill_ob()  
          self.bullet_kill_aliens() 
          self.destroy_alien_bullet()    
               
          
          
 
 
  # making a Aliens class
class Aliens(pygame.sprite.Sprite):

     # making a constructor
     def __init__(self, x,y):
          # it give a clearer of the class methods
          super().__init__()
          
          #getting image
          self.image = pygame.image.load(f'img/ene{random.randint(1, 4)}.svg')
          self.image = pygame.transform.smoothscale(self.image,(40, 40))
          self.rect = self.image.get_rect()
          self.rect.center = [x, y]
          self.move_counter = 0
          self.move_direction = 1
      
     def move_side(self):
         self.rect.x += self.move_direction
         self.move_counter += 1
         if abs(self.move_counter) > 75:
              self.move_direction *= -1
              self.move_counter *= self.move_direction
     
     def update(self):
          self.move_side()
          # if len(alien_group) < 2:
          #      global stage
          #      stage += 1
          #      print("Stage : " , stage)
          #      game_on = False
              
              
          
          
          
# Making a Aliens Bullet class
class Aliens_Bullet(pygame.sprite.Sprite):
     # making a constructor
     def __init__(self, x,y):
          # it give a clearer of the class methods
          super().__init__()
          
          #getting image
          self.image = pygame.image.load('img/ene_bullet.svg')
          self.image = pygame.transform.smoothscale(self.image,(5, 5))
          self.rect = self.image.get_rect()
          self.rect.center = [x, y]
          self.obstacle_shot_count = 0
          
      # function that kills the sprite    
     def bullet_kill_sprite(self):
          # check for collision with space ship
          if  pygame.sprite.spritecollide(self, spaceship_group, True):
               global alive
               alive = False
               global game_on
               # make the bullet disappear
               self.kill()
               bullet_destroy = True
               game_on = False 
               
     # collision between the alien bullet anobstacle
     def destroy_obstacle(self):
          if  pygame.sprite.spritecollide(self, obstacle_group, True):
                ob_distroy.play()    
               # make the bullet disappear
                self.kill() 
                 
               
        
     
     def update(self):
          
          self.rect.y += 2 + (stage/2)
          if self.rect.top > screen_height:
               self.kill()
          
          self.bullet_kill_sprite() 
          self.destroy_obstacle()
         
          


  # making a obstacle class
class Obstacle(pygame.sprite.Sprite):
     # making a constructor
     def __init__(self, x,y):
          # it give a clearer of the class methods
          super().__init__()
          
          #getting image
          self.image = pygame.image.load('img/ene_bomb.svg')
          self.image = pygame.transform.smoothscale(self.image,(90, 60))
          self.rect = self.image.get_rect()
          self.rect.center = [x, y]
     


               
               
#to bring in font or text
text_font = pygame.font.Font(None, 30)
text_font_big = pygame.font.Font(None, 85)
        
                    
def make_text(text, font, text_col, x ,y):
     text_surface =text_font.render(text ,None,'White')
     screen.blit(text_surface ,(x, y))   
     
     
def make_text_big(text, font, text_col, x ,y):
     text_surface =text_font_big.render(text ,None,(21, 20, 10))
     screen.blit(text_surface ,(x, y))  
     
def make_text_big2(text, font, text_col, x ,y):
     text_surface =text_font_big.render(text ,None, (133, 32, 20) )
     screen.blit(text_surface ,(x, y))                   
        
        
        
        
#  instance of the the class Spaceship
spaceship_group  = pygame.sprite.Group() 
spaceship = Spaceship((screen_width/2, screen_height - 50))
spaceship_group.add(spaceship) 


# Making an instance of the bullet and sprite group
bullet_group = pygame.sprite.Group() 
# bullet = Bullet() 


#  instance of the the class Aliens
alien_group  = pygame.sprite.Group() 

#  instance of the the class Aliens Bullet
alien_bullet_group  = pygame.sprite.Group() 


#  instance of the the class Aliens Bullet
obstacle_group  = pygame.sprite.Group() 




# Creatiing  Aliens 
def create_aliens():
     for row in range(rows):
          for col in range(cols):
               alien = Aliens(115 + row * 70, 45 + col * 50 )
               alien_group.add(alien) 
     
create_aliens() 


# Creatiing  obstacles 
def create_obstacle():
     for row in range(obstacle_rows):
          for col in range(obstacle_cols):
               obstacle = Obstacle(100 + row * 210,  460 + col *2 )
               obstacle_group.add(obstacle)
          
     
create_obstacle()


# gmae over
def game_over():
          
        game_intro.play()
        game_intro.set_volume(0.1)
        
        # getting the last score from json file
        with open('score.txt') as score_file:
             latest_score= json.load(score_file)
        
        screen.fill((133, 103, 67)) 
            # update the scree with 
       
        text_surface = text_font.render("SCORE : " f'{score}' ,None,'White')

        text_surface_message = text_font.render("Press return key to start the game",None,'White')
        text_surface_message_1 = text_font.render(f'Your Last Score {latest_score['score']}',None,'Gold')
        text_surface_message_2 = text_font.render("Space bar to shoot at Aleins",None,'White')
        text_surface_message_3 = text_font.render("Left / Right Arrow Key For Navigation",None,'White')
        
        make_text("Key 'P' to Pause ", None, 'Yellow', 200, 525)
        make_text("Key 'O' to Play", None, 'Yellow', 200, 550)
     
        if score == 0:
            
            make_text(f'Last Score : {latest_score['score']}', None, 'Yellow', 200, 222)
            make_text(f'Time : {latest_score['current_time']}', None, 'Yellow', 200, 250)
            
            make_text("Press return key to start the game", None, 'Yellow', 200, 450)
            make_text("Space bar to shoot at aliens", None, 'Yellow', 200, 475)
            
          
            
        
            screen.blit(text_surface_message_3, (200, 500)) 
        else:
             if alive == True:
               make_text_big(f'ROUND  {stage}', None, 'Yellow', 250, 200)   
                    
               screen.blit(text_surface, (50, 150));  
               screen.blit(text_surface_message, (200, 450)) 
               screen.blit(text_surface_message_2, (200, 475)) 
               screen.blit(text_surface_message_3, (200, 500)) 
             else:
                  
               make_text_big2("GAME OVER", None, 'Yellow', 220, 280)    
               played = False
               game_intro.stop()
                 
               screen.blit(text_surface, (50, 150));  
               screen.blit(text_surface_message, (200, 450)) 
               screen.blit(text_surface_message_2, (200, 475)) 
               screen.blit(text_surface_message_3, (200, 500)) 
                    
                    
               
           

 

     
              


while True:
     #  gmae backeground
     screen.fill((00, 11, 11)) 
     
     
     
     # all class update when the count is zero
     if countdown == 0 and game_on:   
     
          # settinh time interval for alien shooting
          time_now_alien_bullet = pygame.time.get_ticks()
          
          # limit the amount of bullet that will be released
          if time_now_alien_bullet -  last_alien_shot  > 1000  and len(alien_bullet_group) < 5 and len(alien_group) > 0:
               attacking_alien = random.choice(alien_group.sprites())
                    
                    # making instance of alien bullet
               alien_bullet = Aliens_Bullet(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
               alien_bullet_group.add(alien_bullet)
               last_alien_shot = last_alien_shot
                
               
               
          if len(alien_group) < 1:
               game_on = False
               stage += 1
               alive = True
               
               

          # calling the update classes       
          update_classes()
     
     # setting the ready time
     def time_count_down():
          global countdown
          global last_count
          if countdown > 0 :
               make_text('Get Ready', None, 'White', screen_width/2 -100, screen_height/2)
               make_text(f'{countdown}', None, 'White', screen_width/2 - 65, screen_height/2 + 30 )     
               
               current_time = pygame.time.get_ticks()
               if current_time - last_count > 1000 :
                    countdown -= 1
                    last_count = current_time
                    
               
     time_count_down()     
     
     def update_classes():
          
          if game_on == True and pause == False:
               # update aliens
               alien_group.update()
               
               # update Alien Bullet
               alien_bullet_group.update()
               
               # spaceship_group.draw(screen)
               spaceship.update()
               
               # bullet updated as a group
               bullet_group.update()
               
               # bullet updated as a group
               obstacle_group.update()
               
          if game_on == True and pause == True:
               make_text("PAUSED", None, 'Yellow', 350, 275)     
           
               
          
     # Draw on the screen)
     spaceship_group.draw(screen)
     
     #drw bullet
     bullet_group.draw(screen) 
     
     # draw the aliens
     alien_group.draw(screen)
     
     
     # draw the obstacle group
     obstacle_group.draw(screen)
     
     # draw the alien bullet on the screen
     alien_bullet_group.draw(screen)
     
     make_text(f'Score : {score}', None, 'White', screen_width/2- 65 , 50 )
     
     current_time = datetime.datetime.now()
     
     score_data = {
          "score" : score,
          "current_time" : f'{current_time}'
     } 
     
     
     
     
     if game_on == False:
          game_over()
     
     
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               
               # write the score in a file
               with open('score.txt', 'w') as score_file :
                    json.dump(score_data, score_file )
               
               pygame.quit()
               sys.exit()
               
          if event.type == pygame.KEYDOWN:
               # to pause the game
               if event.key == pygame.K_p:
                    if pause == False:
                         pause = True 
                        
                    make_text("PAUSED", None, 'Yellow', 300, 275)
               
               if event.key == pygame.K_o:
                    # to continue the game
                    if pause == True:
                         pause = False           
                      
               
               if event.key == pygame.K_RETURN:
                         
                    if alive == True :
                         #  reset sprite group
                         spaceship_group = pygame.sprite.Group()
                         spaceship = Spaceship((screen_width/2, screen_height -50)) 
                         spaceship_group.add(spaceship)
                         spaceship_group.draw(screen)
                         spaceship_group.update()
                         
                         #  instance of the the class Aliens 
                         alien_group  = pygame.sprite.Group() 
                         alien_group.update()
                         create_aliens()
                         
                         obstacle_group = pygame.sprite.Group()
                         obstacle_group.update()
                         create_obstacle()
                         
                         alien_bullet = Aliens_Bullet(30, 30)
                         alien_bullet_group = pygame.sprite.Group()
                         alien_bullet_group.draw(screen)
                         alien_bullet_group.update()
                         
                         bullet_group = pygame.sprite.Group()
                         bullet = Bullet(0, 0)
                         bullet_group.add(bullet)
                         bullet_group.draw(screen)
                         bullet.update()
                         
                    
                         game_on = True
                        
                         
                    else:
                         #  reset sprite group
                         spaceship_group = pygame.sprite.Group()
                         spaceship = Spaceship((screen_width/2, screen_height -50)) 
                         spaceship_group.add(spaceship)
                         spaceship_group.draw(screen)
                         spaceship_group.update()
                         
                         #  instance of the the class Aliens 
                         alien_group  = pygame.sprite.Group() 
                         alien_group.update()
                         create_aliens()
                         
                         obstacle_group = pygame.sprite.Group()
                         obstacle_group.update()
                         create_obstacle()
                         
                         alien_bullet = Aliens_Bullet(30, 30)
                         alien_bullet_group = pygame.sprite.Group()
                         alien_bullet_group.draw(screen)
                         alien_bullet_group.update()
                         
                         bullet_group = pygame.sprite.Group()
                         bullet = Bullet(0, 0)
                         bullet_group.add(bullet)
                         bullet_group.draw(screen)
                         bullet.update()
                         
                         score = 0 
                         game_on = True
                         stage = 1
                              
                         
                              
                         # register manager  
               #           MANAGER.process_events(event)
          
               # # update manager
               # MANAGER.update(clock.tick(60) /1000)
          

     pygame.display.update()
     clock.tick(60)