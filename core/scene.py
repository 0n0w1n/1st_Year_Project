import pygame
from settings import HEIGHT, WIDTH
from data.dialogue_data import dialogues

class Scene:
    def __init__(self, zone_id, items):
        self.zone_id = zone_id
        self.items = items

        # load scene
        self.bg_past = self.load_image(f"assets/image/background/zone{zone_id}_past.png")
        self.bg_present = self.load_image(f"assets/image/background/zone{zone_id}_present.png")
        self.bg_future = self.load_image(f"assets/image/background/zone{zone_id}_future.png")
        

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
            screen.blit(self.bg_present, (0, 0))
        elif current_time == "future":
            screen.blit(self.bg_future, (0, 0))

        for item in self.items:
            if item.time_period == current_time:
                # Check for spot pot to show when hold pot
                if item.name == "pot_spot_zone1":
                    if selected_item and selected_item.name == "pot_zone3":
                        item.draw(screen)
                
                # Check for draw Tree
                elif item.name == "tree2_future" and not game.flags["tree_grow"] and item.is_active:
                    game.flags["tree_grow"] = True
                    game.dialogue_ui.show(dialogues["discover_giant_vine"])

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

                    # Check if it collectable
                    if item.is_collectable:
                        if game.inventory.add_item(item):
                            # For tube to show dialogue
                            if item.name == "test_tube_zone3":
                                game.dialogue_ui.show(dialogues["pickup_glass_tube"])

                            item.is_active = False
                            print(f"Collected: {item.name}")

                            # for first time pick up time tuner
                            if not game.flags["has_tuner"] and item.name == "Time_Tuner":
                                game.dialogue_ui.show(dialogues["pickup_tuner"])
                                game.flags["has_tuner"] = True
                            return "collected"
                    else:
                        return item.on_click(game)