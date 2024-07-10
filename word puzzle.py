import pygame
import random

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 10
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
WORD_LIST = ["monkey", "airplane", "school", "internet", "ostrich", "eel", "fish", "burger", "bear"]
LEVELS = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
current_level = 0

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Word Search Game")

# Fonts
font = pygame.font.Font(None, 30)
word_font = pygame.font.Font(None, 24)

# Generate random grid and words for the level
def generate_level():
    grid = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    words = random.sample(WORD_LIST, len(WORD_LIST))
    for word in words:
        direction = random.choice([(1, 0), (0, 1), (1, 1)])
        if direction == (1, 0):
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - len(word))
        elif direction == (0, 1):
            x = random.randint(0, GRID_SIZE - len(word))
            y = random.randint(0, GRID_SIZE - 1)
        else:
            x = random.randint(0, GRID_SIZE - len(word))
            y = random.randint(0, GRID_SIZE - len(word))
        for i in range(len(word)):
            grid[y + i * direction[1]][x + i * direction[0]] = word[i]
    return grid, words

# Highlight the found words in yellow
def highlight_word(word, grid):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == word:
                pygame.draw.rect(screen, YELLOW, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                text_surface = word_font.render(word, True, WHITE)
                screen.blit(text_surface, (x * CELL_SIZE + 5, y * CELL_SIZE + 5))

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the grid and words
    screen.fill(WHITE)
    grid, words = generate_level()
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cell_content = grid[y][x]
            pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            text_surface = font.render(cell_content, True, (0, 0, 0))
            screen.blit(text_surface, (x * CELL_SIZE + 15, y * CELL_SIZE + 15))

    # Display the words to find at the top
    level_text = font.render(LEVELS[current_level], True, (0, 0, 0))
    screen.blit(level_text, (10, 10))
    words_to_find_text = "Find these words: " + ", ".join(words)
    words_to_find_rendered = font.render(words_to_find_text, True, (0, 0, 0))
    screen.blit(words_to_find_rendered, (10, 40))

    # Highlight found words
    for word in words:
        highlight_word(word, grid)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()

