import pygame
from sys import exit #exit() funtion to close game(properly #1)
from player import Player
from backgd import Background
from stuff import Stuff
import os 
BASE_DIR = os.path.dirname(__file__)
clock=pygame.time.Clock() #clockobject made

HEIGHT=600 #we need to write a code to automatically find the size of
LENGTH=1000 #the screen of the player and adjust the screen size automatically i gess
FPS=24
PLAYER_FAT=32
PLAYER_HEIGHT=32
PLAYER_X=150
PLAYER_Y=150
PLAYER_SPEED=20
BLOCKSIZE=32 #must take h and w if make non square blocks
ICON = pygame.image.load(os.path.join(BASE_DIR, "enemies", "CatBasket.png"))
"""we made them constant for easy to use"""

pygame.init #nothing just starting on game
#screen = pygame.display.set_mode((1000,600))
screen = pygame.display.set_mode((LENGTH,HEIGHT))
pygame.display.set_caption("we are on the box")

pygame.display.set_icon(ICON)


world = Background(screen,(69,69,69),os.path.join(BASE_DIR, "background", "realbg.jpeg"))
#world=Background(screen,(69,69,69),None)
""" object=pygame.Rect(300,400,32,32)
    pygame.draw.rect(screen,(0,250,250),object,0,1,100,-50,90,1110)
    test code to undersatnt Rect and rect
"""
gameloop=True
object=pygame.Rect(300,400,32,32)
cat=Stuff(screen,LENGTH-((BLOCKSIZE)*6),HEIGHT-(BLOCKSIZE+BLOCKSIZE+25),BLOCKSIZE,BLOCKSIZE,os.path.join(BASE_DIR, "enemies", "CatBasket.png"),2,None)
#define player and objects(for now object and plaer both by player class)
tom=Player(screen,PLAYER_X,PLAYER_Y,PLAYER_FAT,PLAYER_HEIGHT,os.path.join(BASE_DIR, "enemies", "CatBasket.png"),1)
floor=[]
for i in range(0,LENGTH,BLOCKSIZE):
    jerry=Stuff(screen,i,HEIGHT-BLOCKSIZE,32,32,os.path.join(BASE_DIR, "lands", "forestland.jpeg"))
    floor.append(jerry)

while gameloop==True:
        
   
    world.draw()  
    tom.draw()
    cat.draw()
    for i in floor:
        i.draw()
    

    for event in pygame.event.get():#pygame.event.get gives  all events happned in a [list] every frame (60 frame per sec) 
        if event.type == pygame.QUIT : #pygame.QUIT gives  1 if cross red is pressed 
            
            pygame.quit() #closes pygame (can do gameloop= False also dude)
            exit() #closes entire code (pygame adnpython are diff so alagse close)
        if  event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
            pygame.quit()
            exit()
    tom.move(PLAYER_SPEED)
    
    
        
    pygame.draw.rect(screen,(0,250,250),object,0,1,100,-50,90,1110)
    pygame.display.update() #load new screen
    clock.tick(FPS)
