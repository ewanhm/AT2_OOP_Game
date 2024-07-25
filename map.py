import random
import pygame
from assets import GAME_ASSETS
from enemy import Enemy
from healthbar import Healthbar
from character import Character
from warrior import Warrior
from rogue import Rogue
from mage import Mage

class Map:
    def __init__(self, window, map_type):
        """
        Initialise the Map with window, map type, and load relevant assets.
        """
        self.window = window  # The Pygame window where the map will be drawn
        self.map_type = map_type  # Type of the map (grass, cave, dungeon)
        self.map_image = pygame.image.load(GAME_ASSETS[map_type]).convert_alpha()  # Load the map image
        self.map_image = pygame.transform.scale(self.map_image, (self.window.get_width(), self.window.get_height()))  # Scale map image to window size
        self.player_images = {  # Dictionary to hold player images for different character types
            'Warrior': pygame.image.load(GAME_ASSETS['warrior']).convert_alpha(),
            'Mage': pygame.image.load(GAME_ASSETS['mage']).convert_alpha(),
            'Rogue': pygame.image.load(GAME_ASSETS["rogue"]).convert_alpha()
        }
        self.player_type = None  # Type of the player character
        self.player_position = [self.window.get_width() / 2, self.window.get_height() / 2]  # Initial player position at the centre of the window
        self.enemies = []  # List to hold enemies in the map
        self.blue_orb = None  # The blue orb that appears when all enemies are defeated
        self.game_over = False  # Flag to indicate if the game is over
        self.in_combat = False  # Flag to indicate if the player is in combat
        self.current_enemy = None  # The enemy currently in combat with the player
        self.player_character = None  # Instance of the player's character
        self.healthbar = None  # Instance of the health bar
        self.selected_skill = 0  # Index of the selected skill (not used in this code)
        self.skills = []  # List of skills available to the player

        # Initialise enemies based on the map type
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
            self.enemies = [
                Enemy(GAME_ASSETS["orc"], [self.window.get_width() - 120, 50], self.window),
                Enemy(GAME_ASSETS["skeleton"], [self.window.get_width() / 4, self.window.get_height() / 4], self.window)
            ]

    def load_player(self, character_type):
        """
        Initialise the player character based on the character type and load their image and health bar.
        """
        self.player_type = character_type  # Set player type
        self.player_image = self.player_images[character_type]  # Get the player's image
        self.player_image = pygame.transform.scale(self.player_image, (int(self.player_image.get_width() * 2), int(self.player_image.get_height() * 2)))  # Scale player image

        # Initialise the correct subclass based on player_type
        if character_type == 'Warrior':
            self.player_character = Warrior('Player', 100)  # Create a Warrior instance
        elif character_type == 'Mage':
            self.player_character = Mage('Player', 100)  # Create a Mage instance
        elif character_type == 'Rogue':
            self.player_character = Rogue('Player', 100)  # Create a Rogue instance

        self.healthbar = Healthbar(self.player_character, self.window)  # Create a health bar for the player
        self.skills = list(self.player_character.attacks.keys()) if hasattr(self.player_character, 'attacks') else []  # List of skills if attacks attribute exists

    def check_for_combat(self):
        """
        Check if the player is close enough to any enemy to initiate combat.
        """
        for enemy in self.enemies:
            if pygame.math.Vector2(enemy.position).distance_to(self.player_position) < 50:  # Check distance to enemy
                self.in_combat = True  # Set combat flag to True
                self.current_enemy = enemy  # Set the current enemy
                print("Combat initiated with enemy at position:", enemy.position)
                return True
        return False

    def handle_combat(self):
        """
        Handle the combat between the player and the current enemy.
        """
        if self.in_combat and self.current_enemy:
            player_damage = random.randint(5, 10)  # Random damage value for player
            print("Player deals damage:", player_damage)
            enemy_defeated = self.current_enemy.take_damage(player_damage)  # Apply damage to enemy
            if enemy_defeated:
                print("Enemy defeated!")
                self.enemies.remove(self.current_enemy)  # Remove defeated enemy from the list
                self.in_combat = False  # End combat
                self.current_enemy = None  # Reset current enemy
                if not self.enemies:  # Check if no enemies remain
                    self.spawn_blue_orb()  # Spawn a blue orb
            else:
                enemy_damage = random.randint(1, 2)  # Random damage value for enemy
                print("Enemy deals damage:", enemy_damage)
                self.player_character.take_damage(enemy_damage)  # Apply damage to player
                self.healthbar.update()  # Update the health bar
                if not self.player_character.is_alive():  # Check if player is defeated
                    print("Player has been defeated!")
                    self.game_over = True  # Set game over flag

    def spawn_blue_orb(self):
        """
        Spawn a blue orb in the centre of the map.
        """
        self.blue_orb = pygame.image.load(GAME_ASSETS["blue_orb"]).convert_alpha()  # Load blue orb image
        self.blue_orb = pygame.transform.scale(self.blue_orb, (50, 50))  # Scale blue orb image
        self.orb_position = [self.window.get_width() / 2 - 25, self.window.get_height() / 2 - 25]  # Set blue orb position

    def check_orb_collision(self):
        """
        Check if the player has collided with the blue orb.
        """
        if self.blue_orb and pygame.math.Vector2(self.orb_position).distance_to(self.player_position) < 25:  # Check collision distance
            if self.map_type == 'dungeon_map':
                self.game_over = True  # Set game over if in dungeon map
                return 'quit'
            else:
                return 'next_level'  # Move to the next level if not in dungeon map
        return None

    def handle_events(self):
        """
        Handle player input and game events.
        """
        if self.game_over:
            return 'quit'

        keys = pygame.key.get_pressed()  # Get state of all keyboard keys
        move_speed = 0.6  # Speed at which the player moves
        if keys[pygame.K_LEFT]:
            self.player_position[0] -= move_speed  # Move player left
        if keys[pygame.K_RIGHT]:
            self.player_position[0] += move_speed  # Move player right
        if keys[pygame.K_UP]:
            self.player_position[1] -= move_speed  # Move player up
        if keys[pygame.K_DOWN]:
            self.player_position[1] += move_speed  # Move player down

        if not self.in_combat:
            if self.check_for_combat():  # Check for combat initiation
                return
        self.handle_combat()  # Handle ongoing combat

        orb_collision_result = self.check_orb_collision()  # Check if player collided with the blue orb
        if orb_collision_result:
            return orb_collision_result

    def draw(self):
        """
        Draw the map, player, enemies, and health bar on the window.
        """
        self.window.fill((0, 0, 0))  # Fill the window with black
        self.window.blit(self.map_image, (0, 0))  # Draw the map image
        self.window.blit(self.player_image, (self.player_position[0], self.player_position[1]))  # Draw the player image
        for enemy in self.enemies:
            enemy.draw()  # Draw each enemy
        if self.blue_orb:
            self.window.blit(self.blue_orb, self.orb_position)  # Draw the blue orb
        if self.healthbar:
            self.healthbar.display(self.window)  # Draw the health bar
        pygame.display.flip()  # Update the display
