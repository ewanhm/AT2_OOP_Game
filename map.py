import random

import pygame
from assets import GAME_ASSETS
from enemy import Enemy


class Map:
    def __init__(self, window, map_type):
        """
        Initialize the Map class.

        Args:
            window (pygame.Surface): The game window surface.
            map_type (str): The type of map (level) to load.
        """
        self.window = window
        self.map_type = map_type
        self.map_image = pygame.image.load(GAME_ASSETS[map_type]).convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (self.window.get_width(), self.window.get_height()))
        self.player_images = {
            'Warrior': pygame.image.load(GAME_ASSETS['warrior']).convert_alpha(),
            'Mage': pygame.image.load(GAME_ASSETS['mage']).convert_alpha(),
            'Rogue': pygame.image.load(GAME_ASSETS["rogue"]).convert_alpha()
        }
        self.player_type = None
        self.player_position = [self.window.get_width() / 2, self.window.get_height() / 2]
        self.enemies = []
        self.blue_orb = None
        self.game_over = False
        self.in_combat = False
        self.current_enemy = None

        # Load enemies based on the level type
        if self.map_type == 'grass_map':
            self.enemies = [
                Enemy(GAME_ASSETS["goblin"], [50, 50], self.window),
                Enemy(GAME_ASSETS["goblin"], [self.window.get_width() - 120, 50], self.window)
            ]
        
        elif self.map_type == 'cave_map':
            self.enemies = [
                Enemy(GAME_ASSETS["orc"], [self.window.get_width() - 120, 50], self.window),
                Enemy(GAME_ASSETS["skeleton"], [50, self.window.get_height() - 120], self.window),
                Enemy(GAME_ASSETS["skeleton"], [self.window.get_width() - 120, self.window.get_height() - 120], self.window)
            ]

        elif self.map_type == 'dungeon_map':
            # Example enemies for dungeon, adjust as needed
            self.enemies = [
                Enemy(GAME_ASSETS["orc"], [self.window.get_width() / 2, self.window.get_height() / 2], self.window),
                Enemy(GAME_ASSETS["skeleton"], [self.window.get_width() / 4, self.window.get_height() / 4], self.window)
            ]

    def load_player(self, character_type):
        """
        Load the player character.

        Args:
            character_type (str): The type of character to load.
        """
        self.player_type = character_type
        self.player_image = self.player_images[character_type]
        self.player_image = pygame.transform.scale(self.player_image, (int(self.player_image.get_width() * 2), int(self.player_image.get_height() * 2)))

    def check_for_combat(self):
        """
        Check if the player is in combat with any enemy.

        Returns:
            bool: True if the player is in combat, False otherwise.
        """
        for enemy in self.enemies:
            if pygame.math.Vector2(enemy.position).distance_to(self.player_position) < 50:
                self.in_combat = True
                self.current_enemy = enemy
                return True
        return False

    def handle_combat(self):
        """
        Handle combat between the player and the current enemy.
        """
        if self.in_combat and self.current_enemy:
            player_damage = random.randint(5, 10)
            enemy_defeated = self.current_enemy.take_damage(player_damage)
            print(f"Player attacks! Deals {player_damage} damage to the enemy.")
            if enemy_defeated:
                print("Enemy defeated!")
                self.enemies.remove(self.current_enemy)
                self.in_combat = False
                self.current_enemy = None
                if not self.enemies:
                    self.spawn_blue_orb()
            else:
                enemy_damage = random.randint(5, 10)
                print(f"Enemy attacks back! Deals {enemy_damage} damage to the player.")
                # Assume player has a method to take damage
                # self.player.take_damage(enemy_damage)

    def spawn_blue_orb(self):
        """
        Spawn the blue orb in the centre of the map for level transition.
        """
        self.blue_orb = pygame.image.load(GAME_ASSETS["blue_orb"]).convert_alpha()
        self.blue_orb = pygame.transform.scale(self.blue_orb, (50, 50))
        self.orb_position = [self.window.get_width() / 2 - 25, self.window.get_height() / 2 - 25]

    def check_orb_collision(self):
        """
        Check if the player has collided with the blue orb.

        Returns:
            str: 'quit' if the player has collided with the blue orb and it's the dungeon level,
                'next_level' otherwise, or None if there is no collision.
        """
        if self.blue_orb and pygame.math.Vector2(self.orb_position).distance_to(self.player_position) < 25:
            if self.map_type == 'dungeon_map':
                self.game_over = True
                return 'quit'
            else:
                return 'next_level'
        return None


    def handle_events(self):
        """
        Handle user input events.
        
        Returns:
            str: 'quit' if the game is over and should be exited, 'next_level' if level should be changed, or None otherwise.
        """
        if self.game_over:
            return 'quit'

        keys = pygame.key.get_pressed()
        move_speed = 3
        if keys[pygame.K_LEFT]:
            self.player_position[0] -= move_speed
        if keys[pygame.K_RIGHT]:
            self.player_position[0] += move_speed
        if keys[pygame.K_UP]:
            self.player_position[1] -= move_speed
        if keys[pygame.K_DOWN]:
            self.player_position[1] += move_speed

        if not self.in_combat:
            if self.check_for_combat():
                return
        self.handle_combat()

        orb_collision_result = self.check_orb_collision()
        if orb_collision_result:
            return orb_collision_result


    def draw(self):
        """
        Draw the game objects on the window.
        """
        self.window.fill((0, 0, 0))
        self.window.blit(self.map_image, (0, 0))
        self.window.blit(self.player_image, (self.player_position[0], self.player_position[1]))
        for enemy in self.enemies:
            enemy.draw()
        if self.blue_orb:
            self.window.blit(self.blue_orb, self.orb_position)
        pygame.display.flip()



