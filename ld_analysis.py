from __future__ import division
import sys
import os
import numpy as np
from scipy.spatial import distance
from expyriment.misc import data_preprocessing
from ld_utils import extractCorrectAnswers, printErrors, printBasicResults, extractRecognitionAnswers
from ld_utils import correctCards, wrongCards
from config import matrixSize
subjectFolder = sys.argv[1]
subjectFolder = os.getcwd() + os.path.sep  + subjectFolder + os.path.sep + 'Data' + os.path.sep

verbose = True

allFiles = os.listdir(subjectFolder)

declarativeFiles = []

for iFile in allFiles:
    if 'ld_recognition' in iFile:
        recognitionFile = iFile
    elif 'ld_declarativeTask' in iFile:
        declarativeFiles.append(iFile)


class Days(object):

    def __init__(self):
        self.name = ''
        self.header = ''
        self.ifile = ''
        self.data = []
        self.correctCards = correctCards()
        self.wrongCards = wrongCards()
        self.matrix = []

isInterference = False
dayOneTestLearning = Days()
dayTwoTestLearning = Days()
dayThreeTestLearning = Days()
dayTwoTestInterference = Days()
dayThreeTestInterference = Days()
dayThreeRecognition = Days()
dayTwoInterference = Days()
dayOneLearning = Days()

testFiles = []

