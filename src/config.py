import glob
import os
from math import ceil

rawFolder = os.getcwd() + os.path.sep

picturesFolder = rawFolder + 'stimulis' + os.path.sep
picturesExamplesFolder = rawFolder + 'stimulisExample' + os.path.sep
dataFolder = rawFolder + 'data' + os.path.sep
soundsFolder = rawFolder + 'stimulis' + os.path.sep + 'sounds' + os.path.sep

mouseButton = 1

windowMode = False  # if False use FullScreen
windowSize = (1024, 768)  # if windowMode is True then use windowSize

picturesExamples = ['triangle.png', 'square.png', 'circle.png']
sounds = ['shortest-1-100ms.wav', 'shortest-2-100ms.wav', 'shortest-3-100ms.wav']

templatePicture = picturesFolder + 'a001.png'

linesThickness = 0
colorLine = (0, 0, 0)  # expyriment.misc.constants.C_BLACK

cueCardColor = (255, 255, 255)   # expyriment.misc.constants.C_WHITE
cardColor = (255, 255, 255)  # expyriment.misc.constants.C_WHITE

clickColor = (200, 200, 200)
restBGColor = (0, 0, 0)  # expyriment.misc.constants.C_BLACK
restCrossColor = (255, 255, 255)  # expyriment.misc.constants.C_WHITE
restCrossSize = (100, 100)
restCrossThickness = 20
dotColor = (0, 0, 0)  # expyriment.misc.constants.C_BLACK
bgColor = (150, 150, 150)
textColor = (0, 0, 0)  # expyriment.misc.constants.C_BLACK


textSize = 50
matrixSize = (7, 7)
cardSize = (90, 90)

''' Circles '''

startSpace = cardSize[1] + 20

nbBlocksMax = 10

presentationCard = 2000
responseTime = 5000

shortRest = 2500
restPeriod = 25000
clicPeriod = 200

min_max_ISI = [500, 1500]  # [min, max] inter_stimulus interval

##

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


arrow = ("xX                      ",
         "X.X                     ",
         "X..X                    ",
         "X...X                   ",
         "X....X                  ",
         "X.....X                 ",
         "X......X                ",
         "X.......X               ",
         "X........X              ",
         "X.........X             ",
         "X......XXXXX            ",
         "X...X..X                ",
         "X..XX..X                ",
         "X.X XX..X               ",
         "XX   X..X               ",
         "X     X..X              ",
         "      X..X              ",
         "       X..X             ",
         "       X..X             ",
         "        XX              ",
         "                        ",
         "                        ",
         "                        ",
         "                        ")

arrow1 = (' XX                                                                             ',
          ' XXXX                                                                           ',
          ' XX.XXX                                                                         ',
          ' XX...XXX                                                                       ',
          ' XX.....XXX                                                                     ',
          ' XX.......XXX                                                                   ',
          ' XX.........XXX                                                                 ',
          ' XX...........XXX                                                               ',
          ' XX.............XXX                                                             ',
          ' XX...............XXX                                                           ',
          ' XX.................XXX                                                         ',
          ' XX...............XXXX                                                          ',
          ' XX..............XX                                                             ',
          ' XX....  ......XX                                                               ',
          ' XX..XX......XX                                                                 ',
          ' XXX   XX......XX                                                               ',
          '        XX......XX                                                              ',
          '         XX......XX                                                             ',
          '          XX......XX                                                            ',
          '           XX......XX                                                           ',
          '            XX......XX                                                          ',
          '             XX......XX                                                         ',
          '              XX......XX                                                        ',
          '               XX......XX                                                       ',
          '                XX......XX                                                      ',
          '                 XXXXXXXXXX                                                     ',
          '                                                                                ',
          '                                                                                ',
          '                                                                                ',
          '                                                                                ',
          '                                                                                ',
          '                                                                                ')

if matrixSize == (5,5):
    matrixTemplate = [2,0,2,1,3,1,3,0,2,0,3,2,0,1,2,1,3,2,3,0,3,1,0,1]
    removeCards = [12]
elif matrixSize == (6,6):
    removeCards = []
    matrixTemplate = [0, 1, 1, 2, 0, 2,
                      2, 0, 0, 2, 1, 1,
                      1, 0, 2, 1, 2, 0,
                      0, 2, 1, 0, 1, 2,
                      1, 2, 1, 2, 0, 1,
                      0, 1, 0, 2, 2, 0]
elif matrixSize == (7, 7):
    removeCards = [24]  # we remove the center of the matrix
    centralCard = 24
    matrixTemplate = [0, 1, 1, 0, 2, 0, 2,
                      2, 0, 0, 1, 2, 1, 1,
                      1, 0, 2, 2, 1, 2, 0,
                      2, 1, 0,    2, 0, 1,
                      0, 2, 1, 2, 0, 1, 2,
                      1, 2, 1, 0, 2, 0, 1,
                      0, 1, 0, 1, 2, 2, 0]

correctAnswersMax = int(ceil((matrixSize[0]*matrixSize[0] - len(removeCards))*7./10))

classPictures = ['a', 'b', 'c']

listPictures = []
for classPicture in classPictures:
    listPictures.append(glob.glob(picturesFolder + classPicture + '*'))
for NClass in range(len(classPictures)):
    listPictures[NClass] = [p.replace(picturesFolder, '') for p in listPictures[NClass]]

debug = False
