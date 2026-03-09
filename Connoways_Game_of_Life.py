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

    # Can make colors using https://redketchup.io/color-picker

    def draw(self, screen):
        line_height = self.font.get_linesize()
        line_x = self.location.left
        line_y = self.location.top

        for line_text in self.text.split("\n"):
            line = self.font.render(line_text, True, self.color)
            screen.blit(line, (line_x, line_y))
            line_y += line_height

    def clicked(self, pos):
        return self.location.collidepoint(pos)



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
    "Press 1, 2, or 3 to autoplay, 0 to stop autoplay, space to progress once.\n\n"
    "Choose a grid size below to get started."
    )

    instructions_left = margin_x
    instructions_top = margin_y

    instructions_width = WINDOW_WIDTH - 2 * margin_x
    instructions_height = WINDOW_HEIGHT // 2 - margin_y

    instruction_box = MenuButton(instructions, (255, 255, 255), instructions_left, instructions_top, instructions_width, instructions_height)
    menu_button_list.append(instruction_box)

    # Make buttons
    window_horizontal_midpoint = WINDOW_WIDTH // 2
    window_vertical_midpoint = WINDOW_HEIGHT // 2
    # Need 7 equal portions of window below the window vertical midpoint (space, button, space, button, space, button, space)
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
    global game_grid_size
    game_grid_size = 2
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
                        else:
                            break
                        game_state = "game"

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

# Did compute neighbors ahead of time, but more efficient (and easier) to just compute at runtime

# Define cell class
class Cell:
    def __init__(self, grid_pos_x, grid_pos_y, width, height, status):
        self.grid_pos_x = grid_pos_x
        self.grid_pos_y = grid_pos_y
        self.width = width
        self.height = height
        self.status = status
        self.live_color = (30, 225, 30)
        self.dead_color = (60, 60, 60)

    # Vibe coded
    def draw(self, screen):
        # Inefficient but eh
        grid_pixel_width = self.width * game_grid_size
        grid_pixel_height = self.height * game_grid_size

        offset_x = (WINDOW_WIDTH - grid_pixel_width) // 2
        offset_y = (WINDOW_HEIGHT - grid_pixel_height) // 2

        left = offset_x + self.grid_pos_x * self.width
        top = offset_y + self.grid_pos_y * self.height

        outer_rect = pygame.Rect(left, top, self.width, self.height)

        border = 1

        inner_rect = pygame.Rect(
            left + border,
            top + border,
            self.width - 2 * border,
            self.height - 2 * border
        )

        pygame.draw.rect(screen, (30, 30, 30), outer_rect)

        color = (30, 225, 30) if self.status else (60, 60, 60)
        pygame.draw.rect(screen, color, inner_rect)

    def clicked(self, pos):
        # Computing size of grid
        grid_pixel_width = self.width * game_grid_size
        grid_pixel_height = self.height * game_grid_size

        # Offset to center grid in window
        offset_x = (WINDOW_WIDTH - grid_pixel_width) // 2
        offset_y = (WINDOW_HEIGHT - grid_pixel_height) // 2

        left = offset_x + self.grid_pos_x * self.width
        top = offset_y + self.grid_pos_y * self.height
        rect = pygame.Rect(left, top, self.width, self.height)
        # Returns true if pos is in rect, false otherwise
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
    print("cell_widthxheight = ", cell_width, "x", cell_height)

    # Compute neighbors at runtime

    for x in range(grid_width):
        for y in range(grid_height):
            grid_cells[x][y] = Cell(x, y, cell_width, cell_height, False)

# Define core game rules and grid updater
def progress_game(grid_cells):
    # Check grid cells based on Connoway's rules
    # WARNING: Vibe coded
    size = len(grid_cells)

    # store next state separately
    next_state = [
        [False for _ in range(size)]
        for _ in range(size)
    ]

    for x in range(size):
        for y in range(size):

            alive_neighbors = 0

            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        # Never seen this before, either
                        continue

                    nx = x + dx
                    ny = y + dy

                    # bounds check (no wrapping)
                    if 0 <= nx < size and 0 <= ny < size:
                        if grid_cells[nx][ny].status:
                            alive_neighbors += 1

            alive = grid_cells[x][y].status

            # Conway rules
            if alive:
                next_state[x][y] = alive_neighbors in (2, 3)
            else:
                next_state[x][y] = alive_neighbors == 3

    # apply results
    for x in range(size):
        for y in range(size):
            grid_cells[x][y].status = next_state[x][y]

# Define "progress one step" function
def progress_one_step(grid_cells):
    progress_game(grid_cells)

