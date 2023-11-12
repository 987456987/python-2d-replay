import pygame
import json

import pygame_gui

import pygame.font

import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1024, 1024
FPS = 32
FAST_FORWARD_SPEED = 10  # Change this to your desired speed
clock = pygame.time.Clock()

frame_count = 0
start_time = pygame.time.get_ticks()

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
ct_dead_image = pygame.image.load('ctDead.png')
t_dead_image = pygame.image.load('tDead.png')
player_image = ''

currentRound = 1


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
    relative_rect=pygame.Rect((100, 940), (800, 30)),  # Position and size of the slider
    start_value=0,  # Initial value (0.0 to 1.0)
    value_range=(0, len(data[currentRound]['Tick']) - 1),  # Value range
    manager=manager,
)

# Create two buttons
prevRound = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 970), (100, 40)),  # Position and size of Button 1
    text='Previous',  # Button text
    manager=manager,
)

nextRound = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((850, 970), (100, 40)),  # Position and size of Button 2
    text='Next',  # Button text
    manager=manager,
)

# Create a text entry line
text_round = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((450, 970), (100, 40)),
    manager=manager,
)

text_round.set_text("Round: " + str(currentRound))

current_slider_value = slider.get_current_value()

# Main loop
running = True
currentTick = 0
is_animating = True
fast_forward = False  # Flag to control fast-forward

