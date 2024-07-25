import pygame
from assets import GAME_ASSETS

class MainMenu:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font(None, 36)  # Specify the font size and style
        self.menu_options = ['Start Game', 'Settings', 'Exit']
        self.selected_option = 0  # The index of the currently selected menu option
        self.background_image = pygame.image.load(GAME_ASSETS['main_menu_background'])  # Load the background image
        # Scale the background image to match the window size
        self.scaled_background = pygame.transform.scale(self.background_image, (self.window.get_width(), self.window.get_height()))

    def draw_text_with_border(self, text, font, position, colour, border_colour, border_width):
        """Draw text with a border effect."""
        # Render the border text first
        border_text = font.render(text, True, border_colour)
        border_rect = border_text.get_rect(center=position)
        # Render the main text on top
        main_text = font.render(text, True, colour)
        main_rect = main_text.get_rect(center=position)

        # Draw the border text multiple times around the main text
        for x_offset in (-border_width, 0, border_width):
            for y_offset in (-border_width, 0, border_width):
                if x_offset != 0 or y_offset != 0:
                    self.window.blit(border_text, border_rect.move(x_offset, y_offset))

        # Draw the main text
        self.window.blit(main_text, main_rect)

    def run(self):
        """Handles the display and interaction logic for the main menu."""
        running = True
        while running:
            # Blit the scaled background image to fill the entire window
            self.window.blit(self.scaled_background, (0, 0))

            # Display each menu option on the screen with border
            for index, option in enumerate(self.menu_options):
                # Highlight the selected option in red
                colour = (255, 0, 0) if index == self.selected_option else (255, 255, 255)
                border_colour = (0, 0, 0)  # Black border
                border_width = 2  # Border width
                text_position = (self.window.get_width() / 2, 400 + 50 * index)
                self.draw_text_with_border(option, self.font, text_position, colour, border_colour, border_width)

            pygame.display.flip()  # Update the display with the new frame

            # Event handling in the menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'  # Return 'quit' if the window is closed
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        # Return the current selected option when Enter is pressed
                        return self.menu_options[self.selected_option]

        return 'quit'  # Default return value if the loop ends
