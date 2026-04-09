# game/game.py
import pygame
from settings import FPS, COLORS, HEIGHT, WIDTH, ZONE_NAME
from core.ui import TimeSlider, Inventory, MainComUI, DialogueUI
from core.scene import Scene
from data.dialogue_data import dialogues
class Game:
    def __init__(self, screen):
        from data import scene_data
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.is_running = True
        
        # Game States
        self.current_zone = 2
        self.current_time = "present"
        self.inventory = Inventory("assets/image/ui/inventory.png")
        
        # game flags
        self.flags = {
            "has_seen_intro": False,
            "Enter_main_zone" : False,
            "has_tuner": False,
            "knows_main_objective": False,
            "is_pot_placed" : False,
            "is_seed_planted": False,
            "tree_grow" : False,
            "found_safe" : False,
            "knows_about_entropy": False,
            "is_safe_opened": False
        }

        # Scene
        self.scenes = {
            1: Scene(1,scene_data.zone1),
            2: Scene(2,scene_data.zone2),
            3: Scene(3,scene_data.zone3),
            4: Scene(4,scene_data.zone4),
            5: Scene(5,scene_data.zone5),
            6: Scene(6,scene_data.zone6),
        }
        
        # Create UI
        self.time_slider = TimeSlider(500, 20, 240, 40)
        
        self.font = pygame.font.SysFont(None, 48)
        self.font_large = pygame.font.SysFont(None, 100)

        # main com UI
        self.main_com_ui = MainComUI()
        self.active_ui = None

        # Text Dialogue
        self.dialogue_ui = DialogueUI("assets/image/ui/dialogue.png")

        # For Fade text
        self.fade_text = ""
        self.fade_alpha = 0
        self.fade_start_time = 0

        # Transition
        self.flash_alpha = 0
        self.flash_surface = pygame.Surface((WIDTH, HEIGHT))
        self.flash_surface.fill((255, 255, 255))

    def handle_events(self):
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.is_running = False

            # for debug
            elif event.type == pygame.KEYDOWN:
                if 49 <= event.key <= 54:
                    self.current_zone = event.key-48

            # Click checker
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Click check
                if event.button == 1:
                    mouse_pos = event.pos
                    
                    # Debug
                    print(self.flags)
                    try:
                        print(self.inventory.get_selected_item().name)
                    except:
                        print(None)

                    # Check for dialogue first
                    if self.dialogue_ui.is_active:
                        self.dialogue_ui.handle_click(mouse_pos)
                        continue

                    # for debug
                    print(mouse_pos)
                    # Main com UI
                    if self.active_ui:
                        action = self.active_ui.handle_click(mouse_pos, self.current_time)
                        
                        if action == "close_ui":
                            self.active_ui = None
                        elif action == "go_zone5":
                            self.active_ui = None
                            self.current_zone = 5
                            self.fade(ZONE_NAME[f"zone{self.current_zone}"])

                        # For using in main com UI only
                        continue
                    
                    # For changing time
                    new_time = self.time_slider.handle_click(mouse_pos, self)
                    if new_time is not None and not self.active_ui:
                        self.current_time = new_time
                        self.flash_alpha = 255

                    if self.inventory.handle_click(mouse_pos):
                        continue 

                    click_event_code = self.scenes[self.current_zone].handle_click(mouse_pos, self, self.current_time)

                    if click_event_code is not None:
                        if click_event_code == "open_main_com":
                                self.active_ui = self.main_com_ui

                        elif click_event_code[:7] == "go_zone":
                            self.current_zone = int(click_event_code[-1])
                            self.fade(ZONE_NAME[f"zone{self.current_zone}"])

            # Hover Check
            is_hovering_item = self.scenes[self.current_zone].check_hover(mouse_pos, self.current_time)
            if self.active_ui or self.dialogue_ui.is_active:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            else:
                if is_hovering_item:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                
    def fade(self, text):
        self.fade_text = text
        self.fade_alpha = 255
        self.fade_start_time = pygame.time.get_ticks()

    def draw_text_with_outline(self, surface, text, font, text_color, outline_color, center_pos, outline_width, alpha):
        # main text and outline
        base_text = font.render(text, True, text_color)
        outline_text = font.render(text, True, outline_color)
        
        w, h = base_text.get_size()
        temp_surf = pygame.Surface((w + outline_width * 2, h + outline_width * 2), pygame.SRCALPHA)
        
        # All direction of text
        offsets = [
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),          (1,  0),
            (-1,  1), (0,  1), (1,  1)
        ]
        
        # Draw Color for every direction
        for dx, dy in offsets:
            temp_surf.blit(outline_text, (outline_width + (dx * outline_width), outline_width + (dy * outline_width)))
            
        # Draw main color
        temp_surf.blit(base_text, (outline_width, outline_width))
        
        # Fade
        temp_surf.set_alpha(alpha)
        
        # Draw on screen
        rect = temp_surf.get_rect(center = center_pos)
        surface.blit(temp_surf, rect)

    def draw(self):
        # Draw Scene
        self.scenes[self.current_zone].draw(self.screen, self.current_time, self.inventory.get_selected_item(), self)

        # Draw UI
        self.time_slider.draw(self.screen, self.current_time, self)
        self.inventory.draw(self.screen)

        if self.active_ui:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(100)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            self.active_ui.draw(self.screen, self.flags["is_safe_opened"])

        self.dialogue_ui.draw(self.screen)

        # Fade Text
        if self.fade_text != "":
            self.draw_text_with_outline(
                surface = self.screen,
                text = self.fade_text,
                font = self.font_large,
                text_color = COLORS["LIGHT_PURPLE"],
                outline_color = COLORS["BLACK"],
                center_pos = (WIDTH // 2, HEIGHT // 8),
                outline_width = 3,
                alpha = self.fade_alpha
            )
            
            # Time of start text
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.fade_start_time
            
            # Fade
            if elapsed_time > 1000:
                self.fade_alpha -= 5 
            if self.fade_alpha <= 0:
                self.fade_text = ""
                self.fade_alpha = 0

        # Draw Transition
        if self.flash_alpha > 0:
            self.flash_surface.set_alpha(self.flash_alpha)
            self.screen.blit(self.flash_surface, (0, 0))
            self.flash_alpha -= 15 
            
            if self.flash_alpha < 0:
                self.flash_alpha = 0

        pygame.display.flip()

    def run(self):
        # start first dialogue
        if not self.flags["has_seen_intro"]:
            self.dialogue_ui.show(dialogues["intro_wake_up"])
            self.flags["has_seen_intro"] = True

        while self.is_running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
