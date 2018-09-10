import rospy
import rosbag
import csv
import os
import tf

dir_parent = '/media/song/disk/food_manipulation/tactile/gelsight/calib_data/'
dir_child = '1_2/'
dir_rosbag = dir_parent+'rosbag/'+dir_child
dir_csv = dir_parent+'csv/'+dir_child
latency_fv = 0.15 # latency of fingervision is approximately 0.1s.

for trial in range (1,21):
    print str(trial)
    bag = rosbag.Bag(dir_rosbag+str(trial)+'.bag')
    topics = bag.get_type_and_topic_info()[1].keys()
    types = []

    for i in range(0,len(bag.get_type_and_topic_info()[1].values())):
        types.append(bag.get_type_and_topic_info()[1].values()[i][0])

    if not os.path.exists(dir_csv):
                os.makedirs(dir_csv)
    csv_file = open(dir_csv+str(trial)+".csv",'w')
    writer = csv.writer(csv_file,delimiter=',')

    row_forque = []
    row_fv_r = []
    row_fv_l = []
    row_forque_sync = []
    row_fv_r_sync = []
    row_fv_l_sync = []
    
    time_temp = []
    time_sync = []

    row_all = []

    for topic, msg, t in bag.read_messages(topics):
        # time = float(t.secs)+float(t.nsecs)/1000000000.0
        if topic == "/ft_sensor/netft_data":
            row_forque_t = [float(msg.header.stamp.secs)+float(msg.header.stamp.nsecs)/1000000000.0, msg.wrench.force.x, msg.wrench.force.y, -msg.wrench.force.z]
            row_forque.append(row_forque_t)
        # elif topic == '/fingervision/fv_3_l/wrench':
        elif topic == '/gelsight/Wrench':    
            row_fv_l_t = [float(msg.header.stamp.secs)+float(msg.header.stamp.nsecs)/1000000000.0-latency_fv, msg.wrench.force.x, msg.wrench.force.y, -msg.wrench.force.z]
            row_fv_l.append(row_fv_l_t)
        # elif topic == '/gelsight/Wrench':
            row_fv_r_t = [float(msg.header.stamp.secs)+float(msg.header.stamp.nsecs)/1000000000.0-latency_fv, msg.wrench.force.x, msg.wrench.force.y, -msg.wrench.force.z]
            row_fv_r.append(row_fv_r_t)    

    # Synchronization by linear interpolation
    len_ft = len(row_forque)
    len_l = len(row_fv_l)
    len_r = len(row_fv_r)
    # print(len_l, len_r)
    j=0
    k=0
    if len_l<=len_r:

        min_len = len_l
        for i in range(0,min_len):
            t_fv_l = row_fv_l[i][0]
            t_ft = row_forque[j][0]
            # print (i, k)
            if k>=len_r:
                force_fv_r_new = row_fv_r[len_r-1][1]
                t_fv_r = t_fv_l+1

            else:
                t_fv_r = row_fv_r[k][0]

            # print("i=", i)
            while t_ft<t_fv_l:
                j += 1
                if j==len_ft:
                    force_ft_new = row_forque[len_ft-1][3]
                    break
                else:
                    t_ft = row_forque[j][0]
            while t_fv_r<t_fv_l:
                k += 1
                # print(k)
                if k==len_r:
                    force_fv_r_new = row_fv_r[len_r-1][1]
                    break
                else:
                    t_fv_r = row_fv_r[k][0]

            if j==0: # if t_0 of t_fv_l is earlier than t_0 of t_ft
                force_ft_new = row_forque[j][3]
            elif j<len_ft:
                t_ft_prev = row_forque[j-1][0]
                force_ft = row_forque[j][3] # force_z_ft
                force_ft_prev = row_forque[j-1][3]
                force_ft_new = force_ft_prev+(force_ft-force_ft_prev)*(t_fv_l-t_ft_prev)/(t_ft-t_ft_prev)
            if k==0: # if t_0 of t_fv_l is earlier than t_0 of t_fv_r
                force_fv_r_new = row_fv_r[k][1]
            elif k<len_r:
                t_fv_r_prev = row_fv_r[k-1][0]
                force_fv_r = row_fv_r[k][1] # force_x_r
                force_fv_r_prev = row_fv_r[k-1][1]
                force_fv_r_new = force_fv_r_prev+(force_fv_r-force_fv_r_prev)*(t_fv_l-t_fv_r_prev)/(t_fv_r-t_fv_r_prev)
            
            row_forque_sync.append(force_ft_new)
            row_fv_r_sync.append(force_fv_r_new)
            row_fv_l_sync.append(row_fv_l[i][1])

        for row in row_fv_l:
            time_temp.append(row[0])
        time_init = time_temp[0]
        time_sync = [float(t)-time_init for t in time_temp]
    
    else:

        min_len = len_r
        for i in range(0,min_len):
            if k>=len_l:
                force_fv_l_new = row_fv_l[len_l-1][1]
                t_fv_l = t_fv_r+1

            else:
                t_fv_l = row_fv_l[k][0]
            # print(i, k)
            # t_fv_l = row_fv_l[k][0]
            t_ft = row_forque[j][0]
            t_fv_r = row_fv_r[i][0]

            while t_ft<t_fv_r:
                j += 1
                if j==len_ft:
                    force_ft_new = row_forque[len_ft-1][3]
                    break
                else:
                    t_ft = row_forque[j][0]
            while t_fv_l<t_fv_r:
                k += 1
                if k==len_l:
                    force_fv_l_new = row_fv_l[len_l-1][1]
                    break
                else:
                    t_fv_l = row_fv_l[k][0]

            if j==0: # if t_0 of t_fv_r is earlier than t_0 of t_ft
                force_ft_new = row_forque[j][3]
            elif j<len_ft:
                t_ft_prev = row_forque[j-1][0]
                force_ft = row_forque[j][3] # force_z_ft
                force_ft_prev = row_forque[j-1][3]
                force_ft_new = force_ft_prev+(force_ft-force_ft_prev)*(t_fv_r-t_ft_prev)/(t_ft-t_ft_prev)
            if k==0: # if t_0 of t_fv_r is earlier than t_0 of t_fv_l
                force_fv_l_new = row_fv_l[k][1]
            elif k<len_l:
                t_fv_l_prev = row_fv_l[k-1][0]
                force_fv_l = row_fv_l[k][1] # force_x_r
                force_fv_l_prev = row_fv_l[k-1][1]
                # print (k, t_fv_l_prev, t_fv_l)
                force_fv_l_new = force_fv_l_prev+(force_fv_l-force_fv_l_prev)*(t_fv_r-t_fv_l_prev)/(t_fv_l-t_fv_l_prev)
            
            row_forque_sync.append(force_ft_new)
            row_fv_r_sync.append(row_fv_r[i][1])
            row_fv_l_sync.append(force_fv_l_new)

        for row in row_fv_r:
            time_temp.append(row[0])
        time_init = time_temp[0]
        time_sync = [float(t)-time_init for t in time_temp]
    

    # print(row_forque_l)
    # print(row_fv_l)
    # print(row_forque_l)

    # time(s) f_z(N) f_l_x f_r_x  
    for i in range(0,min_len):
        row_all.append([time_sync[i]]+[row_forque_sync[i]]+[-row_fv_l_sync[i]]+[row_fv_r_sync[i]])

    # print(row_all)
    writer.writerows(row_all)
    csv_file.close()
    bag.close()