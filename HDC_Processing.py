import scipy.io as scp
from pathlib import Path
import numpy as np
import math
import random
import time
import HDC_functions as HDC

def run_EEG(p_max_or_threshold, writing_dir, patient, mode, use_p_max_or_threshold, thinning, generate_new_HVs):


    D = 1024 #HV length
    LBP_length = 6 #number of bits
    p = 0.0078125*2 #density
    nb_segments = int(round(D*p))
    length_segment = int(round(1/p))

    class_bundling_p = 0.50

    max_p_sparse_bundle = p_max_or_threshold
    threshold = p_max_or_threshold


    dict_pat_to_nb_seizures = {2:4, 5:6, 16:2}
    dict_pat_to_channels = {2:64, 5:59 , 16:64}
    channels = dict_pat_to_channels[patient]
    nb_LBP = dict_pat_to_nb_seizures[patient]

    #generate_new_HVs = 0
    #thinning: 
    #0 means majority thinning, 
    #1 is segmented thinning, 
    #2 is random thinning, 3 is CDT thinning

    #mode:
    #0 is dense, 
    #1 is sparse with segmented shifting as binding with thinning on second bundling, 
    #2 is sparse with segmented shifting as binding with thinning on both bundlings,
    #3 is sparse with binding by shifting whole EM vector by LBP value, 
    #4 is sparse with binding by shifting each segment by the LBP value,
    #5 is sparse with CDT-binding

    working_dir = Path(__file__).parent / ('Pat'+str(patient))
    

    K = 32
    random_perm_list = HDC.random_permutation_list(K)


    #IM and EM initialization
    if (generate_new_HVs):
        if (mode == 0): #dense
            IM = HDC.create_item_mem_dense(2**(LBP_length), D) 
            EM = HDC.create_item_mem_dense(channels, D)
            #write to files:
            with open('IM.txt','w') as file: 
                for index in IM:
                    HV = IM[index]
                    file.writelines('[')
                    for hv_index in range(len(HV)):
                        file.writelines(str(HV[hv_index]) + ' ')
                    file.writelines(']'+'\n')
            with open('EM.txt','w') as file: 
                for index in EM:
                    HV = EM[index]
                    file.writelines('[')
                    for hv_index in range(len(HV)):
                        file.writelines(str(HV[hv_index]) + ' ')
                    file.writelines(']'+'\n')

        elif (mode == 1 or mode == 2 or mode == 4): #sparse
            IM = HDC.compressed_IM_sparse(2**(LBP_length), nb_segments, length_segment)
            EM = HDC.EM_sparse(channels, nb_segments, length_segment)
            #write to files:
            with open('IM.txt','w') as file: 
                for index in IM:
                    HV = IM[index]
                    file.writelines('[')
                    for hv_index in range(len(HV)):
                        file.writelines(str(HV[hv_index]) + ' ')
                    file.writelines(']'+'\n')

            with open('EM.txt','w') as file:
                for index in EM:
                    HV = EM[index]
                    for i in range(len(HV)):
                        file.writelines('[')
                        segment = HV[i]
                        for j in range(len(segment)):
                            file.writelines(str(segment[j]) + ' ')
                        file.writelines(']'+'\n')
        elif (mode == 3 or mode == 5): #sparse, but not segmented
            IM = HDC.create_item_mem_sparse(2**(LBP_length), D, p)
            EM = HDC.create_item_mem_sparse(channels, D, p)
            #write to files:
            with open('IM.txt','w') as file: 
                for index in IM:
                    HV = IM[index]
                    file.writelines('[')
                    for hv_index in range(len(HV)):
                        file.writelines(str(HV[hv_index]) + ' ')
                    file.writelines(']'+'\n')
            with open('EM.txt','w') as file: 
                for index in EM:
                    HV = EM[index]
                    file.writelines('[')
                    for hv_index in range(len(HV)):
                        file.writelines(str(HV[hv_index]) + ' ')
                    file.writelines(']'+'\n')

    else: #read from files
        if (mode == 0 or mode == 3 or mode == 5): #dense or sparse non-segmented
            IM = {}
            file = open('IM.txt','r')
            content = file.read()
            i = 1
            IM_counter = 0
            content = content.split("\n")
            content = content[0:-1]
            for element in content:
                temp = element[1:len(element)-2]
                temp_list = np.array(temp.split(" "))
                IM[IM_counter] = temp_list.astype(int)
                IM_counter += 1
            file.close()

            EM = {}
            file = open('EM.txt','r')
            content = file.read()
            i = 1
            EM_counter = 0
            content = content.split("\n")
            content = content[0:-1]
            for element in content:
                temp = element[1:len(element)-2]
                temp_list = np.array(temp.split(" "))
                EM[EM_counter] = temp_list.astype(int)
                EM_counter += 1
            file.close()

        elif (mode == 1 or mode == 2 or mode == 4): #sparse
            IM = {}
            vector = []
            file = open('IM.txt','r')
            content = file.read()
            i = 1
            IM_counter = 0
            content = content.split("\n")
            content = content[0:-1]
            for element in content:
                temp = element[1:len(element)-2]
                temp_list = np.array(temp.split(" "))
                IM[IM_counter] = temp_list.astype(int)
                IM_counter += 1
            file.close()

            EM = {}
            vector = []
            file = open('EM.txt','r')
            content = file.read()
            i = 1
            EM_counter = 0
            content = content.split("\n")
            for n in range(64):
                part_content = content[n*nb_segments:(n+1)*nb_segments]
                HV = []
                for element in part_content:
                    temp = element[1:len(element)-2]
                    temp_list = np.array(temp.split(" "))
                    HV.append(temp_list.astype(int))
                EM[n] = np.array(HV)
                EM_counter += 1
            file.close()
        


    #First train for each LBP
    ictal_HV_list = []
    interictal_HV_list = []
    block_outputs_per_halfsecond_list = []
    for i in range(1, nb_LBP+1):
        print('Starting LBP' + str(i) + ':')
        LBP_address = working_dir / ('LBP_' + str(i) + '.mat')
        f1 = scp.loadmat(LBP_address)
        LBP_train = np.array(f1['LBP'])

        block_outputs_per_halfsecond = []
        nb_of_halfseconds = math.ceil(len(LBP_train)*1.0/256)
        for k in range(nb_of_halfseconds):
            LBP_part = LBP_train[k*256:((k+1)*256),:]
            block_outer = []
            for k2 in range(len(LBP_part)):
                LBP_row = LBP_part[k2]
                block_inner = []
                for electrode_nb in range(len(LBP_row)):
                    if (mode == 0):
                        block_inner.append(HDC.bind_dense(IM[LBP_row[electrode_nb]], EM[electrode_nb]))
                    elif (mode == 1 or mode == 2):
                        block_inner.append(HDC.binding_sparse_segm_shift_fast(-IM[LBP_row[electrode_nb]], EM[electrode_nb], D))
                    elif (mode == 3):
                        block_inner.append((HDC.perm(EM[electrode_nb], -int(LBP_row[electrode_nb])))) #flatten if segmented EM is used
                    elif (mode == 4):
                        block_inner.append(HDC.binding_sparse_last(np.array([-int(LBP_row[electrode_nb])]*nb_segments), EM[electrode_nb], D))
                    elif (mode == 5):
                        block_inner.append(HDC.binding_CDT(np.array([IM[LBP_row[electrode_nb]], EM[electrode_nb]]), D, random_perm_list))
                if (mode == 0):
                    block_outer.append(HDC.bundle_dense(block_inner))
                elif (mode == 1 or mode == 3 or mode == 4 or mode == 5):
                    block_outer.append(HDC.bundle_sparse_space(block_inner))
                elif (mode == 2):
                    if (thinning == 0):
                        block_outer.append(HDC.bundle_sparse_time_ideal(block_inner, max_p_sparse_bundle, D))
                    elif (thinning == 1):
                        block_outer.append(HDC.bundle_sparse_time_ideal_laiho(block_inner, D, nb_segments, length_segment))
                    elif (thinning == 2):
                        block_outer.append(HDC.bundle_sparse_time_ideal_random_thinning(block_inner, max_p_sparse_bundle, D))
                    elif (thinning == 3):
                        block_outer.append(HDC.bundle_sparse_space_CDT(block_inner, D, random_perm_list))
            if (mode == 0):
                block_outputs_per_halfsecond.append(HDC.bundle_dense(block_outer))
            elif (use_p_max_or_threshold == 0):
                if (thinning == 0):
                    block_outputs_per_halfsecond.append(HDC.bundle_sparse_time_ideal(block_outer, max_p_sparse_bundle, D))
                elif (thinning == 1):
                    block_outputs_per_halfsecond.append(HDC.bundle_sparse_time_ideal_laiho(block_outer, D, nb_segments, length_segment))
                elif (thinning == 2):
                    block_outputs_per_halfsecond.append(HDC.bundle_sparse_time_ideal_random_thinning(block_outer, max_p_sparse_bundle, D))
                elif (thinning == 3):
                    block_outputs_per_halfsecond.append(HDC.bundle_sparse_time_CDT(block_outer, D, random_perm_list))
            elif (use_p_max_or_threshold == 1):
                block_outputs_per_halfsecond.append(HDC.bundle_sparse_time(block_outer, threshold, D))

        block_outputs_per_halfsecond_list.append(block_outputs_per_halfsecond)
        if (mode == 0):
            interictal_HV = HDC.bundle_dense(block_outputs_per_halfsecond[:360])
            ictal_HV = HDC.bundle_dense(block_outputs_per_halfsecond[360:-360])
            
        elif (mode == 1 or mode == 2 or mode == 3 or mode == 4 or mode == 5):
            if (thinning == 0):
                interictal_HV = HDC.bundle_sparse_time_ideal(block_outputs_per_halfsecond[:360], class_bundling_p, D)
                ictal_HV = HDC.bundle_sparse_time_ideal(block_outputs_per_halfsecond[360:-360], class_bundling_p, D)
            elif (thinning == 1):
                interictal_HV = HDC.bundle_sparse_time_ideal_laiho(block_outputs_per_halfsecond[:360], D, nb_segments, length_segment)
                ictal_HV = HDC.bundle_sparse_time_ideal_laiho(block_outputs_per_halfsecond[360:-360], D, nb_segments, length_segment)
            elif (thinning == 2):
                interictal_HV = HDC.bundle_sparse_time_ideal_random_thinning(block_outputs_per_halfsecond[:360], class_bundling_p, D)
                ictal_HV = HDC.bundle_sparse_time_ideal_random_thinning(block_outputs_per_halfsecond[360:-360], class_bundling_p, D)
            elif (thinning == 3):
                interictal_HV = HDC.bundle_sparse_time_ideal(block_outputs_per_halfsecond[:360], 0.5, D)
                ictal_HV = HDC.bundle_sparse_time_ideal(block_outputs_per_halfsecond[360:-360], 0.5, D)

        ictal_HV_list.append(ictal_HV)
        interictal_HV_list.append(interictal_HV)    

        #write ictal and interictal HV
        folder_to_write = writing_dir / ('LBP_' + str(i))
        folder_to_write.mkdir(exist_ok=True)
        file = open(folder_to_write / 'ictal_HV.txt', 'w')
        file.writelines('[')
        for hv_index in range(len(ictal_HV)):
            file.writelines(str(ictal_HV[hv_index]) + ' ')
        file.writelines(']'+'\n')
        file.close()
        file = open(folder_to_write / 'interictal_HV.txt', 'w')
        file.writelines('[')
        for hv_index in range(len(interictal_HV)):
            file.writelines(str(interictal_HV[hv_index]) + ' ')
        file.writelines(']'+'\n')
        file.close()


    print(len(ictal_HV_list))
    print(len(block_outputs_per_halfsecond_list))
    #Now test for every combination of LBPs (can reuse block_outputs_per_halfsecond from training as training and testing use the same algorithm)
    print('Similarity Search in progress:')
    for i in range(1, nb_LBP+1):
        ictal_HV = ictal_HV_list[i-1]
        interictal_HV = interictal_HV_list[i-1]
        for j in range(1, nb_LBP+1):
            block_outputs_per_halfsecond = block_outputs_per_halfsecond_list[j-1]
            sim_scores_interictal = []
            sim_scores_ictal = []
            classifications = [] #per halfsecond
            for hv in block_outputs_per_halfsecond:
                if (mode == 0): #dense
                    sim_ictal = HDC.distance(hv,ictal_HV)
                    sim_scores_ictal.append(sim_ictal)
                    sim_interictal = HDC.distance(hv,interictal_HV)
                    sim_scores_interictal.append(sim_interictal)
                    if (sim_ictal < sim_interictal):
                        classifications.append(1)
                    else:
                        classifications.append(0)
                elif (mode == 1 or mode == 2 or mode == 3 or mode == 4 or mode == 5): #sparse
                    sim_ictal = HDC.similarity_sparse(hv,ictal_HV,D)
                    sim_scores_ictal.append(sim_ictal)
                    sim_interictal = HDC.similarity_sparse(hv,interictal_HV,D)
                    sim_scores_interictal.append(sim_interictal)
                    if (sim_ictal > sim_interictal):
                        classifications.append(1)
                    else:
                        classifications.append(0)

            #write classifications and sim_scores to file
            folder_to_write = writing_dir / ('LBP_' + str(i)) / ('LBP_' + str(j))
            folder_to_write.mkdir(exist_ok=True)
            file = open(folder_to_write / 'classifications.txt', 'w')
            for index in range(len(classifications)):
                file.writelines(str(classifications[index]) + ', ')
            file.close()
            file = open(folder_to_write / 'sim_scores.txt', 'w')
            for index in range(len(sim_scores_ictal)):
                file.writelines('('+str(sim_scores_ictal[index])+','+str(sim_scores_interictal[index])+') ')
            file.close()

