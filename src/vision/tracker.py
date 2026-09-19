import cv2
import mediapipe as mp
from typing import Tuple
from src.vision.head_pose import estimate_head_pose
from src.vision.eye_ear import calculate_ear

class VisionTracker:
    def __init__(self, ear_threshold: float = 0.18):
        self.ear_threshold = ear_threshold
        self.cap = None
        self.has_camera = False
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
        self.init_camera()

    def init_camera(self) -> None:
        """Initializes low-resolution video capture to reduce CPU overhead."""
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            ret, _ = self.cap.read()
            if ret:
                self.has_camera = True
                return
            self.cap.release()
        self.has_camera = False

    def inspect_frame(self) -> Tuple[bool, bool]:
        """
        Captures and evaluates a single video frame.
        Returns:
            Tuple[bool, bool]: (is_facing_screen, is_eyes_open)
        """
        if not self.has_camera:
            return False, False

        ret, frame = self.cap.read()
        if not ret:
            return False, False

        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if not results.multi_face_landmarks:
            return False, False

        landmarks = results.multi_face_landmarks[0].landmark

        pitch, yaw = estimate_head_pose(landmarks, w, h)
        
        # Compensate for 180-degree inverted pitch axis in OpenCV camera coordinates
        pitch_dev = min(abs(pitch), abs(180.0 - abs(pitch)))
        is_facing = pitch_dev <= 35.0 and abs(yaw) <= 35.0

        # Compute Eye Aspect Ratio (EAR) for both eyes
        left_ear = calculate_ear(landmarks, [33, 160, 158, 133, 153, 144], w, h)
        right_ear = calculate_ear(landmarks, [362, 385, 387, 263, 373, 380], w, h)
        avg_ear = (left_ear + right_ear) / 2.0
        is_open = avg_ear >= self.ear_threshold

        return is_facing, is_open

    def release(self) -> None:
        """Releases the camera device and associated hardware handles."""
        if self.cap and self.cap.isOpened():
            self.cap.release()