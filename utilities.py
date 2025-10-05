from math import atan2, asin, sqrt
import csv

M_PI=3.1415926535

class Logger:
    def __init__(self, filename, headers=["e", "e_dot", "e_int", "stamp"]):
        self.filename = filename

        with open(self.filename, 'w') as file:
            header_str=""

            for header in headers:
                header_str+=header
                header_str+=", "
            
            header_str+="\n"
            
            file.write(header_str)


    def log_values(self, values_list):

        with open(self.filename, 'a') as file:
            vals_str = ",".join(str(val) for val in values_list)
            
            vals_str+="\n"
            
            file.write(vals_str)
            

    def save_log(self):
        pass

class LidarLogger:
    def __init__(self, filename, headers=["e", "e_dot", "e_int", "stamp"]):
        self.filename = filename
        
        with open(self.filename, 'a', newline='') as f:
            header_str = ""
            for header in headers:
                header_str+=header
                header_str+= ", "
        header_str+="\n"
        
        f.write(header_str)
    
    def log_values(self, values_list):
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(values_list)

class FileReader:
    def __init__(self, filename):
        
        self.filename = filename
        
        
    def read_file(self):
        
        read_headers=False

        table=[]
        headers=[]
        with open(self.filename, 'r') as file:
            # Skip the header line

            if not read_headers:
                for line in file:
                    values=line.strip().split(',')

                    for val in values:
                        if val=='':
                            break
                        headers.append(val.strip())

                    read_headers=True
                    break
            
            next(file)
            
            # Read each line and extract values
            for line in file:
                values = line.strip().split(',')
                
                row=[]                
                
                for val in values:
                    if val=='':
                        break
                    row.append(float(val.strip()))

                table.append(row)
        
        return headers, table
    
    def read_lidar_file(self):
        with open(self.filename, "r") as f:
            lines = f.readlines()

        headers = [h.strip() for h in lines[0].split(',') if h.strip() != ""]
        data_line = lines[1].strip()  # first scan
        parts = data_line.split(',')

        # angle_increment is second-to-last numeric field (before timestamp)
        angle_increment = float(parts[-2])
        stamp = float(parts[-1])

        # everything before that belongs to the ranges list
        ranges_str = ",".join(parts[:-2])
        if not ranges_str.endswith("]"):
            ranges_str += "]"

        return headers, [ranges_str, angle_increment, stamp]


# TODO Part 5: Implement the conversion from Quaternion to Euler Angles
def euler_from_quaternion(x, y, z, w):
    """
    Convert quaternion (w in last place) to euler roll, pitch, yaw.
    quat = [x, y, z, w]
    """

    # Roll (x-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = atan2(sinr_cosp, cosr_cosp)

    # Pitch (y-axis rotation)
    sinp = sqrt(1 + 2 * (w * y - x * z))
    cosp = sqrt(1 - 2 * (w * y - x * z))
    pitch = 2 * atan2(sinp, cosp) - M_PI / 2

    # Yaw (z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw


