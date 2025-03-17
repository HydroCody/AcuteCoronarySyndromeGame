#Python function creation
init python:
    #Check that the discharge medications puzzle in the work up drawer is correct
    def validate_discharge_choices():
        if selected_discharge_meds == correct_answers:
            renpy.jump("workup_drawer")
        else:
            renpy.notify("I don't think thats right, try again")
    #Add a medication to the workup drawer with check function and notification
    def add_to_workup_drawer(item):
        global inventory, workup_drawer_added_items, workup_drawer_items_completed

        if item in workup_drawer_items:
            workup_drawer_added_items.append(item)
            inventory.remove(item)
            renpy.show_screen("drawer_message", f"{item} successfully added!")

            if set(workup_drawer_added_items) == set(workup_drawer_items):
                workup_drawer_items_completed = True
                renpy.show_screen("drawer_message", "The drawer is now fully stocked!")
                renpy.call_in_new_context("drawer_fully_stocked")
        else:
            renpy.show_screen("drawer_message", "I don't think that goes here")
        
        renpy.restart_interaction()

    #Add a medication to the treatment drawer with check function and notification
    def add_to_treatment_drawer(item):
        global inventory, treatment_drawer_added_items, treatment_drawer_items_completed

        if item in treatment_drawer_items:
            treatment_drawer_added_items.append(item)
            inventory.remove(item)
            renpy.show_screen("drawer_message", f"{item} successfully added!")

            if set(treatment_drawer_added_items) == set(treatment_drawer_items):
                treatment_drawer_items_completed = True
                renpy.show_screen("drawer_message", "The drawer is now fully stocked!")
                renpy.call_in_new_context("drawer_fully_stocked")
        else:
            renpy.show_screen("drawer_message", "I don't think that goes here")
        
        renpy.restart_interaction()

#Image preps for all images to resize/rotate
image 02tankidle:
    "images/o2tank_idle.png"
    zoom 0.2
    rotate 340

image 02tankhover:
    "images/o2tank_hover.png"
    zoom 0.2
    rotate 340

image EDroom:
    "images/edroom.png"
    xzoom 1.25
    yzoom 0.7

image opentackle:
    "images/opentackle.png"
    zoom 0.38


image closedtackleidle:
    "images/closedtackle_idle.png"
    zoom 0.38

image closedtacklehover:
    "images/closedtackle_hover.png"
    zoom 0.38

image aspirinidle:
    "images/aspirin_idle.png"
    zoom 0.08
    rotate 90


image aspirinhover:
    "images/aspirin_hover.png"
    zoom 0.08
    rotate 90

image clothesidle:
    "images/clothes_pile_idle.png"
    zoom 0.8


image clotheshover:
    "images/clothes_pile_hover.png"
    zoom 0.8

image paperhints:
    "images/paper_hint.png"
    zoom 0.8
    xalign 0.5
    yalign 0.5

image clock_blank_idle:
    "images/wall_clock_blank_idle.png"
    zoom 0.38

image clock_flash_idle:
    "images/wall_clock_flash_idle.png"
    zoom 0.38

image clock_blank_hover:
    "images/wall_clock_blank_hover.png"
    zoom 0.38

image clock_flash_hover:
    "images/wall_clock_flash_hover.png"
    zoom 0.38

image clock_complete:
    "images/wall_clock_complete.png"
    zoom 0.38

image crash_cart_idle:
    "images/cc_idle.png"
    xzoom 0.33
    yzoom 0.17


image crash_cart_hover:
    "images/cc_hover.png"
    xzoom 0.33
    yzoom 0.17


#Transformations to create flashing effect for the clock
transform flashing_clock_idle:
    choice:
        "clock_blank_idle"
        pause 1.0
        "clock_flash_idle"
        pause 1.0
        repeat

transform flashing_clock_hover:
    choice:
        "clock_blank_hover"
        pause 1.0
        "clock_flash_hover"
        pause 1.0
        repeat

#Screens
#Take a medication name and shows a pill bottle with that medication found
screen pillbottle(label_text=""):
    vbox:
        xalign 0.5
        yalign 0.5

        text label_text size 40 color "#ffffff" xpos 120
        add "images/pillbottle.png"

