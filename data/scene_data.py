from core.item import Item
from settings import WIDTH, HEIGHT

zone1 = [
    Item("main_com_zone1", 0, 0, 800, 600, False, "past"),
    Item("left_door_zone1", 0, 475, 68, 125, False, "past"),
    Item("right_door_zone1", 742, 389, 58, 158, False, "past"),
    Item("pot_spot_zone1", 20, 150, 80, 80, False, "past"),

    Item("main_com_zone1", 0, 0, 800, 600, False, "present"),
    Item("left_door_zone1", 0, 475, 68, 125, False, "present"),
    Item("right_door_zone1", 742, 389, 58, 158, False, "present"),
    Item("Time_Tuner", 400, 210, 120, 120, True, "present"),
    Item("magnet_zone1", 90, 300, 35, 35, True, "present"),
    Item("plant_kill_zone1", 682, 203, 50, 50, True, "present"),
    Item("pot_spot_zone1", 20, 150, 80, 80, False, "present"),
    Item("tree1_present", -160, 0, WIDTH, HEIGHT, False, "present", False),

    Item("left_door_zone1", 0, 475, 68, 125, False, "future"),
    Item("right_door_zone1", 742, 389, 58, 158, False, "future"),
    Item("pot_spot_zone1", 20, 150, 80, 80, False, "future"),
    Item("tree1_future", -160, 0, WIDTH, HEIGHT, False, "future", False),
    Item("tree2_future", -160, 0, WIDTH, HEIGHT, False, "future", False),
]

zone2 = [
    Item("left_door_zone2", 0, 475, 68, 125, False, "past"),
    Item("broom_zone2", 123, 558, 68, 125, True, "past"),
    Item("left_door_zone2", 0, 475, 68, 125, False, "present"),
    Item("wire_zone2", 735, 140, 50, 50, True, "present"),
    Item("left_door_zone2", 0, 475, 68, 125, False, "future"),
]

zone3 = [
    Item("right_door_zone3", 742, 389, 58, 158, False, "past"),
    Item("pot_zone3", 700, 300, 50, 50, True, "past"),
    Item("test_tube_zone3", 52, 287, 50, 50, True, "past"),

    Item("right_door_zone3", 742, 389, 58, 158, False, "present"),
    Item("entropy_zone3", 0, 0, WIDTH, HEIGHT, False, "present"),

    Item("seed_zone3", 100, 100, 50, 50, True, "future"),
    Item("right_door_zone3", 742, 389, 58, 158, False, "future"),
]

zone4 = [
    Item("paper_zone4", 448, 105, 50, 50, False, "past"),
    Item("safe_zone4", 0, 0, WIDTH, HEIGHT, False, "past"),
    Item("safe_zone4", 0, 0, WIDTH, HEIGHT, False, "present"),
    Item("safe_zone4", 0, 0, WIDTH, HEIGHT, False, "future"),

]

zone5 = []

zone6 = [
    Item("energy_zone6", 385, 235, 50, 50, False, "past"),
    Item("energy_zone6", 385, 235, 50, 50, False, "present"),
    Item("energy_zone6", 385, 235, 50, 50, False, "future"),
]