# Module 1: Building the Video Pipeline

**Status**: In Progress  
**Started**: [Date]  
**Completed**: [Date]

---

## Pre-Module Notes

Before starting this module, I believe:
- Videos are files you read with OpenCV
- Processing means calling functions on frames
- The hard part will be the computer vision algorithms

Let's see what's actually true.

---

## Module Content

[Paste the module instructions you gave me earlier here]

---

## Implementation Journal

### Session 1: First Attempt

**What I tried**: Opened a video with `cv2.VideoCapture()`, looped with `while True`, called `cap.read()`.

**What happened**: Worked until the video ended, then it hung because I wasn't checking the return value of `read()`.

**What I learned**: `cap.read()` returns `(success, frame)`. When `success` is `False`, the frame is garbage. Always check.

### Session 2: Refactoring to a Class

**What I tried**: Moved all video logic into a `VideoReader` class.

**What happened**: Immediately realized `__init__` shouldn't open the file. What if the file doesn't exist? Then the object exists in a broken state.

**What I learned**: Construction ≠ initialization. Use an `open()` method or a factory function so failure is explicit.

### Session 3: Metadata as an Object

**What I tried**: Added properties like `reader.width`, `reader.height`, `reader.fps`.

**What happened**: Every time I accessed a property, it called `cap.get()`. This felt wrong — these values don't change.

**What I learned**: Extract metadata once in `open()` and store it. The `VideoMetadata` dataclass is an immutable snapshot of video properties.

---

## Post-Module Reflection

**What I believed before**:
- [Write what you thought you knew]

**What I know now**:
- [Write what changed]

**Surprising discoveries**:
- [Anything unexpected]

**Mistakes I made**:
- [Be honest — this is for future you]

**Questions I still have**:
- [These become future learning targets]

---

## Code

Final implementation: `src/io/video_reader.py`

Tests: `tests/test_video_reader.py`

---

## Answers to Module Questions

1. **Why is a video just a sequence of images?**
   [Your answer]

2. **Why does every computer vision algorithm process one frame at a time?**
   [Your answer]

3. **What information can you obtain before reading the first frame?**
   [Your answer]

4. **Why is it important to release the video resource?**
   [Your answer]

5. **If the video has 900 frames at 30 FPS, how long is it?**
   [Your answer with calculation]

---

*Next module: [02-roi-selection.md](./02-roi-selection.md)*