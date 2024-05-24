from   import         #حط اسم ال file
from   import
import  

class game:
    def      (self):                 #حط اسم الfunction
       self.score=0
    

def update_score(self, lines_cleared,move_down_points):
    if lines_cleared == 1:
        self.score+= 100
    elif lines_cleared ==2:
        self.score+=300
    elif lines_cleared ==3:
           self.score+=500
    self.score += move_down_points       





#ده فى ال lock block
rows_cleared=self.grid.clear_full_block()   
self.update_score(rows_cleared,0)


def   (self):        #دى بتاعت الreset
self.score=0



#ده فى فايل الmain 
game.update_score(0,1)    #تحت الkey down




#  تحت ال drawing
score_value_surface = title_font.render(str(game.score), true ,colors.white)

#pygame.draw.rect تحتها 
screen.blit(score_value_surface,score_value_surface.get_rect(centerx =score_rect.centerx,
                                                             centery =score_rect.centery))
