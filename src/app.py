"""
app.py — Application entry point.

Orchestrates the video pipeline:
    Reader → Process → Writer

This file wires components together. It does NOT:
    - Open video files directly (VideoReader does that)
    - Write video files directly (VideoWriter does that)
    - Process frames (future modules do that)
"""

import sys
from pathlib import Path

# Add src to path so imports work
sys.path.insert(0, str(Path(__file__).parent))

from src.io.video_reader import VideoReader
from src.io.video_writer import VideoWriter


def process_frame(frame):
    """
    Placeholder for future processing.
    Currently just returns the frame unchanged.
    
    Later, this is where tracking, masking, etc. will happen.
    """
    return frame


def run_pipeline(input_path, output_path=None):
    """
    Run the full pipeline: read → process → write.
    
    Args:
        input_path: Path to input video file
        output_path: Path to output video file (optional — if None, just display)
    """
    # Step 1: Open input video
    print(f"Opening: {input_path}")
    reader = VideoReader(input_path)
    reader.open()
    
    # Step 2: Show what we're working with
    print(reader.metadata)
    print()
    
    # Step 3: Set up output (if requested)
    writer = None
    if output_path:
        print(f"Output will be saved to: {output_path}")
        writer = VideoWriter.from_metadata(output_path, reader.metadata)
        writer.open()
    
    # Step 4: Process frames
    print("Processing frames...")
    print("Press 'q' to quit early\n")
    
    window_name = "Video Pipeline"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    try:
        while True:
            # Read
            success, frame = reader.read_frame()
            if not success:
                print(f"\nReached end of video at frame {reader.current_frame_number}")
                break
            
            # Process (placeholder — will be replaced with actual processing)
            processed = process_frame(frame)
            
            # Display
            cv2.imshow(window_name, processed)
            
            # Write (if output is configured)
            if writer:
                writer.write_frame(processed)
            
            # Show progress every 30 frames
            if reader.current_frame_number % 30 == 0:
                print(f"  Frame {reader.current_frame_number} / {reader.metadata.total_frames}")
            
            # Check for quit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print(f"\nQuit by user at frame {reader.current_frame_number}")
                break
    
    finally:
        # Step 5: Clean up
        reader.close()
        if writer:
            writer.close()
        cv2.destroyAllWindows()
        print("Done.")


def display_only(input_path):
    """
    Open a video and display it without saving.
    Useful for previewing or debugging.
    """
    run_pipeline(input_path, output_path=None)


def process_and_save(input_path, output_path):
    """
    Open a video, process it, and save the result.
    """
    run_pipeline(input_path, output_path)


# ===== Command-line interface =====

if __name__ == "__main__":
    import cv2  # Needed here for the display loop
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Display only:  python app.py <video_path>")
        print("  Process & save: python app.py <input_path> <output_path>")
        print("\nExample:")
        print("  python app.py assets/videos/test.mp4")
        print("  python app.py assets/videos/test.mp4 outputs/result.mp4")
        sys.exit(0)
    
    input_video = sys.argv[1]
    output_video = sys.argv[2] if len(sys.argv) > 2 else None
    
    run_pipeline(input_video, output_video)