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

# Game grid size initialized to debug setting
game_grid_size = 2

# Defining Functions & Classes
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
        line_x = self.location.left
        line_y = self.location.top

        for line_text in self.text.split("\n"):
            line = self.font.render(line_text, True, self.color)
            screen.blit(line, (line_x, line_y))
            line_y += line_height

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

    # Infinite loop
    global game_state
    print(game_state)
    while game_state == "menu":
        # "in" is interpreted different ways, boolean or iterator, depending on the context
        # So I have to remove the parentheses from this and all lines, just to make things consistent
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("QUIT")
                game_state = "quit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("ESC")
                game_state = "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("MOUSEBUTTONDOWN")
                mouse_pos = pygame.mouse.get_pos()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in menu_button_list:
                    if button.left <= mouse_x <= button.left + button.width and button.top <= mouse_y <= button.top + button.height:
                        if "16" in button.text:
                            game_grid_size = 16
                        elif "32" in button.text:
                            game_grid_size = 32
                        elif "64" in button.text:
                            game_grid_size = 64
                        game_state = "game"
                # TODO: make this a separate function

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

# define neighbors class
class Neighbors:
    def __init__(self, top, top_right, right, bottom_right, bottom, bottom_left, left, top_left):
        self.top = top
        self.top_right = top_right
        self.right = right
        self.bottom_right = bottom_right
        self.bottom = bottom
        self.bottom_left = bottom_left
        self.left = left
        self.top_left = top_left

# Define cell class
class Cell:
    def __init__(self, grid_pos_x, grid_pos_y, width, height, neighbors, status):
        self.grid_pos_x = grid_pos_x
        self.grid_pos_y = grid_pos_y
        self.width = width
        self.height = height
        self.neighbors = neighbors
        self.status = status
        self.live_color = (30, 225, 30)
        self.dead_color = (60, 60, 60)

    # Vibe coded
    def draw(self, screen):
        left = margin_x + self.grid_pos_x * self.width
        top = margin_y + self.grid_pos_y * self.height

        rect = pygame.Rect(left, top, self.width, self.height)

        # Never seen this formatting before
        color = (30, 225, 30) if self.status else (60, 60, 60)

        pygame.draw.rect(screen, color, rect)

    def clicked(self, pos):
        left = margin_x + self.grid_pos_x * self.width
        top = margin_y + self.grid_pos_y * self.height
        rect = pygame.Rect(left, top, self.width, self.height)
        return rect.collidepoint(pos)

# Define grid builder function
def grid_builder(grid_cells):
    grid_width = game_grid_size
    grid_height = game_grid_size

    cell_width = (WINDOW_WIDTH - 2 * margin_x) // grid_width
    cell_height = (WINDOW_HEIGHT - 2 * margin_y) // grid_height
    # Make them square
    if (cell_width > cell_height):
        cell_width = cell_height
    elif (cell_width < cell_height):
        cell_height = cell_width

    # Will need these
    top_neighbor = (-1, -1)
    top_right_neighbor = (-1, -1)
    right_neighbor = (-1, -1)
    bottom_right_neighbor = (-1, -1)
    bottom_neighbor = (-1, -1)
    bottom_left_neighbor = (-1, -1)
    left_neighbor = (-1, -1)
    top_left_neighbor = (-1, -1)

    # Or, since tuples are immutable & N^2...
    top_neighbor_x = -1
    top_right_neighbor_x = -1
    right_neighbor_x = -1
    bottom_right_neighbor_x = -1
    bottom_neighbor_x = -1
    bottom_left_neighbor_x = -1
    left_neighbor_x = -1
    top_left_neighbor_x = -1

    for x in range(grid_width):
        # To avoid doing things N^2 times

        for y in range(grid_height):
            # Computing this N^2 times (yeesh)
            # TODO: Fix this
            top_neighbor = (x, y + 1)
            top_right_neighbor = (x + 1, y + 1)
            right_neighbor = (x + 1, y)
            bottom_right_neighbor = (x + 1, y - 1)
            bottom_neighbor = (x, y - 1)
            bottom_left_neighbor = (x - 1, y - 1)
            left_neighbor = (x - 1, y)
            top_left_neighbor = (x - 1, y + 1)

            cell_neighbors = (top_neighbor, top_right_neighbor, right_neighbor, bottom_right_neighbor, bottom_neighbor, bottom_left_neighbor, left_neighbor, top_left_neighbor)
            grid_cells[x][y] = Cell(x, y, cell_width, cell_height, cell_neighbors, False)

# Define "progress one step" function

# Define "autoplay" function

# Define "autoplay speed one" helper function

# Define "autoplay speed two" helper function

# Define "autoplay speed three" helper function

# Define "start game" function
def start_game():
    screen.fill((30, 30, 30))

    # Need 2D array for grid builder to build
    grid_cells = [
        [None for _ in range(game_grid_size)]
        for _ in range(game_grid_size)
    ]

    # Call grid_builder to build the grid of cells based on the game_grid_size
    grid_builder(grid_cells)

    global game_state
    print(game_state)
    while game_state == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("QUIT")
                game_state = "quit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("ESC")
                game_state = "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("MOUSEBUTTONDOWN")
                mouse_pos = pygame.mouse.get_pos()

        for x in range(game_grid_size):
            for y in range(game_grid_size):
                print("Drawing Cell " + str(x) + ", " + str(y))
                grid_cells[x][y].draw(screen)
        pygame.display.update()

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
    if game_state == "game":
        start_game()

# Quit properly
pygame.quit()
sys.exit()