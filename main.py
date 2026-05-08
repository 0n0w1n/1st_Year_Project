"""
Main file to run the whole game
"""
import sys
import os
import multiprocessing as mp
import pygame
from settings import WIDTH, HEIGHT
from core.menu import MenuScene
from core.game_loop import Game
from core.stats_window import show_stats


def _stats_process(tracker):
    show_stats(tracker)


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

    game.tracker.finalise()
    pygame.display.quit()
    pygame.quit()

    # Spawn stats
    ctx = mp.get_context("spawn")
    p = ctx.Process(target=_stats_process, args=(game.tracker,))
    p.start()
    p.join()


if __name__ == "__main__":
    main()