while running:
    frame_count += 1
    
    # Calculate elapsed time
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    # Check if one second has passed
    if elapsed_time >= 1000:  # 1000 milliseconds = 1 second
        # Calculate and display frame rate
        actual_frame_rate = frame_count / (elapsed_time / 1000)
        print(f"Actual Frame Rate: {actual_frame_rate:.2f} FPS")

        # Reset frame count and start time
        frame_count = 0
        start_time = current_time
    
    screen.fill((0, 0, 0))  # Fill screen with black

    # Draw map image
    screen.blit(map_image, (0, 0))

    if map_image and ct_player_image and t_player_image:
        for i in range(len(data[currentRound]['Tick'][currentTick]['PlayerPositions'])):
            
            playerAlive = False
            if data[currentRound]['Tick'][currentTick]['PlayerPositions'][i]['IsAlive']:
                playerAlive = True
            if data[currentRound]['Tick'][currentTick]['PlayerPositions'][i]['Team'] == 2:
                if playerAlive:
                    player_image = t_player_image
                else:
                    player_image = t_dead_image
            else:
                if playerAlive:
                    player_image = ct_player_image
                else:
                    player_image = ct_dead_image
            # Get coordinates and draw player image with the specified size
            player_position = transform_coordinates([
                data[currentRound]['Tick'][currentTick]['PlayerPositions'][i]['Position']['X'],
                data[currentRound]['Tick'][currentTick]['PlayerPositions'][i]['Position']['Y']
            ])
            
            # Adjust the position to center the player image within the given size
            player_position[0] -= player_image_size[0] // 2
            player_position[1] -= player_image_size[1] // 2
            
            ################### DRAW FLASH ARC ###################
            # Check for flash effect
            flash_duration = data[currentRound]['Tick'][currentTick]['PlayerPositions'][i]['FlashDuration']
            flash_duration_remaining = data[currentRound]['Tick'][currentTick]['PlayerPositions'][i]['FlashRemaining']

            if flash_duration != 0 and flash_duration_remaining != 0:
                # Calculate the position for the outer ring around the player
                flash_ring_rect = pygame.Rect(player_position[0],
                                              player_position[1],
                                              player_image_size[0], player_image_size[1])

                # Calculate the angle for the arc based on progress
                start_angle = math.radians(0)
                end_angle = math.radians(360 * (flash_duration_remaining / flash_duration))
                
                #Get Flasher Team Color
                flashArcColor = (255, 255, 255)
                if data[currentRound]['Tick'][currentTick]['PlayerPositions'][i]['FlashBy'] == 2:
                    flashArcColor = (222, 155, 53)
                if data[currentRound]['Tick'][currentTick]['PlayerPositions'][i]['FlashBy'] == 3:
                    flashArcColor = (93, 121, 174)

                # Draw the outer ring with a solid white arc
                pygame.draw.arc(screen, flashArcColor, flash_ring_rect, start_angle, end_angle, 2)
                
            ################### DRAW PLAYER ###################
            # Scale the player image with anti-aliasing
            scaled_player_image = pygame.transform.smoothscale(player_image, player_image_size)
            if playerAlive:
                # Calculate the angle of rotation (in degrees)
                rotation_angle = data[currentRound]['Tick'][currentTick]['PlayerPositions'][i]['Rotation']
            else:
                rotation_angle = 0
            # Rotate the player image
            rotated_player_image = pygame.transform.rotate(scaled_player_image, rotation_angle)

            # Get the rotated image's rect
            rotated_player_rect = rotated_player_image.get_rect()

            # Set the center of the rotated image to the player position
            rotated_player_rect.center = (player_position[0] + player_image_size[0] // 2, player_position[1] + player_image_size[1] // 2)

            # Blit the rotated image onto the screen
            screen.blit(rotated_player_image, rotated_player_rect.topleft)
            
            
            
            ################### DRAW NAME ###################
            
            # Render player's name above their head
            player_name = data[currentRound]['Tick'][currentTick]['PlayerPositions'][i]['Name']
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
            
            ################### DRAW WEAPON ###################
            
            # Render player's weapon above their head
            weapon_name = data[currentRound]['Tick'][currentTick]['PlayerPositions'][i]['Weapon']
            text_surface = font.render(weapon_name, True, (255, 255, 255))  # Color: white
            
            background_color = (0, 0, 0, 128)  # Change the alpha value to adjust transparency
            background_surface = pygame.Surface((text_surface.get_width(), text_surface.get_height()), pygame.SRCALPHA)
            background_surface.fill(background_color)

            # Calculate the position for the text and background
            text_rect = text_surface.get_rect()
            text_background_rect = background_surface.get_rect()
            text_rect.midtop = (player_position[0] + player_image_size[0] // 2, player_position[1] - 25)
            text_background_rect.midtop = text_rect.midtop

            # Blit the background and then the text onto the screen
            screen.blit(background_surface, text_background_rect)
            screen.blit(text_surface, text_rect)
            
            ################### DRAW BOMB ###################
            
            # Render bomb
            bomb = data[currentRound]['Tick'][currentTick]['PlayerPositions'][i]['Bomb']
            if bomb:
                text_surface = font.render("Bomb", True, (255, 255, 255))  # Color: white
                
                background_color = (0, 0, 0, 128)  # Change the alpha value to adjust transparency
                background_surface = pygame.Surface((text_surface.get_width(), text_surface.get_height()), pygame.SRCALPHA)
                background_surface.fill(background_color)

                # Calculate the position for the text and background
                text_rect = text_surface.get_rect()
                text_background_rect = background_surface.get_rect()
                text_rect.midtop = (player_position[0] + player_image_size[0] // 2, player_position[1] + 24)
                text_background_rect.midtop = text_rect.midtop

                # Blit the background and then the text onto the screen
                screen.blit(background_surface, text_background_rect)
                screen.blit(text_surface, text_rect)
            
            ################### DRAW SHOOT LINE ###################
            
            if data[currentRound]['Tick'][currentTick]['PlayerPositions'][i]['IsFiring']:
                # Calculate the center point of the rotated image
                center_point = rotated_player_rect.center

                # Calculate the endpoint for the line based on the player's rotation angle
                line_length = 120
                line_angle = math.radians(rotation_angle)
                line_end = (
                    center_point[0] + line_length * math.cos(line_angle),
                    center_point[1] - line_length * math.sin(line_angle)
                )

                # Calculate the offset in the direction of the line
                offset_length = 20
                offset_angle = line_angle  # Use the same angle as the line
                offset = (offset_length * math.cos(offset_angle), -offset_length * math.sin(offset_angle))

                # Calculate the new starting point for the line by adding the offset to the center point
                line_start = (center_point[0] + offset[0], center_point[1] + offset[1])

                # Draw the line on the screen
                pygame.draw.line(screen, (255, 255, 255), line_start, line_end, 1)  # Change the color and line thickness as needed
                
                

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
                    currentTick = new_slider_value
                    current_slider_value = new_slider_value
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == prevRound:
                    if currentRound != 1:
                        currentRound -= 1
                        text_round.set_text("Round: " + str(currentRound))
                        slider.set_current_value(0)
                elif event.ui_element == nextRound:
                    currentRound += 1
                    text_round.set_text("Round: " + str(currentRound))
                    slider.set_current_value(0)


    # Process events for the UI manager
    manager.process_events(event)
    # Update the UI manager
    manager.update(64)

    # Draw the UI
    manager.draw_ui(screen)

    pygame.display.flip()

    # Animation logic
    if is_animating:
        if fast_forward:
            if currentTick + FAST_FORWARD_SPEED >= len(data[currentRound]['Tick']):
                currentTick = 0
                slider.set_current_value(0)
                currentRound += 1
                text_round.set_text("Round: " + str(currentRound))
            else:
                slider.set_current_value((slider.get_current_value() + FAST_FORWARD_SPEED))
                currentTick = (slider.get_current_value() + FAST_FORWARD_SPEED)
        else:
            if currentTick + 2 >= len(data[currentRound]['Tick']):
                currentTick = 0
                slider.set_current_value(0)
                currentRound += 1
                text_round.set_text("Round: " + str(currentRound))
            else:
                slider.set_current_value((slider.get_current_value() + 2))
                currentTick = (slider.get_current_value() + 2)
            

    clock.tick(FPS)

pygame.quit()
