"""
Created on Mon July 4 15:29:42 2022
"""

"""
Project:    Misinformation in Perceptual Decision Making
Last edit:  26/7/2022
Authors:    Lucija Blaževski
Notes:      Version 1: Block AI + Block human, d = orange, b = blue
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
    mydlg       = gui.DlgFromDict(dictionary = dlginfo, title = "Perceptual decision making")
    filename    = my_directory + "/Data/p" + str(dlginfo["Participant number"]) 
    
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
cond_df_ai = pandas.read_excel (my_directory + '/conditions_ai.xlsx')
cond_df_ai = cond_df_ai.sample(frac=1)

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
                                   image = my_directory + "/Instructions/welcome.jpg")
                                   
myMarker = visual.TextStim(win, 
                           text = '', 
                           units = 'norm')
                           
ratingScale = visual.RatingScale(win, 
                                 low = 1, 
                                 high = 4,
                                 marker=myMarker, stretch = 2,
                                 tickMarks = [1, 2, 3, 4], 
                                 tickHeight = 1.5,  
                                 singleClick = True,
                                 labels = ("1 = very uncertain", '2','3', '4 = very certain'),
                                 showAccept = False, 
                                 minTime = 0.0001,
                                 lineColor = 'black', 
                                 textColor = 'black',
                                 noMouse = True, 
                                 respKeys = ['s', 'd', 'k', 'l'])
                                 
myItem = visual.TextStim(win, 
                         pos = (0,0.3),
                         text="How certain are you about your answer?", 
                         height=.08, 
                         units='norm', 
                         color = 'black')

s = visual.TextStim(win,
                    text = 'S',
                    pos = (-0.6, -0.29),
                    height=.08,
                    units = 'norm',
                    color = 'darkgray')

d = visual.TextStim(win,
                    text = 'D',
                    pos = (-0.2, -0.29),
                    height=.08,
                    units = 'norm',
                    color = 'darkgray')
                    
k = visual.TextStim(win,
                    text = 'K',
                    pos = (0.2, -0.29),
                    height=.08,
                    units = 'norm',
                    color = 'darkgray')
                    
l = visual.TextStim(win,
                    text = 'L',
                    pos = (0.6, -0.29),
                    height=.08,
                    units = 'norm',
                    color = 'darkgray')
                    
                                        
# Define sound elements:
sound_ai_o = sound.Sound (my_directory + '/sounds/OrangeAI.wav')
sound_ai_b = sound.Sound (my_directory + '/sounds/BlueAI.wav')
sound_h_o = sound.Sound (my_directory + '/sounds/OrangeH.wav')
sound_h_b = sound.Sound (my_directory + '/sounds/BlueH.wav')


# Create a function to display instructions
def display_instructions(file = "instructions.jpg"):
    
    instructions.image = file
    instructions.draw()
    win.flip()
    event.clearEvents(eventType = "keyboard")
    keys = event.waitKeys(keyList = "space")



###################
## COLORED PATCH ##
###################

# Create a function that generates the grid with blue and orange pixels
def grid_f (re_elements_b=8192): # The argument that can be defined is the number of blue pixels
    # Create grid
    num_check = 128
    check_size = [5, 5]
    location = [0, 0]
    # Generate loc array
    loc = np.array(location) + np.array(check_size) // 2
    orange = np.array([1, 0.294117647058824, -1])   # RGB code for orange 
    blue = np.array([0.0588235294117647, 0.615686274509804, 0.96078431372549])   # RGB code for blue
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
    grid = visual.ElementArrayStim(win,
                                   xys=xys,
                                   fieldPos=loc,
                                   colors=col,
                                   nElements=num_check ** 2,
                                   elementMask=None,
                                   elementTex=None,
                                   sizes=(check_size[0],
                                          check_size[1]))
    return grid
    
    

########################
### BEGIN EXPERIMENT ###
########################

# Display the instructions
display_instructions(file = my_directory + "/instructions/welcome.jpg")
display_instructions(file = my_directory + "/instructions/ins2.jpg")
display_instructions(file = my_directory + "/instructions/ins3_do.jpg")
display_instructions(file = my_directory + "/instructions/ins4_ai.jpg")
display_instructions(file = my_directory + "/instructions/ins5_ai.jpg")
display_instructions(file = my_directory + "/instructions/ins6.jpg")
display_instructions(file = my_directory + "/instructions/ins7_do.jpg")
display_instructions(file = my_directory + "/instructions/ins8_do.jpg")


# Start of the trial loop
trial_nr = 0

for idx, row in cond_df_ai.iterrows():
    trial_nr += 1
    
    # Extract current number of blue squares and the voice
    curr_blue_nr = int(row['orange_n'])
    curr_voice = row['voice']
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
     
    # Save trail info
    AIexp.addData("block", 'AI')        
    AIexp.addData("trial_index", idx)
    AIexp.addData("trial_nr", trial_nr)  
    AIexp.addData("trial_type", trial_type)  
    AIexp.addData("blue_squares_nr",  curr_blue_nr)
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
        win.flip()

        # Get responses
        keys = kb.getKeys(['s','d', 'k','l','escape', None])
        if 'escape' in keys:
            core.quit()
        if len(keys) > 0:  # If not an empty list ...
            # Only pick the last one [-1]
            # Overwrite existing data with current one
            response = keys[-1].name
            reaction_time = keys[-1].rt
            
    if curr_blue_nr == 8192:
        accuracy = 'NA'
    elif ((response == 'd') or (response == 's')) and (curr_blue_nr == 7782):
        accuracy = 1
    elif ((response == 'k') or (response == 'l')) and (curr_blue_nr == 8602):
        accuracy = 1
    else:
        accuracy = 0 
    
    AIexp.addData("response", response)
    AIexp.addData("accuracy", accuracy)    
    AIexp.addData("rt", reaction_time)    
    
    my_clock.reset()
    kb.clearEvents(eventType='keyboard')
    ratingScale.reset()
    
    while ratingScale.noResponse:
        myItem.draw()
        ratingScale.draw()
        s.draw()
        d.draw()
        k.draw()
        l.draw()
        win.flip()
        if event.getKeys(['escape']):
            core.quit()
        
    rating = ratingScale.getRating()
    decisionTime = ratingScale.getRT()
    AIexp.addData("certainty", rating)   
    AIexp.addData("rt_certainty", decisionTime)    
    
    # Proceed to next line of the output file
    AIexp.nextEntry()
    
    ratingScale.reset()
    
    # Exit after a few trials in the demo version
    if earlyExit == 1 and trial_nr == 3:
        break
    
 
 
#################
## BLOCK BREAK ##
#################

display_instructions(file = my_directory + "/instructions/blockswitch_do_ai.jpg")
 
cond_df_h = pandas.read_excel (my_directory + '/conditions_h.xlsx')
cond_df_h = cond_df_h.sample(frac=1)


# Start of the trial loop
trial_nr = 0

for idx, row in cond_df_ai.iterrows():
    trial_nr += 1
    
    # Extract current number of blue squares and the voice
    curr_blue_nr = int(row['orange_n'])
    curr_voice = row['voice']
    nextFlip = win.getFutureFlipTime(clock='ptb')
        
    # Load the sound based on the condition
    if curr_voice == 'ORANGE':
        sound_h_o.play(when=nextFlip)  # Sync with screen refresh
    else: 
        sound_h_b.play(when=nextFlip)

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
     
    # Save trail info
    AIexp.addData("block", 'human')        
    AIexp.addData("trial_index", idx)
    AIexp.addData("trial_nr", trial_nr)  
    AIexp.addData("trial_type", trial_type)  
    AIexp.addData("blue_squares_nr",  curr_blue_nr)
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
        win.flip()

        # Get responses
        keys = kb.getKeys(['s','d', 'k','l','escape', None])
        if 'escape' in keys:
            core.quit()
        if len(keys) > 0:  # If not an empty list ...
            # Only pick the last one [-1]
            # Overwrite existing data with current one
            response = keys[-1].name
            reaction_time = keys[-1].rt
            
    if (response == 'd') or (response == 's') and (curr_blue_nr == 7782):
        accuracy = 1
    elif (response == 'k') or (response == 'l') and (curr_blue_nr == 8602):
        accuracy = 1
    elif curr_blue_nr == 8192:
        accuracy = 'NA'
    else:
        accuracy = 0 
    
    AIexp.addData("response", response)
    AIexp.addData("accuracy", accuracy)    
    AIexp.addData("rt", reaction_time)    
    
    my_clock.reset()
    kb.clearEvents(eventType='keyboard')
    ratingScale.reset()
    
    while ratingScale.noResponse:
        myItem.draw()
        ratingScale.draw()
        s.draw()
        d.draw()
        k.draw()
        l.draw()
        win.flip()
        if event.getKeys(['escape']):
            core.quit()
        
    rating = ratingScale.getRating()
    decisionTime = ratingScale.getRT()
    AIexp.addData("certainty", rating)   
    AIexp.addData("rt_certainty", decisionTime)    
    
    # Proceed to next line of the output file
    AIexp.nextEntry()
    
    ratingScale.reset()
    
    # Exit after a few trials in the demo version
    if earlyExit == 1 and trial_nr == 3:
        break
    
 
display_instructions(file = my_directory + "/instructions/ciao.jpg")