import numpy as np

from UR_gym.envs.core import RobotTaskEnv
from UR_gym.envs.robots.UR5 import UR5, UR5Reg, UR5Ori
from UR_gym.envs.tasks.reach import ReachIAI, ReachReg, ReachOri, ReachObs
from UR_gym.pyb_setup import PyBullet


class UR5IAIReachEnv(RobotTaskEnv):
    """Reach task wih UR5 robot. (Original, use distance to target only)

    Args:
        render (bool, optional): Activate rendering. Defaults to False.
        reward_type (str, optional): "sparse" or "dense". Defaults to "sparse".
        control_type (str, optional): "ee" to control end-effector position or "joints" to control joint values.
            Defaults to "ee".
    """

    def __init__(self, render: bool = False, reward_type: str = "sparse", control_type: str = "ee") -> None:
        sim = PyBullet(render=render)
        robot = UR5(sim, block_gripper=True, base_position=np.array([0.0, 0.0, 0.0]), control_type=control_type)
        task = ReachIAI(sim, reward_type=reward_type, get_ee_position=robot.get_ee_position)
        super().__init__(robot, task)


class UR5RegReachEnv(RobotTaskEnv):
    """Reach task wih UR5 robot. (Added joint regulation reward)

    Args:
        render (bool, optional): Activate rendering. Defaults to False.
        reward_type (str, optional): "sparse" or "dense". Defaults to "sparse".
        control_type (str, optional): "ee" to control end-effector position or "joints" to control joint values.
            Defaults to "ee".
    """

    def __init__(self, render: bool = False, reward_type: str = "sparse", control_type: str = "ee") -> None:
        sim = PyBullet(render=render)
        robot = UR5Reg(sim, block_gripper=True, base_position=np.array([0.0, 0.0, 0.0]), control_type=control_type)
        task = ReachReg(sim, reward_type=reward_type, robot=robot)
        super().__init__(robot, task)


class UR5OriReachEnv(RobotTaskEnv):
    """Reach task wih UR5 robot. (Added orientation reward)

    Args:
        render (bool, optional): Activate rendering. Defaults to False.
        reward_type (str, optional): "sparse" or "dense". Defaults to "sparse".
        control_type (str, optional): "ee" to control end-effector position or "joints" to control joint values.
            Defaults to "ee".
    """

    def __init__(self, render: bool = False, reward_type: str = "sparse", control_type: str = "ee") -> None:
        sim = PyBullet(render=render)
        robot = UR5Ori(sim, block_gripper=True, base_position=np.array([0.0, 0.0, 0.0]), control_type=control_type)
        task = ReachOri(sim, reward_type=reward_type, robot=robot)
        super().__init__(robot, task)


class UR5ObsReachEnv(RobotTaskEnv):
    """Reach task wih UR5 robot. (Added obstacle reward)

    Args:
        render (bool, optional): Activate rendering. Defaults to False.
        reward_type (str, optional): "sparse" or "dense". Defaults to "sparse".
        control_type (str, optional): "ee" to control end-effector position or "joints" to control joint values.
            Defaults to "ee".
    """

    def __init__(self, render: bool = False, reward_type: str = "sparse", control_type: str = "ee") -> None:
        sim = PyBullet(render=render)
        robot = UR5Ori(sim, block_gripper=True, base_position=np.array([0.0, 0.0, 0.0]), control_type=control_type)
        task = ReachOri(sim, reward_type=reward_type, robot=robot)
        super().__init__(robot, task)
