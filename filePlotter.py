# You can use this file to plot the loged sensor data
# Note that you need to modify/adapt it to your own files
# Feel free to make any modifications/additions here
import ast
import math

import matplotlib.pyplot as plt
from utilities import FileReader, euler_from_quaternion

def plot_lidar_scan(filename, row=0):
    headers, values=FileReader(filename).read_file()
    row_vals = values[row]

    acc_x = float(row_vals[headers.index("acc_x")])
    acc_y = float(row_vals[headers.index("acc_y")])
    time = float(row_vals[headers.index("stamp")])

    angle_increment = float(row_vals[headers.index("angular_z")])
    
    # get cartesian points x, y from angle theta and radial distance (ranges)
    yaw_list = []
    # for i, x in enumerate(acc_x):
    #     if math.isinf(x) or math.isnan(x):
    #         continue
    #     q = [x, acc_y[i], 0, angle_increment[i]]
    #     roll, pitch, yaw = euler_from_quaternion(q)
    #     yaw_list.append(yaw)



    plt.scatter(acc_x, time)
    plt.axis("equal")
    plt.xlabel("x")
    plt.ylabel("time")
    plt.title(f"X IMU data")
    plt.grid()
    plt.show()

def plot_errors(filename):
    headers, values=FileReader(filename).read_file() 
    time_list=[]
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)

    for i in range(0, len(headers) - 1):
        plt.plot(time_list, [lin[i] for lin in values], label= headers[i]+ " linear")
    
    #plt.plot([lin[0] for lin in values], [lin[1] for lin in values])

    plt.legend()
    plt.grid()
    plt.show()
    
import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files
    for filename in filenames:
        plot_errors(filename)
