import ast
import ntpath
import os
import pygame
from datetime import datetime

import numpy as np
from dateutil.parser import parse
from expyriment import misc, stimuli
from expyriment.io import Keyboard
from expyriment.misc._timer import get_time
from expyriment.misc.geometry import coordinates2position

from config import linesThickness, cardSize, colorLine, windowSize, bgColor, matrixSize, dataFolder, removeCards


def checkWindowParameters(iWindowSize):
    result = False

    originalResolution = misc.get_monitor_resolution()

    if iWindowSize[0] <= originalResolution[0] and iWindowSize[1] <= originalResolution[1]:
        result = True

    return result


def drawLines(windowSize, gap, bs):

    linesPositions = np.empty([2,2], object)
    linesPositions[0,0] = (-windowSize[0]/float(2), windowSize[1]/float(2) - 2 * gap - cardSize[0] - linesThickness / float(2))
    linesPositions[0,1] = (windowSize[0]/float(2), windowSize[1]/float(2) - 2 * gap - cardSize[0] - linesThickness / float(2))
    linesPositions[1,0] = (-windowSize[0]/float(2), -windowSize[1]/float(2) + 2 * gap + cardSize[1] + linesThickness / float(2))
    linesPositions[1,1] = (windowSize[0]/float(2), -windowSize[1]/float(2) + 2 * gap + cardSize[1] + linesThickness / float(2))

    lines = np.empty([2], object)
    lines[0] = stimuli.Line(linesPositions[0,0], linesPositions[0,1], linesThickness, colour=colorLine, anti_aliasing=None)
    lines[1] = stimuli.Line(linesPositions[1,0], linesPositions[1,1], linesThickness, colour=colorLine, anti_aliasing=None)

    for line in lines:
        line.plot(bs)

    bs.present()


def plotLine(bs, gap, color=bgColor):
    linePositions = np.empty([2], object)
    linePositions[0] = (-cardSize[0]/float(2), windowSize[1]/float(2) - 2*gap - cardSize[0] - linesThickness/float(2))
    linePositions[1] = (cardSize[0]/float(2), windowSize[1]/float(2) - 2*gap - cardSize[0] - linesThickness/float(2))

    line = stimuli.Line(linePositions[0], linePositions[1], linesThickness, colour=color)
    line.plot(bs)

    return bs


def newRandomPresentation(oldPresentation=None):

    newPresentation = np.array(range(matrixSize[0]*matrixSize[1]))
    if removeCards:
        removeCards.sort(reverse=True)
        for nCard in removeCards:
            newPresentation = np.delete(newPresentation, nCard)

    newPresentation = np.random.permutation(newPresentation)

    if oldPresentation is not None:

        while len(longestSubstringFinder(str(oldPresentation), str(newPresentation)).split()) > 2:
            newPresentation = np.array(range(matrixSize[0]*matrixSize[1]))

            if removeCards:
                removeCards.sort(reverse=True)
                for nCard in removeCards:
                    newPresentation = np.delete(newPresentation, nCard)

            newPresentation = np.random.permutation(newPresentation)

    return newPresentation


def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): answer = match
                match = ""
    return answer


def getPreviousMatrix(subjectName, daysBefore, experienceName):

    currentDate = datetime.now()

    dataFiles = [each for each in os.listdir(dataFolder) if each.endswith('.xpd')]

    for dataFile in dataFiles:
        agg = misc.data_preprocessing.read_datafile(dataFolder + dataFile, only_header_and_variable_names=True)

        previousDate = parse(agg[2]['date'])

        try:
            agg[3].index(experienceName)
        except (ValueError):
            continue

        if daysBefore == 0 or ((currentDate-previousDate).total_seconds() > 72000*daysBefore and (currentDate-previousDate).total_seconds() < 100800*daysBefore):
            header = agg[3].split('\n#e ')

            indexSubjectName = header.index('Subject:') + 1
            if subjectName in header[indexSubjectName]:
                print 'File found: ' + dataFile
                indexPositions = header.index('Positions pictures:') + 1
                previousMatrix = ast.literal_eval(header[indexPositions].split('\n')[0].split('\n')[0])
                return previousMatrix

    return False


def subfinder(mylist, pattern):
    answers = []
    for i in range(len(mylist) - len(pattern)+1):
        if np.all(mylist[i:i+len(pattern)] == pattern):
            answers.append(True)
        else:
            answers.append(False)

    try:
        answers.index(True)
    except ValueError:
        return False

    return True


def setCursor(arrow):
    hotspot = (0, 0)
    s2 = []
    for line in arrow:
        s2.append(line.replace('x', 'X').replace(',', '.').replace('O', 'o'))
    cursor, mask = pygame.cursors.compile(s2, 'X', '.', 'o')
    size = len(arrow[0]), len(arrow)
    pygame.mouse.set_cursor(size, hotspot, cursor, mask)


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def readMouse(startTime, button, duration=None):
    iKeyboard = Keyboard()
    if duration is not None:
        while int((get_time() - startTime) * 1000) <= duration:
            alle = pygame.event.get()
            rt = int((get_time() - startTime)*1000)
            for e in alle:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == button:
                    return rt, coordinates2position(e.pos)

            if iKeyboard.process_control_keys():
                break

        return None, None

    else:
        while True:
            alle = pygame.event.get()
            rt = int((get_time() - startTime)*1000)
            for e in alle:
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == button:
                    return rt, coordinates2position(e.pos)

            if iKeyboard.process_control_keys():
                break
    #
    # if nBlock < 0:  # if nBlock == 0:
    #
    #     ''' Presentation all locations + memorization'''
    #
    #     list = np.random.permutation(m.size[0] * m.size[1])
    #     list = list.tolist()
    #     list.remove((m.size[0]*m.size[1])/2)
    #
    #     for nCard in list:
    #         isLearned = False
    #
    #         while not isLearned:
    #             mouse.hide_cursor(True, True)
    #             bs = m.plotCard(nCard,True,bs)  # Show Location for ( 2s )
    #             bs.present(False, True)
    #             exp.clock.wait(presentationCard)
    #
    #             bs = m.plotCard(nCard, False, bs)  # Hide Location
    #             m._cueCard.setPicture(m._matrix.item(nCard).stimuli[0].filename)
    #             bs = m.plotCueCard(True, bs)  # Show Cue
    #             bs.present(False, True)  # Update Screen
    #
    #             exp.clock.wait(presentationCard)  # Wait
    #
    #             bs = m.plotCueCard(False, bs)  # Hide Cue
    #             bs.present(False, True)  # Update Screen
    #             mouse.show_cursor(True, True)  # Show cursor
    #
    #             position = None
    #             [event_id, position, rt] = mouse.wait_press(buttons=None, duration=responseTime, wait_for_buttonup=True)
    #
    #             if position is not None:
    #                 if m.checkPosition(position) == nCard:
    #                     mouse.hide_cursor(True, True)
    #                     isLearned = True
    #
    #             ISI = design.randomize.rand_int(min_max_ISI[0], min_max_ISI[1])
    #             exp.clock.wait(ISI)