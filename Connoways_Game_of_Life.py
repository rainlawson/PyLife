# My project, I will refactor as I please

import pygame
import sys

# Setup Work & Globals
# ------------------------------------------------------------------------------------------------------------------- #
# Need Pygame for input, drawing, and game logic
pygame.init()

# Figure out screem and subsequently window size
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
WINDOW_WIDTH = int(SCREEN_WIDTH * 0.8)
WINDOW_HEIGHT = int(SCREEN_HEIGHT * 0.8)

# Margins for use later
margin_x = int(WINDOW_WIDTH * 0.05)  # 5% padding
margin_y = int(WINDOW_HEIGHT * 0.05)

# TODO: add min/max screen and window size checks

# Declare cell sizes and initialize for debugging
cell_width = WINDOW_WIDTH // 2
cell_height = WINDOW_HEIGHT // 2

# Declare game state and initialize to "menu"
game_state = "menu"

# Defining Functions
# ------------------------------------------------------------------------------------------------------------------- #
# Define draw menu button function
class MenuButton:
    # These are optional, but it's my project
    font: pygame.font.Font
    surface: pygame.Surface
    location: pygame.Rect

    def __init__(self, text, color, left, top, width, height):
        self.font: pygame.font.Font = pygame.font.SysFont("Arial", 30, bold=True)
        self.surface: pygame.Surface = self.font.render(text, True, color)
        self.location: pygame.Rect = pygame.Rect(left, top, width, height)
        self.text = text
        self.base_color = color
        self.hover_color = (255, 0, 255)
        self.color = color
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    # TODO: make color class (use https://redketchup.io/color-picker)

    def draw(self, screen):
        # screen.blit(self.surface, self.location)
        line_height = self.font.get_linesize()
        x = self.location.left
        y = self.location.top

        for line in self.text.split("\n"):
            surface = self.font.render(line, True, self.color)
            screen.blit(surface, (x, y))
            y += line_height

    def clicked(self, pos):
        return self.location.collidepoint(pos)

    # Old
    # def make_menu_button(button_text, color_1, color_2, color_3, left, top, height, width):
    #     font = pygame.font.SysFont("Arial", 30, bold=True)
    #     surface = font.render(button_text, True, (color_1, color_2, color_3))
    #     box = pygame.Rect(left, top, width, height)


# Define "create menu" function
def create_menu():
    # Background color for the window
    screen.fill((30, 30, 30))

    # Declare list of "buttons" with text box and menu buttons
    menu_button_list = []

    # Make text box
    instructions = (
    "Conway's Game of Life:\n"
    "Each cell lives or dies based on its neighbors.\n"
    "Alive cells with 2–3 neighbors survive. Dead cells with exactly 3 neighbors are born.\n"
    "All other cells die or remain empty.\n\n"
    "Press ESC to quit.\n"
    "In game, press ESC to return to the menu.\n"
    "Click cells to toggle them on or off.\n"
    "Press P to play or pause the game.\n\n"
    "Choose a grid size below to get started."
    )

    instructions_left = margin_x
    instructions_top = margin_y

    instructions_width = WINDOW_WIDTH - 2 * margin_x
    instructions_height = WINDOW_HEIGHT // 2 - margin_y

    instruction_box = MenuButton(instructions, (255, 255, 255), instructions_left, instructions_top, instructions_width, instructions_height)
    menu_button_list.append(instruction_box)
    # TODO: make it separate from menu buttons

    # Make buttons
    window_horizontal_midpoint = WINDOW_WIDTH // 2
    window_vertical_midpoint = WINDOW_HEIGHT // 2
    # need 7 equal portions of window below the window vertical midpoint (space, button, space, button, space, button, space)
    button_spacer = (WINDOW_WIDTH // 2) // 7

    small_grid_button = MenuButton("16x16", (255, 0, 0), window_horizontal_midpoint - button_spacer, window_vertical_midpoint + button_spacer, button_spacer, button_spacer)
    medium_grid_button =MenuButton("32x32", (0, 255, 0), window_horizontal_midpoint - button_spacer, window_vertical_midpoint + (2 * button_spacer), button_spacer, button_spacer)
    large_grid_button =MenuButton("64x64", (0, 0, 255), window_horizontal_midpoint - button_spacer, window_vertical_midpoint + (3 * button_spacer), button_spacer, button_spacer)

    menu_button_list.append(small_grid_button)
    menu_button_list.append(medium_grid_button)
    menu_button_list.append(large_grid_button)
    # TODO: 3 buttons with different positions & add them to a list of buttons

    # Infinite loop
    global game_state
    print(game_state)
    while game_state == "menu":
        # "in" is interpreted different ways, boolean or iterator, depending on the context
        # So I have to remove the parentheses from this and all lines, just to make things consistent
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                print("ESC")
                game_state = "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("MOUSEBUTTONDOWN")
                mouse_pos = pygame.mouse.get_pos()

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Checking mouse pos against button pos, setting button color accordingly
        for button in menu_button_list:
            if button.left <= mouse_x <= button.left + button.width and button.top <= mouse_y <= button.top + button.height:
                button.color = button.hover_color
            else:
                button.color = button.base_color
        for button in menu_button_list:
            button.draw(screen)
        pygame.display.update()

# Define cells

# Define "start game" function

# Define "progress one step" function

# Define "autoplay" function

# Define "autoplay speed one" helper function

# Define "autoplay speed two" helper function

# Define "autoplay speed three" helper function

# Playing The Game
# ------------------------------------------------------------------------------------------------------------------- #
# Launch the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")

# Clock and framerate
clock = pygame.time.Clock()
FPS = 30

# Create infinite master loop
while game_state != "quit":

    # Implement master "quit" key
    # if (event.type == pygame.K_ESCAPE):
    #     game_state = "quit"

    # Check game state
    # If "menu", launch the menu
    if game_state == "menu":
        create_menu()
        # Handle menu behavior in "create menu" function

    # If quit was selected, quit
    if game_state == "quit":
        break

    # Once menu options are selected, launch "start game" function and change game state\
    # Rest should be handled withing the "start game" function

# Quit properly
pygame.quit()
sys.exit()