import sys

import numpy as np
from expyriment import control, stimuli, io, design, misc
from expyriment.misc._timer import get_time

from ld_matrix import LdMatrix
from ld_utils import setCursor, getPreviousMatrix, newRandomPresentation, readMouse
from config import *

if not noLabjack:
    import labjack_interface as lji

if not windowMode:  # Check WindowMode and Resolution
    control.defaults.window_mode = windowMode
    control.defaults.window_size = misc.get_monitor_resolution()
    windowSize = control.defaults.window_size
else:
    control.defaults.window_mode = windowMode
    control.defaults.window_size = windowSize

m = LdMatrix(matrixSize, windowSize)  # Create Matrix

arguments = str(''.join(sys.argv[1:])).split(',')  # Get arguments - experiment name and subject

experimentName = arguments[0]
subjectName = arguments[1]

exp = design.Experiment(experimentName)  # Save experiment name
exp.add_experiment_info(['Subject: '])  # Save Subject Code
exp.add_experiment_info([subjectName])  # Save Subject Code

# Save time, Response, correctAnswer, RT
exp.add_data_variable_names(['Time', 'Matrix', 'CorrectAnswer', 'RT'])

exp.add_experiment_info(['Learning: '])  # Save Subject Code
learningMatrix = getPreviousMatrix(subjectName, 0, 'DayOne-Learning')
exp.add_experiment_info([learningMatrix])  # Add listPictures

interferenceMatrix = getPreviousMatrix(subjectName, 0, 'DayTwo-Interference')

exp.add_experiment_info(['RandomMatrix: '])  # Save Subject Code
randomMatrix = m.findMatrix(learningMatrix)
if np.any(randomMatrix == interferenceMatrix):
    randomMatrix = m.findMatrix(learningMatrix)
exp.add_experiment_info([randomMatrix])  # Add listPictures

exp.add_experiment_info(['Presentation Order: '])  # Save Presentation Order

presentationMatrixLearningOrder = newRandomPresentation()
presentationMatrixLearningOrder = np.vstack((presentationMatrixLearningOrder,np.zeros(m.size[0]*m.size[1]-len(removeCards))))

presentationMatrixRandomOrder = newRandomPresentation(presentationMatrixLearningOrder)
presentationMatrixRandomOrder = np.vstack((presentationMatrixRandomOrder,np.ones(m.size[0]*m.size[1]-len(removeCards))))

presentationOrder = np.hstack((presentationMatrixLearningOrder, presentationMatrixRandomOrder))

presentationOrder = presentationOrder[:, np.random.permutation(presentationOrder.shape[1])]

listCards = []
for nCard in range(presentationOrder.shape[1]):
    if removeCards:
        removeCards.sort()
        removeCards = np.asarray(removeCards)
        tempPosition = presentationOrder[0][nCard]
        index = 0
        try:
            index = int(np.where(removeCards == max(removeCards[removeCards<tempPosition]))[0]) + 1
        except:
            pass

        position = tempPosition - index

    else:
        position = presentationOrder[0][nCard]

    if presentationOrder[1][nCard] == 0: # Learning Matrix
        listCards.append(learningMatrix[int(position)])
    else:
        listCards.append(randomMatrix[int(position)])

exp.add_experiment_info(presentationOrder)  # Add listPictures

control.initialize(exp)
control.start(exp, auto_create_subject_id=True, skip_ready_screen=True)

# LOG and SYNC
exp.add_experiment_info(['StartExp: {}'.format(exp.clock.time)])  # Add sync info
if not noLabjack:
    lji.run_stimulation({'channel': 7})

mouse = io.Mouse()  # Create Mouse instance
mouse.set_logging(True)  # Log mouse
mouse.hide_cursor(True, True)  # Hide cursor

setCursor(arrow)

matrixA = stimuli.TextLine('  Matrix A  ',
                           position=(-windowSize[0]/float(4),
                                     -windowSize[1]/float(2) + (2*m.gap + cardSize[1])/float(2)),
                           text_size=textSize,
                           text_colour=textColor,
                           background_colour=cardColor)

matrixARectangle = stimuli.Rectangle(size=matrixA.surface_size, position=matrixA.position,
                                     colour=cardColor)

matrixNone = stimuli.TextLine('  None  ',
                            position=(windowSize[0]/float(4),
                                      -windowSize[1]/float(2) + (2*m.gap + cardSize[1])/float(2)),
                            text_size=textSize,
                            text_colour=textColor,
                            background_colour=cardColor)

matrixNoneRectangle = stimuli.Rectangle(size=matrixNone.surface_size, position=matrixNone.position,
                                     colour=cardColor)


bs = stimuli.BlankScreen(bgColor)  # Create blank screen
bs = m.plotDefault(bs)  # Draw default grid
matrixARectangle.plot(bs)
matrixA.plot(bs)
matrixNone.plot(bs)
m._cueCard.color = bgColor
bs = m.plotCueCard(False, bs)

