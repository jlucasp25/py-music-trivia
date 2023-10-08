import os
import random
import eyed3
import pygame
import sys
from pygame.locals import *

# Define the path to your MP3 files folder
mp3_folder = "mp3_folder"

# Function to extract cover art, title, artist, and album from an MP3 file
def extract_info(mp3_file):
    audiofile = eyed3.load(mp3_file)
    if audiofile.tag:
        title = audiofile.tag.title
        if not title:
            title = "Unknown Title"
        artist = audiofile.tag.artist
        if not artist:
            artist = "Unknown Artist"
        album = audiofile.tag.album
        if not album:
            album = "Unknown Album"
        return (title, audiofile.tag.images[0].image_data if audiofile.tag.images else None, artist, album)
    return ("Unknown Title", None, "Unknown Artist", "Unknown Album")

# Function to play a random MP3 file from a folder and its subdirectories
def play_random_mp3(folder):
    mp3_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".mp3"):
                mp3_files.append(os.path.join(root, file))

    if mp3_files:
        mp3_file = random.choice(mp3_files)
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.play()
        return mp3_file  # Return the path of the currently playing song
    return None

# Initialize Pygame
pygame.init()

# Create Pygame window
screen_width, screen_height = 1400, 900  # Increased size and added padding
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Trivia Game")

# Load font for buttons, text, and title
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)

# Initialize points for each player as global variables
player1_points = 0
player2_points = 0

# Get player names from the terminal
player1_name = input("Enter the name of Player 1: ")
player2_name = input("Enter the name of Player 2: ")

# Define buttons for player 1 and player 2
button_width = 240  # Increased button size
button_height = 80  # Increased button size
button_color1 = (255, 165, 0)  # Orange
button_color2 = (0, 191, 255)  # Sky Blue

player1_buttons = [
    [(50, 650, button_width, button_height), button_color1, font.render(f"{player1_name}: 1 pt", True, (0, 0, 0))],
    [(350, 650, button_width, button_height), button_color1, font.render(f"{player1_name}: 2 pts", True, (0, 0, 0))],
    [(650, 650, button_width, button_height), button_color1, font.render(f"{player1_name}: 3 pts", True, (0, 0, 0))],
]

player2_buttons = [
    [(50, 760, button_width, button_height), button_color2, font.render(f"{player2_name}: 1 pt", True, (0, 0, 0))],
    [(350, 760, button_width, button_height), button_color2, font.render(f"{player2_name}: 2 pts", True, (0, 0, 0))],
    [(650, 760, button_width, button_height), button_color2, font.render(f"{player2_name}: 3 pts", True, (0, 0, 0))],
]

# Define buttons for the jury
jury_buttons = [
    [(1050, 300, button_width, button_height), button_color1, font.render("Pause", True, (0, 0, 0))],
    [(1050, 450, button_width, button_height), button_color1, font.render("Next Track", True, (0, 0, 0))],
    [(1050, 650, button_width, button_height), button_color2, font.render("Restart Song", True, (0, 0, 0))],
    [(1050, 760, button_width, button_height), button_color2, font.render("Toggle Title/Cover", True, (0, 0, 0))],
]

# Flag to control track playback
is_paused = False

# Flags to control title/cover visibility
show_title = False
show_cover = False

# Variable to store the path of the currently playing song
current_song_path = None
last_song_path = None  # Store the path of the last played song

# Function to print track information to the terminal
def print_track_info(mp3_file):
    title, cover_art, artist, album = extract_info(mp3_file)
    print("Title:", title)
    print("Artist:", artist)
    print("Album:", album)
    if cover_art:
        print("Cover Art: Available")
    else:
        print("Cover Art: Not Available")
    print("-" * 50)  # Add a spacer

