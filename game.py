import pygame
from menu import MainMenu
from character_select import CharacterSelect
from map import Map
from assets import load_assets, GAME_ASSETS

class Game:
    def __init__(self):
        pygame.init()  # Initialise the Pygame library
        load_assets()  # Load game image assets
        self.window = pygame.display.set_mode((800, 600))  # Create the game window
        self.menu = MainMenu(self.window)  # Initialise the main menu
        self.character_select = CharacterSelect(self.window)  # Initialise character selection
        self.current_level = 'grass'  # Set initial level to 'grass'
        self.game_map = self.load_map(self.current_level)  # Load the map for the initial level
        self.state = 'menu'  # Set the initial state to 'menu'
        self.current_character = None  # No character selected initially

    def load_map(self, level):
        """
        Load the map for the specified level.
        """
        if level == 'grass':
            return Map(self.window, 'grass_map')  # Load grass map
        elif level == 'cave':
            return Map(self.window, 'cave_map')  # Load cave map
        elif level == 'dungeon':
            return Map(self.window, 'dungeon_map')  # Load dungeon map

    def run(self):
        """
        Main game loop handling different states.
        """
        while True:
            if self.state == 'menu':
                result = self.menu.run()  # Run the menu and get the result
                if result == 'Start Game':
                    self.state = 'character_select'  # Switch to character selection
                elif result == 'Settings':
                    pass  # Handle settings (not implemented)
                elif result == 'Exit':
                    pygame.quit()  # Quit the game
                    return

            elif self.state == 'character_select':
                selected_character = self.character_select.run()  # Run character selection and get the result
                if selected_character == 'back':
                    self.state = 'menu'  # Go back to the menu
                elif selected_character:
                    self.current_character = selected_character  # Set the selected character
                    self.game_map.load_player(selected_character)  # Load the player into the map
                    self.state = 'game_map'  # Switch to game map

            elif self.state == 'game_map':
                result = self.game_map.handle_events()  # Handle events in the game map
                if result == 'back':
                    self.state = 'character_select'  # Go back to character selection
                elif result == 'quit':
                    pygame.quit()  # Quit the game
                    return
                elif result == 'next_level':
                    self.current_level = self.next_level(self.current_level)  # Move to the next level
                    self.game_map = self.load_map(self.current_level)  # Load the new map
                    self.game_map.load_player(self.current_character)  # Load the player into the new map
                else:
                    self.game_map.draw()  # Draw the game map

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Quit the game on window close
                    return

    def next_level(self, current_level):
        """
        Determine the next level based on the current level.
        """
        if current_level == 'grass':
            return 'cave'  # Next level after grass is cave
        elif current_level == 'cave':
            return 'dungeon'  # Next level after cave is dungeon
        elif current_level == 'dungeon':
            return 'game_over'  # End of game after dungeon

if __name__ == "__main__":
    game = Game()  # Create an instance of the Game class
    game.run()  # Run the game
