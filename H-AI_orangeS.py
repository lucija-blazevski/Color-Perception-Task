"""
Created on Mon July 4 15:29:42 2022
"""

"""
Project:    Misinformation in Perceptual Decision Making
Last edit:  29/8/2022
Authors:    Lucija Blaževski
Notes:      Version 1: Block H + Block AI,  s = orange, d = blue
"""


####################
## Import Modules ##
####################

# Import modules
import numpy as np
from psychopy import visual, event, core, gui, data, sound
import os, math, pandas, random, time
from psychopy.hardware import keyboard
import psychtoolbox as ptb


##########
## Test ##
##########

# Provide a short test while programming (if set to 1)
earlyExit = 0



#########################
## Datafile Management ##
#########################

# Set directory
my_directory = os.getcwd()

# Create and save datafile
exists = True
while exists:

    dlginfo     = {"Participant number": 0, "Gender": ["Female","Male", 'Other', 'Prefer not to say'], "Handedness": ["Right","Left"], "Age": 0}
    mydlg       = gui.DlgFromDict(dictionary = dlginfo, title = "Perceptual Decision Making")
    filename    = my_directory + "/data/p" + str(dlginfo["Participant number"]) 
    
    if not os.path.isfile(filename + ".csv"):
        exists  = False
    else:
        mydlg2  = gui.Dlg(title = "Error")
        mydlg2.addText("Participant number already exists. Please enter another one.")
        mydlg2.show
        


####################
## Initialization ##
####################

# Initilialize the experiment handler and perform randomization
AIexp = data.ExperimentHandler(dataFileName = filename, extraInfo = dlginfo)
cond_df_h = pandas.read_excel (my_directory + '/conditions_h.xlsx')
cond_df_h = cond_df_h.sample(frac=1)

# Prepare the keyboard (response) module
kb = keyboard.Keyboard()

# Create clock
my_clock = core.Clock()

# Define visual elements:
win = visual.Window(units='pix', 
                    fullscr = True, 
                    color = [211,211,211])
            
fix = visual.TextStim(win, 
                      text = "+", 
                      pos = (0, 0), 
                      height = 60, 
                      color = 'black')

instructions    = visual.ImageStim(win, 
                                   size = (1500, 1000), 
                                   pos = (0, 0), 
                                   image = my_directory + "/Instructions/welcome.JPG")
                                   
ratingScale = visual.RatingScale(win, 
                                 low = 1, 
                                 high = 4,
                                 marker='circle', stretch = 2,
                                 tickMarks = [1, 2, 3, 4], 
                                 tickHeight = 1.5,  
                                 singleClick = True,
                                 labels = ("1 = very uncertain", '2','3', '4 = very certain'),
                                 showAccept = False, 
                                 minTime = 0.0001,
                                 lineColor = 'black', 
                                 textColor = 'black',
                                 noMouse = False)
                                 
myItem = visual.TextStim(win, 
                         pos = (0,0.3),
                         text="How certain are you about your answer?", 
                         height=.08, 
                         units='norm', 
                         color = 'black')

orange_legend = visual.TextStim (win, 
                            text = 'ORANGE', height = 37, colorSpace = 'rgb255',
                            color = [197, 102, 20], 
                            pos = (-200, -380))
                            
orange_key = visual.TextStim (win, 
                            text = 'S', height = 30, color = 'black',   
                            pos = (-200, -430))
                            
blue_legend = visual.TextStim (win, 
                            text = 'BLUE', height = 37, colorSpace = 'rgb255', 
                            color = [29, 44, 160],   
                            pos = (200, -380))
                            
blue_key = visual.TextStim (win, 
                            text = 'D', height = 30, color = 'black',   
                            pos = (200, -430))

blank = visual.TextStim(win, 
                      text = "", 
                      pos = (0, 0), 
                      height = 60, 
                      color = 'black')

