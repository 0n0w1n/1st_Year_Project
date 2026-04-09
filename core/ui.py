import pygame
from settings import COLORS, HEIGHT, WIDTH
    

class TimeSlider:
    def __init__(self, x, y, width, height):
        # Hit rect UI
        self.rect = pygame.Rect(x, y, width, height)
        self.segment_width = width // 3 
        
        self.knob_rect = pygame.Rect(x, y, self.segment_width, height)
        
        self.font = pygame.font.SysFont(None, 20)

    def draw(self, screen, current_time, game):
        selected_item = game.inventory.get_selected_item()

        # Check for selected item to be time tuner
        if selected_item and selected_item.name == "Time_Tuner":
            pygame.draw.rect(screen, (150, 150, 150), self.rect, border_radius=10)
            pygame.draw.rect(screen, COLORS["BLACK"], self.rect, 2, border_radius=10)
            
            # set current time button to be different
            if current_time == "past":
                self.knob_rect.x = self.rect.x
            elif current_time == "present":
                self.knob_rect.x = self.rect.x + self.segment_width
            elif current_time == "future":
                self.knob_rect.x = self.rect.x + (self.segment_width * 2)
                
            pygame.draw.rect(screen, COLORS["WHITE"], self.knob_rect, border_radius=10)
            pygame.draw.rect(screen, COLORS["BLACK"], self.knob_rect, 2, border_radius=10)
            
            # show what is current time
            screen.blit(self.font.render("PAST", True, COLORS["BLACK"]), (self.rect.x + 15, self.rect.y + 45))
            screen.blit(self.font.render("PRESENT", True, COLORS["BLACK"]), (self.rect.x + self.segment_width + 5, self.rect.y + 45))
            screen.blit(self.font.render("FUTURE", True, COLORS["BLACK"]), (self.rect.x + (self.segment_width * 2) + 5, self.rect.y + 45))

    def handle_click(self, mouse_pos, game):
        selected_item = game.inventory.get_selected_item()

        # check when click whether we hold time tuner or not
        if self.rect.collidepoint(mouse_pos) and selected_item and selected_item.name == "Time_Tuner":
            if mouse_pos[0] < self.rect.x + self.segment_width:
                return "past"
            elif mouse_pos[0] < self.rect.x + (self.segment_width * 2):
                return "present"
            else:
                return "future"
        return None
    

