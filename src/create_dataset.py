import trajectories
from robot import Robot
import numpy as np

def dataset_builder(rbt: Robot, start_points:np.ndarray, end_points:np.ndarray, execution_time:np.ndarray, N_samples:int, noise_level:float = 0.2)->dict:
    _, n = start_points.shape
    dataset = dict.fromkeys(["traj_" + str(key) for key in range(N_samples)])
    for point in range(n):
        start_q = rbt.inverseKinimatics(start_points[0,point], start_points[1,point])
        end_q = rbt.inverseKinimatics(end_points[0,point], end_points[1,point])
        traj = trajectories.createTrajectory(start_q, end_q, execution_time[point], 0.1)
        _, N = traj.shape
        required_torque = np.zeros((2,N))
        for i in range(N): 
            required_torque[:,i:i+1] = rbt.forward_dynamics(traj[:2,i:i+1], traj[2:4,i:i+1], traj[4:6,i:i+1])

        data = np.zeros((2*N_samples, N))
        
        for sample in range(N_samples):
            data[sample:sample+2,:] = required_torque + np.random.normal(0, noise_level, (2,N))
        
        dataset["traj_" + str(point)] = data
    return dataset