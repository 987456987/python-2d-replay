import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Loading Animation")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Font for loading text
font = pygame.font.Font(None, 36)

# Function to draw the loading animation
def draw_loading_animation(progress):
    screen.fill(white)  # Fill the screen with white background

    # Calculate the position for the loading text
    text = font.render("Loading... {}%".format(progress), True, black)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)

    # Calculate the position for the outer ring
    outer_ring_rect = pygame.Rect(50, 50, width - 100, height - 100)

    # Calculate the angle for the arc based on progress
    start_angle = math.radians(0)
    end_angle = math.radians(360 * progress / 100)

    # Draw the outer ring with changing color gradient
    pygame.draw.arc(screen, get_gradient_color(progress), outer_ring_rect, start_angle, end_angle, 10)

# Function to get the gradient color based on progress
def get_gradient_color(progress):
    # Calculate the color based on progress
    r = int(255 - (progress / 100) * 255)
    g = int((progress / 100) * 255)
    return r, g, 0

# Main game loop
progress = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_loading_animation(progress)

    pygame.display.flip()

    # Increment the progress for demonstration purposes
    progress += 1
    if progress > 100:
        progress = 0

    clock.tick(30)  # Cap the frame rate to 30 FPS

# Quit Pygame
pygame.quit()
sys.exit()
