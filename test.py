import pygame
import pygame_gui

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 200

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Slider Example')

# Create a UI manager for the GUI elements
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Create a slider
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((100, 100), (200, 20)),  # Position and size of the slider
    start_value=0.5,  # Initial value (0.0 to 1.0)
    value_range=(0.0, 1.0),  # Value range
    manager=manager,
)

# Create a label to display the slider value
slider_value_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((100, 20), (200, 20)),  # Position and size of the label
    text=f'Slider Value: {slider.get_current_value():.2f}',  # Initial text with slider value
    manager=manager,
)

# Create two buttons
button1 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((100, 150), (100, 40)),  # Position and size of Button 1
    text='Subtract 0.1',  # Button text
    manager=manager,
)

button2 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((200, 150), (100, 40)),  # Position and size of Button 2
    text='Add 0.1',  # Button text
    manager=manager,
)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:  # Check for custom events (button clicks)
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button1:
                    slider.set_current_value(max(0.0, slider.get_current_value() - 0.1))  # Subtract 0.1, but ensure it stays >= 0.0
                elif event.ui_element == button2:
                    slider.set_current_value(min(1.0, slider.get_current_value() + 0.1))  # Add 0.1, but ensure it stays <= 1.0

        # Process events for the UI manager
        manager.process_events(event)

    # Get the current slider value and update the label text
    slider_value_label.set_text(f'Slider Value: {slider.get_current_value():.2f}')

    # Clear the screen
    screen.fill((0, 0, 0))

    # Update the UI manager
    manager.update(30)

    # Draw the UI
    manager.draw_ui(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
