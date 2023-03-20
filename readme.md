[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7708972.svg)](https://doi.org/10.5281/zenodo.7708972)


### General
The experiment was created at the University of Amsterdam by Lucija Blaževski for the project *Misinformation in Perceptual Decision Making*. 


### Citation
Blaževski, L. (2023). Colour Classification Paradigm for Social Influences on Decision-Making: PsychoPy Version [Computer software]. https://doi.org/https://doi.org/10.5281/zenodo.7708972


### Theoretical Description
The experiment is aimed to test the social influence on decision-making. 
An abundance of psychological research throughout the years focused on the effect of conformity and social pressure on decision making. 
It has been widely shown that the social influence alters individual's decision. This, however, raised an interesting question regarding whether socials factors could
influence basic perceptual processing. A series of studies explored colour classification paradigms to examine underlying perceptual and judgemental 
influences on decision-making. 
In these studies, ambiguous visual stimuli of either dominantly blue or orange colour were utilized (Germar et al., 2013; Germar et al., 2016, Voss et al., 2008).
The present experiment uses the same stimuli to study the effects of source trustworthiness on perception when providing (mis)information. 

### Procedure
To study the effect of source trustworthiness on perception, participants were told that the task has been previously performed by a trained artificial intelligence (AI) and a student assistant.
They were presented with a grid containing blue and orange pixels. The ratio of orange to blue pixels was varied. On each trial, participants were asked if the grid was predominantly orange or blue.
Before seeing the grid, participants heard the voice of either the research assistant or the AI, that supposedly represented their response on the same trial. 
Particioants were instructed to ignore the auditive ratings of the AI and a student assistant, because their responses were necessary to validate the choices made by these sources. 

### Task
#### Layout
The experiment starts with task innstructions, followed by questions *'On a scale from 1 to 100, how accurately do you think a trained AI algorithm categorizes colours?'* and *'On a scale from 1 to 100, how accurately do you think people categorize colours?'*
The practice session follows, with the 10 practice trials having no time limit. The purpose of this practice block is to familiarize participants with stimuli and response keys.
The second practice block fully resembles the actual experiment and, therefore, has the time limit for colour judgment.
The experiment consist of two blocks - one for each information source. Thus, there is an AI block and a human block. Each block consists of 240 trials and has a 30-second break after 120 trials. 
In-between blocks, there in an unlimited break.

#### Trial
Each trial starts with a 1000 ms fixation cross during which the (AI's or student assistant's) voice is played. Then, the visual stimulus is shown for 1500 ms during which
the participant has to rate the dominant colour of the grid with the use of 'S' and 'D' keys on the keyboard. Each trial ends with the question 'How certain are you about your answer?' 
The certainty is rated from 1 ('*very uncertain*') to 4 ('*very certain*') with a mouse click on a scale. 

#### Extra information
Block order and the keys to respond 'orange' or 'blue' were counterbalanced across subjects. Therefore, there are 4 versions of the experiment, each in a different script. See the next sections for details.

### File guide
instructions = folder with *.JPG* images representing task instructions.


sounds = folder with *.wav* sound files with AI and human voices.


AI voices.zip = zipped files of different voices that could be used as an alternative to the voices in the 'sounds' folder.


**AI-H_orangeD.py** = Experiment version with the AI block coming first and response 'orange' given with the 'D' key.


**AI-H_orangeS.py** = Experiment version with the AI block coming first and response 'orange' given with the 'S' key.


**H-AI_orangeD.py** = Experiment version with the human block coming first and response 'orange' given with the 'D' key.


**H-AI_orangeS.py** = Experiment version with the human block coming first and response 'orange' given with the 'S' key.


conditions_ai.xlsx = condition file for the AI block specifying parameters for each trial: 
                    1) a proportion of blue pixels (0.5, 0.475, or 0.525), 
                    2) a number of blue pixels (8192, 8602, or 7782, 
                    and 3) a response given by a source ('ORANGE' or 'BLUE').
                    

conditions_h.xlsx = condition file for the human block specifying parameters for each trial: 
                    1) a proportion of blue pixels (0.5, 0.475, or 0.525), 
                    2) a number of blue pixels (8192, 8602, or 7782, 
                    and 3) a response given by a source ('ORANGE' or 'BLUE').


grid function.py = can be ignored. The script that contains only the function used to generate the grid with blue and orange pixels.


instructions_misinformation.pptx = *ppt* file that was used to create *JPG* images of instructions. If adapted, slides have to be exported again as *JPG* with names remaining the same as in the *.py* folder or the script has to be adjusted.


practiceconditions_ai.xlsx = condition file for the AI practice block.


practiceconditions_h. xlsx = condition file for the human practice block.
### Usage
The script can be re-used on any device with PsychoPy. The full folder should be downloaded and un-zipped. Names and a location of sub-folders should not be changed or the script should be adjusted accordingly.