reliability1 = visual.RatingScale (win, 
                                low=0, high=100, 
                                marker='slider',
                                tickMarks=[0, 50, 100], 
                                stretch=2.3, 
                                tickHeight=1.5, 
                                labels=["1 = completely inaccurately",'', "100 = completely accurately"], 
                                lineColor = 'black', textColor = 'black', 
                                pos = (0,-0.2))
                                

reliability1_text = visual.TextStim (win, text= "On a scale from 1 to 100, how accurately do you think a trained AI algorithm categorizes colours?",
                                    height=.08, 
                                    units='norm', 
                                    color = 'black', 
                                    pos = (0,0.3))

reliability2 = visual.RatingScale (win, 
                                low=0, high=100, 
                                marker='slider',
                                tickMarks=[0, 50, 100], 
                                stretch=2.3, 
                                tickHeight=1.5, 
                                labels=["1 = completely inaccurately",'', "100 = completely accurately"], 
                                lineColor = 'black', textColor = 'black', 
                                pos = (0,-0.2))
                                

reliability2_text = visual.TextStim (win, text= "On a scale from 1 to 100, how accurately do you think a psychology student categorizes colours?",
                                    height=.08, 
                                    units='norm', 
                                    color = 'black', 
                                    pos = (0,0.3))                   
# Define sound elements:
sound_ai_o = sound.Sound (my_directory + '/sounds/OrangeAI.wav')
sound_ai_b = sound.Sound (my_directory + '/sounds/BlueAI.wav')
sound_h_o = sound.Sound (my_directory + '/sounds/OrangeH.wav')
sound_h_b = sound.Sound (my_directory + '/sounds/BlueH.wav')

# Create a function to display instructions
def display_instructions(file = "instructions.JPG"):
    
    instructions.image = file
    instructions.draw()
    win.flip()
    event.clearEvents(eventType = "keyboard")
    keys = event.waitKeys(keyList = "space")

# Create a function to display break
def display_break(file = "instructions.JPG"):
    
    instructions.image = file
    instructions.draw()
    win.flip()



###################
## COLORED PATCH ##
###################

# Create a function that generates the grid with blue and orange pixels
def grid_f (re_elements_b): # The argument that can be defined is the number of blue pixels
    
    # Create grid
    num_check = 128
    check_size = [5, 5]
    location = [0, 0]
    
    # Generate loc array
    loc = np.array(location) + np.array(check_size) // 2
    orange = np.array([197, 102, 20])   # RGB code for orange 
    blue = np.array([29, 44, 160])   # RGB code for blue
    orange_full = np.tile(orange, ((128*128)-re_elements_b, 1))
    blue_full = np.tile(blue, (re_elements_b, 1))
    together = np.concatenate((orange_full, blue_full))
    rand_colors = sorted(together, key=lambda x: random.random())
    col = rand_colors
    
    # Array of coordinates for each element
    xys = []
    
    # Populate xys
    low, high = num_check // -2, num_check // 2
    for y in range(low, high):
        for x in range(low, high):
            xys.append((check_size[0] * x,
                        check_size[1] * y))
                        
    # Use all of it to create a visual element                
    grid = visual.ElementArrayStim(win,
                                   xys=xys,
                                   fieldPos=loc,
                                   colors=col,colorSpace='rgb255',
                                   nElements=num_check ** 2,
                                   elementMask=None,
                                   elementTex=None,
                                   sizes=(check_size[0],
                                          check_size[1]))
    return grid
    
click = event.Mouse()

########################
### BEGIN EXPERIMENT ###
########################
while reliability1.noResponse:
    # Make mouse visible 
    win.mouseVisible = True
    reliability1.draw()
    reliability1_text.draw()
    win.flip()
    if event.getKeys(['escape']):
        core.quit() 

AIexp.addData("reliability_AI", reliability1.getRating())

while reliability2.noResponse:
    # Make mouse visible 
    win.mouseVisible = True
    reliability2.draw()
    reliability2_text.draw()
    win.flip()
    if event.getKeys(['escape']):
        core.quit() 

