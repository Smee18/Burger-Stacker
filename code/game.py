import pygame
from random import choice
import string

pygame.init()

# VARIABLES
ingredients = [
    r"../images/lettuce.png",
    r"../images/beef.png",
    r"../images/tomato.png",
    r"../images/cheese.png",
    r"../images/onion.png",
]

final_guess = ""
guess = ""
expected_text = ""
score = 0
to_display = []
game_over = False
line_speed_i = 1
frame_count = 0
current_h = 250
score_x = 1
difficulty = 3
running = True
in_menu = True

# COLORS
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

fen = pygame.display.set_mode((500, 670))

# FUNCTIONS
def display_ing(e, x, y, s):
    police = pygame.font.Font(r'../fonts/Grand9K Pixel.ttf', s)
    dessin_text1 = police.render(e, 1, NOIR)
    fen.blit(dessin_text1, (x, y))

def display_pic(name, x, y, r1, r2):
    pic = pygame.image.load(name)
    pic = pygame.transform.scale(pic, (r1, r2))
    fen.blit(pic, (x, y))

def draw_static_elements(h):
    fen.fill((222, 253, 255))  # Draw the background image
    display_pic(r"../images/plate.png", 170, h - 17, 170, 170)
    display_pic(current_request, 20, 20, 80, 80)
    display_ing(expected_text, 34, 105, 25)  # Draw the expected text
    display_ing(f"Score: {score}", 330, 20, 25)
    display_ing(guess, 400, 590, 25)
    if to_display:
        for elt in to_display:
            display_pic(elt, 196, h, 120, 120)
            h -= 15

def ingred_count(li):
    count = 0
    for _ in li:
        count += 1
    return count

def menu_burger():
    to_display.append(r"../images/bottom.png")
    for _ in range(33):
        current_request = choice(ingredients)
        to_display.append(current_request)
    to_display.append(r"../images/top.png")

def random_sentence(difficulty):
    word = ""
    for _ in range(0, difficulty):
        letter = choice(string.ascii_uppercase)
        word += letter
    return word

#MENU
menu_burger()

while in_menu:
    h = 530
    text_h = 250

    if frame_count % 30 >= 15:
        text_h = 240
    
    frame_count += 1
    fen.fill((222, 253, 255))  # Draw the background image
    display_ing("BURGER", 240, text_h - 50, 40)
    display_ing("STACKER", 240, text_h, 40)
    display_ing("Press  [B]  to start", 200, 400, 25)
    display_pic(r"../images/plate.png", 27, h-17, 170, 170)
    for elt in to_display:
        display_pic(elt, 50, h, 120, 120)
        h -= 15
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            in_menu = False
            to_display = []


# INITd

current_request = choice(ingredients)
expected_text = random_sentence(difficulty)
to_display.append(r"../images/bottom.png")
draw_static_elements(current_h)
pygame.display.flip()


# LOOP
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()

        # Handle typing input
        if event.type == pygame.TEXTINPUT and not game_over:
            guess += event.text.upper()
            draw_static_elements(current_h)
            pygame.display.flip()
            if len(guess) == len(expected_text):
                final_guess = guess

        # Handle reset
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            # Reset all game variables
            score = 0
            to_display = []
            game_over = False
            line_speed_i = 1
            frame_count = 0
            current_h = 250
            score_x = 1
            difficulty = 3
            guess = ""
            final_guess = ""
            current_request = choice(ingredients)
            expected_text = random_sentence(difficulty)
            to_display.append(r"../images/bottom.png")
            pygame.event.clear(pygame.TEXTINPUT)
            draw_static_elements(current_h)
            pygame.display.flip()

    # Only process gameplay if not game over
    if not game_over:
        # Adjust difficulty/speed scaling
        if score >= 100:
            line_speed_i = 4
            score_x = 2
        elif score >= 2000:
            line_speed_i = 7
            score_x = 3

        # Drop ingredients downward over time
        if frame_count % 1000 == 0:
            current_h += 0.5 * line_speed_i
            draw_static_elements(current_h)
            pygame.display.flip()

        frame_count += 1

        # Correct guess
        if final_guess == expected_text and len(final_guess) == len(expected_text):
            guess = ""
            final_guess = ""
            to_display.append(current_request)
            current_request = choice(ingredients)
            expected_text = random_sentence(difficulty)
            score += 10 * score_x
            difficulty = len(str(score)) + 1
            draw_static_elements(current_h)
            pygame.display.flip()

        # Wrong guess
        elif len(guess) == len(expected_text) and final_guess != expected_text:
            current_h += 20
            draw_static_elements(current_h)
            pygame.display.flip()
            guess = ""
            final_guess = ""

        # Game Over condition
        elif current_h - (20 * ingred_count(to_display)) >= 640:
            to_display.append(r"../images/top.png")
            # Animate burger stack moving up
            while current_h > 500:
                draw_static_elements(current_h)
                display_ing("Game Over", 170, 220, 25)
                display_ing(f"Score: {score}", 170, 260, 25)
                display_ing(f"[R] to Retry", 170, 300, 25)
                current_h -= 1
                pygame.display.flip()
            game_over = True


pygame.quit()
