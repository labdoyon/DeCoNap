import sys
import os
import csv
import numpy as np
import re
import unicodedata
from scipy.spatial import distance

from expyriment.misc import data_preprocessing

# from config import matrix_size
from ld_utils_fromScratch import extract_correct_answers
from ld_utils_fromScratch import Days

# ***INSTRUCTIONS***
# Please input the location of the subject folder containing the data you wish to convert to .csv format
# e.g. You are in DeCoNap/ and you wish to convert data located in DeCoNap/data/subject_41/
# Please input: python ld_analysis.py data/subject_41

# Output csv file will be created in the folder containing the folder you specified (in this example, DeCoNap/data/)
# and will have the same name as the directory you specified
# In this example, Output will be:  <subject_41.csv> <DeCoNap/data/subject_41.csv>

sep = os.path.sep

# Declaring <subjectFolder> and <outputFile> variables, which are self-explanatory
# subjectLocation = sys.argv[1]
subjectLocation = '../data/Latifa_early_data_reorganized/HBHL_Dec48_NO_004/'
if subjectLocation[-1] == sep:  # removing path separator if not present. e.g. <data/> to <data>
    subjectLocation = subjectLocation[:-1]
subjectFolder = os.getcwd() + sep + subjectLocation + sep
outputFileLearning = os.getcwd() + sep + subjectLocation + '_learning.csv'
outputFileTests = os.getcwd() + sep + subjectLocation + '_tests&recognition.csv'

# Gathering all subject files
allFiles = os.listdir(subjectFolder)
declarativeFiles = []
for iFile in allFiles:
    # There is only one recognition test (and therefore only one file) in our research paradigm
    if 'ld_recognition' in iFile:
        recognitionFile = iFile
    elif 'ld_declarativeTask' in iFile:
        declarativeFiles.append(iFile)

isInterference = False
dayOneTestLearning = Days()
dayTwoTestLearning = Days()
dayThreeTestLearning = Days()
dayThreeRecognition = Days()

for iFile in allFiles:
    header = data_preprocessing.read_datafile(subjectFolder + iFile, only_header_and_variable_names=True)
    header[3].split('\n#e ')
    for field in header:
        if "DayOne-Learning" in field and "Experiment" in field:
            dayOneTestLearning.name = 'DayOne-TestLearning'
            dayOneTestLearning.header = header
            dayOneTestLearning.ifile = iFile
            dayOneTestLearning.matrix, dayOneTestLearning.data, \
            dayOneTestLearning.correctCards, dayOneTestLearning.wrongCards, number_blocks \
                = extract_correct_answers(subjectFolder, iFile)
            break
    for field in header:
        if "DayOne-TestLearning" in field and "Experiment" in field:
            dayTwoTestLearning.name = 'DayOne-TestLearning'
            dayTwoTestLearning.header = header
            dayTwoTestLearning.ifile = iFile
            dayTwoTestLearning.matrix, dayOneTestLearning.data, \
            dayTwoTestLearning.correctCards, dayOneTestLearning.wrongCards, number_blocks \
                = extract_correct_answers(subjectFolder, iFile)
            break

if len(dayOneTestLearning.matrix) > 36:
    matrix_size = (7, 7)
elif len(dayOneTestLearning.matrix) < 35:
    matrix_size = (5, 5)
else:
    matrix_size = (6, 6)

# as a rule of thumb, for 'DayRec_MatrixA_answer' and 'DayRec_matrixRec_answer', remember that
# 0 means "the subject made a mistake"
# 1 means "the subject got it right"
# 1 in 'DayRec_matrixRec_answer' means the subject clicked "Wrong" when presented with the wrong position. And 0, that
# they were mistaken
iCSV = csv.writer(open(outputFileLearning, "wb"))
firstRow = ['Item', 'Class']
for i in range(number_blocks):
    firstRow.extend(['Day1_Block' + str(i) + '_matrixA_order', 'Day1_Block' + str(i) + '_matrixA_distanceToMatrixA'])
iCSV.writerow(firstRow)

# card_events in DayOneTest
events = dayOneTestLearning.header[-1].split('\n')
events = [element.encode('ascii') for element in events]
cards_position = []
cards_distanceToCorrectCard = []
cards_order = []

for event in events:
    if 'Block' in event and 'Test' in event:
        cards_position.append({})
        cards_distanceToCorrectCard.append({})
        cards_order.append({})
        block_number = len(cards_position) - 1
        register_on = True
        order = 0
    elif 'Block' in event and 'Presentation' in event:
        register_on = False
    elif 'ShowCueCard' in event and register_on:
        card = re.search('(?<=card_)\w+', event).group(0)
        position = cards_position[block_number][card] = re.search('pos_([0-9]+)_', event).group(1)
        cards_order[block_number][card] = order
        order += 1
        cards_distanceToCorrectCard[block_number][card] = 'NaN'
    elif 'Response' in event and 'NoResponse' not in event and 'pos_None_ERROR' not in event and register_on:
        response = re.search('(?<=card_)\w+', event).group(0)
        if response == card:
            cards_distanceToCorrectCard[block_number][card] = 0
        else:
            response_position = re.search('pos_([0-9]+)_', event).group(1)
            cards_distanceToCorrectCard[block_number][card] = distance.euclidean(
                np.unravel_index(int(position), matrix_size),
                np.unravel_index(int(response_position), matrix_size))

assert number_blocks == block_number+1, "Two methods for block counting don't output the same result," \
                                      " please check the log files"

for card in np.sort(dayOneTestLearning.matrix):
    # Add item; Add category
    card = card.rstrip('.png')
    itemList = [card, card[0]]
    for block_number in range(number_blocks):
        try:
            itemList.extend([cards_order[block_number][card], cards_distanceToCorrectCard[block_number][card]])
        except KeyError:
            itemList.extend(['NaN', 'NaN'])
    iCSV.writerow(itemList)

# DAY 2 ################################################################################################################



iCSV = csv.writer(open(outputFileTests, "wb"))
iCSV.writerow(['Item', 'Class',
               'Day1_matrixA_order', 'Day1_matrixA_distanceToMatrixA',
               'Day2_matrixA_order', 'Day2_matrixA_distanceToMatrixA',
               'Day3_matrixA_order', 'Day3_matrixA_distanceToMatrixA',
               'DayRec_matrixA_order', 'DayRec_MatrixA_answer',
               'DayRec_matrixRec_order', 'DayRec_matrixRec_answer',
               'D3RecMR_distanceToMatrixA'])
# MORE DETAILED COMMENTS ARE TO BE WRITTEN AT A LATER TIME ON THIS PART
