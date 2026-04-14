"""
Main file to run the whole game
"""
import sys
import pygame
from settings import WIDTH, HEIGHT
from core.menu import MenuScene
from core.game_loop import Game
from core.stats_window import show_stats


def main():
    """starting the game"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("The TRION")

    # Zone 0 Main Menu
    menu = MenuScene(screen)
    result = menu.run()

    if result == "quit":
        pygame.quit()
        sys.exit()

    # Main Game
    game = Game(screen)
    game.run()

    # Freeze pygame while stats window is open
    pygame.display.iconify()

    game.tracker.finalise()
    show_stats(game.tracker)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