#Take a medication name and shows a vial with that medication found
screen vial_found(label_text=""):
    vbox:
        xalign 0.5
        yalign 0.5

        text label_text size 40 color "#ffffff" xpos 120
        add "images/vial_highlight.png"

#Shows the hints paper that are the clues to open the crash cart
screen hints_to_cart():
    add "paperhints"

#Screen to show drawer message overlays as you put medications into the drawer
screen drawer_message(message):
    modal True  # Prevents interaction with other UI elements
    frame:
        background "#0008"  # Semi-transparent background
        xfill True
        yfill True

        vbox:
            align (0.5, 0.5)  # Center the message
            spacing 20
            frame:
                background "#0000"
                xsize 500
                ysize 200
                padding (30, 20)

                vbox:
                    text message size 40 xalign 0.5
                    textbutton "OK":
                        xalign 0.5
                        action [SetVariable("message_text", None), Hide("drawer_message")]  # Closes message


#Main ED room with all the puzzle images creation - multiple if statements to show puzzles that havent been solved
screen edroom():
    add "EDroom"

    if workup_drawer_items_completed and fibrinolytics_complete and treatment_drawer_items_completed:
        $ puzzle_incomplete = False

    #Create series of if statements for all the puzzles to show them if not completed or remove them if completed
    if puzzle_incomplete:

        #Oxygen tank puzzle - rewards Nitroglycerin
        if o2_incomplete:
            imagebutton:
                idle "02tankidle"
                hover "02tankhover"
                xpos 0.2
                ypos 0.7
                action Jump("o2tankquestion")
        
        #Tackle box puzzle - if completed shows open tackle box - tackle box must be complete to access crash cart puzzles
        #Rewards questions for crash cart as well as heparin and enoxaparin
        if tackle_incomplete:
            imagebutton:
                idle "closedtackleidle"
                hover "closedtacklehover"
                xpos 760
                ypos 440
                action Jump("tacklequestion")

        else:
            imagebutton:
                idle "opentackle"
                xpos 760
                ypos 440

        #Aspirin puzzle - rewards aspirin
        if aspirin_incomplete:
            imagebutton:
                idle "aspirinidle"
                hover "aspirinhover"
                xpos 478
                ypos 290

                action Jump("aspirin_bottle")
        
        #Pile of clothes puzzle - rewards metoprolol
        if clothes_incomplete:
            imagebutton:
                idle "clothesidle"
                hover "clotheshover"
                xpos -80
                ypos 370

                action Jump("clothes_pickup")
        
        #Clock puzzle - rewards clopidogrel
        #Completion changes clock to 10 minute timer
        if clock_incomplete:
            imagebutton:
                idle At("clock_blank_idle", flashing_clock_idle)
                hover At("clock_flash_idle", flashing_clock_hover)
                action Jump("clock_interaction")
                xpos 650
                ypos 100

        else:
            imagebutton:
                idle "clock_complete"
                xpos 650
                ypos 100
        #Crash cart selector - jumps to which drawer you would like to review
        imagebutton:
            idle "crash_cart_idle"
            hover "crash_cart_hover"
            action Jump("crash_cart_puzzle")
            xpos 995
            ypos 358


    else:
        frame:
            xalign 0.5 
            yalign 0.5
            padding (200, 100)
            vbox:
                spacing 10
                align (0.5, 0.5)
                text "You win!" size 50
                text "\n"
                text "You got the ACS Cart refilled" size 30
                text "\n"
                text "Looks like you know your Acute Coronary Syndrome stuff!" size 30
                textbutton "Continue" action Jump("GameOver")

#Dicharge summary puzzle creation - select which medications should be prescribed at discharge or not
#Needs default dictionary to have answer key as well as submission slots
screen discharge_summary():
    tag menu

    modal True

    frame:
        align (0.5, 0.5)
        padding (20, 20)
        background "#333"



        vbox:
            spacing 5
            align (0.5, 0.5)

            text "At discharge select if a medication should be Started or Not Started at home:" color "#fff" size 22

        
            viewport:
                xysize (750, 400)
                mousewheel True

                vbox:
                    spacing 5
                    for med in ["Statin", "ACE Inhibitor", "Heparin", "Tenecteplase", "Nitroglycerin", "Eliquis", "Aspirin", "Beta Blocker"]:
                        hbox:
                            spacing 15

                            text med color "#fff" size 20

                            textbutton "Start":
                                action SetDict(selected_discharge_meds, med, "start")
                                if selected_discharge_meds.get(med) == "start":
                                    style "discharge_button_selected"
                                else:
                                    style "discharge_button" 
                            
                            
                            textbutton "Don't Start":
                                action SetDict(selected_discharge_meds, med, "dont_start")
                                if selected_discharge_meds.get(med) == "dont_start":
                                    style "discharge_button_deselected"
                                else:
                                    style "discharge_button"


    vbox:
        xalign 0.5
        yalign 0.9
        spacing 10
    
        textbutton "Submit":
            action Function(validate_discharge_choices)
            style "submit_button"

