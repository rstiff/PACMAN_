import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 560
SCREEN_HEIGHT = 620
CELL_SIZE = 20
FPS = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Yellow color

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Multiplayer")

font = pygame.font.SysFont('Arial', 18)

# Game board (same as in the original code)
board = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "######.##### ## #####.######",
    "######.##          ##.######",
    "######.## ###--### ##.######",
    "######.## #      # ##.######",
    "       ## #      # ##       ",
    "######.## #      # ##.######",
    "######.## ######## ##.######",
    "######.##          ##.######",
    "######.## ######## ##.######",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#o..##................##..o#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################"
]

# Load images
pacman_img = pygame.image.load('assets/pacman.png')
ghost_imgs = [
    pygame.image.load('assets/yellow.png'),
    pygame.image.load('assets/red.png'),
    pygame.image.load('assets/blue.png'),
    pygame.image.load('assets/pink.png')
]

# Scale images to fit cell size
pacman_img = pygame.transform.scale(pacman_img, (CELL_SIZE, CELL_SIZE))
for i in range(len(ghost_imgs)):
    ghost_imgs[i] = pygame.transform.scale(ghost_imgs[i], (CELL_SIZE, CELL_SIZE))

# Menu variables
menu_active = True
try:
    logo_img = pygame.image.load('assets/pacmanlogo.png')  # Ensure the file path is correct
except pygame.error as e:
    print(f"Error loading logo: {e}")
    logo_img = None  # Fallback if the logo can't be loaded
logo_rect = logo_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)) if logo_img else None
start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 75, 200, 50)

# Initialize game variables
def reset_game():
    global pacman_x1, pacman_y1, pacman_x2, pacman_y2, pacman_direction1, pacman_direction2, score, ghosts, board
    pacman_x1, pacman_y1 = 1, 1  # Starting position of Player 1
    pacman_x2, pacman_y2 = 2, 1  # Starting position of Player 2 (slightly offset)
    pacman_direction1 = 'RIGHT'  # Default movement direction for Player 1
    pacman_direction2 = 'RIGHT'  # Default movement direction for Player 2
    score = 0  # Initial score

    # Reset ghosts
    ghosts = [
        {'x': 9, 'y': 9},  # First ghost
        {'x': 10, 'y': 10},  # Second ghost
        {'x': 11, 'y': 11},  # Third ghost
        {'x': 12, 'y': 12}   # Fourth ghost
    ]

    # Reload the board to restore pellets
    board = [
        "############################",
        "#............##............#",
        "#.####.#####.##.#####.####.#",
        "#o####.#####.##.#####.####o#",
        "#.####.#####.##.#####.####.#",
        "#..........................#",
        "#.####.##.########.##.####.#",
        "#.####.##.########.##.####.#",
        "#......##....##....##......#",
        "######.##### ## #####.######",
        "######.##### ## #####.######",
        "######.##          ##.######",
        "######.## ###--### ##.######",
        "######.## #      # ##.######",
        "       ## #      # ##       ",
        "######.## #      # ##.######",
        "######.## ######## ##.######",
        "######.##          ##.######",
        "######.## ######## ##.######",
        "######.## ######## ##.######",
        "#............##............#",
        "#.####.#####.##.#####.####.#",
        "#.####.#####.##.#####.####.#",
        "#o..##................##..o#",
        "###.##.##.########.##.##.###",
        "###.##.##.########.##.##.###",
        "#......##....##....##......#",
        "#.##########.##.##########.#",
        "#.##########.##.##########.#",
        "#..........................#",
        "############################"
    ]

# Initialize game variables
reset_game()

def draw_board():
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Draw walls
            elif cell == '.':
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 3)  # Draw pellets
            elif cell == 'o':
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 7)  # Draw power pellets

def draw_pacman():
    screen.blit(pacman_img, (pacman_x1 * CELL_SIZE, pacman_y1 * CELL_SIZE))  # Draw Player 1 Pac-Man
    screen.blit(pacman_img, (pacman_x2 * CELL_SIZE, pacman_y2 * CELL_SIZE))  # Draw Player 2 Pac-Man

def draw_ghosts():
    for i, ghost in enumerate(ghosts):
        screen.blit(ghost_imgs[i], (ghost['x'] * CELL_SIZE, ghost['y'] * CELL_SIZE))  # Draw ghosts