for iFile in allFiles:
    header = data_preprocessing.read_datafile(subjectFolder + iFile, only_header_and_variable_names=True)
    header = header[3].split('\n#e ')

    for field in header:
        if "DayOne-TestLearning" in field and "Experiment" in field:
            print 'DayOne-TestLearning'
            dayOneTestLearning.name = 'DayOne-TestLearning'
            dayOneTestLearning.header = header
            dayOneTestLearning.ifile = iFile
            dayOneTestLearning.data, dayOneTestLearning.correctCards, dayOneTestLearning.wrongCards, dayOneTestLearning.matrix = extractCorrectAnswers(subjectFolder, iFile)
            for nBlock in range(int(np.max(dayOneTestLearning.data['NBlock']))+1):
                print 'Block: ' + str(nBlock)
                print str(int(dayOneTestLearning.data['Time'][dayOneTestLearning.data['NBlock']==nBlock][-1]-dayOneTestLearning.data['Time'][dayOneTestLearning.data['NBlock']==nBlock][0])/60000) + ' min'
            break
        elif "DayTwo-TestLearning" in field and "Experiment" in field:
            print 'DayTwo-TestLearning'
            dayTwoTestLearning.name = 'DayTwo-TestLearning'
            dayTwoTestLearning.header = header
            dayTwoTestLearning.ifile = iFile
            dayTwoTestLearning.data, dayTwoTestLearning.correctCards, dayTwoTestLearning.wrongCards, dayTwoTestLearning.matrix = extractCorrectAnswers(subjectFolder, iFile)
            for nBlock in range(int(np.max(dayTwoTestLearning.data['NBlock']))+1):
                print 'Block: ' + str(nBlock)
                print str(int(dayTwoTestLearning.data['Time'][dayTwoTestLearning.data['NBlock']==nBlock][-1]-dayTwoTestLearning.data['Time'][dayTwoTestLearning.data['NBlock']==nBlock][0])/60000) + ' min'
            break
        elif "DayThree-TestLearning" in field and "Experiment" in field:
            print 'DayThree-TestLearning'
            dayThreeTestLearning.name = 'DayThree-TestLearning'
            dayThreeTestLearning.header = header
            dayThreeTestLearning.ifile = iFile
            dayThreeTestLearning.data, dayThreeTestLearning.correctCards, dayThreeTestLearning.wrongCards, dayThreeTestLearning.matrix = extractCorrectAnswers(subjectFolder, iFile)
            for nBlock in range(int(np.max(dayThreeTestLearning.data['NBlock']))+1):
                print 'Block: ' + str(nBlock)
                print str(int(dayThreeTestLearning.data['Time'][dayThreeTestLearning.data['NBlock']==nBlock][-1]-dayThreeTestLearning.data['Time'][dayThreeTestLearning.data['NBlock']==nBlock][0])/60000) + ' min'
            break
        elif "DayTwo-TestInterference" in field and "Experiment" in field:
            print 'DayTwo-TestInterference'
            dayTwoTestInterference.name = 'DayTwo-TestInterference'
            dayTwoTestInterference.header = header
            dayTwoTestInterference.ifile = iFile
            isInterference = True
            dayTwoTestInterference.data, dayTwoTestInterference.correctCards, dayTwoTestInterference.wrongCards, dayTwoTestInterference.matrix = extractCorrectAnswers(subjectFolder, iFile)
            for nBlock in range(int(np.max(dayTwoTestInterference.data['NBlock']))+1):
                print 'Block: ' + str(nBlock)
                print str(int(dayTwoTestInterference.data['Time'][dayTwoTestInterference.data['NBlock']==nBlock][-1]-dayTwoTestInterference.data['Time'][dayTwoTestInterference.data['NBlock']==nBlock][0])/60000) + ' min'
            break
        elif "DayThree-TestInterference" in field and "Experiment" in field:
            print 'DayThree-TestInterference'
            dayThreeTestInterference.name = 'DayThree-TestInterference'
            dayThreeTestInterference.header = header
            dayThreeTestInterference.ifile = iFile
            dayThreeTestInterference.data, dayThreeTestInterference.correctCards, dayThreeTestInterference.wrongCards, dayThreeTestInterference.matrix = extractCorrectAnswers(subjectFolder, iFile)
            for nBlock in range(int(np.max(dayThreeTestInterference.data['NBlock']))+1):
                print 'Block: ' + str(nBlock)
                print str(int(dayThreeTestInterference.data['Time'][dayThreeTestInterference.data['NBlock']==nBlock][-1]-dayThreeTestInterference.data['Time'][dayThreeTestInterference.data['NBlock']==nBlock][0])/60000) + ' min'
            break
        elif "recognition" in iFile:
            print 'recognition'
            dayThreeRecognition.name = 'recognition'
            dayThreeRecognition.header = header
            dayThreeRecognition.ifile = iFile
            dayThreeRecognition.data, dayThreeRecognition.correctCards, dayThreeRecognition.wrongCards, dayThreeRecognition.matrix = extractRecognitionAnswers(subjectFolder, iFile)
            break
        elif "DayTwo-Interference" in field:
            print 'DayTwo-Interference'
            dayTwoInterference.name = 'DayTwo-Interference'
            dayTwoInterference.header = header
            dayTwoInterference.ifile = iFile
            dayTwoInterference.data, dayTwoInterference.correctCards, dayTwoInterference.wrongCards, dayTwoInterference.matrix = extractCorrectAnswers(subjectFolder, iFile)
            print dayTwoInterference.matrix[0][0] + ' ' + dayTwoInterference.matrix[1][0] + ' ' + dayTwoInterference.matrix[2][0] + ' ' + dayTwoInterference.matrix[6][0]
            for nBlock in range(int(np.max(dayTwoInterference.data['NBlock']))+1):
                print 'Block: ' + str(nBlock)
                print str(int(dayTwoInterference.data['Time'][dayTwoInterference.data['NBlock']==nBlock][-1]-dayTwoInterference.data['Time'][dayTwoInterference.data['NBlock']==nBlock][0])/60000) + ' min'
            break
        elif "DayOne-Learning" in field:
            print 'DayOne-Learning'
            dayOneLearning.name = 'DayOne-Learning'
            dayOneLearning.header = header
            dayOneLearning.ifile = iFile
            dayOneLearning.data, dayOneLearning.correctCards, dayOneLearning.wrongCards, dayOneLearning.matrix = extractCorrectAnswers(subjectFolder, iFile)
            print dayOneLearning.matrix[0][0] + ' ' + dayOneLearning.matrix[1][0] + ' ' + dayOneLearning.matrix[2][0] + ' ' + dayOneLearning.matrix[6][0]
            for nBlock in range(int(np.max(dayOneLearning.data['NBlock']))+1):
                print 'Block: ' + str(nBlock)
                print str(int(dayOneLearning.data['Time'][dayOneLearning.data['NBlock']==nBlock][-1]-dayOneLearning.data['Time'][dayOneLearning.data['NBlock']==nBlock][0])/60000) + ' min'
            break


unionDayOneMatrixA = set(dayOneTestLearning.correctCards.name).intersection(dayOneLearning.correctCards.name)
newDayOneMatrixA = set(dayOneTestLearning.correctCards.name).difference(dayOneLearning.correctCards.name)
forgotDayOneMatrixA = set(dayOneLearning.correctCards.name).difference(dayOneTestLearning.correctCards.name)