#Puzzle screen to add medications to the workup drawer - must add metoprolol, nitroglycerin, and aspirin
#On completion jumps to screen showing puzzle complete and then to main room    
screen workup_drawer_screen():
    modal True

    frame:
        xsize 800
        ysize 700
        xpos 0.2
        ypos 0.001

        vbox:
            xalign 0.4
            spacing 10
            text "Click an item from your inventory to add it to the drawer."
            # Section for displaying medications already in the drawer
            text "Current Drawer Contents:"
            if workup_drawer_added_items:
                for added in workup_drawer_added_items:
                    text f"- {added}" color "#008000"
            else:
                text "The drawer is empty."

            text "\n"

            # Display inventory items as buttons
            text "Select a medication to add:"
            for item in inventory:
                textbutton item:
                    action Function(add_to_workup_drawer, item)
    
            # Exit button
            textbutton "Exit":
                xalign 0.5
                action Jump("main_room")
    if message_text:
        use drawer_message(message_text)

#Puzzle screen to add medications to the workup drawer - must add enoxaparin, fondaparinux, heparin, bilvalrudin, clopidogrel, ticagrelor, and prasugrel
#On completion jumps to screen showing puzzle complete and then to main room   
screen treatment_drawer_screen():
    modal True

    frame:
        xsize 800
        ysize 700
        xpos 0.2
        ypos 0.001

        vbox:
            xalign 0.4
            spacing 10
            text "Click an item from your inventory to add it to the drawer."
            # Section for displaying medications already in the drawer
            text "Current Drawer Contents:"
            if treatment_drawer_added_items:
                for added in treatment_drawer_added_items:
                    text f"- {added}" color "#008000"
            else:
                text "The drawer is empty."

            text "\n"

            # Display inventory items as buttons
            text "Select a medication to add:"
            for item in inventory:
                textbutton item:
                    action Function(add_to_treatment_drawer, item)
    
            # Exit button
            textbutton "Exit":
                xalign 0.5
                action Jump("main_room")
    if message_text:
        use drawer_message(message_text)

#Win screen
screen win_popupA():
    modal True  # Prevents clicking outside the popup
    frame:
        xpos 0.5 xanchor 0.5
        ypos 0.5 yanchor 0.5
        padding 20
        background "#222222DD"
        
        vbox:
            text "You win!" size 40 color "#FFFFFF"
            textbutton "End Game":
                action Return()  # Ends the game        



style med_choice_button:
    size 16
    background "#444"
    hover_background "#666"
    xsize 100

style submit_button:
    size 20
    background "#008000"
    hover_background "#00A000"
    xalign 0.5

style discharge_button:
    background "#CCCCCC"
    padding (10, 5)
    size 24

style discharge_button_selected:
    background "#32CD32"  # Green for selected "Start"
    padding (10, 5)
    size 24

style discharge_button_deselected:
    background "#FF6347"  # Red for selected "Don't Start"
    padding (10, 5)
    size 24

style discharge_submit:
    background "#1E90FF"
    padding (15, 10)
    size 26
    xalign 0.5

#Create flags for all the puzzles being solved or not
default puzzle_incomplete = True
default o2_incomplete = True
default tackle_incomplete = True
default aspirin_incomplete = True
default clothes_incomplete = True
default clock_incomplete = True
default all_cart_solved = 0

#Create flags for first time events or completion events for correct phrasing on questions
default first_o2_time = True
default first_aspirin = True
default first_clothes = True
default first_tackle = True
default first_clock = True
default workup_drawer_flag = True
default treatment_drawer_flag = True
default fibrinolytic_drawer_flag = False
default fibrinolytics_complete = False
default fibrinolytic_break = False
default discharge_paperwork_not_solved = True
default first_visit_workup_drawer = True
default message_text = None
default first_treatment_drawer = True


