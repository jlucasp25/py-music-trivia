from io import BytesIO

import pygame
from PIL import Image
from mutagen.id3 import ID3
from pygame import mixer

VICENTE_BUTTONS = [2, 3]
SIMAO_BUTTONS = [9, 10]


class MusicTriviaGame:
    _SCREEN_SIZE = (1500, 800)
    _players_window = None
    _host_window = None
    STOP_ROUND = False

    def __init__(self):
        # Setup Pygame.
        pygame.init()
        pygame.joystick.init()
        # Search for joysticks...
        if pygame.joystick.get_count() == 0:
            print("No joystick found.")
            quit()
        # Setup joystick.
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        # Setup windows.
        self._players_window = pygame.display.set_mode(self._SCREEN_SIZE)
        self._host_window = pygame.display.set_mode(self._SCREEN_SIZE)
        # Display entry page.
        self.display_string(window=self._players_window, text="Bem-vindo ao jogo musical!", background_color='yellow')
        self.game_loop()

    def _game_round(self):
        file_path = input("Insira a música:")
        cover_image = self.extract_cover_from_mp3(
            file_path=file_path)
        music_data = self.extract_data_from_mp3(file_path=file_path)
        cover_image.save("tmp.jpg")
        mixer.init()
        mixer.music.load(file_path)
        mixer.music.set_volume(1)
        mixer.music.play()
        while True:
            for event in pygame.event.get():
                if hasattr(event, "button"):
                    if event.button in VICENTE_BUTTONS and not self.STOP_ROUND:
                        self.display_string(window=self._players_window, text="VICENTE", background_color='blue')
                        self.STOP_ROUND = True
                    elif event.button in SIMAO_BUTTONS and not self.STOP_ROUND:
                        self.display_string(window=self._players_window, text="SIMÃO", background_color='blue')
                        self.STOP_ROUND = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.display_string(window=self._players_window, text=f"MUDANÇA DE RONDA {str(music_data)}",
                                            background_color='red')
                        self.set_image('tmp.jpg', self._players_window)
                    if event.key == pygame.K_BACKSPACE:
                        mixer.music.stop()
                        return

    def game_loop(self):
        while True:
            self._game_round()
            # Display entry page.
            self.display_string(window=self._players_window, text="Bem-vindo ao jogo musical!",
                                background_color='yellow')

    def set_image(self, image, window):
        # create a surface object, image is drawn on it.
        imp = pygame.image.load(image).convert()
        # Using blit to copy content from one surface to other
        window.blit(imp, (10, 10))
        pygame.display.flip()

    def extract_cover_from_mp3(self, file_path):
        # Generate ID3 object
        tags = ID3(file_path)
        # Get the picture tags
        pict = tags.get("APIC:").data
        # Generate image from byte data.
        # Pillow image.
        return Image.open(BytesIO(pict))

    def extract_data_from_mp3(self, file_path):
        # Generate ID3 object
        tags = ID3(file_path)
        return {'title': tags.get('title'), 'artist': tags.get('artist')}

    def display_string(self, window, text, background_color='red'):
        # Set the title of the window
        pygame.display.set_caption("Display String")

        # Set the font and size for the text
        font = pygame.font.Font(None, 120)

        # Render the text with anti-aliasing
        text_surface = font.render(text, True, (255, 255, 255))

        # Get the size of the text surface
        text_rect = text_surface.get_rect()

        # Center the text on the screen
        text_rect.center = window.get_rect().center

        # Clear the screen and draw the text
        window.fill(pygame.Color(background_color))
        window.blit(text_surface, text_rect)

        # Update the display
        pygame.display.flip()


app = MusicTriviaGame()
