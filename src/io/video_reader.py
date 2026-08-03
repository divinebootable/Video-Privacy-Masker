import cv2
from .metadata import VideoMetadata 

class VideoReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self._cap = None
        self.metadata = None
        self._current_frame = None

    def open(self):
        self._cap = cv2.VideoCapture(self.file_path)
        
        if not self._cap.isOpened():
            raise RuntimeError(f"Cannot open: {self.file_path}")
        
        self.metadata = VideoMetadata(self._cap)
        self._current_frame = 0
        
        return self 

    def read_frame(self):
        """Returns (success, frame)."""
        if self._cap is None:
            raise RuntimeError("Call open() first")
        
        success, frame = self._cap.read()
        
        if success:
            self._current_frame += 1
        
        return success, frame
    
    @property
    def current_frame_number(self):
        """Which frame we're on (1-indexed after reading)."""
        return self._current_frame
    
    def close(self):
        if self._cap is not None:
            self._cap.release()
            self._cap = None
        
        self._current_frame = 0
    