default inventory = []
default workup_answers = ["monab", "mona-b", "mona b"]

#Create the lists for the drawers and their answers
#Workup drawers
default workup_drawer_added_items = []
default workup_drawer_items = ["Aspirin", "Nitroglycerin", "Metoprolol"]
default workup_drawer_items_completed = False
#Treatment drawers
default treatment_drawer_added_items = []
default treatment_drawer_items = ["Prasugrel", "Clopidogrel", "Ticagrelor", "Enoxaparin", "Fondaparinux", "Heparin", "Bivalrudin"]
default treatment_drawer_items_completed = False

#Create list and answers for discharge list medication mini game
default selected_discharge_meds = {
    "Statin": None,
    "ACE Inhibitor": None,
    "Heparin": None,
    "Tenecteplase": None,
    "Nitroglycerin": None,
    "Eliquis": None,
    "Aspirin": None,
    "Beta Blocker": None
    }
default correct_answers = {
    "Statin": "start",
    "ACE Inhibitor": "start",
    "Heparin": "dont_start",
    "Tenecteplase": "dont_start",
    "Nitroglycerin": "start",
    "Eliquis": "dont_start",
    "Aspirin": "start",
    "Beta Blocker": "start"  
    }


label start:
    show screen edroom


    "Welcome to the Emergency Department, we need your help!"

    "The last STEMI that rolled through here cleaned out the crash cart of all the meds, we need to get it refilled!"

    "It was a mess, meds are everywhere and I hear the next patient coming in, please get everything sorted and the cart refilled!"

label main_room:
    call screen edroom

#Oxygen tank puzzle screen - Rewards Nitroglycerin
label o2tankquestion:
    
    show edroom

    if first_o2_time:
        "This isn't where the oxygen tanks go, lets put this back"

        "Weird, the last person who used this reset the oxygen percent, we need to fix it"

        $ first_o2_time = False

    $ player_answer = renpy.input("If a patients oxygen is below what percent should we start oxygen on them?").strip()

    if player_answer == "90":
        "Thats right! Got the oxygen put away."

        show screen pillbottle("Nitroglycerin found!")



        "Somebody accidently put the nitroglycerin tablets in the oxygen tank storage, at least we found those!"
        window hide
        pause 


    else:
        "No, I dont think thats right, lets try again."
        jump o2tankquestion

    
    $ o2_incomplete = False

    $ inventory.append("Nitroglycerin")

    hide screen pillbottle

    jump main_room

#Aspirin puzzle screen - Rewards Aspirin
label aspirin_bottle:

    show edroom

    if first_aspirin:
        "How did the aspirin bottle get thrown all the way over here?"

        "Lets get this refilled and put up"

        $ first_aspirin = False

    $ player_answer = renpy.input("How many 81mg aspirin tablets should I put in the bottle so they have a full dose?").strip()

    if player_answer == "4":
        "Thats right, they need between 162mg and 324mg for their loading dose so we need at least four, lets get that filled up"

        show screen pillbottle("Aspirin found!")


        "Got that cleaned up!"
        window hide
        pause 


    else:
        "No, I dont think thats right, lets try again."
        jump aspirin_bottle

    $ aspirin_incomplete = False

    $ inventory.append("Aspirin")

    hide screen pillbottle

    jump main_room

#Clothes pile puzzle screen (Beta blocker question) - Rewards Metoprolol
label clothes_pickup:

    show edroom

    if first_clothes:

        "Lets get these blankets and clothes cleaned up, this place can be a mess after a code!"

        "Wait whats this in the pile?"

        "Looks like they left some metoprolol behind, do I need to rush this to them?"

        $ first_clothes = False
    
    $ player_answer = renpy.input("Beta blockers are supposed to be given to our STEMI patients within how many hours?").strip()

    if player_answer == "24":
        "Thats right, they have 24 hours to start the beta-blocker, so we just need to remind them later on the last patient"

        show screen pillbottle("Metoprolol found!")

        window hide
        pause
    else:
        "No I don't think thats right"

        jump clothes_pickup
    
    $ clothes_incomplete = False

    $ inventory.append("Metoprolol")

    hide screen pillbottle

    jump main_room

