import random
import pygame
from assets import GAME_ASSETS
from enemy import Enemy
from healthbar import Healthbar
from character import Character

class Map:
    def __init__(self, window, map_type):
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
        self.player_character = None  # Character instance
        self.healthbar = None  # Healthbar instance

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
        self.player_type = character_type
        self.player_image = self.player_images[character_type]
        self.player_image = pygame.transform.scale(self.player_image, (int(self.player_image.get_width() * 2), int(self.player_image.get_height() * 2)))
        self.player_character = Character(self.player_type, self.player_type, 5)  # Example: armour value of 5
        self.healthbar = Healthbar(self.player_character, self.window)

    def check_for_combat(self):
        for enemy in self.enemies:
            if pygame.math.Vector2(enemy.position).distance_to(self.player_position) < 50:
                self.in_combat = True
                self.current_enemy = enemy
                print("Combat initiated with enemy at position:", enemy.position)
                return True
        return False

    def handle_combat(self):
        if self.in_combat and self.current_enemy:
            player_damage = random.randint(5, 10)
            print("Player deals damage:", player_damage)
            enemy_defeated = self.current_enemy.take_damage(player_damage)
            if enemy_defeated:
                print("Enemy defeated!")
                self.enemies.remove(self.current_enemy)
                self.in_combat = False
                self.current_enemy = None
                if not self.enemies:
                    self.spawn_blue_orb()
            else:
                enemy_damage = random.randint(1, 2)
                print("Enemy deals damage:", enemy_damage)
                self.player_character.take_damage(enemy_damage)
                self.healthbar.update()
                if not self.player_character.is_alive():
                    print("Player has been defeated!")
                    self.game_over = True

    def spawn_blue_orb(self):
        self.blue_orb = pygame.image.load(GAME_ASSETS["blue_orb"]).convert_alpha()
        self.blue_orb = pygame.transform.scale(self.blue_orb, (50, 50))
        self.orb_position = [self.window.get_width() / 2 - 25, self.window.get_height() / 2 - 25]

    def check_orb_collision(self):
        if self.blue_orb and pygame.math.Vector2(self.orb_position).distance_to(self.player_position) < 25:
            if self.map_type == 'dungeon_map':
                self.game_over = True
                return 'quit'
            else:
                return 'next_level'
        return None

    def handle_events(self):
        if self.game_over:
            return 'quit'

        keys = pygame.key.get_pressed()
        move_speed = 0.6
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
        self.window.fill((0, 0, 0))
        self.window.blit(self.map_image, (0, 0))
        self.window.blit(self.player_image, (self.player_position[0], self.player_position[1]))
        for enemy in self.enemies:
            enemy.draw()
        if self.blue_orb:
            self.window.blit(self.blue_orb, self.orb_position)
        if self.healthbar:
            self.healthbar.display(self.window)
        pygame.display.flip()
