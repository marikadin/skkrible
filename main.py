import pygame
import json
import random
import sys
import time

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 600
screen_height = 500  # Increased height to make room for the chat box
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Drawing App with Chat")

# Load words from "words.json"
with open('words.json', 'r') as file:
    data = json.load(file)
    words = data['drawable_words']

# Randomly select 3 words
random_words = random.sample(words, 3)

# Button settings
button_width = 200
button_height = 50
button_color = (100, 200, 255)
text_color = (0, 0, 0)
font = pygame.font.Font(None, 36)

# Set up the input box for chat
input_box = pygame.Rect(20, screen_height - 50, screen_width - 40, 40)
text = ''
messages = []


# Function to draw text on buttons
def draw_button(text, x, y):
    pygame.draw.rect(screen, button_color, (x, y, button_width, button_height))
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + button_width // 2, y + button_height // 2))
    screen.blit(text_surface, text_rect)


# Function to draw chat input box
def draw_input_box():
    pygame.draw.rect(screen, (255, 255, 255), input_box)
    txt_surface = font.render(text, True, text_color)
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))


# Function to draw messages in the chat
def draw_messages():
    y_offset = 20
    for message in messages:
        txt_surface = font.render(message, True, text_color)
        screen.blit(txt_surface, (20, y_offset))
        y_offset += 40


# Function to handle drawing app
def drawing_app():
    drawing = False
    last_pos = None
    drawn_lines = []  # List to store drawn lines
    running = True
    start_time = time.time()
    while running and start_time - time.time() > -60:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                last_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    pygame.draw.line(screen, (0, 0, 0), last_pos, event.pos, 5)
                    drawn_lines.append((last_pos, event.pos))  # Store the line
                    last_pos = event.pos

        # Redraw all the lines stored in drawn_lines list
        for line in drawn_lines:
            pygame.draw.line(screen, (0, 0, 0), line[0], line[1], 5)

        pygame.display.flip()


# Main loop
running = True
in_drawing_mode = False
while running:
    screen.fill((255, 255, 255))  # Fill screen with a background color

    if not in_drawing_mode:
        # Draw buttons for the 3 random words
        for i, word in enumerate(random_words):
            draw_button(word, 50, 50 + i * (button_height + 20))

    draw_messages()  # Draw chat messages
    draw_input_box()  # Draw the input box for chat

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for i, word in enumerate(random_words):
                if 50 < mouse_x < 50 + button_width and 50 + i * (button_height + 20) < mouse_y < 50 + i * (
                        button_height + 20) + button_height:
                    print(f"Button clicked: {word}")
                    in_drawing_mode = True
                    screen.fill((255, 255, 255))
                    drawing_app()
                    in_drawing_mode = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Send the message when Enter is pressed
                if text:
                    messages.append(text)
                    text = ''  # Clear the input box after sending
            elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                text = text[:-1]
            else:
                text += event.unicode  # Append typed character to the text

    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()