import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread
import numpy as np
import time


def get_dataset_info(main_folder_name):
    #
    # report summury of dataset 
    #
    
    total_number=0
    folders=os.listdir(main_folder_name)
    positive_pairs_count=0
    negative_pairs_count=0
    
    image_weight_folder=folders[0]
    folder_image_name=os.listdir(main_folder_name+'/'+image_weight_folder)[0]
    image=imread(main_folder_name+'/'+ image_weight_folder+'/'+folder_image_name)
    image_weight=image.nbytes
    image_shape=image.shape

    # number of classes
    for folder in folders:
        total_number+=len(os.listdir(main_folder_name+'/'+folder))

    # counting total amount of pairs
    for folder in folders:
        l=len(os.listdir(main_folder_name+'/'+folder))
        positive_pairs_count+=l**2
        negative_pairs_count+=l*(total_number-l)

    # calculating images weight
    positive_pairs_weight=round((image_weight*positive_pairs_count*2)/(1024**3),3)
    negative_pairs_weight=round((image_weight*negative_pairs_count*2)/(1024**3),3)


    number_classes=len(os.listdir(main_folder_name))
    
    print('-------------------------------------------------------')
    print('Dataset info\n')
    print('image shape = ',image_shape)
    print('image weight = ',round(image_weight/1024,3),' KiB')
    print('number of classes = ',number_classes)
    print('number of pictures = ',total_number)


    print('positive pairs count =',positive_pairs_count)
    print('positive pairs images weight =',positive_pairs_weight,' GiB')

    print('negative pairs count =',negative_pairs_count)
    print('negative pairs images weight =',negative_pairs_weight,' GiB')
    
    print('\ntotal memory size =', positive_pairs_weight+negative_pairs_weight,' GiB')

    
def calculate_dataset(main_folder_name,
                     max_positive,
                     max_negative,
                     calculated_positive,
                     calculated_negative ):
    #
    #  calculate memory size to load all pairs
    #

    folder=os.listdir(main_folder_name)[0]
    folder_image_name=os.listdir(main_folder_name+'/'+folder)[0]
    image=imread(main_folder_name+'/'+folder+'/'+folder_image_name)
    image_weight=image.nbytes

    header='Calculated info \n'
    calculated_positive_pairs_weight=round((image_weight*calculated_positive*2)/(1024**3),3)
    calculated_negative_pairs_weight=round((image_weight*calculated_negative*2)/(1024**3),3)

    print('-------------------------------------------------------')
    print(header)

    print('desired positive pairs count =',max_positive)
    print('calculated positive pairs count =',calculated_positive)
    print('positive pairs images weight =',calculated_positive_pairs_weight,' GiB')
    print('\ndesired negative pairs count =',max_negative)
    print('calculated negative pairs count =',calculated_negative)
    print('negative pairs images weight =',calculated_negative_pairs_weight,' GiB')
    
    print('\ntotal memory size =', calculated_positive_pairs_weight+calculated_negative_pairs_weight,' GiB')
    
def estimate_dataset(main_folder_name,
                     max_positive,
                     max_negative ):
    #
    # estimate memory size to load all pairs 
    #

    folder=os.listdir(main_folder_name)[0]
    folder_image_name=os.listdir(main_folder_name+'/'+folder)[0]
    image=imread(main_folder_name+'/'+folder+'/'+folder_image_name)
    image_weight=image.nbytes

    header='Estimated info\n'
    calculated_positive_pairs_weight=round((image_weight*max_positive*2)/(1024**3),3)
    calculated_negative_pairs_weight=round((image_weight*max_negative*2)/(1024**3),3)

    print('-------------------------------------------------------')
    print(header)

    print('desired positive pairs count =',max_positive)
    print('positive pairs images weight =',calculated_positive_pairs_weight,' GiB')
    
    print('\ndesired negative pairs count =',max_negative)
    print('negative pairs images weight =',calculated_negative_pairs_weight,' GiB')
    
    print('\ntotal memory size =', calculated_positive_pairs_weight+calculated_negative_pairs_weight,' GiB')

    
    
def get_pairs(main_folder_name,max_positive_pairs_count,max_negative_pairs_count):
    #
    # creating positive pairs sum Li**2 pairs 
    #
    start_time = time.clock()
    
    labels = []
    pair_len=2
    folders=os.listdir(main_folder_name)
    pairs_num=max_positive_pairs_count+max_negative_pairs_count
    
    folder=os.listdir(main_folder_name)[0]
    folder_image_name=os.listdir(main_folder_name+'/'+folder)[0]
    image=imread(main_folder_name+'/'+folder+'/'+folder_image_name)
    
    image_shape=image.shape
    pairs_shape = [pairs_num,pair_len]+list(image_shape)
    pairs = np.zeros(pairs_shape,dtype='uint8')
    
    positive_counter=0
    
    while positive_counter <max_positive_pairs_count:
        for folder in folders:
            # choosing class folder
            folder_images_names=(os.listdir(main_folder_name+'/'+folder))
            for kernel_image_name in folder_images_names:
                # choosing class image
                for second_image_name in folder_images_names:
                    # choosing second class image
                    if positive_counter!=max_positive_pairs_count:
                        # creating a pair
                        kernel_image=imread(main_folder_name+'/'+folder+'/'+kernel_image_name)
                        second_image=imread(main_folder_name+'/'+folder+'/'+second_image_name)
                        pairs[positive_counter]=[kernel_image,second_image]
                        labels.append([1])
                        positive_counter+=1
                    else:
                        # if number of positive pairs is bigger, then max_positive_pairs_count
                        break
        # if number of positive pairs is smmaller, then max_positive_pairs_count
        break

    #
    # creating negative pairs
    #


    negative_counter=positive_counter
    
    # creating random negative pairs
    while negative_counter <max_negative_pairs_count+positive_counter:
        # choosing 2 random classes
        first_folder=np.random.choice(folders)
        second_folder=np.random.choice(folders)
        #
        # if folders are the same
        #
        while first_folder==second_folder:
            first_folder=np.random.choice(folders)
            second_folder=np.random.choice(folders)

        first_folder_images=os.listdir(main_folder_name+'/'+first_folder)
        second_folder_images=os.listdir(main_folder_name+'/'+second_folder)

        first_image_name=np.random.choice(first_folder_images)
        second_image_name=np.random.choice(second_folder_images)

        first_image=imread(main_folder_name+'/'+first_folder+'/'+first_image_name)
        second_image=imread(main_folder_name+'/'+second_folder+'/'+second_image_name)
        # creating a pair
        pairs[negative_counter]=[first_image,second_image]
        labels.append([0])
        negative_counter+=1
    
    calculate_dataset(main_folder_name,
                      max_positive_pairs_count,
                      max_negative_pairs_count,
                      positive_counter,
                      negative_counter-positive_counter)
    print('\npassed seconds: ',round(time.clock()-start_time,3),' seconds')
    return pairs,labels
    
    