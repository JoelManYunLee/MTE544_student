# You can use this file to plot the loged sensor data
# Note that you need to modify/adapt it to your own files
# Feel free to make any modifications/additions here
import ast
import math

import matplotlib.pyplot as plt
from utilities import FileReader, euler_from_quaternion

def plot_lidar_scan(filename, row=0):
    headers, values = FileReader(filename).read_lidar_file()

    # --- Extract data from the first scan ---
    row = values[0]  # plot only 1 message
    angle_increment = float(values[headers.index("angle_increment")])

    # --- Convert 'ranges' string into a real list of floats ---
    ranges_clean = row.replace('inf', 'float("inf")').replace('nan', 'float("nan")')

    ranges = eval(ranges_clean)
    # --- Convert to Cartesian coordinates ---
    angle_min = 0.0  # assume first beam at +x direction
    xs, ys = [], []

    for i, r in enumerate(ranges):
        if math.isinf(r) or math.isnan(r):
            continue  # skip invalid readings
        theta = angle_min + i * angle_increment
        xs.append(r * math.cos(theta))
        ys.append(r * math.sin(theta))

    # --- Plot ---
    plt.figure()
    plt.scatter(xs, ys, s=5)
    plt.axis("equal")
    plt.grid(True)
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.title("Spiral Lidar scan (first message)")
    plt.show()

def plot_imu_odom(filename):
    headers, values=FileReader(filename).read_file() 
    time_list=[]
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)

    for i in range(0, len(headers) - 1):
        plt.plot(time_list, [lin[i] for lin in values], label= headers[i]+ " linear")
    
    #plt.plot([lin[0] for lin in values], [lin[1] for lin in values])

    plt.xlabel("Time (s)")
    plt.ylabel("Odometry data (position [m], orientation [rad])")
    plt.title("Robot odometry data over time: Line")
    plt.legend()
    plt.grid()
    plt.show()

def plot_trajectory(filename):
    headers, values = FileReader(filename).read_file() 
    time_list = []
    first_stamp = values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)

    num_signals = len(headers) - 1  # exclude timestamp
    fig, axes = plt.subplots(num_signals + 1, 1, figsize=(8, 10), sharex=False)
    fig.suptitle("Spiral Odometry Data and Trajectory", fontsize=14, fontweight='bold')

    # Plot x, y, and theta vs time
    for i in range(num_signals):
        axes[i].plot(time_list, [row[i] for row in values], label=headers[i])
        axes[i].set_ylabel(headers[i])
        axes[i].legend(loc='upper right')
        axes[i].grid(True)

    axes[num_signals - 1].set_xlabel("Time (s)")

    # Plot x vs y trajectory (final subplot)
    x_idx = headers.index('x [m]')
    y_idx = headers.index('y [m]')

    axes[-1].plot([row[x_idx] for row in values],
                  [row[y_idx] for row in values],
                  label="Trajectory", color='purple')
    axes[-1].set_xlabel("x position (m)")
    axes[-1].set_ylabel("y position (m)")
    # axes[-1].set_title("Trajectory (x vs y)")
    axes[-1].axis('equal')  # keep aspect ratio equal for proper geometry
    axes[-1].grid(True)
    axes[-1].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

def plot_imu_odom_subplots(filename):
    headers, values = FileReader(filename).read_file() 
    time_list = []
    first_stamp = values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)

    num_signals = len(headers) - 1  # exclude timestamp
    fig, axes = plt.subplots(num_signals, 1, figsize=(8, 6), sharex=True)
    fig.suptitle("IMU msg data vs Time: Line", fontsize=14, fontweight='bold')

    for i in range(num_signals):
        axes[i].plot(time_list, [row[i] for row in values], label=headers[i])
        axes[i].set_ylabel(headers[i])
        axes[i].legend(loc='upper right')
        axes[i].grid(True)

    axes[-1].set_xlabel("Time (s)")
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # leave space for main title
    plt.show()
    
import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files
    for filename in filenames:
        plot_trajectory(filename)