# Main game loop
def trivia_game():
    global player1_points  # Declare player1_points as global
    global player2_points  # Declare player2_points as global
    global is_paused
    global show_title
    global show_cover
    global current_song_path  # Declare current_song_path as global
    global last_song_path  # Declare last_song_path as global

    current_song_path = play_random_mp3(mp3_folder)  # Play the first random track
    print_track_info(current_song_path)  # Print information for the first song

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check if player 1 buttons were clicked
                for i, button in enumerate(player1_buttons):
                    button_rect = pygame.Rect(button[0])
                    if button_rect.collidepoint(mouse_pos):
                        player1_points += i + 1

                # Check if player 2 buttons were clicked
                for i, button in enumerate(player2_buttons):
                    button_rect = pygame.Rect(button[0])
                    if button_rect.collidepoint(mouse_pos):
                        player2_points += i + 1

                # Check if jury buttons were clicked
                for i, button in enumerate(jury_buttons):
                    button_rect = pygame.Rect(button[0])
                    if button_rect.collidepoint(mouse_pos):
                        if i == 0:  # Pause button
                            if is_paused:
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.pause()
                            is_paused = not is_paused
                        elif i == 1:  # Next Track button
                            pygame.mixer.music.stop()
                            last_song_path = current_song_path
                            current_song_path = play_random_mp3(mp3_folder)
                            show_title = False  # Hide title when a new track starts
                            show_cover = False  # Hide cover when a new track starts
                            # Print track information to the terminal
                            print_track_info(current_song_path)
                        elif i == 2:  # Restart Song button
                            pygame.mixer.music.rewind()
                            player1_points = 0
                            player2_points = 0
                            show_title = False  # Hide title when restarting
                            show_cover = False  # Hide cover when restarting
                        elif i == 3:  # Toggle Title/Cover button
                            show_title = not show_title
                            show_cover = not show_cover

        # Clear the screen
        screen.fill((255, 255, 255))

        # Display cover art, title, and points
        if current_song_path:
            title, cover_art, artist, album = extract_info(current_song_path)

            if show_cover and cover_art:
                with open("cover_art.jpg", "wb") as cover_file:
                    cover_file.write(cover_art)
                cover_image = pygame.image.load("cover_art.jpg")
                cover_image = pygame.transform.scale(cover_image, (400, 400))

                # Suppress libpng warning by modifying the environment
                os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
                screen.blit(cover_image, (300, 170))  # Adjust position of cover art

            if show_title:
                # Display title, artist, and album of the song
                title_text = title_font.render(f"Title: {title}", True, (0, 0, 0))
                artist_text = font.render(f"Artist: {artist}", True, (0, 0, 0))
                album_text = font.render(f"Album: {album}", True, (0, 0, 0))
                title_rect = title_text.get_rect(center=(screen_width // 2, 50))
                artist_rect = artist_text.get_rect(center=(screen_width // 2, 100))
                album_rect = album_text.get_rect(center=(screen_width // 2, 140))
                screen.blit(title_text, title_rect)
                screen.blit(artist_text, artist_rect)
                screen.blit(album_text, album_rect)

            # Display points for players at the top left and top right
            player1_points_text = font.render(f"{player1_name}: {player1_points} pts", True, (0, 0, 0))
            player2_points_text = font.render(f"{player2_name}: {player2_points} pts", True, (0, 0, 0))
            screen.blit(player1_points_text, (10, 10))
            screen.blit(player2_points_text, (screen_width - player2_points_text.get_width() - 10, 10))

            # Display buttons for both players and jury
            for button in player1_buttons + player2_buttons + jury_buttons:
                pygame.draw.rect(screen, button[1], button[0])
                screen.blit(button[2], (button[0][0] + 10, button[0][1] + 10))  # Adjust text position

        pygame.display.flip()

    pygame.quit()
    # Reset the environment variable
    del os.environ['PYGAME_HIDE_SUPPORT_PROMPT']

if __name__ == "__main__":
    show_title = False  # Start the game without showing the title
    show_cover = False  # Start the game without showing the cover
    current_song_path = play_random_mp3(mp3_folder)  # Play the first random track and print its information
    print_track_info(current_song_path)  # Print information for the first song
    trivia_game()
