import sys, ast, csv
import os
import numpy as np
from scipy.spatial import distance
from expyriment.misc import data_preprocessing
from ld_utils import extractCorrectAnswers, printErrors, printBasicResults, extractRecognitionAnswers
from ld_utils import correctCards, wrongCards
from config import matrixSize
import argparse

class Days(object):

    def __init__(self):
        self.name = ''
        self.header = ''
        self.ifile = ''
        self.data = []
        self.correctCards = correctCards()
        self.wrongCards = wrongCards()
        self.matrix = []


def get_arguments():
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description="",
		epilog="""
			Extract data for DeCoNap project
			
			Input:  subject folder
			""")

	parser.add_argument(
			"-i", "--subjectCode",
			required=False, nargs="+",
			)

	parser.add_argument(
			"-o", "--outputFolder",
			required=True, nargs="+",
			help="Output Folder",
			)   

	args =	parser.parse_args()
	if	len(sys.argv) == 1:
		parser.print_help()
		sys.exit()
	else:
		return args


def runDeCoNapExtraction(subjectCode, outputFolder):

	subjectCode = subjectCode[0]
	outputFolder = outputFolder[0]

	if not os.path.exists(outputFolder):
		os.mkdir(outFolder)

	subjectFolder = os.getcwd() + os.path.sep  + subjectCode + os.path.sep
	outputFile = outputFolder + os.path.sep  + subjectCode + '_o.csv'

	allFiles = os.listdir(subjectFolder)

	declarativeFiles = []

	for iFile in allFiles:
	    if 'ld_recognition' in iFile:
        	recognitionFile = iFile
	    elif 'ld_declarativeTask' in iFile:
        	declarativeFiles.append(iFile)

	if len(declarativeFiles)<3:
	    print 'Not enough files'
	    sys.exit()

	# Create output file
	iCSV = csv.writer(open(outputFile, "wb"))

	isInterference = False
	dayOneTestLearning = Days()
	dayOneTestConsolidation = Days()
	dayOneLearning = Days()

	iCSV.writerow(['Item','Class','Subject', '#BlocksOfLearning', 'D1MA_order','D1MA_distanceMA','D1MA_rt','D1MAConso_order','D1MAConso_distanceMA','D1MAConso_rt','D1LearningB1_order','D1LearningB1_distanceMA','D1LearningB1_rt','D1LearningB2_order','D1LearningB2_distanceMA','D1LearningB2_rt','D1LearningB3_order','D1LearningB3_distanceMA','D1LearningB3_rt','D1LearningB4_order','D1LearningB4_distanceMA','D1LearningB4_rt','D1LearningB5_order','D1LearningB5_distanceMA','D1LearningB5_rt','D1LearningB6_order','D1LearningB6_distanceMA','D1LearningB6_rt','D1LearningB7_order','D1LearningB7_distanceMA','D1LearningB7_rt','D1LearningB8_order','D1LearningB8_distanceMA','D1LearningB8_rt','D1LearningB9_order','D1LearningB9_distanceMA','D1LearningB9_rt','D1LearningB10_order','D1LearningB10_distanceMA','D1LearningB10_rt','orderMatrixA','answerMatrixA','orderMatrixR','answerMatrixR','recog_distanceMA'])

	for iFile in allFiles:
	    first_header = data_preprocessing.read_datafile(subjectFolder + iFile, only_header_and_variable_names=True)
	    header = first_header[3].split('\n#e ')

	    for field in header:
	        if "DayOne-TestLearning" in field and "Experiment" in field:
        	    print 'DayOne-TestLearning'
	            dayOneTestLearning.name = 'DayOne-TestLearning'
	            dayOneTestLearning.header = header
	            dayOneTestLearning.ifile = iFile
	            dayOneTestLearning.data, dayOneTestLearning.correctCards, dayOneTestLearning.wrongCards, dayOneTestLearning.matrix = extractCorrectAnswers(subjectFolder, iFile)
	            break
	        elif "DayOne-TestConsolidation" in field and "Experiment" in field:
        	    print 'DayOne-TestConsolidation'
	            dayOneTestConsolidation.name = 'DayOne-TestConsolidation'
	            dayOneTestConsolidation.header = header
	            dayOneTestConsolidation.ifile = iFile
	            dayOneTestConsolidation.data, dayOneTestConsolidation.correctCards, dayOneTestConsolidation.wrongCards, dayOneTestConsolidation.matrix = extractCorrectAnswers(subjectFolder, iFile)
	            break
	        elif "DayOne-Learning" in field:
	            print 'DayOne-Learning'
	            dayOneLearning.name = 'DayOne-Learning'
	            dayOneLearning.header = header
	            dayOneLearning.ifile = iFile
	            dayOneLearning.data, dayOneLearning.correctCards, dayOneLearning.wrongCards, dayOneLearning.matrix = extractCorrectAnswers(subjectFolder, iFile)
	            break
		elif "recognition" in iFile:
	            print 'DayOne-Recognition'
	            dayOneRecognition = Days()
	            dayOneRecognition.name = 'recognition'
	            dayOneRecognition.header = header
	            dayOneRecognition.ifile = iFile
	            dayOneRecognition.data, dayOneRecognition.correctCards_matA, dayOneRecognition.wrongCards_matA, dayOneRecognition.correctCards_matR, dayOneRecognition.wrongCards_matR, dayOneRecognition.matrixA, dayOneRecognition.matrixR, dayOneRecognition.order , dayOneRecognition.matrixOrder = extractRecognitionAnswers(subjectFolder, iFile)
		    break

	results = []
	for item in np.sort(dayOneTestLearning.matrix):
	    itemList = []
	    # Add item
	    itemList.append(item.rstrip('.png'))
	    # Add class
	    itemList.append(item.rstrip('.png')[0])
	
	    # Add Subject Code
	    itemList.append(subjectCode)

	    # Add # Blocks of Learning
	    itemList.append(int(max(dayOneLearning.correctCards.nblock))+1)

	    ##
	    # Day One Test Learning

	    # Order item in dayOneTestLearning
	    itemList.append(ast.literal_eval(dayOneTestLearning.header[13]).index(dayOneTestLearning.matrix.index(item)))
	    # Find item in DayOneTest
	    if set(dayOneTestLearning.correctCards.answer).intersection([item]):
	        pressItem = item
	        indexItem = dayOneTestLearning.correctCards.answer.index(item)
	        rtItem = dayOneTestLearning.correctCards.rt[indexItem]
	        #Append distance
	        itemList.append(0)
	        #Append RT
	        itemList.append(rtItem)
	    else:
	        indexItem = dayOneTestLearning.wrongCards.picture.index(item)
	        pressItem =  dayOneTestLearning.wrongCards.answer[indexItem]
	        rtItem = dayOneTestLearning.wrongCards.rt[indexItem]
	        if not pressItem=='None':
	            #Append distance
	            itemList.append(distance.euclidean(np.unravel_index(dayOneTestLearning.matrix.index(item), matrixSize), np.unravel_index(dayOneTestLearning.matrix.index(pressItem),matrixSize)))
	            #Append RT
	            itemList.append(rtItem)
	        else:
	            #Append distance
	            itemList.append('NaN')
	            #Append RT
	            itemList.append('NaN')
	    ##
	    # Day One
	
	    # Order item in dayOneConsolidation
	    itemList.append(ast.literal_eval(dayOneTestConsolidation.header[13]).index(dayOneTestConsolidation.matrix.index(item)))
	    # Find item in dayOneTestConsolidation
	    if set(dayOneTestConsolidation.correctCards.answer).intersection([item]):
	        pressItem = item
	        indexItem = dayOneTestConsolidation.correctCards.answer.index(item)
	        rtItem = dayOneTestConsolidation.correctCards.rt[indexItem]

	        #Append distance
	        itemList.append(0)
	        #Append RT
	        itemList.append(rtItem)
	    else:
	        indexItem = dayOneTestConsolidation.wrongCards.picture.index(item)
	        pressItem = dayOneTestConsolidation.wrongCards.answer[indexItem]
        	rtItem = dayOneTestConsolidation.wrongCards.rt[indexItem]
	        if not pressItem=='None':
	            #Append distance
        	    itemList.append(distance.euclidean(np.unravel_index(dayOneTestConsolidation.matrix.index(item), matrixSize), np.unravel_index(dayOneTestConsolidation.matrix.index(pressItem),matrixSize)))
	            #Append RT
        	    itemList.append(rtItem)
	        else:
	            #Append distance
	            itemList.append('NaN')
	            #Append RT
	            itemList.append('NaN')
	
	    ##
	    # Day One Learning
	
	    tmpCorrectCards = correctCards()
	    tmpWrongCards = wrongCards()
	
	    tmpCorrectCards.nblock = np.asarray(dayOneLearning.correctCards.nblock)
	    tmpWrongCards.nblock = np.asarray(dayOneLearning.wrongCards.nblock)
	
	    # Find item in dayOneLearning
	    for nBlock in range(0, int(max(dayOneLearning.correctCards.nblock)) + 1):
	        #print 'NBlock'+str(nBlock)
	        indexList = [i for i, s in enumerate(dayOneLearning.header) if 'Block '+str(nBlock)+' - Test' in s][0]+1
	        #print dayOneLearning.header[indexList]
	        #print tmpCorrectCards.answer.shape
	        tmpCorrectCards.answer = np.asarray(dayOneLearning.correctCards.answer)[tmpCorrectCards.nblock==nBlock]
	        tmpCorrectCards.rt = np.asarray(dayOneLearning.correctCards.rt)[tmpCorrectCards.nblock==nBlock]
	        tmpWrongCards.answer = np.asarray(dayOneLearning.wrongCards.answer)[tmpWrongCards.nblock==nBlock]
	        tmpWrongCards.picture = np.asarray(dayOneLearning.wrongCards.picture)[tmpWrongCards.nblock==nBlock]
	        tmpWrongCards.rt = np.asarray(dayOneLearning.wrongCards.rt)[tmpWrongCards.nblock==nBlock]
	
	        tmpCorrectCards.answer = tmpCorrectCards.answer.tolist()
	        tmpCorrectCards.rt = tmpCorrectCards.rt.tolist()
	
	        tmpWrongCards.answer = tmpWrongCards.answer.tolist()
	        tmpWrongCards.picture = tmpWrongCards.picture.tolist()
	        tmpWrongCards.rt = tmpWrongCards.rt.tolist()
	
	
	        #print 'HERE CORRECT'
	        #print len(tmpCorrectCards.answer)
	
	        #print 'HERE WRONG'
	        #print len(tmpWrongCards.picture)
	
	        # Order item in dayOneLearning

	        itemList.append(ast.literal_eval(dayOneLearning.header[indexList]).index(dayOneLearning.matrix.index(item)))

	        if set(tmpCorrectCards.answer).intersection([item]):
	            pressItem = item
	            indexItem = tmpCorrectCards.answer.index(item)
	            rtItem = tmpCorrectCards.rt[indexItem]
	
	            #Append distance
	            itemList.append(0)
	            #Append RT
	            itemList.append(rtItem)
	        else:
	            indexItem = tmpWrongCards.picture.index(item)
	            pressItem =  tmpWrongCards.answer[indexItem]
	
	            rtItem = tmpWrongCards.rt[indexItem]
	            if not pressItem=='None':
	                #Append distance
	                itemList.append(distance.euclidean(np.unravel_index(dayOneLearning.matrix.index(item), matrixSize), np.unravel_index(dayOneLearning.matrix.index(pressItem),matrixSize)))
	                #Append RT
	                itemList.append(rtItem)
	            else:
	                #Append distance
	                itemList.append('NaN')
	                #Append RT
	                itemList.append('NaN')
	
	    remainingBlocks = 10 - nBlock - 1
	    for nBlock in range(remainingBlocks):
	        itemList.append(' ')
	        itemList.append(' ')
	        itemList.append(' ')
	
	
	    if 'dayOneRecognition' in locals():
	        #######
	        # Day One Recognition
	
	        # Find index in MatrixA
	        indexItemA = dayOneRecognition.matrixA.index(item)
	        indices = [i for i, x in enumerate(dayOneRecognition.order) if x == indexItemA]
	        if not dayOneRecognition.matrixOrder[indices[0]]: #item from matrixA
	            #Append Order MatrixA
	            itemList.append(indices[0])
	        else:
	            #Append Order MatrixA
	            itemList.append(indices[1])
	
	        if set(dayOneRecognition.correctCards_matA.answer).intersection([item]):
	            #Append correct answer MatA
	            itemList.append(1)
	        else:
	            #Append wrong answer MatA
	            itemList.append(0)
	
	        # Find index in Matrix Random
	        indexItemR = dayOneRecognition.matrixR.index(item)
	        indices = [i for i, x in enumerate(dayOneRecognition.order) if x == indexItemR]
	        if dayOneRecognition.matrixOrder[indices[0]]: #item from matrix Random
	            #Append Order MatrixR
	            itemList.append(indices[0])
	        else:
	            #Append Order MatrixR
        	    itemList.append(indices[1])

	        if set(dayOneRecognition.correctCards_matR.answer).intersection([item]):
	            #Append correct answer MatR
	            itemList.append(1)
	        else:
	            #Append wrong answer MatR
	            itemList.append(0)
	
	        # Add distance to matrix A
	        itemList.append(distance.euclidean(np.unravel_index(dayOneRecognition.matrixR.index(item), matrixSize), np.unravel_index(dayOneTestLearning.matrix.index(item),matrixSize)))
	
	    # Write CSV file
	    iCSV.writerow(itemList)



def main():
	"""Let's go"""
	args =	get_arguments()
	runDeCoNapExtraction(**vars(args))
	

if __name__ == '__main__':
	sys.exit(main())	

