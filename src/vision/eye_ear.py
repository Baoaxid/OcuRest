import numpy as np

def calculate_ear(landmarks, eye_indices, width: int, height: int) -> float:
    pts = [np.array([landmarks[idx].x * width, landmarks[idx].y * height]) for idx in eye_indices]
    dist_v1 = np.linalg.norm(pts[1] - pts[5])
    dist_v2 = np.linalg.norm(pts[2] - pts[4])
    dist_h = np.linalg.norm(pts[0] - pts[3])
    if dist_h == 0:
        return 0.0
    return float((dist_v1 + dist_v2) / (2.0 * dist_h))
