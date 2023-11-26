import pygame
import json

import pygame_gui

import pygame.font

import math

from scoreboard import draw_scoreboard

from weapontable import weapon_icon_table
from mapTable import map_table

import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1300, 950
mapWIDTH, mapHEIGHT = 900, 900
mapOFFSET = 400
FPS = 32
PLAYBACK_SPEED = 2 
clock = pygame.time.Clock()

frame_count = 0
start_time = pygame.time.get_ticks()

# font and size
font = pygame.font.Font(None, 16)
fontMed = pygame.font.Font(None, 28)
fontLarge = pygame.font.Font(None, 32)
fontWeapons = pygame.font.Font("assets/custom_csgo_icons.ttf", 14)
fontMedWeapons = pygame.font.Font("assets/custom_csgo_icons.ttf", 20)
fontLargeWeapons = pygame.font.Font("assets/custom_csgo_icons.ttf", 26)


ctColor = (93, 121, 174)
tColor = (222, 155, 53)

# Load JSON data using the command-line argument
if len(sys.argv) < 2:
    print("Usage: python replay.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path) as f:
    data = json.load(f)

# Initialize Pygame window and canvas
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2D Replay')


gameData = data["GameData"]

demoMap = data["MapName"]

# Load images
map_image = pygame.image.load('assets/maps/' + demoMap + '.png')
ct_player_image = pygame.image.load('assets/ctPlayer.png')
t_player_image = pygame.image.load('assets/tPlayer.png')
ct_dead_image = pygame.image.load('assets/ctDead.png')
t_dead_image = pygame.image.load('assets/tDead.png')
player_image = ''

currentRound = 0

# Set the desired player image size
player_image_size = (28, 28)  # Change the size as needed

# Function to transform coordinates
def transform_coordinates(original_coords):
    conversionCoord = map_table.get(demoMap)
    scale = mapWIDTH / conversionCoord[0]
    x_offset = conversionCoord[1]
    y_offset = conversionCoord[2]
    x_new = (original_coords[0] + x_offset) * scale
    y_new = mapWIDTH - (original_coords[1] + y_offset) * scale
    return [x_new + mapOFFSET, y_new]

# Create a UI manager for the GUI elements
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

round_buttons = []

roundButtonWidth = int(900/len(gameData))
if len(gameData) < 25 :
    roundButtonWidth = int(900/len(gameData))
else:
    roundButtonWidth = int(900/24)

# Create buttons for each round
for i in range(len(gameData)):
    if i < 24:
        round_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400 + i * roundButtonWidth, 920), (roundButtonWidth, 30)),
            text=str(i + 1),
            manager=manager,
        )
        round_buttons.append(round_button)

# Create a slider
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((480, 880), (720, 30)),  # Position and size of the slider
    start_value=0,  # Initial value (0.0 to 1.0)
    value_range=(0, len(gameData[currentRound]['Tick']) - 1),  # Value range
    manager=manager,
)

# Create two buttons
pausePlay = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((400, 880), (80, 30)),  # Position and size of Button 1
    text='Play',  # Button text
    manager=manager,
)
# Create two buttons
prevRound = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((1200, 880), (50, 30)),  # Position and size of Button 1
    text='<',  # Button text
    manager=manager,
)

nextRound = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((1250, 880), (50, 30)),  # Position and size of Button 2
    text='>',  # Button text
    manager=manager,
)

#Speed Buttons
speedOne = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((400, 850), (40, 30)),  # Position and size of Button 2
    text='1x',  # Button text
    manager=manager,
)
speedTwo = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((440, 850), (40, 30)),  # Position and size of Button 2
    text='2x',  # Button text
    manager=manager,
)
speedFour = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((480, 850), (40, 30)),  # Position and size of Button 2
    text='4x',  # Button text
    manager=manager,
)
speedEight = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((520, 850), (40, 30)),  # Position and size of Button 2
    text='8x',  # Button text
    manager=manager,
) 