AIexp.addData("reliability_H", reliability2.getRating())

# Proceed to next line of the output file
AIexp.nextEntry()

# Make mouse invisible for the first part 
win.mouseVisible = False

# Display the instructions
display_instructions(file = my_directory + "/instructions/welcome.JPG")
display_instructions(file = my_directory + "/instructions/ins2.JPG")
display_instructions(file = my_directory + "/instructions/ins3_so.JPG")
display_instructions(file = my_directory + "/instructions/ins4_h.JPG")
display_instructions(file = my_directory + "/instructions/ins5_h.JPG")
display_instructions(file = my_directory + "/instructions/ins6.JPG")
display_instructions(file = my_directory + "/instructions/ins7_so.JPG")
display_instructions(file = my_directory + "/instructions/ins8_so.JPG")

#############
## PRACTICE #
#############
display_instructions(file = my_directory + "/instructions/practice1.JPG")
display_instructions(file = my_directory + "/instructions/practice2.JPG")

## NO LIMIT ##
# Start of the practice trial loop - human block
pcond_df_h = pandas.read_excel (my_directory + '/practiceconditions_h.xlsx')
pcond_df_h = pcond_df_h.sample(5)

trial_nr = 0

for idx, row in pcond_df_h.iterrows():
    trial_nr += 1
    
    # Extract current number of blue squares and the voice
    curr_blue_nr = int(row['orange_n'])
    curr_voice = row['voice']

    # Get time to sync the sound with the window flip
    nextFlip = win.getFutureFlipTime(clock='ptb')
        
    # Load the sound based on the condition
    if curr_voice == 'ORANGE':
        sound_h_o.play(when=nextFlip)  # Sync with screen refresh
    else: 
        sound_h_b.play(when=nextFlip)

    # Create and draw the grid
    grid = grid_f(re_elements_b = curr_blue_nr)
    
    # Present stimuli
    my_clock.reset()
    kb.clearEvents(eventType='keyboard')
    kb.clock.reset()
    while my_clock.getTime() < 1:
        fix.draw()
        kb.clearEvents(eventType='keyboard')
        kb.clock.reset()
        win.flip()
    else:
        grid.draw()
        blue_legend.draw()
        blue_key.draw()
        orange_legend.draw()
        orange_key.draw()
        win.flip()    

        # Get responses
        keys = kb.waitKeys(keyList = ['s','d', 'escape', None])
        if 'escape' in keys:
            core.quit()  
    
    my_clock.reset()
    kb.clearEvents(eventType='mouse')
    ratingScale.reset()
    
    # Reset mouse position
    click.setPos(newPos=(0,0))
    
    while ratingScale.noResponse:
        # Make mouse visible 
        win.mouseVisible = True
        myItem.draw()
        ratingScale.draw()
        win.flip()
        if event.getKeys(['escape']):
            core.quit() 
   
    win.mouseVisible = False

    # Inter-trial blank screen
    my_clock.reset()
    while my_clock.getTime()<0.5:
        blank.draw()
        win.flip()
    
    ratingScale.reset()

display_instructions(file = my_directory + "/instructions/practice3.JPG")

# Start of the practice trial loop - AI block
pcond_df_ai = pandas.read_excel (my_directory + '/practiceconditions_ai.xlsx')
pcond_df_ai = pcond_df_ai.sample(5)

trial_nr = 0