def move_pacman():
    global pacman_x1, pacman_y1, pacman_x2, pacman_y2, score
    # Player 1 movement
    if pacman_direction1 == 'LEFT' and board[pacman_y1][pacman_x1 - 1] != '#':
        pacman_x1 -= 1
    elif pacman_direction1 == 'RIGHT' and board[pacman_y1][pacman_x1 + 1] != '#':
        pacman_x1 += 1
    elif pacman_direction1 == 'UP' and board[pacman_y1 - 1][pacman_x1] != '#':
        pacman_y1 -= 1
    elif pacman_direction1 == 'DOWN' and board[pacman_y1 + 1][pacman_x1] != '#':
        pacman_y1 += 1
    
    # Player 2 movement
    if pacman_direction2 == 'LEFT' and board[pacman_y2][pacman_x2 - 1] != '#':
        pacman_x2 -= 1
    elif pacman_direction2 == 'RIGHT' and board[pacman_y2][pacman_x2 + 1] != '#':
        pacman_x2 += 1
    elif pacman_direction2 == 'UP' and board[pacman_y2 - 1][pacman_x2] != '#':
        pacman_y2 -= 1
    elif pacman_direction2 == 'DOWN' and board[pacman_y2 + 1][pacman_x2] != '#':
        pacman_y2 += 1

    # Check if any Pac-Man eats a pellet
    if board[pacman_y1][pacman_x1] == '.':
        board[pacman_y1] = board[pacman_y1][:pacman_x1] + ' ' + board[pacman_y1][pacman_x1 + 1:]
        score += 10
    elif board[pacman_y1][pacman_x1] == 'o':
        board[pacman_y1] = board[pacman_y1][:pacman_x1] + ' ' + board[pacman_y1][pacman_x1 + 1:]
        score += 50

    if board[pacman_y2][pacman_x2] == '.':
        board[pacman_y2] = board[pacman_y2][:pacman_x2] + ' ' + board[pacman_y2][pacman_x2 + 1:]
        score += 10
    elif board[pacman_y2][pacman_x2] == 'o':
        board[pacman_y2] = board[pacman_y2][:pacman_x2] + ' ' + board[pacman_y2][pacman_x2 + 1:]
        score += 50

def move_ghosts():
    for ghost in ghosts:
        direction = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        if direction == 'LEFT' and board[ghost['y']][ghost['x'] - 1] != '#':
            ghost['x'] -= 1
        elif direction == 'RIGHT' and board[ghost['y']][ghost['x'] + 1] != '#':
            ghost['x'] += 1
        elif direction == 'UP' and board[ghost['y'] - 1][ghost['x']] != '#':
            ghost['y'] -= 1
        elif direction == 'DOWN' and board[ghost['y'] + 1][ghost['x']] != '#':
            ghost['y'] += 1

def check_collisions():
    # Check if any Pac-Man collides with a ghost
    for ghost in ghosts:
        if (ghost['x'] == pacman_x1 and ghost['y'] == pacman_y1) or (ghost['x'] == pacman_x2 and ghost['y'] == pacman_y2):
            return True
    return False

def check_all_pellets_eaten():
    for row in board:
        if '.' in row or 'o' in row:
            return False
    return True

def draw_game():
    screen.fill(BLACK)
    draw_board()
    draw_pacman()
    draw_ghosts()

    # Display the score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 30))

def game_loop():
    global pacman_direction1, pacman_direction2, score, ghosts
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Player 1 controls (Arrow keys)
                if event.key == pygame.K_LEFT:
                    pacman_direction1 = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    pacman_direction1 = 'RIGHT'
                elif event.key == pygame.K_UP:
                    pacman_direction1 = 'UP'
                elif event.key == pygame.K_DOWN:
                    pacman_direction1 = 'DOWN'

                # Player 2 controls (WASD)
                elif event.key == pygame.K_a:
                    pacman_direction2 = 'LEFT'
                elif event.key == pygame.K_d:
                    pacman_direction2 = 'RIGHT'
                elif event.key == pygame.K_w:
                    pacman_direction2 = 'UP'
                elif event.key == pygame.K_s:
                    pacman_direction2 = 'DOWN'

        move_pacman()
        move_ghosts()

        if check_collisions():
            print("Game Over!")
            return  # End the game and go back to the menu

        if check_all_pellets_eaten():
            print("You Win!")
            return  # End the game and go back to the menu

        draw_game()
        pygame.display.flip()
        clock.tick(FPS)

def draw_menu():
    screen.fill(BLACK)

    if logo_img:
        logo_width = 300
        logo_height = int(logo_img.get_height() * (logo_width / logo_img.get_width()))
        logo_img_resized = pygame.transform.scale(logo_img, (logo_width, logo_height))
        logo_rect = logo_img_resized.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(logo_img_resized, logo_rect)

    welcome_text = font.render("Welcome to Pac-Man Multiplayer", True, WHITE)
    welcome_rect = welcome_text.get_rect(center=(SCREEN_WIDTH // 2, logo_rect.bottom + 0))
    screen.blit(welcome_text, welcome_rect)
    
    pygame.draw.rect(screen, YELLOW, start_button)
    pygame.draw.rect(screen, YELLOW, quit_button)

    start_text = font.render("Start", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)

    screen.blit(start_text, (start_button.centerx - start_text.get_width() // 2, start_button.centery - start_text.get_height() // 2))
    screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

    pygame.display.flip()

def menu():
    global menu_active
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    reset_game()  # Reset game state when starting a new game
                    game_loop()  # Start a new game loop
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        draw_menu()

# Start menu loop
menu()

pygame.quit()
sys.exit()