bs.present(False, True)

ISI = design.randomize.rand_int(min_max_ISI[0], min_max_ISI[1])
exp.clock.wait(ISI)

for nCard in range(presentationOrder.shape[1]):
    locationCard = int(presentationOrder[0][nCard])

    if bool(presentationOrder[1][nCard] == 0):
        showMatrix = 'MatrixA'
    else:
        showMatrix = 'MatrixRandom'

    m._matrix.item(locationCard).setPicture(picturesFolder + listCards[nCard])
    m.plotCard(locationCard, True, bs, True)

    # LOG and SYNC: Show Card
    exp.add_experiment_info(['ShowCard_pos_{}_card_{}_timing_{}'.format(locationCard, listCards[nCard], exp.clock.time)])  # Add sync info
    if not noLabjack:
        lji.run_stimulation({'channel': 7})
	
    exp.clock.wait(presentationCard)
    m.plotCard(locationCard, False, bs, True)
    # LOG and SYNC: Hide Card
    exp.add_experiment_info(['HideCard_pos_{}_card_{}_timing_{}'.format(locationCard, listCards[nCard], exp.clock.time)])  # Add sync info
    if not noLabjack:
        lji.run_stimulation({'channel': 7})
	
    mouse.show_cursor(True, True)

    start = get_time()
    rt, position = readMouse(start, mouseButton, responseTime)
	
    mouse.hide_cursor(True, True)

    if rt is not None:
        if matrixARectangle.overlapping_with_position(position):
            exp.data.add([exp.clock.time, showMatrix, bool(presentationOrder[1][nCard] == 0), rt])
            matrixA = stimuli.TextLine('  Matrix A  ',
                                          position=(-windowSize[0]/float(4),
                                                    -windowSize[1]/float(2) + (2*m.gap + cardSize[1])/float(2)),
                                          text_font=None, text_size=textSize, text_bold=None, text_italic=None,
                                          text_underline=None, text_colour=textColor,
                                          background_colour=clickColor,
                                          max_width=None)
            matrixA.plot(bs)
            bs.present(False, True)
            exp.clock.wait(clicPeriod)
            matrixA = stimuli.TextLine('  Matrix A  ',
                                      position=(-windowSize[0]/float(4),
                                                -windowSize[1]/float(2) + (2*m.gap + cardSize[1])/float(2)),
                                      text_font=None, text_size=textSize, text_bold=None, text_italic=None,
                                      text_underline=None, text_colour=textColor,
                                      background_colour=cardColor,
                                      max_width=None)
            matrixA.plot(bs)
            bs.present(False, True)
			
            # LOG and SYNC: response matrixA
            exp.add_experiment_info(['Response_{}_timing_{}'.format('MatrixA', exp.clock.time)])  # Add sync info
            if not noLabjack:
                lji.run_stimulation({'channel': 7})
			
            #print presentationOrder[1][nCard] == 0

        elif matrixNoneRectangle.overlapping_with_position(position):
            exp.data.add([exp.clock.time, showMatrix, bool(presentationOrder[1][nCard]==1), rt])
            matrixNone = stimuli.TextLine('  None  ',
                                          position=(windowSize[0]/float(4),
                                                    -windowSize[1]/float(2) + (2*m.gap + cardSize[1])/float(2)),
                                          text_font=None, text_size=textSize, text_bold=None, text_italic=None,
                                          text_underline=None, text_colour=textColor,
                                          background_colour=clickColor,
                                          max_width=None)
            matrixNone.plot(bs)
            bs.present(False, True)
            exp.clock.wait(clicPeriod)
            matrixNone = stimuli.TextLine('  None  ',
                                          position=(windowSize[0]/float(4),
                                                    -windowSize[1]/float(2) + (2*m.gap + cardSize[1])/float(2)),
                                          text_font=None, text_size=textSize, text_bold=None, text_italic=None,
                                          text_underline=None, text_colour=textColor,
                                          background_colour=cardColor,
                                          max_width=None)
            matrixNone.plot(bs)
            bs.present(False, True)
			
            # LOG and SYNC: response matrixA
            exp.add_experiment_info(['Response_{}_timing_{}'.format('None', exp.clock.time)])  # Add sync info
            if not noLabjack:
                lji.run_stimulation({'channel': 7})
        else:
            exp.data.add([exp.clock.time, showMatrix, False, rt])
			
    else:
        exp.data.add([exp.clock.time, showMatrix, False, rt])
        # LOG and SYNC: response matrixA
        exp.add_experiment_info(['Response_{}_timing_{}'.format('NoRT', exp.clock.time)])  # Add sync info
        if not noLabjack:
            lji.run_stimulation({'channel': 7})

    ISI = design.randomize.rand_int(min_max_ISI[0], min_max_ISI[1])
    exp.clock.wait(ISI)

exp.clock.wait(5000)