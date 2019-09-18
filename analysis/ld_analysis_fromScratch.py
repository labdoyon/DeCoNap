import os
import csv
import sys

from expyriment.misc import data_preprocessing

# from config import matrix_size
from ld_utils_fromScratch import day, extract_matrix_and_data, extract_events, write_csv

# ***INSTRUCTIONS***
# Please input the location of the subject folder containing the data you wish to convert to .csv format
# e.g. You are in DeCoNap/ and you wish to convert data located in DeCoNap/data/subject_41/
# Please input: python ld_analysis.py data/subject_41

# Output csv file will be created in the folder containing the folder you specified (in this example, DeCoNap/data/)
# and will have the same name as the directory you specified
# In this example, Output will be:  <subject_41.csv> <DeCoNap/data/subject_41.csv>

sep = os.path.sep
#
# Declaring <subject_folder> and <outputFile> variables, which are self-explanatory
# subject_location = sys.argv[1]
subject_location = '../../DeCoNap-HBHL_DT48_v0.3/data/Latifa_early_data_reorganized/HBHL_Dec48_NO_004/'
if subject_location[-1] == sep:  # removing path separator if not present. e.g. <data/> to <data>
    subject_location = subject_location[:-1]
subject_folder = os.getcwd() + sep + subject_location + sep
output_file_learning = os.getcwd() + sep + subject_location + '_learning.csv'
outputFileTests = os.getcwd() + sep + subject_location + '_tests&recognition.csv'

# Gathering all subject files
allFiles = os.listdir(subject_folder)
declarativeFiles = []
for iFile in allFiles:
    # There is only one recognition test (and therefore only one file) in our research paradigm
    if 'ld_recognition' in iFile:
        recognitionFile = iFile
    elif 'ld_declarativeTask' in iFile:
        declarativeFiles.append(iFile)

day1_learning = day()
day2_test = day()
day3_test = day()
day3_recognition = day()

for iFile in allFiles:
    header = data_preprocessing.read_datafile(subject_folder + iFile, only_header_and_variable_names=True)
    header[3].split('\n#e ')
    for field in header:
        if "DayOne-Learning" in field and "Experiment" in field:
            events, matrix_pictures, matrix_size = extract_matrix_and_data(subject_folder, iFile)
            cards_order, cards_distance_to_correct_card, number_blocks = extract_events(events, matrix_size)
            write_csv(output_file_learning, matrix_pictures, cards_order, cards_distance_to_correct_card, number_blocks)
            break
    for field in header:
        if "DayOne-TestLearning" in field and "Experiment" in field:
            # dayTwoTestLearning.header = header
            # dayTwoTestLearning.matrix = extract_matrix(subject_folder, iFile)
            break
    for field in header:
        if "DayOne-TestLearning" in field and "Experiment" in field:
            # dayThreeTestLearning.header = header
            # dayThreeTestLearning.matrix = extract_matrix(subject_folder, iFile)
            break

# as a rule of thumb, for 'DayRec_MatrixA_answer' and 'DayRec_matrixRec_answer', remember that
# 0 means "the subject made a mistake"
# 1 means "the subject got it right"
# 1 in 'DayRec_matrixRec_answer' means the subject clicked "Wrong" when presented with the wrong position. And 0, that
# they were mistaken

iCSV = csv.writer(open(outputFileTests, "wb"))
iCSV.writerow(['Item', 'Class',
               'Day1_matrixA_order', 'Day1_matrixA_distanceToMatrixA',
               'Day2_matrixA_order', 'Day2_matrixA_distanceToMatrixA',
               'Day3_matrixA_order', 'Day3_matrixA_distanceToMatrixA',
               'DayRec_matrixA_order', 'DayRec_MatrixA_answer',
               'DayRec_matrixRec_order', 'DayRec_matrixRec_answer',
               'D3RecMR_distanceToMatrixA'])
# MORE DETAILED COMMENTS ARE TO BE WRITTEN AT A LATER TIME ON THIS PART
