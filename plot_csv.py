import sys
import getopt
import csv
import itertools
import pickle
import os
import rosbag
import math
import tf
import matplotlib.pyplot as plt
import numpy as np
from shutil import copyfile
from math import sqrt

dir_csv = '/media/hanjuns/disk/food_manipulation/tactile/fingervision/calib_data/csv/gripping_force/1_3/'
# dir_csv = '/media/song/disk/food_manipulation/tactile/gelsight/calib_data/csv/1_2/'

sampleNum = 30  # 50 for normal, 10 for hummus
dataNum = 0
# sampleNum_ = 10
# # forceThr = 0.5 #0.5
# crop_flag = 0
# prev_crop_flag = 0
# phase_change = 0
# minDataNum = 10 # 20 for normal, 10 for hummus
# # lookBehind = 30 # apple, cantaloupe, egg: 20,
# lookBehind_thr = 0.1 # 0.2 for force, 0.0005 for torque
# mocap_delay = 3 # 21.3ms, which is 2.556 data points for 120hz
# sampleNum_sum = 0
force_ft_total = []
force_fv_l_total = []
force_fv_r_total = []


def plotCalib(trial, y1_values, y2_values, y3_values):
    global dataNum
    # Calibration plot
    plt.figure(trial)
    plt.title("Fingervision Calibration (# of data = " + str(dataNum) + ")")
    plt.grid(True)
    plt.ylabel('Force (N)')
    plt.xlabel('Sensor Values')
    # plt.scatter(y2_values, y1_values, label='fv_left', c='r')
    plt.scatter(y3_values, y1_values, label='fv_right', c='g')
    plt.legend(loc='upper right')


def plotForce(trial, x_values, y1_values, y2_values, y3_values):
    plt.figure(trial)

    # Force history plot
    plt.title("Vertical Force History (Trial: " + str(trial) + ")")
    plt.grid(True)
    plt.ylabel('Force (N)')
    plt.xlabel('Time (s)')
    plt.plot(x_values, y1_values, label='F/T', c='b')
    plt.plot(x_values, y2_values, label='fv_left', c='r')
    plt.plot(x_values, y3_values, label='fv_right', c='g')
    plt.legend(loc='upper right')


def bias(file, trial):
    global dataNum, force_fv_l_total, force_fv_r_total
    time_list = []
    force_ft = []
    force_fv_l = []
    force_fv_r = []

    data_file = open(file, 'r')
    tf_data = csv.reader(data_file, delimiter=',')
    for row in tf_data:
        time_list.append(row[0])
        force_ft.append(row[1])
        force_fv_l.append(float(row[2]))
        force_fv_r.append(row[3])
    data_file.close()

    length = len(time_list)
    dataNum += length
    force_fv_l_init = sum(float(x) for x in force_fv_l[0:sampleNum]) / sampleNum
    force_fv_r_init = sum(float(y) for y in force_fv_r[0:sampleNum]) / sampleNum

    force_fv_l_zero = [float(x) - force_fv_l_init for x in force_fv_l]
    force_fv_r_zero = [float(y) - force_fv_r_init for y in force_fv_r]

    # plotForce(trial, time_list, force_ft, force_fv_l_zero, force_fv_r_zero)

    # print(len(force_fv_l_zero))
    force_fv_l_total.extend(force_fv_l_zero)
    force_fv_r_total.extend(force_fv_r_zero)
    # print(len(force_fv_l_total))
    force_ft_total.extend(force_ft)


for trial in range(1, 15):
    # print("trial: "+str(trial))
    bias(dir_csv + str(trial) + ".csv", trial)

trial = trial + 1
plotCalib(trial, force_ft_total, force_fv_l_total, force_fv_r_total)


plt.show()
