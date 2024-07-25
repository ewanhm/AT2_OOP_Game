from character import Character
from game import Game
import pygame

class Healthbar:

    def __init__(self, character, window):
        self.character = character
        self.max_hit_points = character.hit_points
        self.current_hit_points = character.hit_points
        self.width = 200
        self.height = 20
        self.window = window

    def update(self):
        self.current_hit_points = self.character.hit_points

    def display(self, screen):
        health_ratio = self.current_hit_points / self.max_hit_points
        filled_width = int(self.width * health_ratio) 

        # red background healthbar
        background_rectangle = pygame.Rect(10, 10, self.width, self.height)
        pygame.draw.rect(screen, (255, 0, 0 ), background_rectangle)

        # green overlaying healthbar
        health_rectangle = pygame.Rect(10, 10, filled_width, self.height)
        pygame.draw.rect(screen, (0, 255, 0), health_rectangle)

    def take_damage(self, amount):
        self.character.take_damage(amount)
        self.update()
    

    
    
