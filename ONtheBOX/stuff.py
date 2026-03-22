import pygame

class Stuff(pygame.Rect):
    def __init__(self,gamewindow,startx,starty,fat,tall,image=None,RATIO=None,colour=None):
        pygame.Rect.__init__(self,startx,starty,fat,tall)
        self.gamewindow=gamewindow
        self.image=None
        self.colour=None

        if image!=None:
            playerimage=pygame.image.load(image)
            playerimage=pygame.transform.scale(playerimage,(fat,tall))
            self.image=playerimage
        elif colour!=None:
            self.colour=colour
            self.image = pygame.Surface((fat, tall))
        if RATIO !=None :
                self.image=pygame.transform.scale_by(self.image,RATIO) 
            

    
    def draw(self):
        self.gamewindow.blit(self.image,(self.topleft))

    