class Inventory:
    def __init__(self, ui_image_path):
        # Load inventory slots image
        self.image = pygame.image.load(ui_image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        
        # items and max item be 9
        self.items = []
        self.max_items = 9
        self.selected_index = None

        # set gap between each slots
        self.slot_size = 45
        self.slot_margin = 2.2

        self.start_x = 190
        self.start_y = 515

        self.slot_rects = []
        for i in range(self.max_items):
            slot_x = self.start_x + (i * (self.slot_size + self.slot_margin))
            slot_y = self.start_y
            self.slot_rects.append(pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size))

    def add_item(self, item):
        if len(self.items) < self.max_items:
            self.items.append(item)
            return True
        return False
    
    def handle_click(self, mouse_pos):
        for i, rect in enumerate(self.slot_rects):
            if rect.collidepoint(mouse_pos):
                # Check whether this slot is empty or not
                if i < len(self.items):
                    # this slot is already select
                    if self.selected_index == i:
                        self.selected_index = None
                    else:
                        self.selected_index = i
                return True
        return False
    
    def get_selected_item(self):
        if self.selected_index is not None and self.selected_index < len(self.items):
            return self.items[self.selected_index]
        return None
    
    def remove_selected_item(self):
        if self.selected_index is not None and self.selected_index < len(self.items):
            removed_item = self.items.pop(self.selected_index)
            self.selected_index = None
            return removed_item
        return None
    
    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        # loop every item in slots to draw item's icon
        for index, item in enumerate(self.items):
            slot_x = self.start_x + (index * (self.slot_size + self.slot_margin))
            slot_y = self.start_y
            
            icon_size = self.slot_size - 10
            item_icon = pygame.transform.scale(item.image, (icon_size, icon_size))
            
            icon_rect = item_icon.get_rect(center=(slot_x + (self.slot_size//2), slot_y + (self.slot_size//2)))
            screen.blit(item_icon, icon_rect)

        # Draw selected slot triangle
        if self.selected_index is not None:
            selected_rect = self.slot_rects[self.selected_index]
            
            tri_size = 8
            bottom_y = selected_rect.top - 5 
            center_x = selected_rect.centerx
            
            p1 = (center_x - tri_size, bottom_y - tri_size)
            p2 = (center_x + tri_size, bottom_y - tri_size) 
            p3 = (center_x, bottom_y)
            
            pygame.draw.polygon(screen, (255, 215, 0), [p1, p2, p3])


class MainComUI:
    def __init__(self):
        # UI image path
        self.image = pygame.image.load("assets/image/ui/main_com_ui.PNG").convert_alpha()
        
        # adjust size
        self.ui_width = WIDTH
        self.ui_height = HEIGHT
        self.image = pygame.transform.scale(self.image, (self.ui_width, self.ui_height))
        
        # Center the UI
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Create hitbox of button
        self.btn_close = pygame.Rect(self.rect.x + 640, self.rect.y + 110, 50, 50)  # Close
        self.btn_floor2 = pygame.Rect(self.rect.x + 200, self.rect.y + 415, 180, 60) # 2nd floor
        self.btn_zone5 = pygame.Rect(self.rect.x + 420, self.rect.y + 415, 180, 60) # zone 5
        
        self.alert_message = ""
        self.font = pygame.font.SysFont(None, 30) # Main font

        # Debug
        self.show_debug_hitbox = False

    def handle_click(self, mouse_pos, state):
        # Check wheter mouse hit hitbox or not
        if self.btn_close.collidepoint(mouse_pos):
            self.alert_message = ""
            return "close_ui"
            
        elif self.btn_floor2.collidepoint(mouse_pos):
            if state == "present":
                self.alert_message = "Elevator not found/Broken"
            else:
                self.alert_message = "Access Denied"
            return "ui_clicked"
            
        elif self.btn_zone5.collidepoint(mouse_pos):
            if state == "present":
                self.alert_message = "Elevator not found/Broken"
                return "ui_clicked"
            self.alert_message = ""
            return "go_zone5"
            
        elif self.rect.collidepoint(mouse_pos):
            return "ui_clicked" 
            
        return None

    def draw(self, screen, safe_open):
        # Main UI
        screen.blit(self.image, self.rect)

        # Text in MainCom
        texts = [
            "TRION MAINFRAME - SYSTEM LOCKDOWN",
            "---------------------------------",
            "EXIT DOOR STATUS: LOCKED",
            "",
            "3 ITEMS REQUIRED TO UNLOCK:",
            "> 1. QUANTUM ENERGY UNIT",
            "> 2. LEVEL-5 KEYCARD",
            "> 3. OVERRIDE PASSWORD"
        ]
        start_y = self.rect.y + 150
        for i, text in enumerate(texts):
            if 5 <= i <= 7:
                if i == 5 and False:
                    text_surf = self.font.render(text, True, COLORS["GREEN"])

                elif i == 6 and safe_open:
                    text_surf = self.font.render(text, True, COLORS["GREEN"])

                elif i == 7 and False:
                    text_surf = self.font.render(text, True, COLORS["GREEN"])
                    
                else:
                    text_surf = self.font.render(text, True, COLORS["RED"])

            else:
                text_surf = self.font.render(text, True, COLORS["VERY_LIGHT_BLUE"])
            screen.blit(text_surf, (self.rect.x + 150, start_y + (i * 30)))
        
        # Button Text
        btn_font = pygame.font.SysFont(None, 23)

        text_f2 = btn_font.render("ELEVATOR: FL.2", True, COLORS["VERY_LIGHT_BLUE"])
        rect_f2 = text_f2.get_rect(center=self.btn_floor2.center)
        screen.blit(text_f2, rect_f2)

        text_z5 = btn_font.render("ELEVATOR: ZONE 5", True, COLORS["VERY_LIGHT_BLUE"])
        rect_z5 = text_z5.get_rect(center=self.btn_zone5.center)
        screen.blit(text_z5, rect_z5)

        # Debug
        if self.show_debug_hitbox:
            pygame.draw.rect(screen, COLORS["RED"], self.btn_close, 2)
            pygame.draw.rect(screen, COLORS["RED"], self.btn_floor2, 2)
            pygame.draw.rect(screen, COLORS["RED"], self.btn_zone5, 2)
            
        # Alert message
        if self.alert_message:
            alert_surf = self.font.render(self.alert_message, True, (255, 50, 50))
            alert_rect = alert_surf.get_rect(center=(self.rect.centerx - 110, self.rect.bottom - 210))
            screen.blit(alert_surf, alert_rect)

        
class DialogueUI:
    def __init__(self, image_path):
        # Text box
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        
        # Center
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
        
        self.font = pygame.font.SysFont("tahoma", 20)

        # list of sentences
        self.messages = []
        # index of sentence
        self.current_index = 0
        self.is_active = False

    def show(self, texts_list):
        self.messages = texts_list
        self.current_index = 0
        self.is_active = True

    def handle_click(self, mouse_pos):
        # Click for next sentence
        if self.is_active:
            self.current_index += 1
            
            # Close when read all sentence
            if self.current_index >= len(self.messages):
                self.is_active = False
            return True
            
        return False

    def draw(self, screen):
        if not self.is_active:
            return

        # Draw text box
        screen.blit(self.image, self.rect)

        # Current text
        current_text = self.messages[self.current_index]
        lines = current_text.split('\n')

        line_height = self.font.get_linesize() + 5 # Text Height
        total_text_height = len(lines) * line_height # Total text height

        box_center_y = 410
        
        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, COLORS["WHITE"])
            
            # Text's rect
            text_rect = text_surf.get_rect()
            
            # Center_X
            text_rect.centerx = self.rect.centerx
            
            # Center_Y
            offset_y = (i - (len(lines) - 1) / 2) * line_height
            text_rect.centery = box_center_y + offset_y
            
            # Draw
            screen.blit(text_surf, text_rect)
            
        # Triangle
        if pygame.time.get_ticks() % 1000 < 500:
            pygame.draw.polygon(screen, COLORS["BLACK"], [
                (self.rect.right - 125, self.rect.bottom - 125),
                (self.rect.right - 105, self.rect.bottom - 125),
                (self.rect.right - 115, self.rect.bottom - 110)
            ])