unionConsolidation =  set(dayOneTestLearning.correctCards.name).intersection(dayTwoTestLearning.correctCards.name)
unionReConsolidation = set(dayTwoTestLearning.correctCards.name).intersection(dayThreeTestLearning.correctCards.name)

newConsolidation = set(dayTwoTestLearning.correctCards.name).difference(dayOneTestLearning.correctCards.name)
newReConsolidation = set(dayThreeTestLearning.correctCards.name).difference(dayTwoTestLearning.correctCards.name)

forgotConsolidation = set(dayOneTestLearning.correctCards.name).difference(dayTwoTestLearning.correctCards.name)
forgotReConsolidation = set(dayTwoTestLearning.correctCards.name).difference(dayThreeTestLearning.correctCards.name)

#print dayThreeTestLearning.correctCards.name
#print dayThreeTestLearning.wrongCards.name

#print dayThreeRecognition.correctCards.name
#print dayThreeRecognition.wrongCards.name


recognitionRecalledFromDayTwo = set(dayThreeRecognition.correctCards.name).intersection(dayTwoTestLearning.correctCards.name)
recognitionRecalledFromDayThree = set(dayThreeRecognition.correctCards.name).intersection(dayThreeTestLearning.correctCards.name)

recognitionForgottenFromDayTwo = set(dayTwoTestLearning.correctCards.name).difference(dayThreeRecognition.correctCards.name)
recognitionForgottenFromDayThree = set(dayThreeTestLearning.correctCards.name).difference(dayThreeRecognition.correctCards.name)

recognitionNewFromDayTwo = set(dayThreeRecognition.correctCards.name).difference(dayTwoTestLearning.correctCards.name)
recognitionNewFromDayThree = set(dayThreeRecognition.correctCards.name).difference(dayThreeTestLearning.correctCards.name)

