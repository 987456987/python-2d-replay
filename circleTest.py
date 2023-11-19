import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Vertical Gradient Circle')

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set up circle parameters
radius = 50
thickness = 5

# Set up gradient variable (0 to 100)
percent = 20  # Adjust this value for the vertical gradient

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill(black)

    # Draw the white outline circle
    pygame.draw.circle(screen, white, (width // 2, height // 2), radius, thickness)

    # Calculate the fill height based on the percent
    fill_height = int((percent / 100) * (2 * radius))

    # Draw the vertical gradient fill within the circle
    for y in range(height // 2 - radius + thickness, height // 2 - radius + thickness + fill_height):
        # Calculate the distance from the center of the circle
        distance_to_center = abs(y - (height // 2))
        # Calculate the maximum alpha value based on the distance
        max_alpha = int((distance_to_center / fill_height) * 255)
        # Calculate the alpha value for the current position
        alpha = min(max_alpha, 255)
        alpha = max(0, alpha)  # Ensure alpha is in the range [0, 255]
        color = (255, 255, 255, alpha)

        # Calculate the start and end points for each line based on the current y position
        line_start = (width // 2 - int(math.sqrt(radius ** 2 - (y - height // 2 + radius - thickness) ** 2)), y)
        line_end = (width // 2 + int(math.sqrt(radius ** 2 - (y - height // 2 + radius - thickness) ** 2)), y)

        # Draw the line only within the circle
        pygame.draw.line(screen, color, line_start, line_end, 1)

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    pygame.time.Clock().tick(60)