#Tackle box question about HIT - Rewards enoxaparin and heparin
#Required to be completed before can access crash cart - "rewards" clues to crash cart
label tacklequestion:
    show edroom

    if first_tackle:
        "Heres the heparin and enoxaparin tacklebox. It looks like its locked."

        "Theres some letter dials on here lets see what they say"

        $ first_tackle = False

    $ player_answer = renpy.input("Anticoagulant box: Heparin and Enoxaparin. Do not use if patient has a history of .... The dial looks like it has three letters that go in it. What are they?").strip().lower()

    if player_answer == "hit":
        "Got that open and got the heparin and enoxaparin"

        show screen vial_found("Enoxaparin found!")

        window hide
        pause 

        show screen vial_found("Heparin found!")

        window hide
        pause 

    else:
        "That doesn't seem to fit, lets try again"
        jump tacklequestion

    
    $ tackle_incomplete = False

    $ inventory.append("Enoxaparin")

    $ inventory.append("Heparin")

    hide screen vial_found

    "Theres also a folded up piece of paper, this looks like the codes into the crash cart. Now we can open that!"

    show screen hints_to_cart

    window hide
    pause
    hide screen hints_to_cart

    $ have_crash_cart_hints = True

    jump main_room

#Clock puzzle (EKG question) - rewards Clopidogrel
label clock_interaction:
    show edroom

    if first_clock:
        "Looks like we need to reset the EKG clock"

        "We need to set this to be a countdown from check in until our time goal for an EKG to occur"

        $ first_clock = False

    $ player_answer = renpy.input("How many minutes is the goal time for a patient with chest pain to get an EKG?").strip().lower()

    if player_answer == "10" or player_answer == "ten":
        "Thats correct, our door to EKG time is 10 minutes"


    else:
        "No, I dont think thats right, lets try again."
        jump clock_interaction

    "How did the bottle of clopidogrel get all the way up here?"

    show screen pillbottle("Clopidogrel found!")

    window hide

    $ inventory.append("Clopidogrel")

    pause

    hide screen pillbottle

    $ clock_incomplete = False

    jump main_room

#Crash Cart puzzle - has a question for each drawer, each drawer has rewards
#Must solve all three to complete escape room
label crash_cart_puzzle:
    show edroom

    if tackle_incomplete:
        "The crash cart is locked. I don't remember what the codes are to get in, I think we wrote the down somewhere in here?"

        "Lets come back to this once we find the codes"

        jump main_room
    else:
        if all_cart_solved == 9:
            jump cart_selection
        else:
            jump still_need_cart_solved

#Director to each of the crash cart drawers with question to open them
label still_need_cart_solved:
    show edroom

    menu:
        "Which drawer do you want to check?"

        "Work Up Medications Drawer":
            if workup_drawer_flag:
                jump workup_drawer_discharge
            else:
                $ user_input = renpy.input("What is the mneumonic to remember all the workup treatments during ACS workup?").strip().lower()
                if user_input in workup_answers:
                    $ workup_drawer_flag = True
                    $ all_cart_solved += 1
                    "Now that drawer is open!"
                    jump workup_drawer_discharge
                else:
                    "That didn't unlock the drawer."
                    jump still_need_cart_solved
        
        "Treatment Medications Drawer":
            if treatment_drawer_flag:
                jump treatment_drawer
            else:
                $ user_input = renpy.input("Number of months to continue DAPT if no bleeding risk").strip().lower()
                if user_input == "12" or user_input == "twelve":
                    $ treatment_drawer_flag = True
                    $ all_cart_solved += 1
                    "The drawer opened!"
                    jump treatment_drawer
                else:
                    "That didn't unlock the drawer"
                    jump still_need_cart_solved
        
        "Fibrinolytics Drawer":
            if fibrinolytic_drawer_flag:
                jump fibrinolytic_drawer
            else:
                $ user_input = renpy.input("How many minutes away from a cath lab do you need to be to consider using fibrinolytics?").strip().lower()
                if user_input == "120":
                    $ fibrinolytic_drawer_flag = True
                    $ all_cart_solved += 1
                    "That opened the drawer!"
                    jump fibrinolytic_drawer
                else:
                    "That didn't unlock the drawer"
                    jump still_need_cart_solved