if verbose:

    print '##################################'
    print 'Day One - Matrix A - Last Block of training'
    printBasicResults(dayOneLearning.correctCards)

    print '##################################'
    print 'Day One - Matrix A'
    printBasicResults(dayOneTestLearning.correctCards)

    print '##################################'
    print 'Day Two - Matrix A'
    printBasicResults(dayTwoTestLearning.correctCards)

    print '##################################'
    print 'Day Three - Matrix A'
    printBasicResults(dayThreeTestLearning.correctCards)

    print '##################################'
    print 'Day Three - Recognition'
    printBasicResults(dayThreeRecognition.correctCards)

    print '##################################'
    print 'Summary Day One vs Day One Last Block of Training - Matrix A'
    print str(len(unionDayOneMatrixA)) + ' correctly recalled locations'

    if not newDayOneMatrixA:
        print '0 new location'
    else:
        print str(len(newDayOneMatrixA)) + ' new locations : ' + str(newDayOneMatrixA)

    if not forgotDayOneMatrixA:
        print '0 forgotten location'
    else:
        print str(len(forgotDayOneMatrixA)) + ' forgotten locations : ' + str(forgotDayOneMatrixA)

    print '##################################'
    print 'Summary Day Two vs Day One - Matrix A'
    print str(len(unionConsolidation)) + ' correctly recalled locations'

    if not newConsolidation:
        print '0 new location'
    else:
        print str(len(newConsolidation)) + ' new locations'

    if not forgotConsolidation:
        print '0 forgotten location'
    else:
        print str(len(forgotConsolidation)) + ' forgotten locations : ' + str(forgotConsolidation)


    print '##################################'
    print 'Summary Day Three vs Day Two Matrix A'
    print str(len(unionReConsolidation)) + ' correctly recalled locations'
    if not newReConsolidation:
        print '0 new location'
    else:
        print str(len(newReConsolidation)) + ' new locations : ' + str(newReConsolidation)

    if not forgotReConsolidation:
        print '0 forgotten location'
    else:
        print str(len(forgotReConsolidation)) + ' forgotten locations : ' + str(forgotReConsolidation)

    print '##################################'
    print 'Summary Day Three Recognition vs Day Two Matrix A'
    print str(len(recognitionRecalledFromDayTwo)) + ' correctly recalled locations'
    if not recognitionNewFromDayTwo:
        print '0 new location'
    else:
        print str(len(recognitionNewFromDayTwo)) + ' new locations : ' + str(recognitionNewFromDayTwo)

    if not recognitionForgottenFromDayTwo:
        print '0 forgotten location'
    else:
        print str(len(recognitionForgottenFromDayTwo)) + ' forgotten locations : ' + str(recognitionForgottenFromDayTwo)

    print '##################################'
    print 'Summary Day Three Recognition vs Day Three Matrix A'
    print str(len(recognitionRecalledFromDayThree)) + ' correctly recalled locations'
    if not recognitionNewFromDayThree:
        print '0 new location'
    else:
        print str(len(recognitionNewFromDayThree)) + ' new locations : ' + str(recognitionNewFromDayThree)

    if not recognitionForgottenFromDayThree:
        print '0 forgotten location'
    else:
        print str(len(recognitionForgottenFromDayThree)) + ' forgotten locations : ' + str(recognitionForgottenFromDayThree)

    print '##################################'
    print 'Check errors DayOne - Matrix A Last Block of training'
    printErrors(dayOneLearning)

    print '##################################'
    print 'Check errors DayOne - Matrix A'
    printErrors(dayOneTestLearning)

    print '##################################'
    print 'Check errors DayTwo-Matrix A'
    printErrors(dayTwoTestLearning, dayOneTestLearning)
    
    if isInterference:

        print '##################################'
        print 'Day Two - Matrix B - Last Block of training'
        printBasicResults(dayTwoInterference.correctCards)

        print '##################################'
        print 'Day Two - Matrix B'
        printBasicResults(dayTwoTestInterference.correctCards)

        print '##################################'
        print 'Day Three - Matrix B'
        printBasicResults(dayThreeTestInterference.correctCards)

        unionDayTwoMatrixB = set(dayTwoTestInterference.correctCards.name).intersection(dayTwoInterference.correctCards.name)
        newDayTwoMatrixB = set(dayTwoTestInterference.correctCards.name).difference(dayTwoInterference.correctCards.name)

        unionConsolidationInterference =  set(dayTwoTestInterference.correctCards.name).intersection(dayThreeTestInterference.correctCards.name)
        newConsolidationInterference = set(dayThreeTestInterference.correctCards.name).difference(dayTwoTestInterference.correctCards.name)

        forgotDayTwoMatrixB = set(dayTwoInterference.correctCards.name).difference(dayTwoTestInterference.correctCards.name)
        forgotDayThreeMatrixB = set(dayTwoTestInterference.correctCards.name).difference(dayThreeTestInterference.correctCards.name)

        print '##################################'
        print 'Summary Day Two vs Day Two Last Block of training - Matrix B'
        print str(len(unionDayTwoMatrixB)) + ' correctly recalled locations'
        if not newDayTwoMatrixB:
            print '0 new location'
        else:
            print str(len(newDayTwoMatrixB)) + ' new locations : ' + str(newDayTwoMatrixB)

        if not forgotDayTwoMatrixB:
            print '0 forgotten location'
        else:
            print str(len(forgotDayTwoMatrixB)) + ' forgotten locations : ' + str(forgotDayTwoMatrixB)

        print '##################################'
        print 'Summary Day Three vs Day Two - Matrix B'
        print str(len(unionConsolidationInterference)) + ' correctly recalled locations'
        if not newReConsolidation:
            print '0 new location'
        else:
            print str(len(newConsolidationInterference)) + ' new locations : ' + str(newConsolidationInterference)

        if not forgotDayThreeMatrixB:
            print '0 forgotten location'
        else:
            print str(len(forgotDayThreeMatrixB)) + ' forgotten locations : ' + str(forgotDayThreeMatrixB)

        print '##################################'
        print 'Check errors DayTwo Last Block of training - Matrix B'
        printErrors(dayTwoInterference, dayOneTestLearning)

        print '##################################'
        print 'Check errors DayTwo-Matrix B'
        printErrors(dayTwoTestInterference, dayOneTestLearning)

        print '##################################'
        print 'Check errors DayThree-Matrix A'
        printErrors(dayThreeTestLearning, dayTwoTestInterference)

        print '##################################'
        print 'Check errors DayThree-Matrix B'
        printErrors(dayThreeTestInterference, dayOneTestLearning)

    else:
        print '##################################'
        print 'Check errors DayThree-Matrix A'
        printErrors(dayThreeTestLearning, dayTwoTestLearning)
	