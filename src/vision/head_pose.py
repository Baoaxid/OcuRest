import cv2
import numpy as np
from typing import Tuple

FACE_MODEL_PTS = np.array([
    (0.0, 0.0, 0.0),          # Nose tip
    (0.0, -330.0, -65.0),     # Chin
    (-225.0, 170.0, -135.0),  # Left eye corner
    (225.0, 170.0, -135.0),   # Right eye corner
    (-150.0, -150.0, -125.0), # Left mouth corner
    (150.0, -150.0, -125.0)   # Right mouth corner
])

def estimate_head_pose(landmarks, width: int, height: int) -> Tuple[float, float]:
    image_points = np.array([
        (landmarks[1].x * width, landmarks[1].y * height),
        (landmarks[199].x * width, landmarks[199].y * height),
        (landmarks[33].x * width, landmarks[33].y * height),
        (landmarks[263].x * width, landmarks[263].y * height),
        (landmarks[61].x * width, landmarks[61].y * height),
        (landmarks[291].x * width, landmarks[291].y * height)
    ], dtype="double")

    focal_length = width
    center = (width / 2, height / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")
    dist_coeffs = np.zeros((4, 1))

    success, rot_vec, _ = cv2.solvePnP(
        FACE_MODEL_PTS, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
    )
    if not success:
        return 999.0, 999.0

    rmat, _ = cv2.Rodrigues(rot_vec)
    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)
    return float(angles[0]), float(angles[1])
