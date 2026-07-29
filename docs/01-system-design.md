# System Design: Video processing pipeline (First application:Video Privacy Masker)

## Design Constrants

1. **Input**: Pre-recorded video files (not live streams)
2. **Processing**: offline, correctness over speed
3. **Output**: New video file with masks applied
4. **User Interaction**: Define ROIs before processing (not during)
5. **Platform**: Development on windows, but code should be cross-platform

## Component Breakdonw

## 1. Video I/O(`src/io/`)

**Responsibility**: Everything that touches files on disk.

io/
├── init.py
├── video_reader.py # Frame-by-frame reading
├── video_writer.py # Output video construction
└── metadata.py # VideoMetadata dataclass

**Why separate reader and writer?**
- Reading is pulled-based(caller requests frames)
- Writing is push-based (caller provides frames)
- Different error modes (file not found vs Disk full)
- Different codec consideartions

**Interface**:
python
reader = VideoReader("input.mp4")
metadata = reader.metadata  # Static information
frame = reader.read_frame()  # Returns (success, frame_array)
reader.close()

## 2. Region of Interest(`src/core/`) 

**Responsibility**: Define Spatial boundaries for masking.

core/
├── __init__.py
├── roi.py               # ROI definitions (polygon, rectangle, full frame)
├── mask_registry.py     # Which ROIs get which mask types
└── frame_coordinates.py # Coordinate system conversions

Why core/ and not roi/?

ROI is a core concept that multiple modules depend on. Tracking needs to know "only track inside this ROI."Masking needs to know"only mask inside this ROI."
It's a shared dependency, not a standalone module.

Design Question: Points vs. polygons vs. rectangles vs. segmentation masks?

- Start simple: rectangular ROIs

- Extend to polygons when needed

- Full semantic segmentation is out of scope

## 3. Object Tracking(`src/tracking/`)

**Responsibility**: Assign persistent IDs to objects across frames.

tracking/
├── __init__.py
├── base_tracker.py      # Abstract interface
├── opencv_trackers.py   # Wrappers for CSRT, KCF, MOSSE
├── tracker_factory.py   # Create tracker by name
└── track.py             # Track dataclass (id, bbox, confidence)

The critical design choice: Abstract base class.

Every tracker (CSRT, KCF, MOSSE, future DeepSORT) must implement:

    class BaseTracker(ABC):
        @abstractmethod
        def init(self, frame, bbox):
            """Initialize tracker with first frame and bounding box."""
            pass
        
        @abstractmethod
        def update(self, frame):
            """Update tracker, return (success, bbox)."""
            pass

This means the rest of the system never knows which tracker is running. It just calls init() and update().

Why this matters: toady I  use MOSSE (fast, simple). Tomorrow will try CSRT (slower, more accurate). The masking code doesn't change because it only depends on BaseTracker, not MOSSETracker.

## 4. Privacy Masking(`src/privacy/`)

**Responsibility**: Apply visual transformations to tracked regions.

privacy/
├── __init__.py
├── base_masker.py       # Abstract interface
├── pixelate.py          # Pixelation masking
├── solid.py             # Solid color fill
├── blur.py              # Gaussian blur
├── edge_only.py         # Edge-preserving mask (future)
└── mask_parameters.py   # Configurable masking parameters

Interface:
         class BaseMasker(ABC):
            @abstractmethod
            def apply(self, frame, bbox, mask_params):
                """Apply mask to frame region defined by bbox."""
                pass

## 5. Visualization(`src/visualization/`)

**Responsibility**: Display and debugging overlays.

visualization/
├── __init__.py
├── display.py           # Frame display with overlays
├── debug_overlay.py     # Bounding boxes, IDs, confidence scores
└── progress.py          # Processing progress indication

## 6. Application(`src.app.py`)

**Responsibility**: Wire components together. The orchestration layer.

# app.py pseudocode — this is the "Process frame" step from Module 1
def process_video(input_path, output_path, rois, tracker_type, masker_type):
    reader = VideoReader(input_path)
    writer = VideoWriter(output_path, reader.metadata)
    tracker_manager = MultiObjectTracker(tracker_type)
    
    for frame in reader.frames():
        # 1. Detect objects in ROIs (Module 2-3 interaction)
        detections = detect_in_rois(frame, rois)
        
        # 2. Update trackers
        tracked_objects = tracker_manager.update(frame, detections)
        
        # 3. Apply masks to tracked objects
        masked_frame = apply_masks(frame, tracked_objects, masker_type)
        
        # 4. Write output
        writer.write(masked_frame)
    
    reader.close()
    writer.close()



Data Flow Diagram:

Input Video
    │
    ▼
[VideoReader] ──metadata──► [VideoWriter]
    │                           ▲
    │ frame                     │ masked_frame
    ▼                           │
[ROI Filter]                    │
    │ regions                   │
    ▼                           │
[Object Detector]               │
    │ detections                │
    ▼                           │
[Tracker Manager]               │
    │ tracked_objects           │
    ▼                           │
[Privacy Masker] ───────────────┘


Key Design Decisions

## 1. Why not use a pipeline framework(GStreamer, FFmpeg pipes)?

Becuase we need frame-level access for tracking. Trackers maintian state between frames. You can't pip frames through a stateless filter when state matters.

## 2. Why separate detection from tracking?

Detection finds objects in a single frame. Tracking maintains identity across frames. These are fundermentally different problems with different algorithms.

## 3. Why start with rectangular ROIs?

Polygons and segmentation masks are more precise but introduce complexity:Point-in-polygon test, mask rasterization, edge cases with concave shapes. Start simple, extend later.

## 4. Why abstract base classes everywhere?

Because this project is a learning vehicle. I will swap trackers. I will try different maskers. The cost of abstraction now is 10 extra lines of code. The cost of no abstraction is rewrting app.py every time i chnage an algortihm

## What Could Go Wrong?

## Failure Mode	                        Impact	                     Mitigation
Video codec unsupported                Cannot open file            Explicit codec checking in VideoReader

Tracker loses object                  Mask jumps to wrong person   Confidence threshold + reinitialization

ROI outside frame bounds              Index error                  Coordinate clamping

Disk full during write                Partial output file          Check available space before processing

Memory with large videos              OOM crash                     Process in segments (future optimization)


## LEVELS OF ABSTRACTION:

Application Layer
    process_video()

────────────────────────

Domain Layer
    Tracking
    Masking
    ROI
    Visualization

────────────────────────

Infrastructure Layer
    VideoReader
    VideoWriter
    File System

────────────────────────

External Libraries
    OpenCV
    NumPy


## *Next: [02-learning-roadmap.md]