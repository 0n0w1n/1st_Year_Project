import pygame
from core.images_path import item_images
from data.dialogue_data import dialogues

class Item:
    def __init__(self, name, x, y, width, height, collectable, time_period, active = True):
        self.name = name
        self.time_period = time_period

        self.image = pygame.image.load(item_images[f"{name}_{self.time_period}"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

        self.mask = pygame.mask.from_surface(self.image, threshold=0)

        self.rect = pygame.Rect(x, y, width, height)
        self.is_active = active
        self.is_collectable = collectable

    def draw(self, screen):
        if self.is_active:
            screen.blit(self.image, self.rect)

    def on_click(self, game):
        if self.is_active:
            print(f"clicked on {self.name}")

            selected_item = game.inventory.get_selected_item()
    
            # Click on main computer in zone1
            if self.name == "main_com_zone1":
                if not game.flags["knows_main_objective"]:
                    game.dialogue_ui.show(dialogues["main_objective_reveal"])
                    game.flags["knows_main_objective"] = True
                return "open_main_com"
            
            # Door to zone3
            elif self.name == "left_door_zone1":
                return "go_zone3"
            
            # door to zone2
            elif self.name == "right_door_zone1":
                return "go_zone2"
            
            # door to zone1
            elif self.name == "right_door_zone3" or self.name == "left_door_zone2":
                if not game.flags["Enter_main_zone"]:
                    game.dialogue_ui.show(dialogues["no_tuner_yet"])
                    game.flags["Enter_main_zone"] = True
                return "go_zone1"
            
        # Pot/seed/tree relate part
            elif self.name == "pot_spot_zone1":
                if selected_item and selected_item.name == "pot_zone3": 
                    
                    if not game.flags["is_pot_placed"]:
                        game.dialogue_ui.show(dialogues["place_empty_pot"])
                        game.flags["is_pot_placed"] = True
                    game.inventory.remove_selected_item()
                    
                    # Change to placed pot
                    self.name = "placed_pot_zone1" 
                    
                    # Use the same picture as pot_zone_3
                    self.image = pygame.image.load(item_images["pot_zone3_past"]).convert_alpha() 
                    self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
                    
                    # hitbox update
                    self.mask = pygame.mask.from_surface(self.image, threshold=0)
                    return "pot_placed"

            # Plant seed
            elif self.name == "pot_spot_zone1":
                if selected_item and selected_item.name == "pot_zone3": 
                    if not game.flags["is_pot_placed"]:
                        game.dialogue_ui.show(dialogues["place_empty_pot"])
                        game.flags["is_pot_placed"] = True
                    game.inventory.remove_selected_item()
                    
                    # Change to placed pot
                    self.name = "placed_pot_zone1" 
                    self.image = pygame.image.load(item_images["pot_zone3_past"]).convert_alpha() 
                    self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
                    self.mask = pygame.mask.from_surface(self.image, threshold=0)
                    return "pot_placed"
                else:
                    return "inspected"

            # Plant Seed or get pot back
            elif self.name == "placed_pot_zone1":
                
                # Plant seed
                if selected_item and selected_item.name == "seed_zone3":
                    if not game.flags["is_seed_planted"]:
                        game.dialogue_ui.show(dialogues["plant_the_seed"])
                        game.flags["is_seed_planted"] = True
                    game.inventory.remove_selected_item()
                    self.name = "placed_pot_zone1_with_seed"

                    # Activate Tree
                    for item in game.scenes[1].items:
                        if self.time_period == "past":
                            if item.name == "tree1_present" and item.time_period == "present":
                                item.is_active = True
                            if item.name == "tree2_future" and item.time_period == "future":
                                item.is_active = True
                        elif self.time_period == "present":
                            if item.name == "tree1_future" and item.time_period == "future":
                                item.is_active = True
                    return "seed_planted"

                # get pot back
                elif selected_item is None or selected_item.name != "seed_zone3":
                    self.name = "pot_spot_zone1"
                    game.inventory.add_item(Item("pot_zone3", 700, 300, 50, 50, True, "past"))
                    
                    self.image = pygame.image.load(item_images["pot_spot_zone1_past"]).convert_alpha() 
                    self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
                    self.mask = pygame.mask.from_surface(self.image, threshold=0)
                    return "pot_removed"

            # get seed back
            elif self.name == "placed_pot_zone1_with_seed":
                self.name = "placed_pot_zone1"
                game.inventory.add_item(Item("seed_zone3", 100, 100, 50, 50, True, "future"))
                
                # Deactivate Tree
                for item in game.scenes[1].items:
                    if item.name in ["tree1_present", "tree1_future", "tree2_future"]:
                        item.is_active = False
                return "seed_removed"

            # Climb to zone 4
            elif self.name == "tree2_future":
                return "go_zone4"
            
            # read paper
            elif self.name == "paper_zone4":
                    if not game.flags["knows_about_entropy"]:
                        game.flags["knows_about_entropy"] = True
                        game.dialogue_ui.show(dialogues["read_safe_document"])
                        game.scenes[4].items.remove(self)

            # click safe
            elif self.name == "safe_zone4":
                # Open safe
                if selected_item and selected_item.name == "liquid_entropy_zone3":
                    game.inventory.remove_selected_item()
                    game.flags["is_safe_opened"] = True
                    game.dialogue_ui.show(dialogues["open_safe_success"])

                    # Remove normal Safe
                    for obj in game.scenes[4].items[::-1]:
                        if obj.name[:4] == "safe":
                            game.scenes[4].items.remove(obj)

                    # get drive and key card
                    game.inventory.add_item(Item("drive_zone4", 0, 0, 100, 100, False, "past"))
                    game.inventory.add_item(Item("card_zone4", 0, 0, 100, 100, False, "past"))
                    
                else:
                    game.flags["found_safe"] = True
                    # Can click more than 1 time
                    game.dialogue_ui.show(dialogues["inspect_safe_locked"])

            # collect liquid entropy
            elif self.name == "entropy_zone3":
                if selected_item and selected_item.name == "test_tube_zone3":
                    game.dialogue_ui.show(dialogues["scoop_liquid_entropy"])
                    game.inventory.remove_selected_item()
                    game.inventory.add_item(Item("liquid_entropy_zone3", 0, 0, 100, 100, False, "present"))
                
