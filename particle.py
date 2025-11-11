
from mapUtilities import *
from utilities import *
from numpy import cos, sin
import numpy as np


class particle:

    def __init__(self, pose, weight):
        self.pose = pose
        self.weight = weight

    def motion_model(self, v, w, dt):
        #TODO: Implement the motion model for the particle
        """
        v: linear velocity
        w: angular velocity
        dt: time step
        """
        
        delta_theta = w * dt
        
        # Calculate the average heading during the time step
        avg_theta = self.pose[2] + delta_theta / 2
        
        # Update x and y using the average heading
        self.pose[0] += v * dt * np.cos(avg_theta)
        self.pose[1] += v * dt * np.sin(avg_theta)
        self.pose[2] += delta_theta

    # TODO: You need to explain the following function to TA
    # TODO: Add comments here explaining the function
    def calculateParticleWeight(self, scanOutput: LaserScan, mapManipulatorInstance: mapManipulator, laser_to_ego_transformation: np.array):
        '''
        Calculates the weight of this particle using the likelihood field model.
        The weight represents the probability P(z|x), where 'z' is the
        laser scan (scanOutput) and 'x' is the particle's pose (self.pose).

        scanOutput: The sensor_msgs/LaserScan message from the robot.
        mapManipulatorInstance: contains the pre-computed likelihood field.
        laser_to_ego_transformation: A 3x3 homogeneous transformation matrix (T_ego_from_laser) 
                                     that transforms points from the laser's frame to the robot's
                                     base frame
        '''

        T = np.matmul(self.__poseToTranslationMatrix(), laser_to_ego_transformation)

        _, scanCartesianHomo = convertScanToCartesian(scanOutput)
        scanInMap = np.dot(T, scanCartesianHomo.T).T

        likelihoodField = mapManipulatorInstance.getLikelihoodField()
        cellPositions = mapManipulatorInstance.position_2_cell(
            scanInMap[:, 0:2])

        lm_x, lm_y = likelihoodField.shape

        cellPositions = cellPositions[np.logical_and.reduce(
                (cellPositions[:, 0] > 0, -cellPositions[:, 1] > 0, cellPositions[:, 0] < lm_y,  -cellPositions[:, 1] < lm_x))]

        log_weights = np.log(
            likelihoodField[-cellPositions[:, 1], cellPositions[:, 0]])
        log_weight = np.sum(log_weights)
        weight = np.exp(log_weight)
        weight += 1e-10

        self.setWeight(weight)

    def setWeight(self, weight):
        self.weight = weight

    def getWeight(self):
        return self.weight

    def setPose(self, pose):
        self.pose = pose

    def getPose(self):
        return self.pose[0], self.pose[1], self.pose[2]

    def __poseToTranslationMatrix(self):
        x, y, th = self.getPose()

        translation = np.array([[cos(th), -sin(th), x],
                                [sin(th), cos(th), y],
                                [0, 0, 1]])

        return translation
