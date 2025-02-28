import socket
import threading
import pygame
import sys
import json

pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Drawing App Client")

font = pygame.font.Font(None, 36)
input_box = pygame.Rect(20, screen_height - 50, screen_width - 40, 40)
text = ''
messages = []
drawing_data = []
is_drawing = False

# Client connection settings
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Ask for player's name
name = input("Enter your name: ")
client_socket.sendall(name.encode())

# Receiving thread
def receive_messages():
    global drawing_data, can_draw
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            if "DRAW:" in data:
                points = json.loads(data.replace("DRAW:", ""))
                drawing_data.append(points)
            elif "DRAWER:" in data:
                can_draw = data.split(":")[1] == name  # Assign drawer role
            else:
                messages.append(data)
        except:
            break

threading.Thread(target=receive_messages, daemon=True).start()

def draw_lines():
    for line in drawing_data:
        pygame.draw.line(screen, (0, 0, 0), tuple(line[0]), tuple(line[1]), 5)

def main_client():
    global text, is_drawing, can_draw
    clock = pygame.time.Clock()
    running = True
    last_pos = None
    can_draw = False  # Determines if this client is the drawer

    while running:
        screen.fill((255, 255, 255))
        draw_lines()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                client_socket.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if text:
                        client_socket.sendall(text.encode())
                        text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            elif can_draw and event.type == pygame.MOUSEBUTTONDOWN:
                is_drawing = True
                last_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                is_drawing = False
            elif event.type == pygame.MOUSEMOTION and is_drawing:
                if last_pos:
                    pygame.draw.line(screen, (0, 0, 0), last_pos, event.pos, 5)
                    drawing_data.append((last_pos, event.pos))
                    client_socket.sendall(f"DRAW:{json.dumps([last_pos, event.pos])}".encode())
                    last_pos = event.pos

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_client()
