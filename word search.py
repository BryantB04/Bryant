import pygame
import random
import string

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 450  # Increase height to make room for the word list at the top
GRID_SIZE = 10
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
WORD_LIST = ["monkey", "airplane", "school", "internet", "ostrich", "eel", "fish", "burger", "bear"]
LEVELS = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
current_level = 0
TOP_MARGIN = 100  # Space at the top for the word list and level

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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
        placed = False
        while not placed:
            direction = random.choice([(1, 0), (0, 1), (1, 1)])
            if direction == (1, 0):  # Horizontal
                x = random.randint(0, GRID_SIZE - len(word))
                y = random.randint(0, GRID_SIZE - 1)
            elif direction == (0, 1):  # Vertical
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - len(word))
            else:  # Diagonal
                x = random.randint(0, GRID_SIZE - len(word))
                y = random.randint(0, GRID_SIZE - len(word))

            # Check if the word fits
            fits = True
            for i in range(len(word)):
                if grid[y + i * direction[1]][x + i * direction[0]] != '':
                    fits = False
                    break

            if fits:
                for i in range(len(word)):
                    grid[y + i * direction[1]][x + i * direction[0]] = word[i]
                placed = True

    # Fill empty spaces with random letters
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == '':
                grid[y][x] = random.choice(string.ascii_lowercase)

    return grid, words

# Highlight the found words in yellow
def highlight_word(word, grid):
    directions = [(1, 0), (0, 1), (1, 1)]
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            for direction in directions:
                dx, dy = direction
                fits = True
                for i in range(len(word)):
                    if not (0 <= x + dx * i < GRID_SIZE and 0 <= y + dy * i < GRID_SIZE):
                        fits = False
                        break
                    if grid[y + dy * i][x + dx * i] != word[i]:
                        fits = False
                        break
                if fits:
                    for i in range(len(word)):
                        pygame.draw.rect(screen, YELLOW, ((x + dx * i) * CELL_SIZE, TOP_MARGIN + (y + dy * i) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        text_surface = word_font.render(word[i], True, BLACK)
                        screen.blit(text_surface, ((x + dx * i) * CELL_SIZE + 5, TOP_MARGIN + (y + dy * i) * CELL_SIZE + 5))

# Main game loop
grid, words = generate_level()
found_words = set()
input_text = ''
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if input_text in words and input_text not in found_words:
                    found_words.add(input_text)
                input_text = ''
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    # Draw the grid and words
    screen.fill(WHITE)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, TOP_MARGIN + y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            cell_content = grid[y][x]
            text_surface = font.render(cell_content, True, BLACK)
            screen.blit(text_surface, (x * CELL_SIZE + 15, TOP_MARGIN + y * CELL_SIZE + 5))

    # Display the words to find at the top
    level_text = font.render(LEVELS[current_level], True, BLACK)
    screen.blit(level_text, (10, 10))
    words_to_find_text = "Find these words: " + ", ".join(words)
    words_to_find_rendered = font.render(words_to_find_text, True, BLACK)
    screen.blit(words_to_find_rendered, (10, 40))

    # Display the input text
    input_text_rendered = font.render(input_text, True, BLACK)
    screen.blit(input_text_rendered, (10, 70))

    # Highlight found words
    for word in found_words:
        highlight_word(word, grid)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()


