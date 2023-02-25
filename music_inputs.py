import pygame

VICENTE_BUTTONS = [2,3]
SIMAO_BUTTONS = [9,10]

STOP_ROUND = False

def display_string(text):

    # Set the size of the window
    size = (1500, 800)
    screen = pygame.display.set_mode(size)

    # Set the title of the window
    pygame.display.set_caption("Display String")

    # Set the font and size for the text
    font = pygame.font.Font(None, 120)

    # Render the text with anti-aliasing
    text_surface = font.render(text, True, (255, 255, 255))

    # Get the size of the text surface
    text_rect = text_surface.get_rect()

    # Center the text on the screen
    text_rect.center = screen.get_rect().center

    # Clear the screen and draw the text
    if text == "MUDANÇA DE RONDA":
        screen.fill(pygame.Color('red'))
    else:
         screen.fill(pygame.Color('blue'))
    screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()


pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick found.")
    quit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

while True:
    for event in pygame.event.get():
        if hasattr(event,"button") and not STOP_ROUND:
            if event.button in VICENTE_BUTTONS:
               display_string("VICENTE")
               STOP_ROUND = True
            elif event.button in SIMAO_BUTTONS:
                display_string("SIMÃO")
                STOP_ROUND = True
            print(event.button)
        if event.type == pygame.KEYDOWN:
            STOP_ROUND = False
            display_string("MUDANÇA DE RONDA")