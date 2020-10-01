import pygame
from main import *




class Interface:
    def __init__(self, width, height, scale):
        pygame.init()

        self.width = width
        self.height = height
        self.scale = scale

        window_width = self.width*self.scale
        window_height = self.height*self.scale
        args2 = args_parse()
        if args2.fullscreen:
            self.screen = pygame.display.set_mode(
                (window_width, window_height), pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode(
                (window_width, window_height)
            )

        self.surface = pygame.Surface((self.width, self.height))

        self.colors = [pygame.Color('black'),
                       pygame.Color('white')]




    def clear(self):
        self.surface.fill(self.colors[0])


    def draw(self, display):
        self.clear()
        self.surface = pygame.Surface((self.width, self.height))

        for i in range(32*64):
            if display[i] == 1:
                self.surface.fill(self.colors[1], ((i%64, 31-i//64), (1, 1)))

        pygame.display.get_surface().blit(
            pygame.transform.scale(
                pygame.transform.flip(self.surface, False, True),
                (self.width*self.scale, self.height*self.scale)
            ),
            (0, 0)
        )
        pygame.display.update()


    def handle_events(self):
        events = pygame.event.get()

        quit_events = [e for e in events if e.type == pygame.QUIT]
        if len(quit_events) > 0:
            pygame.quit()
            exit()

        return events