# Create a text entry line
text_round = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((1200, 850), (100, 30)),
    manager=manager,
)

text_round.set_text("Round: " + str(currentRound + 1))

current_slider_value = slider.get_current_value()

# Main loop
running = True
currentTick = 0
is_animating = False
fast_forward = False  # Flag to control fast-forward

while running:
    frame_count += 1
    
    slider.value_range=(0, len(gameData[currentRound]['Tick']) - 3)
    
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
    
    screen.fill((25, 23, 30))  # Fill screen with black
    
    # Draw the overlay surfaces for each round button
    for i, button in enumerate(round_buttons):
        overlay_surface = pygame.Surface((roundButtonWidth - 4, 10), pygame.SRCALPHA)
        if gameData[i]['Winner'] == 2:
            overlay_surface.fill(tColor)
        if gameData[i]['Winner'] == 3:
            overlay_surface.fill(ctColor)
        screen.blit(overlay_surface, (402 + i * roundButtonWidth, 910))
    
    # Draw overlay surface for playback speed
    playbackPos = 400
    if PLAYBACK_SPEED == 4:
        playbackPos = 440
    if PLAYBACK_SPEED == 8:
        playbackPos = 480
    if PLAYBACK_SPEED == 16:
        playbackPos = 540
    overlay_surface = pygame.Surface((40, 10), pygame.SRCALPHA)
    screen.blit(overlay_surface, (playbackPos, 880))

    # Draw map image
    scaled_image = pygame.transform.scale(map_image, (mapWIDTH, mapHEIGHT))
    screen.blit(scaled_image, (400, 0))
    # Sort array so that players are always rendered in the same order to avoid flickering
    playerArrayAlphabet = sorted(gameData[currentRound]['Tick'][currentTick]['PlayerPositions'], key=lambda x: x["Name"])
    
    # Then, sort based on the 'IsAlive' property (True on top)
    playerArray = sorted(playerArrayAlphabet, key=lambda x: x["IsAlive"])
    
    #Retrieve MatchInfo
    matchInfo = gameData[currentRound]['Tick'][currentTick]['MatchInfo']
    

    if map_image and ct_player_image and t_player_image:
        for i in range(len(playerArray)):
            
            color = ""
            
            playerAlive = playerArray[i]['IsAlive']
            if playerArray[i]['Team'] == 2:
                color = tColor
                if playerAlive:
                    player_image = t_player_image
                else:
                    player_image = t_dead_image
            else:
                color = ctColor
                if playerAlive:
                    player_image = ct_player_image
                else:
                    player_image = ct_dead_image
            # Get coordinates and draw player image with the specified size
            player_position = transform_coordinates([
                playerArray[i]['Position']['X'],
                playerArray[i]['Position']['Y']
            ])
            
            # Adjust the position to center the player image within the given size
            player_position[0] -= player_image_size[0] // 2
            player_position[1] -= player_image_size[1] // 2
            
            ################### DRAW FLASH ARC ###################
            # Check for flash effect
            flash_duration = playerArray[i]['FlashDuration']
            flash_duration_remaining = playerArray[i]['FlashRemaining']

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
                if playerArray[i]['FlashBy'] == 2:
                    flashArcColor = (222, 155, 53)
                if playerArray[i]['FlashBy'] == 3:
                    flashArcColor = (93, 121, 174)

                # Draw the outer ring with a solid white arc
                pygame.draw.arc(screen, flashArcColor, flash_ring_rect, start_angle, end_angle, 2)
                
            ################### DRAW PLAYER ###################
            # Scale the player image with anti-aliasing
            scaled_player_image = pygame.transform.smoothscale(player_image, player_image_size)
            if playerAlive:
                # Calculate the angle of rotation (in degrees)
                rotation_angle = playerArray[i]['Rotation']
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
            player_name = playerArray[i]['Name']
            text_surface = font.render(player_name, True, color)  # Color: white
            
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
            if playerArray[i]["IsAlive"]:
                # Render player's weapon above their head
                weapon_name = playerArray[i]['Weapon']
                # print(weapon_name)
                icon = weapon_icon_table.get(weapon_name, "Unknown")
                text_surface = fontWeapons.render(icon, True, color)  # Color: white
                
                background_color = (0, 0, 0, 128)  # Change the alpha value to adjust transparency
                background_surface = pygame.Surface((text_surface.get_width(), text_surface.get_height()), pygame.SRCALPHA)
                background_surface.fill((0, 0, 0, 50))

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
            bomb = playerArray[i]['Bomb']
            if bomb:
                icon = weapon_icon_table.get("C4", "Unknown")
                text_surface = fontWeapons.render(icon, True, (255,255,255))  # Color: white
                
                background_color = (0, 0, 0, 0)  # Change the alpha value to adjust transparency
                background_surface = pygame.Surface((text_surface.get_width(), text_surface.get_height()), pygame.SRCALPHA)
                background_surface.fill(background_color)

                # Calculate the position for the text and background
                text_rect = text_surface.get_rect()
                text_background_rect = background_surface.get_rect()
                text_rect.midtop = ((player_position[0] + player_image_size[0] // 2) + 5, player_position[1] + 14)
                text_background_rect.midtop = text_rect.midtop

                # Blit the background and then the text onto the screen
                screen.blit(background_surface, text_background_rect)
                screen.blit(text_surface, text_rect)
            
            ################### DRAW SHOOT LINE ###################
            
            if playerArray[i]['IsFiring']:
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
        
        
                
        ################### Bomb On Ground ###################
        if matchInfo['BombOnGround']:
            bombPosition = matchInfo['BombPosition']
            icon = weapon_icon_table.get("C4", "Unknown")
            if matchInfo['BombState'] == 0:
                bombIcon = fontLargeWeapons.render(icon, True, (255,255,255))
            if matchInfo['BombState'] == 1:
                bombIcon = fontLargeWeapons.render(icon, True, (212,55,55))
            if matchInfo['BombState'] == 2:
                bombIcon = fontLargeWeapons.render(icon, True, ctColor)
            if matchInfo['BombState'] == 2:
                icon = weapon_icon_table.get("BombExplode", "Unknown")
                bombIcon = fontLargeWeapons.render(icon, True, (212,55,55))
            bombCoord = transform_coordinates([bombPosition['X'], bombPosition['Y']])
            screen.blit(bombIcon, (bombCoord[0] - 13, bombCoord[1] - 13))
            
        ################### Projectiles ###################
        if gameData[currentRound]['Tick'][currentTick]["Projectiles"]:
            for projectile in gameData[currentRound]['Tick'][currentTick]["Projectiles"]:
                icon = weapon_icon_table.get(projectile["Type"], "Unknown")
                color = ""
                if projectile["Team"] == 2:
                    color = tColor
                else:
                    color = ctColor
                projectileIcon = fontMedWeapons.render(icon, True, color)
                projectilePosition = transform_coordinates([projectile["Position"]['X'], projectile["Position"]['Y']])
                screen.blit(projectileIcon, (projectilePosition[0], projectilePosition[1]))

        ################### SCOREBOARD ###################
        # Separate dictionaries with 'team' equal to 2 and 3
        ctTeamList = [d for d in playerArrayAlphabet if d["Team"] == 3]
        tTeamList = [d for d in playerArrayAlphabet if d["Team"] == 2]
        
        # Call the function to draw scoreboard
        draw_scoreboard(screen, fontLarge, fontMed, fontLargeWeapons, fontMedWeapons, ctColor, tColor, ctTeamList, tTeamList, gameData[currentRound]['Score'])
        
        ################## Kill Feed ###################z
        if gameData[currentRound]["Tick"][currentTick]["KillFeed"]:
            killFeed = gameData[currentRound]["Tick"][currentTick]["KillFeed"]

            for i, kill in enumerate(killFeed):

                # Rest of your code remains the same
                killerColor = tColor if kill["KillerTeam"] == 2 else ctColor
                victimColor = tColor if kill["VictimTeam"] == 2 else ctColor
                killerLabel = fontMed.render(kill["Killer"] + "  ", True, killerColor)
                weaponLabel = fontMedWeapons.render(weapon_icon_table.get(kill["Weapon"], "Unknown") + "  ", True, (255, 255, 255))
                victimLabel = fontMed.render(kill["Victim"], True, victimColor)

                # Get the dimensions of each label
                killer_rect = killerLabel.get_rect()
                victim_rect = victimLabel.get_rect()
                weapon_rect = weaponLabel.get_rect()

                # Calculate the total width of the combined labels
                total_width = killer_rect.width + victim_rect.width + weapon_rect.width

                # Blit the combined surface onto the screen
                screen.blit(killerLabel, (1275 - killer_rect.width - weapon_rect.width - victim_rect.width, i * 25))
                screen.blit(weaponLabel, (1275 - weapon_rect.width - victim_rect.width, i * 25))
                screen.blit(victimLabel, (1275 - victim_rect.width, i * 25))

                 
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                fast_forward = True
            elif event.key == pygame.K_SPACE:
                is_animating = not is_animating  # Toggle the state
                pausePlay.set_text("Pause" if is_animating else "Play")
                print("Hello")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                fast_forward = False
            

        # Check for slider value change event
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                is_animating = False
                pausePlay.set_text("Play")
                new_slider_value = slider.get_current_value()
                if new_slider_value != current_slider_value:
                    currentTick = new_slider_value
                    current_slider_value = new_slider_value
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == prevRound:
                    if currentRound != 0:
                        currentRound -= 1
                        currentTick = 0
                        text_round.set_text("Round: " + str(currentRound + 1))
                        slider.set_current_value(0)
                elif event.ui_element == nextRound:
                    if currentRound != len(gameData) - 1:
                        currentRound += 1
                        currentTick = 0
                        text_round.set_text("Round: " + str(currentRound + 1))
                        slider.set_current_value(0)
                elif event.ui_element == pausePlay:
                    if is_animating:
                        is_animating = False
                        pausePlay.set_text("Play")
                    else:
                        is_animating = True
                        pausePlay.set_text("Pause")
                #Speed Buttons
                elif event.ui_element == speedOne:
                    PLAYBACK_SPEED = 2
                elif event.ui_element == speedTwo:
                    PLAYBACK_SPEED = 4
                elif event.ui_element == speedFour:
                    PLAYBACK_SPEED = 8
                elif event.ui_element == speedEight:
                    PLAYBACK_SPEED = 16
                #Round Buttons
                for i, button in enumerate(round_buttons):
                    if event.ui_element == button:
                        currentRound = i
                        currentTick = 0
                        text_round.set_text("Round: " + str(currentRound + 1))
                        slider.set_current_value(0)
                
                    


    # Process events for the UI manager
    manager.process_events(event)
    # Update the UI manager
    manager.update(32)

    # Draw the UI
    manager.draw_ui(screen)
    
    pygame.display.flip()

    # Animation logic
    if is_animating:
            if (currentTick + PLAYBACK_SPEED >= len(gameData[currentRound]['Tick'])) and (currentRound != len(gameData) - 1):
                currentTick = 0
                slider.set_current_value(0)
                currentRound += 1
                text_round.set_text("Round: " + str(currentRound + 1))
            else:
                slider.set_current_value((slider.get_current_value() + PLAYBACK_SPEED))
                currentTick = (slider.get_current_value() + PLAYBACK_SPEED)
            

    clock.tick(FPS)

pygame.quit()



