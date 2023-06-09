#! /usr/bin/env python
# Time-stamp: <2021-03-23 22:02:10 christophe@pallier.org>
# License: Creative Commons BY-SA-NC

"""Implementation of Posner's endogeneous attention cueing task (see https://en.wikipedia.org/wiki/Posner_cueing_task). One difference with the ANT-R task (Fan et a. 2009) is that the boxe appear above or below the fixation cross, rahter than ion hte left and right. This eliminates the Simon reponse compatibility component, but make the task easier on participants.

Note: This experiment is meant to be run on FullHD (1920x1080) resolution.
"""

import random
import pandas as pd
import argparse
from expyriment import design, control, stimuli, misc

GREY = (80, 80, 80)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

CUE_DISPLAY_DURATION = 100  # 100 in hte original paper
CUE_TARGET_INTERVAL = 400  # 0, 400 or 800 in the original paper
TARGET_DISPLAY_DURATION = 200  # 500 in the original paper
MAX_RESPONSE_DURATION = 1700

LEFT_RESPONSE_KEY = misc.constants.K_f
LEFT_RESPONSE_KEY_CHAR = 'F'
RIGHT_RESPONSE_KEY = misc.constants.K_j
RIGHT_RESPONSE_KEY_CHAR = 'J'

INSTRUCTIONS_FRENCH = f"""Vous allez voir des séquences de flèches comme les suivantes :

< < < < <
> > < < <
> > > > >
< < > > >

Votre tâche sera de déterminer, le plus rapidement possible, la direction vers laquelle pointe la flèche centrale
("gauche"  sur les deux premières lignes ci-dessus, "droite" pour les deux dernières).
    
Les flèches qui l'entourent n'ont pas d'importance, la seule à laquelle vous devez prêter attention est celle du milieu.

Ces flèches s'afficheront dans une "boîte" placée au dessus ou en dessous d'une croix de fixation placée au centre de l'écran.
Parfois, la couleur de ces boîtes changera un peu avant que les flèches apparaissent, pour vous permettre de vous mieux vous préparer à répondre.
Quand une seule boîte changera, cela indiquera la position *la plus probable*  où apparaitront les flèches.

Vous indiquerez votre réponse en appuyant sur la touche '{LEFT_RESPONSE_KEY_CHAR}' si la flèche du milieu pointe vers la gauche, sur '{RIGHT_RESPONSE_KEY_CHAR}' si la flèche pointe vers la droite.
   
Très important:
    1. Il faut fixer en permanence la croix centrale et ne pas déplacer les yeux.
    2. Vous devez répondre rapidement tout en évitant les erreurs. Celles-ci sont néanmoins quasi inevitables. Si vous en faites, ne vous déconcentrez pas, et concentrez vous pour l'essai suivant.

Placez vos index sur les touches '{LEFT_RESPONSE_KEY_CHAR}' (gauche) et '{RIGHT_RESPONSE_KEY_CHAR}' (droite) puis appuyez sur la barre espace pour démarrer,

Bonne expérience !
"""


##################################################################
# Read the trials list

parser = argparse.ArgumentParser()
parser.add_argument("--training", action="store_true")
parser.add_argument("--mri", action="store_true")
args = parser.parse_args()


if args.training:
    print("TRAINING mode!")
    trials = pd.read_csv('trials-vertical-training.csv')
    trials = trials.sample(frac=1)
else:
    trials = pd.read_csv('trials-vertical.csv')
    trials = trials.sample(frac=1)

##################################################################
exp = design.Experiment(name="ANT-R-task",
                        text_size=25,
                        background_colour=GREY,
                        foreground_colour=WHITE)
# control.set_develop_mode()
control.initialize(exp)

##################################################################
blankscreen = stimuli.BlankScreen(colour=GREY)

cross_black = stimuli.FixCross(size=(30, 30), colour=BLACK, line_width=4)
cross_green = stimuli.FixCross(size=(30, 30), colour=GREEN, line_width=4)
cross_red = stimuli.FixCross(size=(30, 30), colour=RED, line_width=4)

cross_black.preload()
cross_green.preload()
cross_red.preload()

fixation_crosses = dict(neutral=cross_black, 
                        positive=cross_green, 
                        negative=cross_red)

### target stimuli

fontfile = "freesans"