patient = 16
lst_p_max = [0.02,0.04,0.06,0.08,0.09,0.10,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.20,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.30,0.31,0.32,0.33,0.34,0.35,0.36,0.38,0.40,0.42,0.44,0.46,0.48,0.50,0.52,0.54,0.56,0.58,0.60,0.62,0.64,0.66,0.68,0.70,0.72,0.74,0.76,0.78,0.80,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98]
lst_threshold = [*range(256)]
lst_threshold = [130]
mode = 2
use_p_max_or_threshold = 0 #0 for p_max, 1 for threshold (independent of mode, exept if mode is 2 then should be 0)
thinning = 3
generate_new_HVs = 1

if (use_p_max_or_threshold == 0):
    for p_max_or_threshold in lst_p_max:
        writing_dir = Path(__file__).parent / ('Pat'+str(patient)) / 'sparse 1024' / ('p_max '+str(round(p_max_or_threshold*100))+'%')
        writing_dir.mkdir(exist_ok=True)
        print("Start working with p_max = "+str(int(round(p_max_or_threshold*100)))+'%')
        run_EEG(p_max_or_threshold, writing_dir, patient, mode, use_p_max_or_threshold, thinning, generate_new_HVs)
elif (use_p_max_or_threshold == 1):
    for p_max_or_threshold in lst_threshold:
        writing_dir = Path(__file__).parent / ('Pat'+str(patient)) / 'sparse 1024' / ('threshold '+str(int(round(p_max_or_threshold))))
        writing_dir.mkdir(exist_ok=True)
        print("Start working with threshold = "+str(int(round(p_max_or_threshold))))
        run_EEG(p_max_or_threshold, writing_dir, patient, mode, use_p_max_or_threshold, thinning, generate_new_HVs)