for idx, row in pcond_df_ai.iterrows():
    trial_nr += 1
    
    # Extract current number of blue squares and the voice
    curr_blue_nr = int(row['orange_n'])
    curr_voice = row['voice']

    # Get time to sync the sound with the window flip
    nextFlip = win.getFutureFlipTime(clock='ptb')
        
    # Load the sound based on the condition
    if curr_voice == 'ORANGE':
        sound_ai_o.play(when=nextFlip)  # Sync with screen refresh
    else: 
        sound_ai_b.play(when=nextFlip)

    # Create and draw the grid
    grid = grid_f(re_elements_b = curr_blue_nr)
    
    # Present stimuli
    my_clock.reset()
    kb.clearEvents(eventType='keyboard')
    kb.clock.reset()
    while my_clock.getTime() < 1:
        fix.draw()
        kb.clearEvents(eventType='keyboard')
        kb.clock.reset()
        win.flip()
    else:
        grid.draw()
        blue_legend.draw()
        blue_key.draw()
        orange_legend.draw()
        orange_key.draw()
        win.flip()    

        # Get responses
        keys = kb.waitKeys(keyList = ['s','d', 'escape', None])
        if 'escape' in keys:
            core.quit()  
    
    my_clock.reset()
    kb.clearEvents(eventType='mouse')
    ratingScale.reset()
    
    # Reset mouse position
    click.setPos(newPos=(0,0))
    
    while ratingScale.noResponse:
        # Make mouse visible 
        win.mouseVisible = True
        myItem.draw()
        ratingScale.draw()
        win.flip()
        if event.getKeys(['escape']):
            core.quit() 
   
    win.mouseVisible = False

    # Inter-trial blank screen
    my_clock.reset()
    while my_clock.getTime()<0.5:
        blank.draw()
        win.flip()
    
    ratingScale.reset()
    

## TIME LIMITED ##
##################
display_instructions(file = my_directory + "/instructions/practice4.JPG")
display_instructions(file = my_directory + "/instructions/practice5.JPG")

# Start of the practice trial loop - human block
trial_nr = 0

for idx, row in pcond_df_h.iterrows():
    trial_nr += 1
    
    # Extract current number of blue squares and the voice
    curr_blue_nr = int(row['orange_n'])
    curr_voice = row['voice']

    # Get time to sync the sound with the window flip
    nextFlip = win.getFutureFlipTime(clock='ptb')
        
    # Load the sound based on the condition
    if curr_voice == 'ORANGE':
        sound_h_o.play(when=nextFlip)  # Sync with screen refresh
    else: 
        sound_h_b.play(when=nextFlip)

    # Create and draw the grid
    grid = grid_f(re_elements_b = curr_blue_nr)
    
    # Present stimuli
    my_clock.reset()
    kb.clearEvents(eventType='keyboard')
    kb.clock.reset()
    while my_clock.getTime() < 2.5:
        # Draw stuff
        if my_clock.getTime() < 1:
            fix.draw()
            kb.clearEvents(eventType='keyboard')
            kb.clock.reset()
        else:
            grid.draw()
            blue_legend.draw()
            blue_key.draw()
            orange_legend.draw()
            orange_key.draw()
        win.flip()

        # Get responses
        keys = kb.getKeys(['s','d', 'escape', None])
        if 'escape' in keys:
            core.quit()
    
    my_clock.reset()
    kb.clearEvents(eventType='mouse')
    ratingScale.reset()
    
    # Reset mouse position
    click.setPos(newPos=(0,0))
    
    while ratingScale.noResponse:
        # Make mouse visible 
        win.mouseVisible = True
        myItem.draw()
        ratingScale.draw()
        win.flip()
        if event.getKeys(['escape']):
            core.quit() 
   
    win.mouseVisible = False

    # Inter-trial blank screen
    my_clock.reset()
    while my_clock.getTime()<0.5:
        blank.draw()
        win.flip()
    
    ratingScale.reset()
    
# Start of the practice trial loop - AI block
display_instructions(file = my_directory + "/instructions/practice3.JPG")

trial_nr = 0

