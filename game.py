import pygame
from menu import MainMenu
from character_select import CharacterSelect
from map import Map
from assets import load_assets, GAME_ASSETS

class Game:
    def __init__(self):
        pygame.init()
        load_assets()  # load the game image assets
        self.window = pygame.display.set_mode((800, 600))
        self.menu = MainMenu(self.window)
        self.character_select = CharacterSelect(self.window)
        self.current_level = 'grass'  # Start at the grass level
        self.game_map = self.load_map(self.current_level)
        self.state = 'menu'
        self.current_character = None

    def load_map(self, level):
        """
        Load the map for the given level.
        """
        if level == 'grass':
            return Map(self.window, 'grass_map')
        elif level == 'cave':
            return Map(self.window, 'cave_map')
        elif level == 'dungeon':
            return Map(self.window, 'dungeon_map')

    def run(self):
        while True:
            if self.state == 'menu':
                result = self.menu.run()
                if result == 'Start Game':
                    self.state = 'character_select'
                elif result == 'Settings':
                    pass
                elif result == 'Exit':
                    pygame.quit()
                    return

            elif self.state == 'character_select':
                selected_character = self.character_select.run()
                if selected_character == 'back':
                    self.state = 'menu'
                elif selected_character:
                    self.current_character = selected_character
                    self.game_map.load_player(selected_character)
                    self.state = 'game_map'

            elif self.state == 'game_map':
                result = self.game_map.handle_events()
                if result == 'back':
                    self.state = 'character_select'
                elif result == 'quit':
                    pygame.quit()
                    return
                elif result == 'next_level':
                    self.current_level = self.next_level(self.current_level)
                    self.game_map = self.load_map(self.current_level)
                    self.game_map.load_player(self.current_character)
                else:
                    self.game_map.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return


    def next_level(self, current_level):
        """
        Determine the next level based on the current level.
        """
        if current_level == 'grass':
            return 'cave'
        elif current_level == 'cave':
            return 'dungeon'
        elif current_level == 'dungeon':
            return 'game_over'
          



if __name__ == "__main__":
    game = Game()  # Create an instance of the Game class
    game.run()  # Run the game

