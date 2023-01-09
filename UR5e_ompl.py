import os.path as osp
import os
import pybullet as p
import math
import sys
import pybullet_data
sys.path.insert(0, osp.join(osp.dirname(osp.abspath(__file__)), '../'))

import gymnasium
import UR_gym
sys.modules["gym"] = gymnasium
from ur_ikfast import ur_kinematics
import numpy as np

import pb_ompl


class UR5e_ompl():
    def __init__(self):
        self.obstacles = []

        p.connect(p.GUI)
        p.setGravity(0, 0, -9.8)
        p.setTimeStep(1./240.)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.loadURDF("plane.urdf")

        # load robot
        robot_id = p.loadURDF(os.getcwd() + "/UR_gym/envs/robots/urdf/ur5e.urdf", (0, 0, 0), useFixedBase=1)
        robot = pb_ompl.PbOMPLRobot(robot_id)
        self.robot = robot

        # setup pb_ompl
        self.pb_ompl_interface = pb_ompl.PbOMPL(self.robot, self.obstacles)
        self.pb_ompl_interface.set_planner("RRTConnect")

        # add obstacles
        self.add_obstacles()

    def clear_obstacles(self):
        for obstacle in self.obstacles:
            p.removeBody(obstacle)

    def add_obstacles(self):
        # add box
        self.add_box([1, 0, 0.7], [0.5, 0.5, 0.05])

        # store obstacles
        self.pb_ompl_interface.set_obstacles(self.obstacles)

    def add_box(self, box_pos, half_box_size):
        colBoxId = p.createCollisionShape(p.GEOM_BOX, halfExtents=half_box_size)
        box_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=colBoxId, basePosition=box_pos)

        self.obstacles.append(box_id)
        return box_id

    def demo(self):
        start = [0, -1.57, 0, 0, 0, 0]
        goal = [0, 0, 0, 0, 0, 0]

        self.robot.set_state(start)
        res, path = self.pb_ompl_interface.plan(goal)
        if res:
            self.pb_ompl_interface.execute(path, dynamics=True)
        return res, path


if __name__ == '__main__':

    env = gymnasium.make("UR5OriReach-v1", render=True)
    ur5e = ur_kinematics.URKinematics('ur5e')
    joints = np.array([0.0, -1.57, 0.0, 0.0, 0.0, 0.0])

    pb_ompl_interface = pb_ompl.PbOMPL(env.robot)
    pb_ompl_interface.set_planner("RRTConnect")

    env.task.reset()
    goal = env.task.get_goal()
    angles = ur5e.inverse(goal, False)

    env.robot.set_state(joints)
    res, path = pb_ompl_interface.plan(angles)
    if res:
        pb_ompl_interface.execute(path, dynamics=False)

