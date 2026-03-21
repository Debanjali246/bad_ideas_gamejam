import pygame

class Player(pygame.Rect):
    #pygame.draw.rect(screen, color, rect)and pygame.Rect diffrece todo->dynamically find size of image and 
    # put accodingly even option toscale
    def __init__(self,gamewindow,startx,starty,fat,tall,image,RATIO):
        self.gamewindow=gamewindow
        self.startx=startx
        self.starty=starty
        playerimage=pygame.image.load(image)
        playerimage=pygame.transform.scale(playerimage,(fat,tall))
        pygame.Rect.__init__(self,startx,starty,fat,tall)

        self.image=playerimage

        if RATIO !=None:
            self.image=pygame.transform.scale_by(self.image,RATIO) 

    
        
        
        
    def move(self,speed):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x=max(0,self.x-speed)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y=min(self.y+speed,self.gamewindow.get_height()-self.height)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x=min(self.x+speed,self.gamewindow.get_width()-self.width)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y = max(self.y-speed,0)
        
    def draw(self):
        self.gamewindow.blit(self.image,(self.topleft))
"""must find some way to find x and y position to update it and 
 in rect it was as simple as rect.x nad rect.y to find x and y
 lol turns out sisnce i inherted rect so i can directly call rect.x lol 
 yahooooooo"""


    
