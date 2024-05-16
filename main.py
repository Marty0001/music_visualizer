import numpy as np
import pygame
from music_player import MusicPlayer
from audio_bar import AudioBar

AUDIO_FILE = 'hope.mp3'

def create_audio_bars(screen_w, screen_h):
    # Create AudioBar for multiple frequencies
    bars = []
    freq_range = np.arange(0, 8000, 50)
    bar_width = screen_w / len(freq_range)
    x = (screen_w - bar_width * len(freq_range)) / 2

    for freq in freq_range:
        bars.append(AudioBar(x, screen_h / 2, freq, max_height=screen_h / 3, width=bar_width))
        x += bar_width

    return bars

def handle_key_presses(event, music_player):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            music_player.fast_forward(5)
        elif event.key == pygame.K_LEFT:
            music_player.reverse(5)
        elif event.key == pygame.K_SPACE:
            music_player.pause()

def main(audio_file):
   
    # Set up the screen
    pygame.init()
    infoObject = pygame.display.Info()
    screen_w = int(infoObject.current_w / 4)
    screen_h = screen_w
    screen = pygame.display.set_mode([screen_w, screen_h])

    # Create audio bars
    bars = create_audio_bars(screen_w, screen_h)

    # Create MusicPlayer object
    music_player = MusicPlayer(audio_file)
    music_player.load_audio_data()
    music_player.play()

    # Initialize timing
    last_frame_ticks = music_player.get_current_time()

    running = True
    while running:
        # Calculate time difference
        current_ticks = music_player.get_current_time()
        delta_time = (current_ticks - last_frame_ticks) / 1000.0
        last_frame_ticks = current_ticks

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_key_presses(event, music_player)

        screen.fill('Black')

        # Display bars
        skip = False  # Make gap between each bar
        for bar in bars:
            if not skip:
                bar.update(delta_time, music_player.get_decibel(current_ticks / 1000.0, bar.freq))
                bar.render(screen)
            skip = not skip

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main(AUDIO_FILE)
