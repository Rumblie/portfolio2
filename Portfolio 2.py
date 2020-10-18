# load package
from psychopy import visual, core, event, gui, data
import pandas as pd
#Define window
win = visual.Window(color = "black")

#Dialog gui
dialog = gui.Dlg(title = "Portfolio 2")
dialog.addField("Participant ID")
dialog.addField("Age:")
dialog.addField("Gender:", choices = ["Female", "Male", "Other"])
dialog.addField("Condition", choices = ["0", "1"])
# Show dialog
dialog.show()

#Saving dialog as variables
if dialog.OK:
    ID = dialog.data[0]
    Age = dialog.data[1]
    Gender = dialog.data[2]
    Condition = dialog.data[3]
elif dialog.Cancel:
    core.quit()
    
# Loging date
date = data.getDateStr()

#Defining columns
columns = ["Timestamp", "ID", "Age", "Gender", "Condition", "Word", "ReactionTime"]

#Creating data frame
DATA = pd.DataFrame(columns = columns)

#Prepare variables
stopwatch = core.Clock()
Key_List = ["space", "escape"]

#Saving my texts in variables
WelcomeTxt = '''
Hello and welcome!!
Relax and get comfortable the experiement is about to begin.  
You shall press SPACEBAR to go to the next page.
'''
IntroTxt = '''
To complete the experiment following must be done: 
1. A story will be shown to you
2. Read the one presented word at a time
3. Press 'space' to continue to the next word
4. Enjoy the story :)
5. (Press SPACEBAR to begin) 
'''
# Choosing what world will be shown in storyG based on condition
if Condition == "0":
    Word_change = "father"
elif Condition == "1":
    Word_change = "Lego"
storyG = '''
Once upon a time there was a boy named Thomas. 
One day walking home from school he stopped at a red light and took a deep breath. 
A tall dark man noticed Thomas' explicit face expression and asked: "Are you okay son?" 
Thomas reacted with a little squeak and a frightened jump. 
He then stuttered: "My mom always told me not to talk to strangers". 
The tall dark man replied: "But I am no stranger, you already know me very well". 
With a new look Thomas inspected the mysterious figure and out of thin air things suddenly made sense. 
Can it be? Is it really my {}? 
Thomas gathered all his courage and hugged the suddenly so familiar face next to him.
'''.format(Word_change)
OutroTxt = '''
Hello my beautiful {}!
Thank you for participating in our experiment. Did you figure it out? What are we testing for?
As a reward for being such a super duper fantastic participant you get a coupon for 1 free massage from your experiment supervisor.
You're very welcome. Have a nice day <3
Goodbye!
'''.format(ID)

#Prepare Functions
# Making a text presentation function
def txt_present(x):
    txt = visual.TextStim(win, text = x)
    txt.draw()
    win.flip()
    key = event.waitKeys(keyList = Key_List)
#Making a function that splits text and presents it word by word. 
def split_present(story):
    global DATA
    split_word = story.split()
    for word in split_word:
        txt = visual.TextStim(win, text = word)
        txt.draw()
        win.flip()
        stopwatch.reset()
        key = event.waitKeys(keyList = Key_List)
        reaction_time = stopwatch.getTime()
        if key[0] == "escape":
            core.quit()
            win.close()
            # Saving data intro pre defined columns
        DATA = DATA.append({
            "Timestamp":date,
            "ID": ID,
            "Age":Age,
            "Gender": Gender,
            "Condition": Condition,
            "Word": word,
            "ReactionTime": reaction_time}, ignore_index = True)


#Running experiment 
txt_present(WelcomeTxt)
txt_present(IntroTxt)
split_present(storyG)
txt_present(OutroTxt)

# Choosing data file directory based in condition 
if Condition == "0":
    logfilename = "logfiles/Condition0/logfile_{}_{}.csv".format(ID,date)
elif Condition == "1":
    logfilename = "logfiles/Condition1/logfile_{}_{}.csv".format(ID,date)
#Saving data as csv file.
DATA.to_csv(logfilename)