# Define "autoplay" function
def autoplay(speed, last_step_time, grid_cells):
    if speed == 0:
        print("ERROR: Autoplay called on speed 0")
    elif speed == 1:
        now = pygame.time.get_ticks()
        time_gap = now - last_step_time
        # print("time gap: ", time_gap)
        if time_gap >= 1000:
            progress_game(grid_cells)
            last_step_time = now
            # print("last, now: ", last_step_time, ", ", now)
        return last_step_time
    elif speed == 2:
        now = pygame.time.get_ticks()
        time_gap = now - last_step_time
        # print("time gap: ", time_gap)
        if time_gap >= 500:
            progress_game(grid_cells)
            last_step_time = now
            # print("last, now: ", last_step_time, ", ", now)
        return last_step_time
    elif speed == 3:
        now = pygame.time.get_ticks()
        time_gap = now - last_step_time
        # print("time gap: ", time_gap)
        if time_gap >= 250:
            progress_game(grid_cells)
            last_step_time = now
            # print("last, now: ", last_step_time, ", ", now)
        return last_step_time

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

    # Set autoplay speed variable
    autoplay_speed = 0 # 0-3 being the speeds of autoplay (eventually)
    last_step_time = 0

    # To make more user friendly (esp on mobile) (hi Jay)
    game_button_list = []

    # temp: MenuButton: def __init__(self, text, color, left, top, width, height)
    # Going to reuse menu_button because too lazy + not necessary to make whole new class and make file longer
    # Two buttons (quit and progress) either on the top or left
    # Another 3 buttons (autoplay 1, 2, 3) on the bottom or right
    # Warning: Partially vibe coded
    if WINDOW_WIDTH < WINDOW_HEIGHT:
        # Portrait mode: buttons on top and bottom strips
        btn_w = WINDOW_WIDTH // 2
        btn_h = margin_y * 2

        # Two buttons, quit and progress, on the top
        game_quit_button = MenuButton("Quit", (255, 0, 0), 0, 0, btn_w, btn_h)
        game_progress_button = MenuButton("Progress", (0, 255, 0), btn_w, 0, btn_w, btn_h)

        # Three autoplay buttons on the bottom
        btn_w3 = WINDOW_WIDTH // 3
        game_autoplay_1_button = MenuButton("Slow", (0, 255, 0), 0, WINDOW_HEIGHT - btn_h, btn_w3, btn_h)
        game_autoplay_2_button = MenuButton("Medium", (0, 255, 0), btn_w3, WINDOW_HEIGHT - btn_h, btn_w3, btn_h)
        game_autoplay_3_button = MenuButton("Fast", (0, 255, 0), btn_w3 * 2, WINDOW_HEIGHT - btn_h, btn_w3, btn_h)
    else:
        # Landscape mode: buttons on left and right strips
        btn_w = margin_x * 2
        btn_h = WINDOW_HEIGHT // 2

        # Two buttons, quit and progress, on the left
        game_quit_button = MenuButton("Quit", (255, 0, 0), 0, 0, btn_w, btn_h)
        game_progress_button = MenuButton("Progress", (0, 255, 0), 0, btn_h, btn_w, btn_h)

        # Three autoplay buttons on the right
        btn_h3 = WINDOW_HEIGHT // 3
        game_autoplay_1_button = MenuButton("Stop", (0, 255, 0), WINDOW_WIDTH - btn_w, 0, btn_w, btn_h3)
        game_autoplay_2_button = MenuButton("Slow", (0, 255, 0), WINDOW_WIDTH - btn_w, btn_h3, btn_w, btn_h3)
        game_autoplay_3_button = MenuButton("Fast", (0, 255, 0), WINDOW_WIDTH - btn_w, btn_h3 * 2, btn_w, btn_h3)

    game_button_list = [
        game_quit_button,
        game_progress_button,
        game_autoplay_1_button,
        game_autoplay_2_button,
        game_autoplay_3_button,
    ]

    # Kickoff
    global game_state
    print(game_state)
    print(game_grid_size)
    while game_state == "game":

        # For performance
        clock.tick(60)

        mouse_x, mouse_y = pygame.mouse.get_pos()

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
                        if grid_cells[x][y].clicked(mouse_pos):
                            if grid_cells[x][y].status == False:
                                grid_cells[x][y].status = True
                            else:
                                grid_cells[x][y].status = False
                for button in game_button_list:
                    if button.left <= mouse_x <= button.left + button.width and button.top <= mouse_y <= button.top + button.height:
                        if "Quit" in button.text:
                            print("QUIT")
                            game_state = "menu"
                        elif "Progress" in button.text:
                            print("PROGRESS")
                            progress_one_step(grid_cells)
                        elif "Stop" in button.text:
                            print("STOP")
                            autoplay_speed = 0
                        elif "Slow" in button.text:
                            print("SLOW")
                            autoplay_speed = 1
                        elif "Fast" in button.text:
                            print("FAST")
                            autoplay_speed = 3
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("SPACE")
                progress_one_step(grid_cells)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                print("0")
                autoplay_speed = 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                print("1")
                autoplay_speed = 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                print("2")
                autoplay_speed = 2
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                print("3")
                autoplay_speed = 3

        if autoplay_speed != 0:
            last_step_time = autoplay(autoplay_speed, last_step_time, grid_cells)

        # TODO: Add clickable buttons that change color when you hover over them
        # Checking mouse pos against button pos, setting button color accordingly
        for button in game_button_list:
            if button.left <= mouse_x <= button.left + button.width and button.top <= mouse_y <= button.top + button.height:
                button.color = button.hover_color
            else:
                button.color = button.base_color
        for button in game_button_list:
            button.draw(screen)

        for x in range(game_grid_size):
            for y in range(game_grid_size):
                # print("Drawing Cell " + str(x) + ", " + str(y))
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