#Discharge medications puzzle - rewards bilvarudin and fondaparinux
label workup_drawer_discharge:
    if discharge_paperwork_not_solved:
        show edroom
        "Somebody's discharge instructions got left in the drawer."

        "We better fill out the rest of the instructions and put those in the discharge pile."
        call screen discharge_summary
    else:
        jump workup_drawer

#Jump to screen for discharge medications puzzle - contains rewards bilvarudin and fondaparinux
label workup_drawer:
    if first_visit_workup_drawer:
        "Somebody left the bivalrudin and the fondaparinux in the discharge pile. Lets grab those."

        show screen vial_found("Bivalrudin found!")

        $ inventory.append("Bivalrudin")

        window hide
        pause 

        show screen vial_found("Fondaparinux found!")

        $ inventory.append("Fondaparinux")


        window hide
        pause
        hide screen vial_found
        $ first_visit_workup_drawer = False
        $ discharge_paperwork_not_solved = False
        "We need to add the right workup medications to the drawer."

        "The morphine is stored in the locked cabinent so we won't need to add that."

        "Let's add the other three medications now."

    if workup_drawer_items_completed:
        "The drawer is refilled!"
    else:
        call screen workup_drawer_screen
    
    jump main_room

#Treatment drawer navigator - question about aspirin and ticagrelor - rewards ticagrelor
#Calls screen for placing medications into the drawer once solved jumps to complete screen then redirects to main room
label treatment_drawer:
    show edroom
    if first_treatment_drawer:
        "Somebody left discharge instructions for Ticagrelor in here. And they are incomplete."

        "Lets fill these out so the next patient can use them."

        $ player_answer = renpy.input("Patients should be on less than ____ mg aspirin while taking ticagrelor.").strip().lower()

        if player_answer == "100" or player_answer == "one hundred":
            "Thats right, ticagrelor is less effective if patients are taking more than 100mg of aspirin a day."

            show screen pillbottle("Ticagrelor found!")

            $ inventory.append("Ticagrelor")
            hide screen pillbottle
            $ first_treatment_drawer = False
        else:
            "No, I dont think thats right, lets try again."
            jump treatment_drawer
    

    if treatment_drawer_items_completed:
        "The drawer is refilled!"
    else:
        "We need to refill the treatment drawer with all the P2Y12 inhibitors and anticoagulants we could need to treat ACS."
        call screen treatment_drawer_screen
    
    jump main_room

#Fibrinolytic drawer, question about ezetimibe - rewards prasugrel
#Drawer itself has no medications to be placed, once question answered drawer is considered solved
label fibrinolytic_drawer:
    if fibrinolytics_complete:
        "Looks like this drawer is complete!"
        jump main_room
    else:
        "It looks like nobody has used the fibrinolytics so they are all here"

        "This hospital has a cath lab so I bet these don't ever get used"

        "Looks like somebody left two bottles in here"

        "One of them is ezetimibe, that shouldn't be in the fibrinolytic drawer."
        
        "When would we use ezetimibe in a patient?"
        while not fibrinolytic_break:
            menu:
                "If their LDL is already below 55 mg/dl":
                    "No I don't think that patient would need ezetimibe"
                
                "If they are already on a high intensity statin and still have a high LDL level":
                    "Thats right, if the patient is on the maximally tolerated statin dose of a high intesity statin and their LDL is still >70 mg/dl we can add ezetimibe"
                    $ fibrinolytic_break = True

                "All patients at discharge from the hospital after an ACS event":
                    "No I don't think every single person who has an ACS event needs to be on ezetimibe"
                
                "Ezetimibe is never used for ACS patients as it is contraindicated":
                    "No I think there are definitely patients who have had ACS who could benefit from ezetimibe"
        
    "The other bottle was some prasugrel. Lets take that."

    show screen pillbottle("Prasugrel found!")

    $ inventory.append("Prasugrel")

    $ fibrinolytics_complete = True

    window hide
    pause

    hide screen pillbottle

    jump main_room

#Landing screen for work up drawer and treatment drawer puzzles to create solved that redirects to main room
label drawer_fully_stocked:
    "Got that added!"

    "The drawer is fully stocked now!"

    jump main_room


label GameOver:
    show edroom

    "Good job! You got the cart refilled!"

    "Just in time too! I hear the next STEMI rolling in!"

    "I hope you enjoyed the ACS review!"

    $ renpy.quit()
