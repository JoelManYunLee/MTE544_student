# You can use this file to plot the loged sensor data
# Note that you need to modify/adapt it to your own files
# Feel free to make any modifications/additions here
import ast
import math

import matplotlib.pyplot as plt
from utilities import FileReader

def plot_lidar_scan(filename, row=0):
    headers, values=FileReader(filename).read_file()
    row_vals = values[row]

    ranges_str = row_vals[headers.index("ranges")]
    ranges_lst = ast.literal_eval(ranges_str)

    angle_increment = float(row_vals[headers.index("angle_increment")])
    
    # get cartesian points x, y from angle theta and radial distance (ranges)
    x, y = [], []
    for i, r in enumerate(ranges_lst):
        if math.isinf(r) or math.isnan(r):
            continue
        theta = 0 + i * angle_increment # 0 because we don't need the plot relative to any frame??
        x.append(r * math.cos(theta))
        y.append(r * math.sin(theta))

    plt.scatter(x, y)
    plt.axis("equal")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Lidar scan in cartesian points (row {row})")
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
        plot_lidar_scan(filename)
