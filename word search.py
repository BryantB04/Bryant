import pygame
import random
import string

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

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
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Word Search Game")

# Fonts
font = pygame.font.Font(None, 30)
word_font = pygame.font.Font(None, 24)

# Load background music
pygame.mixer.music.load('background music.mp3')  
pygame.mixer.music.play(-1)  # Play the music in a loop

# Load click sound effect
click_sound = pygame.mixer.Sound('Click - Sound Effect (HD).mp3')  # Ensure this file exists

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

# Display the starting screen
def display_start_screen():
    screen.fill(WHITE)
    title_text = font.render("Word Search Game", True, BLACK)
    start_text = font.render("Press ENTER to Start", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    pygame.display.flip()

# Main game loop
def main():
    global current_level
    grid, words = generate_level()
    found_words = set()
    selected_cells = []
    running = True
    show_start_screen = True

    while running:
        if show_start_screen:
            display_start_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        show_start_screen = False
            continue

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if mouse_y >= TOP_MARGIN:
                    cell_x = mouse_x // CELL_SIZE
                    cell_y = (mouse_y - TOP_MARGIN) // CELL_SIZE
                    if (cell_x, cell_y) not in selected_cells:
                        selected_cells.append((cell_x, cell_y))
                        # Play click sound
                        click_sound.play()
                    else:
                        selected_cells.remove((cell_x, cell_y))

        # Check if selected cells form a word
        if selected_cells:
            selected_word = ''.join([grid[y][x] for x, y in selected_cells])
            if selected_word in words and selected_word not in found_words:
                found_words.add(selected_word)
                selected_cells = []

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

        y_offset = 40
        max_line_width = SCREEN_WIDTH - 20  # Allow for padding
        line = ""
        for i, word in enumerate(words):
            if i == len(words) - 1:
                line += word
            elif font.size(line + word + ", ")[0] > max_line_width:
                words_to_find_rendered = font.render(line, True, BLACK)
                screen.blit(words_to_find_rendered, (10, y_offset))
                y_offset += 30
                line = word + ", "
            else:
                line += word + ", "
        if line:  # Render the last line if any
            words_to_find_rendered = font.render(line, True, BLACK)
            screen.blit(words_to_find_rendered, (10, y_offset))

        # Highlight found words
        for word in found_words:
            highlight_word(word, grid)

        # Highlight selected cells in red
        for cell_x, cell_y in selected_cells:
            pygame.draw.rect(screen, RED, (cell_x * CELL_SIZE, TOP_MARGIN + cell_y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)  

        # Update the display
        pygame.display.flip()

    pygame.quit()

# Start the game
main()

