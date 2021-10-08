import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread
import numpy as np
import time


def get_dataset_info(main_folder_name):
    #
    # report summury of dataset 
    #

    total_number = 0
    folders = os.listdir(main_folder_name)
    positive_pairs_count = 0
    negative_pairs_count = 0

    image_weight_folder = folders[0]
    folder_image_name = os.listdir(main_folder_name + '/' + image_weight_folder)[0]
    image = imread(main_folder_name + '/' + image_weight_folder + '/' + folder_image_name)
    image_weight = image.nbytes

    image_shape = image.shape

    # number of classes
    for folder in folders:
        total_number += len(os.listdir(main_folder_name + '/' + folder))

    # counting total amount of pairs
    for folder in folders:
        l = len(os.listdir(main_folder_name + '/' + folder))
        positive_pairs_count += l ** 2
        negative_pairs_count += l * (total_number - l)

    # calculating images weight
    positive_pairs_weight = round((image_weight * positive_pairs_count * 2) / (1024 ** 3), 3)
    negative_pairs_weight = round((image_weight * negative_pairs_count * 2) / (1024 ** 3), 3)



    number_classes = len(os.listdir(main_folder_name))

    print('-------------------------------------------------------')
    print('Dataset info\n')
    print('image shape = ', image_shape)
    print('image weight = ', round(image_weight / 1024, 3), ' KiB uint8')
    print('number of classes = ', number_classes)
    print('number of pictures = ', total_number)

    print('\npositive pairs count =', positive_pairs_count)
    print('positive pairs images weight =', positive_pairs_weight, ' GiB (uint8) ')

    print('\nnegative pairs count =', negative_pairs_count)
    print('negative pairs images weight =', negative_pairs_weight, ' GiB (uint8) ')

    print('\ntotal memory size =', round(positive_pairs_weight + negative_pairs_weight, 3), ' GiB (uint8)')


def estimate_dataset(main_folder_name,
                     max_positive,
                     max_negative):
    #
    # estimate memory size to load all pairs 
    #

    folder = os.listdir(main_folder_name)[0]
    folder_image_name = os.listdir(main_folder_name + '/' + folder)[0]
    image = imread(main_folder_name + '/' + folder + '/' + folder_image_name)
    image_weight = image.nbytes
    image_weight_fp32 = image.astype(np.float32).nbytes

    header = 'Estimated info\n'
    calculated_positive_pairs_weight = round((image_weight * max_positive * 2) / (1024 ** 3), 3)
    calculated_negative_pairs_weight = round((image_weight * max_negative * 2) / (1024 ** 3), 3)

    calculated_positive_pairs_weight_fp32 = round((image_weight_fp32 * max_positive * 2) / (1024 ** 3), 3)
    calculated_negative_pairs_weight_fp32 = round((image_weight_fp32 * max_negative * 2) / (1024 ** 3), 3)

    print('-------------------------------------------------------')
    print(header)

    print('desired positive pairs count =', max_positive)
    print('positive pairs images weight =', calculated_positive_pairs_weight, ' GiB (uint8) or ',
          calculated_positive_pairs_weight_fp32,
          'GiB (float32)')

    print('\ndesired negative pairs count =', max_negative)
    print('negative pairs images weight =', calculated_negative_pairs_weight, ' GiB (uint8) or ',
          calculated_negative_pairs_weight_fp32,
          'GiB (float32)')

    print('\ntotal memory size =', round(calculated_positive_pairs_weight + calculated_negative_pairs_weight, 3),
          ' GiB')


def get_pairs(main_folder_name, max_positive_pairs_count, max_negative_pairs_count):
    #
    # creating positive pairs sum Li**2 pairs 
    #
    print('Calculation began\n')
    start_time = time.time()

    labels = []
    pair_len = 2
    folders = os.listdir(main_folder_name)
    pairs_num = max_positive_pairs_count + max_negative_pairs_count

    folder = os.listdir(main_folder_name)[0]
    folder_image_name = os.listdir(main_folder_name + '/' + folder)[0]
    image = imread(main_folder_name + '/' + folder + '/' + folder_image_name)

    image_shape = image.shape
    pairs_shape = [pairs_num, pair_len] + list(image_shape)
    pairs = np.zeros(pairs_shape, dtype='uint8')
    positive_counter = 0

    while positive_counter < max_positive_pairs_count:
        kernel_folder = np.random.choice(folders)
        kernel_folder_images = os.listdir(main_folder_name + '/' + kernel_folder)

        first_image_name = np.random.choice(kernel_folder_images)
        second_image_name = np.random.choice(kernel_folder_images)

        first_image = imread(main_folder_name + '/' + kernel_folder + '/' + first_image_name)
        second_image = imread(main_folder_name + '/' + kernel_folder + '/' + second_image_name)

        # creating a pair
        pairs[positive_counter] = [first_image, second_image]
        labels.append([1])

        positive_counter += 1

    #
    # creating negative pairs
    #

    negative_counter = positive_counter

    # creating random negative pairs
    while negative_counter < max_negative_pairs_count + positive_counter:
        # choosing 2 random classes
        first_folder = np.random.choice(folders)
        second_folder = np.random.choice(folders)
        #
        # if folders are the same
        #
        while first_folder == second_folder:
            first_folder = np.random.choice(folders)
            second_folder = np.random.choice(folders)

        first_folder_images = os.listdir(main_folder_name + '/' + first_folder)
        second_folder_images = os.listdir(main_folder_name + '/' + second_folder)

        first_image_name = np.random.choice(first_folder_images)
        second_image_name = np.random.choice(second_folder_images)

        first_image = imread(main_folder_name + '/' + first_folder + '/' + first_image_name)
        second_image = imread(main_folder_name + '/' + second_folder + '/' + second_image_name)
        # creating a pair
        pairs[negative_counter] = [first_image, second_image]
        labels.append([0])
        negative_counter += 1
    print('Calculation is done\n')

    print('passed seconds: ', round(time.time() - start_time, 3), ' seconds')

    # labels=np.array(labels).reshape(max_positive_pairs_count+max_negative_pairs_count,1)
    labels = np.array(labels, dtype='int32')
    return pairs, labels
