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
                if not game.flags["knows_main_objective"] and game.current_time != "future":
                    game.dialogue_ui.show(dialogues["main_objective_reveal"])
                    game.flags["knows_main_objective"] = True
                    return "open_main_com"

                # Insert drive to start decryption (past) ---
                elif selected_item and selected_item.name == "drive_zone4" and game.current_time == "past":
                    if not game.flags["drive_inserted"]:
                        game.dialogue_ui.show(dialogues["insert_drive_supercomputer"])
                        game.inventory.remove_selected_item()
                        game.flags["drive_inserted"] = True
                        return "inspected"

                # Present: supercomputer is destroyed — explain wire need
                elif game.flags["drive_inserted"] and game.current_time == "future" and not game.flags["wire_connected"]:
                    game.dialogue_ui.show(dialogues["supercomputer_destroyed"])
                    return "inspected"

                # Past: connect fiber wire to back up before the explosion
                elif selected_item and selected_item.name == "fiber_wire_zone2" and game.current_time == "past":
                    if game.flags["drive_inserted"] and not game.flags["wire_connected"]:
                        game.dialogue_ui.show(dialogues["connect_wire_supercomputer"])
                        game.inventory.remove_selected_item()
                        game.flags["wire_connected"] = True
                        return "inspected"
            
            # Charge Battery
                # If not charge
                elif not game.flags["is_battery_charging"]:
                    if selected_item and selected_item.name == "battery_zone6" and game.current_time != "future":
                        if game.current_time == "past":
                            game.dialogue_ui.show(dialogues["put_battery_charger"])
                            game.inventory.remove_selected_item()
                            game.flags["is_battery_charging"] = True
                            return "battery_inserted"
                        elif game.current_time == "present":
                            game.dialogue_ui.show(["Charge function is working.", "But the port is broken."])
                            return "inspected"
                        
                # full in future time
                else:
                    if game.current_time == "future":
                        game.dialogue_ui.show(dialogues["get_full_battery"])
                        game.inventory.add_item(Item("charged_battery_zone1", 0, 0, 50, 50, True, "future"))
                        game.flags["is_battery_charging"] = False
                        game.flags["has_charged_battery"] = True
                        return "got_charged_battery"

                if game.current_time != "future":
                    return "open_main_com"
                else:
                    return "inspected"


            # Door to zone3
            elif self.name == "left_door_zone1":
                return "go_zone3"
            
            # door to zone2
            elif self.name == "right_door_zone1":
                return "go_zone2"
            
            # door to zone1
            elif self.name == "right_door_zone3" or self.name == "left_door_zone2" or self.name == "elevator_zone5":
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
                                for item2 in game.scenes[4].items:
                                    if item2.name == "tree2nd_future":
                                        item2.is_active = True
                                        break
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
                    if item.name in ["tree1_present", "tree1_future", "tree2_future", "tree2nd_future"]:
                        item.is_active = False
                return "seed_removed"

            # Climb to zone 4 — medicine check
            elif self.name == "tree2_future":
                if selected_item and selected_item.name == "medicine_zone1":
                    game.dialogue_ui.show(dialogues["use_medicine_before_climb"])
                    game.inventory.remove_selected_item()
                    game.flags["has_taken_medicine"] = True
                    game.flags["is_injured"] = False
                    return "go_zone4"
                elif not game.flags["has_taken_medicine"]:
                    # Climb without medicine — apply injury penalty
                    if not game.flags["is_injured"]:
                        game.flags["is_injured"] = True
                        game.dialogue_ui.show(dialogues["vine_climb_no_medicine"])
                    else:
                        game.dialogue_ui.show(["My hand is injured.", "I have to treat this wound first."])
                    return "Not go"
                else:
                    return "go_zone4"
                
            # Climb back to zone 1
            elif self.name == "tree2nd_future":
                return "go_zone1"
                
            # Use Elevator
            elif self.name == "elevator_zone4":
                if selected_item and selected_item.name == "card_zone4":
                    if game.current_time == "past":
                        return "go_zone1"
                    else:
                        game.dialogue_ui.show(["Elevator is not working."])
                        return "inspected"
                else:
                    game.dialogue_ui.show(["Need Key Card level-5 to use Elevator"])
                    return "inspected"
            
            elif self.name == "door_zone5":
                if selected_item and selected_item.name == "card_zone4":
                    return "go_zone6"
                else:
                    game.dialogue_ui.show(["Need Key Card level-5 to use Elevator"])
                    return "inspected"
            elif self.name == "door_zone6":
                if selected_item and selected_item.name == "card_zone4":
                    return "go_zone5"
                else:
                    game.dialogue_ui.show(["Need Key Card level-5 to use Elevator"])
                    return "inspected"
                    
            
            # read paper
            elif self.name == "paper_zone4":
                    if not game.flags["knows_about_entropy"]:
                        game.flags["knows_about_entropy"] = True
                        game.dialogue_ui.show(dialogues["read_safe_document"])
                        game.scenes[4].items.remove(self)

            # click safe
            elif self.name == "safe_zone4":
                # Injured penalty — show warning first, but still allow after second click
                if game.flags["is_injured"] and not game.flags["found_safe"]:
                    game.dialogue_ui.show(dialogues["safe_injured_hands"])
                    game.flags["found_safe"] = True
                    return "inspected"

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
                
        # Reactor Part
            elif self.name == "battery_zone6":
                # If glass is already open
                if not game.flags["is_glass_open"]:
                    # Use key
                    if selected_item and selected_item.name == "key_zone1":
                        game.dialogue_ui.show(dialogues["use_key"])
                        game.inventory.remove_selected_item()
                        game.flags["is_glass_open"] = True
                        self.is_collectable = True
                        return "glass_opened"
                    else:
                        game.dialogue_ui.show(dialogues["machine_need_key"])
                else:
                    game.dialogue_ui.show(dialogues["get_dead_battery"])

            # Key via magnet
            elif self.name == "rubble_zone1":
                # If its not cleared
                if not game.flags["is_rubble_swept"]:
                    # If use broom
                    if selected_item and selected_item.name == "broom_zone2":
                        game.dialogue_ui.show(dialogues["key_in_hole"])
                        game.flags["is_rubble_swept"] = True
                        game.scenes[1].items.remove(self)

                        # Key falls into hole — activate the hole item
                        game.flags["is_key_on_ground"] = True
                        for item in game.scenes[1].items:
                            if item.name == "key_on_ground_zone1":
                                item.is_active = True
                        return "rubble_swept"

                    # If does not use broom
                    else:
                        game.dialogue_ui.show(dialogues["rubble_heavy"])
                        return "inspected"

            # Key stuck in hole — need magnet
            elif self.name == "key_on_ground_zone1":
                if selected_item and selected_item.name == "magnet_zone1":
                    game.dialogue_ui.show(dialogues["magnet_get_key"])
                    game.inventory.remove_selected_item()
                    game.scenes[1].items.remove(self)
                    # Spawn the real key
                    game.scenes[1].items.append(Item("key_zone1", 443, 262, 50, 50, True, "future"))
                    return "key_retrieved"
                else:
                    game.dialogue_ui.show(dialogues["key_on_ground_no_magnet"])
                    return "inspected"

            # Blackbox terminal in Zone 5
            elif self.name == "blackbox_zone5":
                # Wire not connected yet — explain what's needed
                if not game.flags["wire_connected"]:
                    game.dialogue_ui.show(dialogues["blackbox_no_data"])
                    return "inspected"
                
                # Data still encrypting

                if game.current_time == "future":
                    # Wire connected: first time — finger scan identity reveal
                    if not game.flags["has_seen_identity"]:
                        game.dialogue_ui.show(dialogues["finger_scan_identity"])
                        game.flags["has_seen_identity"] = True
                        return "inspected"

                    # Second click: watch video diary
                    if not game.flags["blackbox_unlocked"]:
                        game.dialogue_ui.show(dialogues["blackbox_video_diary"])
                        game.flags["blackbox_unlocked"] = True
                        return "inspected"

                    # Third click: full confession + get password
                    if not game.flags["has_password"]:
                        game.dialogue_ui.show(dialogues["blackbox_confession"])
                        game.flags["has_password"] = True
                        return "inspected"
                    
                else:
                    game.dialogue_ui.show(["Encrypting..."])
                    return "inspected"

