dialogues = {
    # start
    "intro_wake_up": [
        "Ugh... my head... where am I?",
        "Everything is broken.",
        "Was I inside that... stasis pod?",
        "I can't remember anything.",
        "Not even my own name."
    ],

    # collect trion tuner
    "pickup_tuner": [
        "What is this strange device on the floor?",
        "[ SYSTEM: 'TRION TUNER' ACQUIRED ]",
        "It has three years marked on it:\n1986, 2026, and 2066...",
        "Wait... is this some kind of time machine?"
    ],

    # first time open main com
    "main_objective_reveal": [
        "The main exit is completely locked.",
        "The terminal says I need three items\nto unlock the system:",
        "1. Quantum Energy\n2. Level-5 Keycard\n3. Override Password",
        "I need to search this place.",
        "Maybe I should check 2nd floor."
    ],

    # try to go to 2nd floor (access denied)
    "elevator_floor2_1986": [
        "[ SYSTEM: ADMINISTRATOR ACCESS REQUIRED ]",
        "The panel is working,\nbut I don't have access.",
        "I need to find a high-level keycard."
    ],
    
    # no trion tuner
    "no_tuner_yet": [
        "I feel stuck in this time.\nI need a device to get out of here."
    ],

    # Place pot
    "place_empty_pot": [
        "Maybe I need to use something with this pot."
    ],

    # found seed
    "pickup_seed": [
        "A strange glowing seed...",
        "The label says 'Experimental Specimen'.",
        "I should take it with me."
    ],
    
    # Plant seed
    "plant_the_seed": [
        "I placed the pot here and planted the seed.",
        "Nothing is happening now.",
        "But if I wait long enough... maybe decades...",
        "what will happen?"
    ],
    
    # Tree is growing through 2nd floor
    "discover_giant_vine": [
        "Incredible! After 80 years, that small seed\ngrew into a huge glowing vine.",
        "It broke through the ceiling to 2nd floor.",
        "It looks strong enough.",
        "I can climb it."
    ],

    # Found Safe
    "inspect_safe_locked": [
        "A personal safe.\nThe name says 'Dr. XXXXX'.",
        "It's made of Trion Alloy.\nVery strong and impossible to break.",
        "I can't open it with normal tools."
    ],
    
    # read
    "read_safe_document": [
        "A note on the desk...",
        "'Note: Trion Alloy is almost impossible to break.\nDo not lose the code.'",
        "'Only Liquid Entropy can break it\nby speeding up time around it.'",
        "Liquid Entropy... I need to find it."
    ],
    
    # pickup tube
    "pickup_glass_tube": [
        "A thick glass tube.",
        "It can hold very dangerous substances."
    ],
    
    # scoop liq entropy
    "scoop_liquid_entropy": [
        "The tanks broke many years ago.",
        "The chemicals reacted and became Liquid Entropy.",
        "Very dangerous.",
        "I carefully put some into the glass tube."
    ],
    
    # Open safe
    "open_safe_success": [
        "I poured the Liquid Entropy on the safe...",
        "Unbelievable! Time sped up around the metal.",
        "The safe aged thousands of years in seconds\nand turned to dust!",
        "Inside, I found a 'Data Drive'\nand a 'Level-5 Keycard'."
    ],

    # Found reactor
    "machine_need_key": [
        "The machine is working.",
        "But it needs a key to open the glass.",
        "The battery is inside.",
        "I can't reach it."
    ],
    
    # not have broom to use yet
    "rubble_heavy": [
        "A pile of dangerous trash.",
        "I shouldn't touch it with my hands."
    ],
    
    # sweep
    "sweep_rubble": [
        "I used the broom to clean the trash...",
        "Look! Something is glowing on the floor!"
    ],
    
    # found key
    "pickup_key": [
        "It's a key!",
        "There is a tag on it.",
        "It looks like a Reactor Key."
    ],
    
    # Use key
    "use_key": [
        "I put the key in.",
        "The glass shield is opening!"
    ],

    # take battery
    "get_dead_battery": [
        "The glass is open.",
        "I got the dead battery.",
        "I need to charge it at the main computer."
    ],

    # Charge battery
    "put_battery_charger": [
        "I put the battery in the charger.",
        "The screen says..."
    ],
    "charger_wait": [
        "The battery is still charging.",
        "I need to wait... a long time."
    ],

    # take charged battery
    "get_full_battery": [
        "80 years later...",
        "The battery is now 100% full.",
        "I got the charged battery!"
    ],

    # key stuck in hole after sweeping
    "key_in_hole": [
        "The trash is gone!",
        "But the key is stuck in the hole...",
        "It's too tight to grab.",
        "I need something that can pull metal."
    ],

    # try to grab key from hole without magnet
    "key_on_ground_no_magnet": [
        "The key is right there in the hole.",
        "My hand can't fit through.",
        "I need something magnetic."
    ],

    # use magnet on hole
    "magnet_get_key": [
        "I held the magnet over the hole...",
        "The key flew up through the hole!",
        "That worked."
    ],

    # climb vine without medicine — penalty
    "vine_climb_no_medicine": [
        "The thorns cut my hands.",
        "I'm bleeding badly.",
        "My hands are shaking.",
        "I can barely hold anything."
    ],

    # use medicine before climbing
    "use_medicine_before_climb": [
        "I wrapped my hands before climbing.",
        "The thorns still hurt, but the wounds are safe.",
        "I reached the top safely."
    ],

    # try to open safe while injured
    "safe_injured_hands": [
        "My hands are shaking too much.",
        "I can barely hold anything.",
        "I need to treat the wounds first."
    ],

    # Insert drive into supercomputer
    "insert_drive_supercomputer": [
        "I plugged the Data Drive into the supercomputer.",
        "The screen flickers...",
        "[ QUANTUM FILE DETECTED ]",
        "[ TIME TO DECRYPT: 80 YEARS ]",
        "I have to come back later."
    ],

    # supercomputer is destroyed in present
    "supercomputer_destroyed": [
        "The supercomputer is broken.",
        "The data I started... is gone.",
        "Wait — maybe I can save it before the explosion...",
        "There should be an emergency port.",
        "I need a fast cable to send data to the B1 Blackbox."
    ],

    # Pick up fiber optic wire
    "pickup_fiber_wire": [
        "A high-speed fiber cable.",
        "It can send a lot of data very fast.",
    ],

    # Connect wire to supercomputer
    "connect_wire_supercomputer": [
        "I connected the cable to the port.",
        "[ DATA SENT TO B1 BLACKBOX ]",
        "[ BACKUP COMPLETE ]",
        "Now I need to go to B1 and check it."
    ],

    # wire not connected to black box yet
    "blackbox_no_data": [
        "The Blackbox terminal. It survived everything.",
        "[ WAITING FOR DATA ]",
        "I need to connect the supercomputer first."
    ],

    # Finger scan moment
    "finger_scan_identity": [
        "[ ADMIN ACCESS REQUIRED ]",
        "[ SCAN: DR. XXXXX ]",
        "I'm just an assistant... but let me try.",
        "...",
        "[ ACCESS GRANTED ]",
        "This feels wrong.",
        "Why did it accept my fingerprint?"
    ],

    # Video diary begins
    "blackbox_video_diary": [
        "[ DECRYPTION COMPLETE ]",
        "[ PLAYING VIDEO... ]",
        "A man appears on screen.",
        "He looks scared.",
        "That face...",
        "It's mine."
    ],

    # Full confession
    "blackbox_confession": [
        "'The experiment has failed...'",
        "'Time is collapsing.'",
        "'I have no choice.'",
        "'I will erase my memory and hide in the pod.'",
        "'If you find this... the code is 1986.'",
        "Now I understand everything.",
        "I am Dr. XXXXX.",
        "I caused this.",
        "And I ran away."
    ],

    # Exit door
    "exit_enter_password": [
        "Battery inserted... power on.",
        "Keycard accepted... unlocked.",
        "[ PASSWORD REQUIRED ]",
        "I know this code.",
        "It's 1986."
    ],

    # Drive insert blocked when not have battery yet
    "drive_needs_battery": [
        "The Supercomputer needs power to run the decryption.",
        "I need to charge the battery first.",
        "The main computer needs a Charged Battery \nin the system before I can insert the drive."
    ],
    # Ending

    "game_ending": [
        "[ PASSWORD ACCEPTED ]",
        "[ TIME RESET STARTED ]",
        "The three timelines — 1986, 2026, 2066 —",
        "are merging into one.",
        "The lab becomes quiet.",
        "Light comes in from outside.",
        "Dr. XXXXX walks out.",
        "Into a changed world.",
        "[ END ]"
    ],

    # charger port broken in present
    "charger_port_broken": [
        "Charge function is working.",
        "But the port is broken."
    ],

    # injured hand reminder
    "hand_injured_reminder": [
        "My hand is injured.",
        "I have to treat this wound first."
    ],

    # elevator not working in future
    "elevator_not_working": [
        "Elevator is not working."
    ],

    # need keycard for elevator
    "need_keycard_elevator": [
        "Need Key Card level-5 to use Elevator"
    ],

    # need keycard for gate
    "need_keycard_gate": [
        "Need Key Card level-5 to use gate"
    ],

    # blackbox encrypting in past/present
    "blackbox_encrypting": [
        "Encrypting..."
    ],

    # first time seeing battery in past reactor room
    "first_time_battery_past": [
        "Look like there's only battery in past."
    ],
}