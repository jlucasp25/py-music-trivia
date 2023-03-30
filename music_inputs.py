import os
from io import BytesIO

import easygui
import pygame
from PIL import Image
from mutagen.id3 import ID3
from wx.core import wx

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

    def game_loop(self):
        while True:
            import tkinter as tk
            from tkinter import filedialog

            root = tk.Tk()
            root.withdraw()

            file_path = filedialog.askopenfilename()
            cover_image = self.extract_cover_from_mp3(
                file_path=file_path)
            cover_image.save("tmp.jpg")
            self.set_image('tmp.jpg', self._players_window)
            for event in pygame.event.get():
                if hasattr(event, "button") and not self.STOP_ROUND:
                    if event.button in VICENTE_BUTTONS:
                        self.display_string(window=self._players_window, text="VICENTE", background_color='blue')
                        self.STOP_ROUND = True
                    elif event.button in SIMAO_BUTTONS:
                        self.display_string(window=self._players_window, text="SIMÃO", background_color='blue')
                        self.STOP_ROUND = True
                    print(event.button)
                # if event.type == pygame.KEYDOWN:
                #     self.STOP_ROUND = False
                #     self.display_string(window=self._players_window, text="MUDANÇA DE RONDA", background_color='red')

    def set_image(self, image, window):
        # create a surface object, image is drawn on it.
        imp = pygame.image.load(image).convert()
        # Using blit to copy content from one surface to other
        window.blit(imp, (50, 50))
        pygame.display.flip()

    def extract_cover_from_mp3(self, file_path):
        # Generate ID3 object
        tags = ID3(file_path)
        # Get the picture tags
        pict = tags.get("APIC:").data
        # Generate image from byte data.
        # Pillow image.
        return Image.open(BytesIO(pict))

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

# import the threading module
import threading


class PlayersGameThread(threading.Thread):
    thread_name = 'GAME'
    thread_id = 1000
    _app = None

    def run(self):
        self._app = MusicTriviaGame()
#
# class HostApplication:
#     BASE_DIRECTORY = '/Users/jlpires/Music/Deep House'
#
#     def __init__(self):
#         print(os.listdir(self.BASE_DIRECTORY))
#
#
# HostApplication()
