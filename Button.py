import pygame
from constants_for_game import screen,font
class Button(pygame.sprite.Sprite):
    def __init__(self,text,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.top_rect = pygame.Rect(x, y, width, height)
        self.top_color = '#475F77'
        self.text_surf = font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center) 

    def draw(self):
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.top_rect, 2, border_radius=10)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, pos):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
        else:
            self.top_color = '#475F77'
        return self.top_rect.collidepoint(pos)