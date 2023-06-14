import numpy as np
import warnings
from scipy.spatial.transform import Rotation as R

def distance_single(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute the distance between two array. This function is vectorized.

    Args:
        a (np.ndarray): First array.
        b (np.ndarray): Second array.

    Returns:
        np.ndarray: The distance between the arrays.
    """
    assert a.shape == b.shape
    return np.sqrt(np.sum((a - b) ** 2, axis=-1)).astype(np.float32)
    # return np.linalg.norm(a - b, axis=-1).astype(np.float32)



def distance(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute the distance between two array. This function is vectorized.

    Args:
        a (np.ndarray): First array.
        b (np.ndarray): Second array.

    Returns:
        np.ndarray: The distance between the arrays.
    """
    assert a.shape == b.shape
    if len(a) == 7:
        return np.linalg.norm(a[:3] - b[:3], axis=-1).astype(np.float32)
    else:
        return np.array([np.linalg.norm(row[0] - row[1], axis=-1) for row in zip(a[:, :3], b[:, :3])]).astype(
            np.float32)


def angle_distance(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute the geodesic distance between two array of angles. This function is vectorized.

    Args:
        a (np.ndarray): First quaternion array in (real, i, j, k) format.
        b (np.ndarray): Second quaternion array in (real, i, j, k) format.

    Returns:
        np.ndarray: The normalised distance between the angles.
    """
    assert a.shape == b.shape
    if len(a) == 7:
        return (2 * np.arccos(np.clip(np.abs(np.sum(np.dot(a[3:], b[3:]))), -1, 1)) / np.pi).astype(np.float32)
    else:
        return np.array([2 * np.arccos(np.clip(np.abs(np.sum(np.dot(row[0], row[1]))), -1, 1)) / np.pi for row in
                         zip(a[:, 3:], b[:, 3:])]).astype(np.float32)


def quaternion_to_euler(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    assert a.shape == b.shape
    if len(a) == 7:
        return np.array(R.from_quat(a[3:]).as_euler('xyz')-R.from_quat(b[3:]).as_euler('xyz')).astype(np.float32)
    else:
        return np.array([R.from_quat(row[0]).as_euler('xyz') - R.from_quat(row[1]).as_euler('xyz') for row in
                         zip(a[:, 3:], b[:, 3:])]).astype(np.float32)

