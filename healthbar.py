from character import Character
import pygame

class Healthbar:
    def __init__(self, character, window):
        """
        Initialise the Healthbar with a character and window.
        """
        self.character = character  # Character whose health is being tracked
        self.max_hit_points = character.hit_points  # Maximum hit points from the character
        self.current_hit_points = character.hit_points  # Current hit points, initially the same as max
        self.width = 200  # Width of the health bar
        self.height = 20  # Height of the health bar
        self.window = window  # Window where the health bar will be drawn

    def update(self):
        """
        Update the current hit points to match the character's current hit points.
        """
        self.current_hit_points = self.character.hit_points  # Refresh current hit points

    def display(self, screen):
        """
        Draw the health bar on the screen.
        """
        health_ratio = self.current_hit_points / self.max_hit_points  # Calculate the ratio of current to maximum health
        filled_width = int(self.width * health_ratio)  # Determine the width of the filled portion of the health bar

        # Draw the background of the health bar in red
        background_rectangle = pygame.Rect(10, 10, self.width, self.height)
        pygame.draw.rect(self.window, (255, 0, 0), background_rectangle)

        # Draw the filled portion of the health bar in green
        health_rectangle = pygame.Rect(10, 10, filled_width, self.height)
        pygame.draw.rect(self.window, (0, 255, 0), health_rectangle)

    def take_damage(self, amount):
        """
        Apply damage to the character and update the health bar.
        """
        self.character.take_damage(amount)  # Apply damage to the character
        self.update()  # Update the health bar to reflect the new health
