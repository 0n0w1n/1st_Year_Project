import pygame
from settings import HEIGHT, WIDTH
from data.dialogue_data import dialogues

INTRO_FADE_SPEED = 3

class Scene:
    def __init__(self, zone_id, items):
        self.fading = False
        self.zone_id = zone_id
        self.items = items
        self.intro_alpha = 255

        # load scene
        if self.zone_id != 7:
            self.bg_past = self.load_image(f"assets/image/background/zone{zone_id}_past.png")
            self.bg_present = self.load_image(f"assets/image/background/zone{zone_id}_present.png")
            self.bg_future = self.load_image(f"assets/image/background/zone{zone_id}_future.png")
        else:
            self.bg_past = self.load_image("assets/image/background/zone7.png")
            self.bg_present = self.load_image("assets/image/background/zone7.png")
            self.bg_future = self.load_image("assets/image/background/zone7.png")
        

    def load_image(self, path):
        try:
            img = pygame.image.load(path).convert()
            img = pygame.transform.scale(img, (WIDTH, HEIGHT))
            return img
        except FileNotFoundError:
            print(f"Cannot find image {path}")
            surf = pygame.Surface((WIDTH, HEIGHT))
            surf.fill((50, 50, 50)) 
            return surf
        

    def draw(self, screen, current_time, selected_item, game):
        if current_time == "past":
            screen.blit(self.bg_past, (0, 0))
        elif current_time == "present":
            # Draw BG
            screen.blit(self.bg_present, (0, 0))

            # Fade black
            if not game.flags["has_seen_intro"]:
                self.fading = True
                
                # Fade down
                self.intro_alpha -= INTRO_FADE_SPEED
                
                if self.intro_alpha <= 0:
                    self.intro_alpha = 0
                    game.flags["has_seen_intro"] = True
                    self.fading = False
                    game.dialogue_ui.show(dialogues["intro_wake_up"])
                else:
                    # create black screen
                    fade_surface = pygame.Surface(screen.get_size())
                    fade_surface.fill((0, 0, 0))
                    fade_surface.set_alpha(self.intro_alpha)
                    screen.blit(fade_surface, (0, 0))
        elif current_time == "future":
            screen.blit(self.bg_future, (0, 0))

        for item in self.items:
            if item.time_period == current_time:
                if self.fading:
                    continue
                # Check for spot pot to show when hold pot
                if item.name == "pot_spot_zone1":
                    if selected_item and selected_item.name == "pot_zone3":
                        item.draw(screen)
                
                # Check for draw Tree
                elif item.name == "tree2_future" and not game.flags["tree_grow"] and item.is_active:
                    game.flags["tree_grow"] = True
                    game.dialogue_ui.show(dialogues["discover_giant_vine"])

                # Check for open glass
                elif item.name == "box_zone6" and game.flags["is_glass_open"]:
                    item.is_active = False

                # first time enter reactor room in past
                elif item.name == "battery_zone6" and not game.flags["first_time_found_battery"]:
                    game.dialogue_ui.show(dialogues["first_time_battery_past"])
                    game.flags["first_time_found_battery"] = True
                    item.draw(screen)

                else:
                    item.draw(screen)

    def check_hover(self, mouse_pos, current_time):
        for item in self.items:
            if item.is_active and item.rect.collidepoint(mouse_pos) and item.time_period == current_time:
                pos_in_mask = (mouse_pos[0] - item.rect.x, mouse_pos[1] - item.rect.y)
                if item.mask.get_at(pos_in_mask):
                    return True
        return False

    def handle_click(self, mouse_pos, game, current_time):
        for item in self.items:
            if item.rect.collidepoint(mouse_pos) and item.time_period == current_time and item.is_active:
                pos_in_mask = (mouse_pos[0] - item.rect.x, mouse_pos[1] - item.rect.y)
                if item.mask.get_at(pos_in_mask):

                    # Track which item was clicked for stats
                    game.last_clicked_item = item.name

                    # Check if it collectable
                    if item.is_collectable:
                        if game.inventory.add_item(item):
                            # For tube to show dialogue
                            if item.name == "test_tube_zone3":
                                game.dialogue_ui.show(dialogues["pickup_glass_tube"])

                            # Fiber wire pickup
                            if item.name == "fiber_wire_zone2":
                                game.dialogue_ui.show(dialogues["pickup_fiber_wire"])

                            item.is_active = False
                            print(f"Collected: {item.name}")

                            # for first time pick up time tuner
                            if not game.flags["has_tuner"] and item.name == "Time_Tuner":
                                game.dialogue_ui.show(dialogues["pickup_tuner"])
                                game.flags["has_tuner"] = True
                            return "collected"
                    else:
                        return item.on_click(game)