for idx, row in pcond_df_ai.iterrows():
    trial_nr += 1
    
    # Extract current number of blue squares and the voice
    curr_blue_nr = int(row['orange_n'])
    curr_voice = row['voice']

    # Get time to sync the sound with the window flip
    nextFlip = win.getFutureFlipTime(clock='ptb')
        
    # Load the sound based on the condition
    if curr_voice == 'ORANGE':
        sound_ai_o.play(when=nextFlip)  # Sync with screen refresh
    else: 
        sound_ai_b.play(when=nextFlip)

    # Create and draw the grid
    grid = grid_f(re_elements_b = curr_blue_nr)
    
    # Present stimuli
    my_clock.reset()
    kb.clearEvents(eventType='keyboard')
    kb.clock.reset()
    while my_clock.getTime() < 2.5:
        # Draw stuff
        if my_clock.getTime() < 1:
            fix.draw()
            kb.clearEvents(eventType='keyboard')
            kb.clock.reset()
        else:
            grid.draw()
            blue_legend.draw()
            blue_key.draw()
            orange_legend.draw()
            orange_key.draw()
        win.flip()

        # Get responses
        keys = kb.getKeys(['s','d', 'escape', None])
        if 'escape' in keys:
            core.quit()
    
    my_clock.reset()
    kb.clearEvents(eventType='mouse')
    ratingScale.reset()
    
    # Reset mouse position
    click.setPos(newPos=(0,0))
    
    while ratingScale.noResponse:
        # Make mouse visible 
        win.mouseVisible = True
        myItem.draw()
        ratingScale.draw()
        win.flip()
        if event.getKeys(['escape']):
            core.quit() 
   
    win.mouseVisible = False

    # Inter-trial blank screen
    my_clock.reset()
    while my_clock.getTime()<0.5:
        blank.draw()
        win.flip()
    
    ratingScale.reset()
        


#######################
## ACTUAL EXPERIMENT ##
#######################

display_instructions(file = my_directory + "/instructions/start.JPG")

# Start of the trial loop
trial_nr = 0

