import numpy as np
# Type of planner
POINT_PLANNER=0; TRAJECTORY_PLANNER=1



class planner:
    def __init__(self, type_):

        self.type=type_

    
    def plan(self, goalPoint=[10, -1.0]):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(goalPoint)
        
        elif self.type==TRAJECTORY_PLANNER:
            return self.trajectory_planner_sig()


    def point_planner(self, goalPoint):
        x = goalPoint[0]
        y = goalPoint[1]
        return x, y

    # TODO Part 6: Implement the trajectories here
    def trajectory_planner_parabola(self):
        x = np.linspace(0.0, 1.5, 30)
        y = x**2

        trajectory = [[float(x[i]), float(y[i])] for i in range(len(x))]

        return trajectory
    
    def trajectory_planner_sig(self):
        x = np.linspace(0.0, 2.5, 30)
        y = 2/(1 + np.e**(-2*x)) - 1

        trajectory = [[float(x[i]), float(y[i])] for i in range(len(x))]

        return trajectory

