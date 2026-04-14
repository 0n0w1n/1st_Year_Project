import pygame
import sys
from settings import WIDTH, HEIGHT, COLORS, FPS


class MenuScene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.result = None  # "start" or "quit"

        # Background
        bg = pygame.image.load("assets/image/background/main_menu.png").convert()
        self.background = pygame.transform.scale(bg, (WIDTH, HEIGHT))

        # Invisible hitboxes
        self.buttons = [
            {"rect": pygame.Rect(75, 252, 225, 80), "action": "start"},
            {"rect": pygame.Rect(75, 335, 175, 70), "action": "quit"},
        ]

        self.hovered_index = None

        # Triangle indicator
        self.tri_size = 12

        # Keyboard shortcut hint font
        self.hint_font = pygame.font.Font("assets/fonts/JetBrainsMono-Medium.ttf", 12)

        # White overlay surface for fade transition
        self.white = pygame.Surface((WIDTH, HEIGHT))
        self.white.fill((255, 255, 255))
        self.fade_alpha   = 0
        self.fading_out   = False
        self.fading_in    = False
        self.FADE_SPEED   = 6

    def _get_hovered(self, mouse_pos):
        for i, btn in enumerate(self.buttons):
            if btn["rect"].collidepoint(mouse_pos):
                return i
        return None

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_index = self._get_hovered(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Block clicks while transitioning
                if self.fading_out or self.fading_in:
                    continue
                idx = self._get_hovered(event.pos)
                if idx is not None:
                    action = self.buttons[idx]["action"]
                    if action == "quit":
                        self.result = "quit"
                        self.is_running = False
                    elif action == "start":
                        # Begin fade to white
                        self.fading_out = True

            elif event.type == pygame.KEYDOWN:
                if self.fading_out or self.fading_in:
                    continue
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.fading_out = True
                elif event.key == pygame.K_ESCAPE:
                    self.result = "quit"
                    self.is_running = False

    def update(self):
        if self.fading_out:
            self.fade_alpha = min(255, self.fade_alpha + self.FADE_SPEED)
            if self.fade_alpha >= 255:
                # Fully white
                self.result = "start"
                self.is_running = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Triangle indicator
        if self.hovered_index is not None and not self.fading_out:
            btn_rect = self.buttons[self.hovered_index]["rect"]
            s  = self.tri_size
            cx = btn_rect.left - s - 6
            cy = btn_rect.centery
            # Right pointing triangle
            p1 = (cx,         cy - s)
            p2 = (cx,         cy + s)
            p3 = (cx + s * 2, cy)
            pygame.draw.polygon(self.screen, COLORS["WHITE"], [p1, p2, p3])

        # Keyboard shortcuts hint
        if not self.fading_out:
            hint = self.hint_font.render("ENTER / SPACE: Start    ESC: Quit", True, (200, 200, 200))
            hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT - 30))
            self.screen.blit(hint, hint_rect)

        # White fade overlay
        if self.fade_alpha > 0:
            self.white.set_alpha(self.fade_alpha)
            self.screen.blit(self.white, (0, 0))

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        return self.result  # "start" or "quit"