for idx, row in cond_df_h.iterrows():
    trial_nr += 1
    
    # Extract current number of blue squares and the voice
    curr_blue_nr = int(row['orange_n'])
    curr_voice = row['voice']
    
    # Get time to sync the sound with the window flip
    nextFlip = win.getFutureFlipTime(clock='ptb')
        
    # Load the sound based on the condition
    if curr_voice == 'ORANGE':
        sound_h_o.play(when=nextFlip)  # Sync with screen refresh
    else: 
        sound_h_b.play(when=nextFlip)

    # Create and draw grid
    grid = grid_f(re_elements_b = curr_blue_nr)
    
    # Save trial type, so it simplifies analysis
    if curr_blue_nr == 8192:
        trial_type = 'equal'
    elif (curr_voice == 'ORANGE') and (curr_blue_nr == 7782):
        trial_type = 'congruent'
    elif (curr_voice == 'ORANGE') and  (curr_blue_nr == 8602):
        trial_type = 'incongruent'
    elif (curr_voice == 'BLUE') and (curr_blue_nr == 7782):
        trial_type = 'incongruent'
    elif (curr_voice == 'BLUE') and (curr_blue_nr == 8602):
        trial_type = 'congruent'
    
    # Save proportion of blue pixels
    if curr_blue_nr == 8192:
        proportion_blue = 0.5
    elif curr_blue_nr == 7782:
        proportion_blue = 0.425
    elif curr_blue_nr == 8602:
        proportion_blue = 0.575
    
    # Save trail info
    AIexp.addData('Version', '1(Blockhuman+BlockAI,s=orange,d=blue)')
    AIexp.addData("block", 'human')        
    AIexp.addData("trial_index", idx)
    AIexp.addData("trial_nr", trial_nr)  
    AIexp.addData("trial_type", trial_type)  
    AIexp.addData("blue_squares_nr", curr_blue_nr)
    AIexp.addData("proportion_blue",  proportion_blue)
    AIexp.addData("voice_choice", curr_voice)
    
    # Set initially to "n/a"
    response = 'NA'
    reaction_time = 'NA'
    
    # Present stimuli
    my_clock.reset()
    kb.clearEvents(eventType='keyboard')
    kb.clock.reset()
    while my_clock.getTime() < 2.5:
        # Draw stuff
        if my_clock.getTime() < 1:
            fix.draw()
            kb.clearEvents(eventType='keyboard') # So the keys pressed during the fixation do not count
            kb.clock.reset()
        else:
            grid.draw()
            blue_legend.draw()
            blue_key.draw()
            orange_legend.draw()
            orange_key.draw()
        win.flip()

        # Get responses
        keys = kb.getKeys(['s','d','escape', None])
        if 'escape' in keys:
            core.quit()
        if len(keys) > 0:  # If not an empty list 
            # Only pick the first one [0]
            # Overwrite existing data with current one
            response = keys[0].name
            reaction_time = keys[0].rt
            
    if curr_blue_nr == 8192:
        accuracy = 'NA'
    elif (response == 's') and (curr_blue_nr == 7782):
        accuracy = 1
    elif (response == 'd') and (curr_blue_nr == 8602):
        accuracy = 1
    else:
        accuracy = 0 
    
    AIexp.addData("response", response)
    AIexp.addData("accuracy", accuracy)    
    AIexp.addData("rt", reaction_time)    
    
    my_clock.reset()
    kb.clearEvents(eventType='keyboard')
    ratingScale.reset()
    
    # Reset mouse position
    click.setPos(newPos=(0,0))
    
    while ratingScale.noResponse:
        # Make mouse visible 
        win.mouseVisible = True
        myItem.draw()
        ratingScale.draw()
        win.flip()
        if event.getKeys(['escape']):
            core.quit()
        
    rating = ratingScale.getRating()
    decisionTime = ratingScale.getRT()
    AIexp.addData("certainty", rating)   
    AIexp.addData("rt_certainty", decisionTime)    
   
    win.mouseVisible = False
    
    # Inter-trial blank screen
    my_clock.reset()
    while my_clock.getTime()<0.5:
        blank.draw()
        win.flip()
        
    # Proceed to next line of the output file
    AIexp.nextEntry()
    
    ratingScale.reset() # Just in case reset it at the end of every trial
    
    # Exit after a few trials in the demo version
    if earlyExit == 1 and trial_nr == 3:
        break
        
    # Break halwfay through the block
    my_clock.reset()
    if trial_nr == 120:
        while my_clock.getTime() < 32:
        # Draw stuff
            if my_clock.getTime() < 30:
                display_break(file = my_directory + "/instructions/break.JPG")
            else:
                display_break(file = my_directory + "/instructions/attention.JPG")
 
 
#################
## BLOCK BREAK ##
#################

# Make mouse invisible for the second part 
win.mouseVisible = False

display_instructions(file = my_directory + "/instructions/blockswitch_so_h.JPG")
display_instructions(file = my_directory + "/instructions/part2.JPG") 
 
 
cond_df_ai = pandas.read_excel (my_directory + '/conditions_ai.xlsx')
cond_df_ai = cond_df_ai.sample(frac=1)

# Start of the trial loop
trial_nr = 0

