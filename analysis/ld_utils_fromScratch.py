import csv

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


class Day(object):
    def __init__(self):
        self.matrix = []
        self.header = []
        self.matrix_pictures = []
        self.number_blocks = 0
        self.cards_order = []
        self.cards_distance_to_correct_card = []
        self.matrix_size = ()
        self.events = []


def extract_matrix_and_data(i_folder, i_file, recognition=False):
    header = data_preprocessing.read_datafile(i_folder + i_file, only_header_and_variable_names=True)

    # Extracting pictures' positions in the matrix
    header2 = header[3].split('\n#e ')
    if not recognition:
        matrix_position = 'Positions pictures:'
        recognition_matrix = False
    else:
        matrix_position = 'Learning:'
        recognition_matrix = matrix_pictures = ast.literal_eval(
            header2[header2.index('RandomMatrix:') + 1].split('\n')[0].split('\n')[0])
        cards_order = header2[header2.index('Presentation Order:') + 1:header2.index('Experiment: DayOne-Recognition')]
        cards_order = ''.join(cards_order)
        non_decimal = re.compile(r'[^\d.]+')
        cards_order = non_decimal.sub('', cards_order)
        cards_order = cards_order.split('.')
        cards_order = [int(x) for x in cards_order[0:-1]]
        matrix_a_or_rec = cards_order[len(cards_order)/2:]
        presentation_order = cards_order[:len(cards_order)/2]

    matrix_pictures = ast.literal_eval(
        header2[header2.index(matrix_position) + 1].split('\n')[0].split('\n')[0])
    matrix_pictures = [element for element in matrix_pictures if element is not None]

    # Extracting data
    events = header[-1].split('\n')
    events = [element.encode('ascii') for element in events]

    if len(matrix_pictures) == 48:
        matrix_size = (7, 7)
    elif len(matrix_pictures) == 36:
        matrix_size = (6, 6)
    elif len(matrix_pictures) == 25:
        matrix_size = (5, 5)
    else:
        raise ValueError('Matrix dimensions cannot be identified')

    if recognition:
        return events, matrix_pictures, matrix_size, recognition_matrix
    else:
        return events, matrix_pictures, matrix_size


def extract_events(events, matrix_size):
    cards_position = []
    cards_distance_to_correct_card = []
    cards_order = []
    for event in events:
        if 'Block' in event and 'Test' in event:
            cards_position.append({})
            cards_distance_to_correct_card.append({})
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
            cards_distance_to_correct_card[block_number][card] = 'NaN'
        elif 'Response' in event and 'NoResponse' not in event and 'pos_None_ERROR' not in event and register_on:
            response = re.search('(?<=card_)\w+', event).group(0)
            if response == card:
                cards_distance_to_correct_card[block_number][card] = 0
            else:
                response_position = re.search('pos_([0-9]+)_', event).group(1)
                cards_distance_to_correct_card[block_number][card] = distance.euclidean(
                    np.unravel_index(int(position), matrix_size),
                    np.unravel_index(int(response_position), matrix_size))

    return cards_order, cards_distance_to_correct_card, block_number+1


def recognition_extract_events(events, matrix_size):

    cards_position = []
    cards_distance_to_correct_card = []
    cards_order = []
    for event in events:
        if 'Block' in event and 'Test' in event:
            cards_position.append({})
            cards_distance_to_correct_card.append({})
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
            cards_distance_to_correct_card[block_number][card] = 'NaN'
        elif 'Response' in event and 'NoResponse' not in event and 'pos_None_ERROR' not in event and register_on:
            response = re.search('(?<=card_)\w+', event).group(0)
            if response == card:
                cards_distance_to_correct_card[block_number][card] = 0
            else:
                response_position = re.search('pos_([0-9]+)_', event).group(1)
                cards_distance_to_correct_card[block_number][card] = distance.euclidean(
                    np.unravel_index(int(position), matrix_size),
                    np.unravel_index(int(response_position), matrix_size))

    return cards_order, cards_distance_to_correct_card, block_number + 1

def write_csv(output_file, matrix_pictures,
              days=[], number_blocks=0, cards_order=[], cards_distance_to_correct_card=[]):

    i_csv = csv.writer(open(output_file, "wb"))

    first_row = ['Item', 'Class']
    if not days:
        for i in range(number_blocks):
            first_row.extend(
                ['Day1_Block' + str(i) + '_matrixA_order', 'Day1_Block' + str(i) + '_matrixA_distanceToMatrixA'])
    else:
        first_row.extend(['Day1_matrixA_order', 'Day1_matrixA_distanceToMatrixA',
                          'Day2_matrixA_order', 'Day2_matrixA_distanceToMatrixA',
                          'DayRec_matrixA_order', 'DayRec_MatrixA_answer',
                          'DayRec_matrixRec_order', 'DayRec_matrixRec_answer',
                          'D3RecMR_distanceToMatrixA'])

    i_csv.writerow(first_row)

    if not days:
        write_csv_learning(i_csv, matrix_pictures, cards_order, cards_distance_to_correct_card, number_blocks)
    else:
        write_csv_learning_test(i_csv, matrix_pictures, days)


def write_csv_learning(i_csv, matrix_pictures, cards_order, cards_distance_to_correct_card, number_blocks):
    for card in np.sort(matrix_pictures):
        # Add item; Add category
        card = card.rstrip('.png')
        item_list = [card, card[0]]
        for block_number in range(number_blocks):
            try:
                item_list.extend([cards_order[block_number][card], cards_distance_to_correct_card[block_number][card]])
            except KeyError:
                item_list.extend(['NaN', 'NaN'])
        i_csv.writerow(item_list)


def write_csv_learning_test(i_csv, matrix_pictures, days):
    for card in np.sort(matrix_pictures):
        # Add item; Add category
        card = card.rstrip('.png')
        item_list = [card, card[0]]
        for day in days:
            try:
                item_list.extend([day.cards_order[0][card], day.cards_distance_to_correct_card[0][card]])
            except KeyError:
                item_list.extend(['NaN', 'NaN'])
        i_csv.writerow(item_list)


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
