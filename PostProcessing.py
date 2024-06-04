import scipy.io as scp
from pathlib import Path
import numpy as np
import math
import random
import time
import os


def str_to_list(string):
    string = string[0:len(string)-2]
    string = string.replace(",", "")
    lst = np.array(string.split(" ")).astype(int)
    return lst



def postProcess(p_max):

    patient = 16


    # directory = Path(__file__).parent / ('Pat'+str(patient)) / 'sparse 1024' / ('p_max '+str(p_max))
    directory = Path(__file__).parent / ('Pat'+str(patient)) / 'shift binding right' / ('threshold '+str(p_max))


    nb_LBPs_dict = {2:4, 4:4, 5:6, 6:2, 8:3, 11:2, 13:2, 16:2} #patient linked to number of seizures
    nb_LBPs = nb_LBPs_dict[patient]

    width_window = 10 #10 halfseconds or 5 second window
    
    for threshold in range(9,0,-1):
    
        detection_delay_list = []
        right0_predictions_list = []
        right1_predictions_list = []
        right_predictions_list = []
        exception_thrown = 0

        for ix in range(1, nb_LBPs+1):
            for j in range(1, nb_LBPs+1):
                right_pred0 = 0
                right_pred1 = 0
                address = directory / ('LBP_' + str(ix)) / ('LBP_' + str(j))
                file = open(address / 'classifications.txt', 'r')
                content = file.read()
                file.close()
                half_sec_data = str_to_list(content)
                data = half_sec_data[:]
                classification_post_proc_data = []
                first_one_not_yet_found = True
                #Make percentage of right predictions
                for i in range(len(data)):
                    if ((i < 360) & (data[i] == 0)):
                        right_pred0 += 1
                    if ((i >= 360) & (data[i] == 1)):
                        right_pred1 += 1
                right0_predictions_list.append(right_pred0)
                right1_predictions_list.append(right_pred1)
                right_predictions_list.append((right_pred0+right_pred1)/(len(data))) #factor between 0 and 1 with 1 being perfect prediction
                
                if (exception_thrown == 0):
                    #In paper they take a post processing measurement every halfsecond! As done here.
                    for i in np.arange(width_window, len(data)):
                        classification = (np.mean(data[i-width_window:i]) > (threshold+0.5)/10)
                        classification_post_proc_data.append(classification)
                        if ((classification == 1) & (i < 360)): 
                            print("Sadly a false alert was send, increase the threshold per patient. For seizure_name: " + "LBP_" + str(ix) + " to LBP_" + str(j) + ", time: " + str(i) + " halfseconds.")
                            exception_thrown = 1
                            break
                        if ((classification == 1) & (i > 360) & first_one_not_yet_found):
                            first_one_not_yet_found = False
                            detection_delay_list.append(i)
                    if (first_one_not_yet_found & (exception_thrown == 0)):
                        print("Sadly no seizure was detected, decrease the threshold per patient. For seizure_name: " + "LBP_" + str(ix) + " to LBP_" + str(j) + ".")
                        exception_thrown = 1
                    

        if (exception_thrown == 0):
            lowest_to_not_throw_an_exception = threshold

    #After going over all possible thresholds, run again for lowest possible threshold and write down results
    if 'lowest_to_not_throw_an_exception' in locals():
        threshold = lowest_to_not_throw_an_exception
        exception_thrown_always = 0
    else: 
        exception_thrown_always = 1
        threshold = 9
    detection_delay_list = []
    right0_predictions_list = []
    right1_predictions_list = []
    right_predictions_list = []
    exception_thrown = 0
    for ix in range(1, nb_LBPs+1):
        for j in range(1, nb_LBPs+1):
            right_pred0 = 0
            right_pred1 = 0
            address = directory / ('LBP_' + str(ix)) / ('LBP_' + str(j))
            file = open(address / 'classifications.txt', 'r')
            content = file.read()
            file.close()
            half_sec_data = str_to_list(content)
            data = half_sec_data[:]
            classification_post_proc_data = []
            first_one_not_yet_found = True
            #Make percentage of right predictions
            for i in range(len(data)):
                if ((i < 360) & (data[i] == 0)):
                    right_pred0 += 1
                if ((i >= 360) & (data[i] == 1)):
                    right_pred1 += 1
            right0_predictions_list.append(right_pred0)
            right1_predictions_list.append(right_pred1)
            right_predictions_list.append((right_pred0+right_pred1)/(len(data))) #factor between 0 and 1 with 1 being perfect prediction
            
            if (exception_thrown == 0):
                #In paper they take a post processing measurement every halfsecond! As done here.
                for i in np.arange(width_window, len(data)):
                    classification = (np.mean(data[i-width_window:i]) > (threshold+0.5)/10)
                    classification_post_proc_data.append(classification)
                    if ((classification == 1) & (i < 360)): 
                        print("Sadly a false alert was send, increase the threshold per patient. For seizure_name: " + "LBP_" + str(ix) + " to LBP_" + str(j) + ", time: " + str(i) + " halfseconds.")
                        exception_thrown = 1
                        break
                    if ((classification == 1) & (i > 360) & first_one_not_yet_found):
                        first_one_not_yet_found = False
                        detection_delay_list.append(i)
                if (first_one_not_yet_found & (exception_thrown == 0)):
                    print("Sadly no seizure was detected, decrease the threshold per patient. For seizure_name: " + "LBP_" + str(ix) + " to LBP_" + str(j) + ".")
                    exception_thrown = 1

    #writing detection delay list and average delay per patient
    file = open(directory / 'detection_delay.txt', 'w')
    if (exception_thrown_always == 0):
        file.writelines('Average Detection Delay for Patient ' + str(patient)+ ' = ' + str(np.mean((np.array(detection_delay_list)-360)/2)) + ' (Threshold = '+str(threshold+0.5)+')' +'\n') #in seconds after ictal starts!

    if (exception_thrown_always == 0):
        file.writelines('Detection delay in seconds: [')
        for index in range(len(detection_delay_list)):
            file.writelines(str((np.array(detection_delay_list)[index]-360)/2) + ' ') #in seconds after ictal starts!
        file.writelines(']'+'\n')

    file.writelines('Right 0-predictions: [')
    for index in range(len(right0_predictions_list)):
        file.writelines(str((np.array(right0_predictions_list)[index])) + ' ') 
    file.writelines(']'+'\n')

    file.writelines('Right 1-predictions: [')
    for index in range(len(right1_predictions_list)):
        file.writelines(str((np.array(right1_predictions_list)[index])) + ' ') 
    file.writelines(']'+'\n')

    file.writelines('Right predictions percentage: [')
    for index in range(len(right_predictions_list)):
        file.writelines(str((np.array(right_predictions_list)[index]*100)) + ' ') 
    file.writelines(']'+'\n')

    file.writelines('Average right predictions percentage: '+str(np.mean(np.array(right_predictions_list))*100)+'\n')

    precision = np.sum(np.array(right1_predictions_list))/(np.sum(np.array(right1_predictions_list))+(360*((nb_LBPs)**(2)))-np.sum(np.array(right0_predictions_list)))
    file. writelines('Precision: '+str(precision)+'\n')


    nb_of_seizure_halfseconds_lst = []
    for k in range(nb_LBPs):
        address = directory / ('LBP_' + str(1)) / ('LBP_' + str(k+1))
        file4 = open(address / 'classifications.txt', 'r')
        content = file4.read()
        file4.close()
        nb_half_seconds = len(str_to_list(content))
        nb_of_seizure_halfseconds_lst.append(nb_half_seconds-360) #first 360 halfseconds are interictal states and last 360 halfseconds are postictal states, the rest are seizure/ictal states


    nb_of_seizure_halfseconds_total = np.sum(np.array(nb_of_seizure_halfseconds_lst))*nb_LBPs
    
    recall = np.sum(np.array(right1_predictions_list))/(np.sum(np.array(right1_predictions_list))+nb_of_seizure_halfseconds_total-np.sum(np.array(right1_predictions_list)))
    file.writelines('Recall: '+str(recall)+'\n')


    file.writelines('F1-score: '+str(2*precision*recall/(precision+recall)))

    file.close()

    

#lst_p_max = [0.02,0.04,0.06,0.08,0.09,0.10,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.20,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.30,0.31,0.32,0.33,0.34,0.35,0.36,0.38,0.40,0.42,0.44,0.46,0.48,0.50,0.52,0.54,0.56,0.58,0.60,0.62,0.64,0.66,0.68,0.70,0.72,0.74,0.76,0.78,0.80,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98]
lst_p_max = [*range(256)]
for p_max in lst_p_max:
    print('Start working with p_max: '+str(round(p_max*100))+'%')
    postProcess(p_max)

