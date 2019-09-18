import numpy as np
import ast
import re
from scipy.spatial import distance

from expyriment.misc import data_preprocessing


class CorrectCards(object):
    def __init__(self):
        self.answer = []
        self.position = []
        self.picture = []


class WrongCards(object):
    def __init__(self):
        self.answer = []
        self.position = []
        self.picture = []


class Days(object):

    def __init__(self):
        self.name = ''
        self.header = ''
        self.ifile = ''
        self.data = []
        self.correctCards = CorrectCards()
        self.wrongCards = WrongCards()
        self.matrix = []


def extract_correct_answers(i_folder, i_file):
    agg = data_preprocessing.Aggregator(data_folder=i_folder, file_name=i_file)
    header = data_preprocessing.read_datafile(i_folder + i_file, only_header_and_variable_names=True)

    # Extracting pictures' positions in the matrix
    header = header[3].split('\n#e ')
    matrix_pictures = ast.literal_eval(header[header.index('Positions pictures:') + 1].split('\n')[0].split('\n')[0])
    matrix_pictures = [element for element in matrix_pictures if element is not None]

    # Extracting data
    data = {}
    for variable in agg.variables:
        data[variable] = agg.get_variable_data(variable)

    block_indexes = np.unique(data['NBlock'])
    for block in block_indexes:
        correct_answers = np.logical_and(data['Picture'] == data['Answers'], data['NBlock'] == block)
        wrong_answers = np.logical_and(data['Picture'] != data['Answers'], data['NBlock'] == block)

    # list(set(my_list)) is one of the smoothest way to eliminate duplicates
    classes = list(set([element[0] for element in matrix_pictures if element is not None]))
    classes = list(np.sort(classes))  # Order the classes
    # classes = ['a', 'b', 'c']
    # WARNING: BUG TO INVESTIGATE ######################################################################################
    # DOCUMENTATION ON CLASSES SHOULD BE WRITTEN AT A DIFFERENT PLACE

    valid_cards = CorrectCards()
    invalid_cards = WrongCards()
    for idx, val in enumerate(correct_answers):
        if val:
            valid_cards.answer.append(data['Answers'][idx][0])
            valid_cards.position.append(matrix_pictures.index(data['Answers'][idx]))

    for idx, val in enumerate(wrong_answers):
        if val:
            invalid_cards.answer.append(data['Answers'][idx][0])
            invalid_cards.picture.append(data['Picture'][idx][0])
            if 'None' in data['Answers'][idx][0]:
                invalid_cards.position.append(100)
            else:
                invalid_cards.position.append(matrix_pictures.index(data['Answers'][idx]))

    for idx, val in enumerate(wrong_answers):
        if val:
            invalid_cards.answer.append(data['Answers'][idx][0])
            invalid_cards.picture.append(data['Picture'][idx][0])
            if 'None' in data['Answers'][idx][0]:
                invalid_cards.position.append(100)
            else:
                invalid_cards.position.append(matrix_pictures.index(data['Answers'][idx]))

    for element in classes:
        valid_cards.element = [word for word in valid_cards.answer if word[0] == element]
        invalid_cards.element = [word for word in invalid_cards.picture if word[0] == element]

    return matrix_pictures, data, valid_cards, invalid_cards, len(block_indexes)

# Here the output is the picture that has been asked.
# invalid_cards.animals = [word for word in invalid_cards.picture if word[0] == 'a']
# invalid_cards.clothes = [word fo#r word in invalid_cards.picture if word[0] == 'c']
# invalid_cards.vehicles = [word for word in invalid_cards.picture if word[0] == 'v']
# invalid_cards.fruits = [word for word in invalid_cards.answer if word[0] == 'f']

# valid_cards.animals = [word for word in valid_cards.answer if word[0] == 'a']
# valid_cards.clothes = [word for word in valid_cards.answer if word[0] == 'c']
# valid_cards.vehicles = [word for word in valid_cards.answer if word[0] == 'v']
# valid_cards.fruits = [word for word in valid_cards.answer if word[0] == 'f']

# self.animals = []
# self.clothes = []
# self.vehicles = []
# self.fruits = []
