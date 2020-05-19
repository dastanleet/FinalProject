import rofl1
import rabbit
# import ai
import pygame
from pygame.locals import *


class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x, y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length // len(text))
        myFont = pygame.font.SysFont("Calibri", font_size + 10)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText,
                     ((x + length // 2) - myText.get_width() // 2, (y + height // 2) - myText.get_height() // 2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):
        for i in range(1, 10):
            s = pygame.Surface((length + (i * 2), height + (i * 2)))
            s.fill(color)
            alpha = (255 / (i + 2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x - i, y - i, length + i, height + i), width)
            surface.blit(s, (x - i, y - i))
        pygame.draw.rect(surface, color, (x, y, length, height), 0)
        pygame.draw.rect(surface, (190, 190, 190), (x, y, length, height), 1)
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:

                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


pygame.init()


def main():
    main_screen = pygame.display.set_mode((800, 600))
    main_surface = pygame.Surface((800, 600))
    button1 = Button()
    button2 = Button()
    button3 = Button()

    main_screen = button1.create_button(main_screen, (255, 0, 0), 340, 95, 100, 50, 2, 'SINGLE PLAYER', (255, 255, 255))
    main_screen = button2.create_button(main_screen, (255, 0, 0), 340, 160, 100, 50, 2, 'MULTI PLAYER', (255, 255, 255))
    main_screen = button3.create_button(main_screen, (255, 0, 0), 340, 220, 100, 50, 2, 'AI MODE', (255, 255, 255))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if button1.pressed(pygame.mouse.get_pos()):
                    game = rofl1.Game(main_screen)
                    game.run()
                if button2.pressed(pygame.mouse.get_pos()):
                    rabbit.main()
                #if button3.pressed(pygame.mouse.get_pos()):
                    #ai.main()


if __name__ == '__main__':
    main()
