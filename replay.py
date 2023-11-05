import pygame
import json

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1024, 1024
FPS = 200
FAST_FORWARD_SPEED = 100  # Change this to your desired speed
clock = pygame.time.Clock()

# Load JSON data
with open('round_data.json') as f:
    data = json.load(f)

# Initialize Pygame window and canvas
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('csReplay')

# Load images
map_image = pygame.image.load('de_ancient.png')
player_image = pygame.image.load('player.png')

# Set the desired player image size
player_image_size = (16, 16)  # Change the size as needed

# Function to transform coordinates
def transform_coordinates(original_coords):
    scale = 1024 / 5100
    x_offset = 2900
    y_offset = 3000
    x_new = (original_coords[0] + x_offset) * scale
    y_new = 1024 - (original_coords[1] + y_offset) * scale
    return [x_new, y_new]

# Main loop
running = True
position = 0
is_animating = True
fast_forward = False  # Flag to control fast-forward

while running:
    screen.fill((0, 0, 0))  # Fill screen with black

    # Draw map image
    screen.blit(map_image, (0, 0))

    if map_image and player_image:
        for i in range(10):
            # Get coordinates and draw player image with the specified size
            player_position = transform_coordinates([
                data[12]['Tick'][position]['PlayerPositions'][i]['Position']['X'],
                data[12]['Tick'][position]['PlayerPositions'][i]['Position']['Y']
            ])

            # Adjust the position to center the player image within the given size
            player_position[0] -= player_image_size[0] // 2
            player_position[1] -= player_image_size[1] // 2

            # Scale the player image with anti-aliasing
            scaled_player_image = pygame.transform.smoothscale(player_image, player_image_size)

            screen.blit(scaled_player_image, (player_position[0], player_position[1]))

        # Update display
        pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                fast_forward = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                fast_forward = False

    # Animation logic
    if is_animating:
        if fast_forward:
            position = (position + FAST_FORWARD_SPEED) % len(data[12]['Tick'])
        else:
            position = (position + 1) % len(data[12]['Tick'])
        print(position)

    clock.tick(FPS)

pygame.quit()
