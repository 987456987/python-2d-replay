import pygame
import json

import pygame_gui

import pygame.font

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1024, 1024
FPS = 200
FAST_FORWARD_SPEED = 100  # Change this to your desired speed
clock = pygame.time.Clock()

# font and size
font = pygame.font.Font(None, 16)

# Load JSON data
with open('round_data.json') as f:
    data = json.load(f)

# Initialize Pygame window and canvas
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('csReplay')

# Load images
map_image = pygame.image.load('de_ancient.png')
ct_player_image = pygame.image.load('ctPlayer.png')
t_player_image = pygame.image.load('tPlayer.png')
player_image = ''

currentRound = 4


# Set the desired player image size
player_image_size = (30, 30)  # Change the size as needed

# Function to transform coordinates
def transform_coordinates(original_coords):
    scale = 1024 / 5100
    x_offset = 2950
    y_offset = 2950
    x_new = (original_coords[0] + x_offset) * scale
    y_new = 1024 - (original_coords[1] + y_offset) * scale
    return [x_new, y_new]

# Create a UI manager for the GUI elements
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Create a slider
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((100, 100), (800, 20)),  # Position and size of the slider
    start_value=0,  # Initial value (0.0 to 1.0)
    value_range=(0, len(data[currentRound]['Tick']) - 1),  # Value range
    manager=manager,
)

# Initialize the current_slider_value to the initial value of the slider
current_slider_value = slider.get_current_value()

# Main loop
running = True
position = 0
is_animating = True
fast_forward = False  # Flag to control fast-forward

while running:
    screen.fill((0, 0, 0))  # Fill screen with black

    # Draw map image
    screen.blit(map_image, (0, 0))

    if map_image and ct_player_image and t_player_image:
        for i in range(10):
            if data[currentRound]['Tick'][position]['PlayerPositions'][i]['IsAlive']:
                if data[currentRound]['Tick'][position]['PlayerPositions'][i]['Team'] == 2:
                    player_image = t_player_image
                else:
                    player_image = ct_player_image
                # Get coordinates and draw player image with the specified size
                player_position = transform_coordinates([
                    data[currentRound]['Tick'][position]['PlayerPositions'][i]['Position']['X'],
                    data[currentRound]['Tick'][position]['PlayerPositions'][i]['Position']['Y']
                ])
                

                # Adjust the position to center the player image within the given size
                player_position[0] -= player_image_size[0] // 2
                player_position[1] -= player_image_size[1] // 2

                # Scale the player image with anti-aliasing
                scaled_player_image = pygame.transform.smoothscale(player_image, player_image_size)

                # Calculate the angle of rotation (in degrees)
                rotation_angle = data[currentRound]['Tick'][position]['PlayerPositions'][i]['Rotation']

                # Rotate the player image
                rotated_player_image = pygame.transform.rotate(scaled_player_image, rotation_angle)

                # Get the rotated image's rect
                rotated_player_rect = rotated_player_image.get_rect()

                # Set the center of the rotated image to the player position
                rotated_player_rect.center = (player_position[0] + player_image_size[0] // 2, player_position[1] + player_image_size[1] // 2)

                # Blit the rotated image onto the screen
                screen.blit(rotated_player_image, rotated_player_rect.topleft)
                
               # Render player's name above their head
                player_name = data[currentRound]['Tick'][position]['PlayerPositions'][i]['Name']
                text_surface = font.render(player_name, True, (255, 255, 255))  # Color: white
                
                background_color = (0, 0, 0, 128)  # Change the alpha value to adjust transparency
                background_surface = pygame.Surface((text_surface.get_width(), text_surface.get_height()), pygame.SRCALPHA)
                background_surface.fill(background_color)

                # Calculate the position for the text and background
                text_rect = text_surface.get_rect()
                text_background_rect = background_surface.get_rect()
                text_rect.midtop = (player_position[0] + player_image_size[0] // 2, player_position[1] - 12)
                text_background_rect.midtop = text_rect.midtop

                # Blit the background and then the text onto the screen
                screen.blit(background_surface, text_background_rect)
                screen.blit(text_surface, text_rect)

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

        # Check for slider value change event
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                new_slider_value = slider.get_current_value()
                if new_slider_value != current_slider_value:
                    position = new_slider_value
                    current_slider_value = new_slider_value

    # Process events for the UI manager
    manager.process_events(event)
    # Update the UI manager
    manager.update(30)

    # Draw the UI
    manager.draw_ui(screen)

    pygame.display.flip()

    # Animation logic
    # if is_animating:
    #     if fast_forward:
    #         position = (position + FAST_FORWARD_SPEED) % len(data[8]['Tick'])
    #     else:
    #         position = (position + 1) % len(data[8]['Tick'])
    #     print(position)

    clock.tick(FPS)

pygame.quit()