for idx, row in cond_df_ai.iterrows():
    trial_nr += 1
    
    # Extract current number of blue squares and the voice
    curr_blue_nr = int(row['orange_n'])
    curr_voice = row['voice']
    
    # Get time to sync the sound with the window flip
    nextFlip = win.getFutureFlipTime(clock='ptb')
        
    # Load the sound based on the condition
    if curr_voice == 'ORANGE':
        sound_ai_o.play(when=nextFlip)  # Sync with screen refresh
    else: 
        sound_ai_b.play(when=nextFlip)

    # Create and draw image
    grid = grid_f(re_elements_b = curr_blue_nr)
    
    # Save trial type, so it simplifies analysis
    if curr_blue_nr == 8192:
        trial_type = 'equal'
    elif (curr_voice == 'ORANGE') and (curr_blue_nr == 7782):
        trial_type = 'congruent'
    elif (curr_voice == 'ORANGE') and  (curr_blue_nr == 8602):
        trial_type = 'incongruent'
    elif (curr_voice == 'BLUE') and (curr_blue_nr == 7782):
        trial_type = 'incongruent'
    elif (curr_voice == 'BLUE') and (curr_blue_nr == 8602):
        trial_type = 'congruent'
    
    # Save proportion of blue pixels
    if curr_blue_nr == 8192:
        proportion_blue = 0.5
    elif curr_blue_nr == 7782:
        proportion_blue = 0.425
    elif curr_blue_nr == 8602:
        proportion_blue = 0.575
    
    # Save trail info
    AIexp.addData('Version', '1(Blockhuman+BlockAI,s=orange,d=blue)')
    AIexp.addData("block", 'AI')        
    AIexp.addData("trial_index", idx)
    AIexp.addData("trial_nr", trial_nr)  
    AIexp.addData("trial_type", trial_type)  
    AIexp.addData("blue_squares_nr",  curr_blue_nr)
    AIexp.addData("proportion_blue",  proportion_blue)
    AIexp.addData("voice_choice",  curr_voice)
    
    # Set initially to "n/a"
    response = 'NA'
    reaction_time = 'NA'
    
    # Present stimuli
    my_clock.reset()
    kb.clearEvents(eventType='keyboard')
    kb.clock.reset()
    while my_clock.getTime() < 2.5:
        # Draw stuff
        if my_clock.getTime() < 1:
            fix.draw()
            kb.clearEvents(eventType='keyboard')
            kb.clock.reset()
        else:
            grid.draw()
            blue_legend.draw()
            blue_key.draw()
            orange_legend.draw()
            orange_key.draw()
        win.flip()

        # Get responses
        keys = kb.getKeys(['s','d','escape', None])
        if 'escape' in keys:
            core.quit()
        if len(keys) > 0:  # If not an empty list 
            # Only pick the first one [0]
            # Overwrite existing data with current one
            response = keys[0].name
            reaction_time = keys[0].rt
            
    if curr_blue_nr == 8192:
        accuracy = 'NA'
    elif (response == 's') and (curr_blue_nr == 7782):
        accuracy = 1
    elif (response == 'd') and (curr_blue_nr == 8602):
        accuracy = 1
    else:
        accuracy = 0 
    
    AIexp.addData("response", response)
    AIexp.addData("accuracy", accuracy)    
    AIexp.addData("rt", reaction_time)    
    
    my_clock.reset()
    kb.clearEvents(eventType='keyboard')
    ratingScale.reset()
    
    # Reset mouse position
    click.setPos(newPos=(0,0))
    
    while ratingScale.noResponse:
        # Make mouse visible 
        win.mouseVisible = True
        myItem.draw()
        ratingScale.draw()
        win.flip()
        if event.getKeys(['escape']):
            core.quit()
        
    rating = ratingScale.getRating()
    decisionTime = ratingScale.getRT()
    AIexp.addData("certainty", rating)   
    AIexp.addData("rt_certainty", decisionTime)    
   
    win.mouseVisible = False
    
    # Inter-trial blank screen
    my_clock.reset()
    while my_clock.getTime()<0.5:
        blank.draw()
        win.flip()
        
    # Proceed to next line of the output file
    AIexp.nextEntry()
    
    ratingScale.reset()
    
    # Exit after a few trials in the demo version
    if earlyExit == 1 and trial_nr == 3:
        break
        
    # Break halwfay through the block
    my_clock.reset()
    if trial_nr == 120:
        while my_clock.getTime() < 32:
        # Draw stuff
            if my_clock.getTime() < 30:
                display_break(file = my_directory + "/instructions/break.JPG")
            else:
                display_break(file = my_directory + "/instructions/attention.JPG")
 
#############
## THE END ##
############# 
display_instructions(file = my_directory + "/instructions/ciao.JPG")