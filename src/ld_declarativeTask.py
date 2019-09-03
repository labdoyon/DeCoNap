import sys

import numpy as np
from expyriment import control, stimuli, io, design, misc
from expyriment.misc import constants
from expyriment.misc._timer import get_time

from ld_matrix import LdMatrix
from ld_utils import setCursor, newRandomPresentation, getPreviousMatrix, getPreviousSoundsAllocation, path_leaf, readMouse, newSoundAllocation
from config import *

if not windowMode:  # Check WindowMode and Resolution
    control.defaults.window_mode = windowMode
    control.defaults.window_size = misc.get_monitor_resolution()
    windowSize = control.defaults.window_size
else:
    control.defaultsk.window_mode = windowMode
    control.defaults.window_size = windowSize

if debug:
    control.set_develop_mode(True)

arguments = str(''.join(sys.argv[1:])).split(',')  # Get arguments - experiment name and subject

experimentName = arguments[0]
subjectName = arguments[1]

exp = design.Experiment(experimentName)  # Save experiment name
exp.add_experiment_info(['Subject: '])  # Save Subject Code
exp.add_experiment_info([subjectName])  # Save Subject Code

# Save time, nblocks, position, correctAnswer, RT
exp.add_data_variable_names(['Time', 'NBlock', 'Picture', 'Answers', 'RT'])

m = LdMatrix(matrixSize, windowSize)  # Create Matrix

if experimentName == 'DayOne-Learning':
    oldListPictures = None
    keepMatrix = True
    keepSoundsAllocation = True
elif experimentName == 'DayOne-TestLearning':
    oldListPictures = getPreviousMatrix(subjectName, 0, 'DayOne-Learning')
    keepMatrix = True
    keepSoundsAllocation = True
    nbBlocksMax = 1
elif experimentName == 'DayOne-TestConsolidation':
    oldListPictures = getPreviousMatrix(subjectName, 0, 'DayOne-Learning')
    keepMatrix = True
    keepSoundsAllocation = True
    nbBlocksMax = 1

if oldListPictures is False:
    print FAIL + "Warning: no old list of pictures found" + ENDC
    sys.exit()

newMatrix = m.findMatrix(oldListPictures, keepMatrix)  # Find newMatrix

exp.add_experiment_info(['Positions pictures:'])

control.initialize(exp)

m.associatePictures(newMatrix)  # Associate Pictures to cards

exp.add_experiment_info([m.listPictures])  # Add listPictures

previousSoundAllocation = getPreviousSoundsAllocation(subjectName, 0, 'DayOne-Learning')

exp.add_experiment_info(['Image classes order:'])
exp.add_experiment_info([classPictures])
exp.add_experiment_info(['Sounds order:'])
exp.add_experiment_info([sounds])

exp.add_experiment_info(['Image classes to sounds:'])
if not previousSoundAllocation or not keepSoundsAllocation:
    soundsAllocation = newSoundAllocation(3)
else:
    soundsAllocation = previousSoundAllocation
exp.add_experiment_info([soundsAllocation])


m.associateSounds(newMatrix, soundsAllocation)  # Associate Sounds to Cards depending on pictures

control.start(exp, auto_create_subject_id=True, skip_ready_screen=True)

# LOG and SYNC
exp.add_experiment_info(['StartExp: {}'.format(exp.clock.time)])  # Add sync info
# lji.run_stimulation({'channel': 7})

mouse = io.Mouse()  # Create Mouse instance
mouse.set_logging(True)  # Log mouse
mouse.hide_cursor(True, True)  # Hide cursor

setCursor(arrow)

bs = stimuli.BlankScreen(bgColor)  # Create blank screen
m.plotDefault(bs, True)  # Draw default grid

exp.clock.wait(shortRest)

correctAnswers = np.zeros(nbBlocksMax)
currentCorrectAnswers = 0
nBlock = 0

instructionRectangle = stimuli.Rectangle(size=(windowSize[0], m.gap * 2 + cardSize[1]), position=(
    0, -windowSize[1]/float(2) + (2 * m.gap + cardSize[1])/float(2)), colour=constants.C_DARKGREY)

''' Presentation all locations '''
presentationOrder = newRandomPresentation()