# arrows_cong_left = stimuli.TextLine("← ← ← ← ←", text_font=fontfile, text_size=50)
# arrows_cong_right = stimuli.TextLine("→ → → → →", text_font=fontfile, text_size=50)
# arrows_incong_left = stimuli.TextLine("→ → ← → →", text_font=fontfile, text_size=50)
# arrows_incong_right = stimuli.TextLine("← ← → ← ←", text_font=fontfile, text_size=50)

arrows_cong_left = stimuli.TextLine(" < < < < < ", text_font=fontfile, text_size=50)
arrows_cong_right = stimuli.TextLine(" > > > > > ", text_font=fontfile, text_size=50)
arrows_incong_left = stimuli.TextLine(" > > < > > ", text_font=fontfile, text_size=50)
arrows_incong_right = stimuli.TextLine(" < < > < < ", text_font=fontfile, text_size=50)

arrows_cong_left.preload()
arrows_cong_right.preload()
arrows_incong_left.preload()
arrows_incong_right.preload()

# Frames
w, h = arrows_incong_right.surface_size
w, h = w + 20, h + 20  # add margins

shift = h 

box_bottom = stimuli.Rectangle((w, h), colour=BLACK, line_width=3, position=(0, -shift))
box_top = stimuli.Rectangle((w, h), colour=BLACK, line_width=3, position=(0, shift))
cue_bottom = stimuli.Rectangle((w, h), colour=WHITE, line_width=3, position=(0, -shift, 0))
cue_top = stimuli.Rectangle((w, h), colour=WHITE, line_width=3, position=(0, shift, 0))

box_bottom.preload()
box_top.preload()
cue_bottom.preload()
cue_top.preload()


def display(cross_type, top_cued, bottom_cued):

    """Displays a central cross and two frames, above and below it.

       Args:
           cross_type: 'neutral', 'positive' or 'negative'
           top_cued: boolean  (top frame color: False=black, True=white)
           bottom_cued: boolean (bottom frame color)
    """
    cross = fixation_crosses[cross_type]
    cross.present(clear=True, update=False)
    if top_cued:
        cue_top.present(clear=False, update=False)
    else:
        box_top.present(clear=False, update=False)

    if bottom_cued:
        cue_bottom.present(clear=False, update=True)
    else:
        box_bottom.present(clear=False, update=True)

exp.add_data_variable_names(list(trials.columns) +
                            ['response_key', 'reaction_time'])

#####################################################################
control.start(skip_ready_screen=True)

stimuli.TextScreen("Instructions", INSTRUCTIONS_FRENCH,
                   size=(1820, 1080), text_justification=0).present()
exp.keyboard.wait(keys=[misc.constants.K_t, misc.constants.K_SPACE])
blankscreen.present()
exp.clock.wait(1000)
    
for trial in trials.itertuples(index=False):
    display('neutral', False, False)  # default_screen
    exp.clock.wait(1500 + random.uniform(0, 2000))

    display("neutral", trial.cue_up, trial.cue_down)
    exp.clock.wait(CUE_DISPLAY_DURATION)
    display('neutral', False, False)
    exp.clock.wait(CUE_TARGET_INTERVAL)

    # select target
    if trial.arrow_direction == 'left':
        if trial.flanker_congruency == 'cong':
            target = arrows_cong_left
        else:
            target = arrows_incong_left
    else:
        if trial.flanker_congruency == 'cong':
            target = arrows_cong_right
        else:
            target = arrows_incong_right

    # display target
    if trial.target_position == 'down':
        target_pos = (0, -shift)
    if trial.target_position == 'up':
        target_pos = (0, shift)

    target.reposition(target_pos)
    display('neutral', False, False)
    target.present(clear=False, update=True)
    exp.clock.wait(TARGET_DISPLAY_DURATION)
    display('neutral', False, False)

    key, rt = exp.keyboard.wait(duration=MAX_RESPONSE_DURATION)
    if rt is not None:
        rt = rt + TARGET_DISPLAY_DURATION
    exp.data.add(list(trial) + [key, rt])

    # feedback
    if (key == LEFT_RESPONSE_KEY and trial.arrow_direction == 'left') or \
       (key == RIGHT_RESPONSE_KEY and trial.arrow_direction == 'right'):
        display("positive", False, False)
    else:
        display("negative", False, False)

    exp.clock.wait(400)

control.end()
