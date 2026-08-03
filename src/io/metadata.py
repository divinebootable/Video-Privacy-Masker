class VideoMetadata:
    """
    Stores static information about a video file.
    Extracted once when the video is opened, never changes.
    """
    
    def __init__(self, cap):
        """
        Extract metadata from an opened cv2.VideoCapture object.
        
        Args:
            cap: An opened cv2.VideoCapture object
        """
        import cv2
        
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.codec = self._decode_fourcc(cap)
        
        # Calculate duration
        if self.fps > 0:
            self.duration_seconds = self.total_frames / self.fps
        else:
            self.duration_seconds = 0.0
    
    def _decode_fourcc(self, cap):
        """Convert the FourCC integer code to a readable string."""
        import cv2
        
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        if fourcc == 0:
            return "unknown"
        
        chars = [
            chr((fourcc >> 0) & 0xFF),
            chr((fourcc >> 8) & 0xFF),
            chr((fourcc >> 16) & 0xFF),
            chr((fourcc >> 24) & 0xFF),
        ]
        return ''.join(chars).strip()
    
    def __repr__(self):
        """Clean representation for printing and debugging."""
        return (
            f"VideoMetadata(\n"
            f"  Resolution: {self.width} x {self.height}\n"
            f"  FPS: {self.fps:.2f}\n"
            f"  Total Frames: {self.total_frames}\n"
            f"  Duration: {self.duration_seconds:.2f}s\n"
            f"  Codec: {self.codec}\n"
            f")"
        )