while currentCorrectAnswers < correctAnswersMax and nBlock < nbBlocksMax:
    presentationOrder = newRandomPresentation(presentationOrder)
    if 1 != nbBlocksMax:
        exp.add_experiment_info(['Block {} - Presentation'.format(nBlock)])  # Add listPictures
        exp.add_experiment_info(presentationOrder)  # Add listPictures
        instructions = stimuli.TextLine(' PRESENTATION ',
                                        position=(0, -windowSize[1]/float(2) + (2*m.gap + cardSize[1])/float(2)),
                                        text_font=None, text_size=textSize, text_bold=None, text_italic=None,
                                        text_underline=None, text_colour=textColor,
                                        background_colour=bgColor,
                                        max_width=None)
        instructionRectangle.plot(bs)
        instructions.plot(bs)
        bs.present(False, True)

        exp.clock.wait(shortRest) ###################################################################################### 2.5s
        instructionRectangle.plot(bs)
        bs.present(False, True)

        ISI = design.randomize.rand_int(min_max_ISI[0], min_max_ISI[1])
        exp.clock.wait(ISI) ############################################################################################ random between 500 and 1500 ms

        # LOG and SYNC: Start Presentation
        exp.add_experiment_info(['StartPresentation_{}_{}'.format(nBlock, exp.clock.time)])  # Add sync info
        # lji.run_stimulation({'channel': 7})

        for nCard in presentationOrder:
            mouse.hide_cursor(True, True)
            m.plotCard(nCard, True, bs, True)  # Show Location for ( 2s )
            m.playSound(nCard)
            # LOG and SYNC: Start Presentation
            exp.add_experiment_info(['ShowCard_pos_{}_card_{}_timing_{}_sound_{}'.format(nCard, m.listPictures[nCard], exp.clock.time, sounds[m._matrix.item(nCard).sound])])  # Add sync info
            # lji.run_stimulation({'channel': 7})

            exp.clock.wait(presentationCard) ########################################################################### 2s
            m.plotCard(nCard, False, bs, True)
            exp.add_experiment_info(['HideCard_pos_{}_card_{}_timing_{}'.format(nCard, m.listPictures[nCard], exp.clock.time)])  # Add sync info
            # lji.run_stimulation({'channel': 7})

            ISI = design.randomize.rand_int(min_max_ISI[0], min_max_ISI[1])
            exp.clock.wait(ISI) ######################################################################################## random between 500 and 1500 ms

    instructions = stimuli.TextLine(' TEST ',
                                    position=(0, -windowSize[1]/float(2) + (2*m.gap + cardSize[1])/float(2)),
                                    text_font=None, text_size=textSize, text_bold=None, text_italic=None,
                                    text_underline=None, text_colour=textColor,
                                    background_colour=bgColor,
                                    max_width=None)
    instructionRectangle.plot(bs)
    instructions.plot(bs)
    bs.present(False, True)

    # LOG and SYNC Start Test
    exp.add_experiment_info(['StartTest_{}_{}'.format(nBlock, exp.clock.time)])  # Add sync info
    # lji.run_stimulation({'channel': 7})

    exp.clock.wait(shortRest)  # Short Rest between presentation and cue-recall

    instructionRectangle.plot(bs)
    bs.present(False, True)

    ISI = design.randomize.rand_int(min_max_ISI[0], min_max_ISI[1])
    exp.clock.wait(ISI)

    ''' Cue Recall '''
    presentationOrder = newRandomPresentation(presentationOrder)
    exp.add_experiment_info(['Block {} - Test'.format(nBlock)])  # Add listPictures
    exp.add_experiment_info(presentationOrder)
    for nCard in presentationOrder:

        m._cueCard.setPicture(m._matrix.item(nCard).stimuli[0].filename)  # Associate Picture to CueCard

        m.plotCueCard(True, bs, True)  # Show Cue
        # LOG and SYNC show cue card
        m.playSoundCueCard(m.listPictures[nCard], soundsAllocation)
        cueCardSound = m.getSoundCueCard(m.listPictures[nCard], soundsAllocation)
        exp.add_experiment_info(['ShowCueCard_pos_{}_card_{}_timing_{}_sound_{}'.format(nCard, m.listPictures[nCard], exp.clock.time, cueCardSound)])  # Add sync info
        # lji.run_stimulation({'channel': 7})

        exp.clock.wait(presentationCard)  # Wait presentationCard

        m.plotCueCard(False, bs, True)  # Hide Cue
        # LOG and SYNC hide cue card
        exp.add_experiment_info(['HideCueCard_pos_{}_card_{}_timing_{}'.format(nCard, m.listPictures[nCard], exp.clock.time)])  # Add sync info
        # lji.run_stimulation({'channel': 7})

        mouse.show_cursor(True, True)

        start = get_time()
        rt, position = readMouse(start, mouseButton, responseTime)

        mouse.hide_cursor(True, True)
        if rt is not None:

            currentCard = m.checkPosition(position)

            # LOG and SYNC Response
            try:
                exp.add_experiment_info(['Response_pos_{}_card_{}_timing_{}'.format(currentCard, m.listPictures[currentCard], exp.clock.time)])  # Add sync info
                # lji.run_stimulation({'channel': 7})
            except:
                exp.add_experiment_info(['Response_pos_{}_ERROR_timing_{}'.format(currentCard, exp.clock.time)])  # Add sync info
                # lji.run_stimulation({'channel': 7})                			

            if currentCard is not None and currentCard not in removeCards:
                m._matrix.item(currentCard).color = clickColor
                m.plotCard(currentCard, False, bs, True)

                exp.clock.wait(clicPeriod)  # Wait 200ms

                m._matrix.item(currentCard).color = cardColor
                m.plotCard(currentCard, False, bs, True)

            if currentCard == nCard:
                correctAnswers[nBlock] += 1
                exp.data.add([exp.clock.time, nBlock,
                              path_leaf(m._matrix.item(nCard).stimuli[0].filename),
                              path_leaf(m._matrix.item(currentCard).stimuli[0].filename),
                              rt])

            elif currentCard is None:
                exp.data.add([exp.clock.time, nBlock,
                              path_leaf(m._matrix.item(nCard).stimuli[0].filename),
                              None,
                              rt])

            else:
                exp.data.add([exp.clock.time, nBlock,
                              path_leaf(m._matrix.item(nCard).stimuli[0].filename),
                              path_leaf(m._matrix.item(currentCard).stimuli[0].filename),
                              rt])
        else:
            exp.data.add([exp.clock.time, nBlock,
                          path_leaf(m._matrix.item(nCard).stimuli[0].filename),
                          None,
                          rt])

            # LOG and SYNC Response
            exp.add_experiment_info(['NoResponse'])  # Add sync info
            # lji.run_stimulation({'channel': 7})

        ISI = design.randomize.rand_int(min_max_ISI[0], min_max_ISI[1])
        exp.clock.wait(ISI)

    currentCorrectAnswers = correctAnswers[nBlock]  # Number of correct answers

    #if currentCorrectAnswers < correctAnswersMax and nBlock + 1 < nbBlocksMax:
    if nbBlocksMax != 1:

        instructions = stimuli.TextLine('You got ' + str(int(correctAnswers[nBlock])) + ' out of ' + str(m._matrix.size-len(removeCards)),
                                        position=(0, -windowSize[1]/float(2) + (2*m.gap + cardSize[1])/float(2)),
                                        text_font=None, text_size=textSize, text_bold=None, text_italic=None,
                                        text_underline=None, text_colour=textColor, background_colour=bgColor,
                                        max_width=None)
        instructions.plot(bs)
        bs.present(False, True)

        exp.clock.wait(shortRest)

        instructionRectangle.plot(bs)
        bs.present(False, True)

    instructions = stimuli.TextLine(
        ' REST ',
        position=(0, -windowSize[1]/float(2) + (2*m.gap + cardSize[1])/float(2)),
        text_font=None, text_size=textSize, text_bold=None, text_italic=None,
        text_underline=None, text_colour=textColor, background_colour=bgColor,
        max_width=None)

    instructions.plot(bs)
    bs.present(False, True)
    # LOG and SYNC Response
    exp.add_experiment_info(['StartShortRest_block_{}_timing_{}'.format(nBlock, exp.clock.time)])  # Add sync info
    # lji.run_stimulation({'channel': 7})

    exp.clock.wait(shortRest)

    # LOG and SYNC Response
    exp.add_experiment_info(['EndShortRest_block_{}_timing_{}'.format(nBlock, exp.clock.time)])  # Add sync info
    # lji.run_stimulation({'channel': 7})

    instructionRectangle.plot(bs)
    bs.present(False, True)

    # LOG and SYNC Response
    exp.add_experiment_info(['StartRest_block_{}_timing_{}'.format(nBlock, exp.clock.time)])  # Add sync info
    # lji.run_stimulation({'channel': 7})

    exp.clock.wait(restPeriod)

    # LOG and SYNC Response
    exp.add_experiment_info(['EndRest_block_{}_timing_{}'.format(nBlock, exp.clock.time)])  # Add sync info
    # lji.run_stimulation({'channel': 7})

    nBlock += 1

exp.clock.wait(5000)
control.end()
