import pygame
from sys import exit #exit() funtion to close game(properly #1)
clock=pygame.time.Clock() #clockobject made

HEIGHT=600 #we need to write a code to automatically find the size of
LENGTH=1000 #the screen of the player and adjust the screen size automatically i gess
FPS=60
"""we made them constant for easy to use"""

pygame.init #nothing just starting on game
#screen = pygame.display.set_mode((1000,600))
screen = pygame.display.set_mode((LENGTH,HEIGHT))

gameloop=True

while gameloop==True:
    for event in pygame.event.get():#pygame.event.get gives  all events happned in a [list] every frame (60 frame per sec) 
        if event.type == pygame.QUIT : #pygame.QUIT gives  1 if cross red is pressed 
            
            pygame.quit() #closes pygame (can do gameloop= False also dude)
            exit() #closes entire code (pygame adnpython are diff so alagse close)
        if  event.type == pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
            pygame.quit()
            exit()

    pygame.display.update() #load new screen
    clock.tick(FPS)
