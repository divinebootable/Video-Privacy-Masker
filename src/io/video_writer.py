import cv2
import numpy as np


class VideoWriter:
    """
    Wrtites frames to a video file. Single responsiblity: Take Numpy Arrays and encode them to a video file. Does not process, display or modify frames.
    Usage:
        writer = VideoWriter("output.mp4", fps=30.0, width=1920, height=1080)
        writer.open()
        
        for frame in processed_frames:
            writer.write_frame(frame)
        
        writer.close()
        
        # Or with context manager:
        with VideoWriter("output.mp4", fps=30.0, width=1920, height=1080) as writer:
            writer.write_frame(frame)
    """
    
    def __init__(self, output_path, fps, width, height, codec='mp4v'):
        """
        Store output settings. Don't create the file yet.
        
        Args:
            output_path: Where to save the video (e.g., 'output.mp4')
            fps: Frames per second for the output video
            width: Frame width in pixels
            height: Frame height in pixels
            codec: FourCC codec code (default: 'mp4v' for H.264 in .mp4)
        """
        
        self.output_path = output_path
        self.fps = fps
        self.width = width
        self.height = height
        self.codec = codec
        
        self._writes = None
        self._frames_written = 0
    
    
    def open(self):
        """
        Create the video file and prepare for writing.
        
        returns:
            self for chaining
        
        Raises:
             RuntimeError: if the file cannot be created
        """
        
        fourcc = cv2.VideoWriter_fourcc(*self.codec)
        self._write = cv2.VideoWriter(self.output_path, fourcc, self.fps, (self.width, self.height))
        if not self._writer.isOpenend():
            raise RuntimeError(
                f"Failed to create ouput video: {self.output_path}\n"
                f"Check that the directory exists and you have write permissions."
            )
        
        self._frames_written = 0
        return self
    
    
    def write_frame(self, frame):
        """
        Write a single frame to the video.
        
        Args:
            frame: numpy array of shape (height, width, 3) in BGR format
            
        Raises:
            RuntimeError: If writer hasn't been opened
            ValueError: If frame dimensions don't match expected size
        """
        if self._writer is None:
            raise RuntimeError("Call open() first")
        
        if frame.shape[0] != self.height or frame.shape[1] != self.width:
            raise ValueError(
                f"Frame size mismatch. Expected ({self.height}, {self.width}), "
                f"got ({frame.shape[0]}, {frame.shape[1]})"
            )
        
        self._writer.write(frame)
        self._frames_written += 1
    
    
    @property
    def frames_written(self):
        """How many frames have been written so far."""
        return self._frames_written
    
    @property
    def is_opened(self):
        """Check if the writer is currently open."""
        return self._writer is not None and self._writer.isOpened()
    
    def close(self):
        """
        Finalize and close the video file.
        Must be called or the file will be corrupted.
        """
        if self._writer is not None:
            self._writer.release()
            self._writer = None
            print(f"Video saved: {self.output_path} ({self._frames_written} frames)")
    
    # Context manager support
    def __enter__(self):
        return self.open()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
    
    # Safety net
    def __del__(self):
        self.close()
    
    
    @classmethod
    def from_metadata(cls, output_path, metadata, codec='mp4v'):
        """
        Create a VideoWriter that matches the properties of an input video.
        
        Args:
            output_path: Where to save the output
            metadata: VideoMetadata object from a VideoReader
            codec: FourCC codec code
            
        Returns:
            VideoWriter instance (not yet opened)
        
        Usage:
            writer = VideoWriter.from_metadata("output.mp4", reader.metadata)
            writer.open()
        """
        return cls(
            output_path=output_path,
            fps=metadata.fps,
            width=metadata.width,
            height=metadata.height,
            codec=codec,
        )