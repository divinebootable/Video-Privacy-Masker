
---

## docs/02-learning-roadmap.md

```markdown
# Learning Roadmap: Video Privacy Masker

This isn't a todo list. It's the conceptual progression from "I know Python" to "I understand computer vision systems."

## Phase 0: Foundations (Before You Write CV Code)

**What you need to believe before starting:**

1. A video is not a moving picture. It's a sequence of matrices.
2. Every CV system is: `open → read → process → write → close`
3. Resource management is not optional. It's the first thing you design.
4. Single Responsibility Principle applies to classes, not just functions.

## Phase 1: The Pipeline (Module 1)

**Goal**: Move frames from disk to screen and back to disk.

**What you'll build**:
- `VideoReader` — opens files, yields frames, exposes metadata
- `VideoWriter` — takes frames, writes output video
- `VideoMetadata` — structured information about video properties

**Concepts internalized**:
- [ ] Why is a frame a `height × width × channels` array?
- [ ] What information exists before reading the first frame?
- [ ] Why does FPS matter for duration calculation?
- [ ] What happens if you don't release a video file handle?

**Deliverable**: Script that plays a video and prints its metadata.

---

## Phase 2: Spatial Thinking (Module 2)

**Goal**: Define and work with regions of interest.

**What you'll build**:
- ROI classes (rectangle, polygon)
- Coordinate validation (is this point inside the frame?)
- ROI drawing tools for user interaction

**Concepts internalized**:
- [ ] OpenCV's coordinate system: `(x, y)` is `(column, row)`, stored as `[row, column]`
- [ ] Point-in-rectangle vs. point-in-polygon
- [ ] Why ROIs are a separate concern from both tracking and masking
- [ ] Coordinate system transformations (image coords → display coords)

**Deliverable**: Script that lets user draw an ROI on a frame and saves the coordinates.

---

## Phase 3: Temporal Thinking (Module 3)

**Goal**: Track objects across frames with persistent IDs.

**What you'll build**:
- Abstract tracker interface
- OpenCV tracker wrappers (MOSSE, KCF, CSRT)
- Multi-object tracker manager
- Track data structure (ID, bbox, age, confidence)

**Concepts internalized**:
- [ ] Detection vs. tracking — when do you run each?
- [ ] Why tracking failure is inevitable and how to detect it
- [ ] ID assignment and re-identification
- [ ] Track lifecycle (born → active → lost → dead)
- [ ] IOU-based association between detections and tracks

**Deliverable**: Script that tracks multiple objects in a video with persistent IDs drawn as overlays.

---

## Phase 4: Privacy Transformations (Module 4)

**Goal**: Apply structured masks to tracked regions.

**What you'll build**:
- Abstract masker interface
- Pixelation masker
- Solid fill masker
- Gaussian blur masker
- Mask parameter configuration

**Concepts internalized**:
- [ ] Why pixelation ≠ blurring (information theory perspective)
- [ ] Spatial frequency and identifiability
- [ ] Mask bleed and boundary artifacts
- [ ] Temporal consistency of masks

**Deliverable**: Script that applies chosen mask type to tracked objects and saves output video.

---

## Phase 5: Integration (Module 5)

**Goal**: Wire everything into a configurable application.

**What you'll build**:
- Configuration system (YAML or JSON)
- Processing pipeline orchestrator
- Progress reporting
- Error recovery

**Concepts internalized**:
- [ ] Why configuration should be declarative, not imperative
- [ ] Pipeline error handling (fail one frame vs. fail entire video)
- [ ] Processing metadata (frames processed, time elapsed, ETA)

**Deliverable**: End-to-end application that takes input video + config and produces masked output.

---

## Phase 6: Understanding (Ongoing)

**Questions you should be able to answer without reference:**

1. A tracker loses its object on frame 147. What do you do?
2. Two tracked objects overlap completely. How do you resolve masking?
3. The output video is larger than the input. Why?
4. Pixelation at block size 8 vs. block size 16 — which is more private and why?
5. How would you extend this to real-time camera input?

---

## Skill Map


─────────────┐
│ Computer │
│ Vision │
│ Concepts │
└──────┬──────┘
│
┌────────────────┼────────────────┐
│ │ │
┌─────▼─────┐ ┌──────▼──────┐ ┌─────▼─────┐
│ Spatial │ │ Temporal │ │ Privacy │
│ Reasoning │ │ Reasoning │ │ Theory │
│ (ROIs) │ │ (Tracking) │ │ (Masking) │
└─────┬─────┘ └──────┬──────┘ └─────┬─────┘
│ │ │
└────────────────┼────────────────┘
│
┌──────▼──────┐
│ Software │
│ Engineering │
│ (Abstraction│
│ Testing, │
│ Docs) │
└─────────────┘


The vertical axis is domain knowledge. The horizontal integration is engineering practice.

---

## When to Move On

Don't move from Module N to Module N+1 until:

1. You can explain Module N's concepts to someone else
2. You've intentionally broken your code and fixed it
3. You've answered all the "Concepts internalized" checkboxes
4. You've written about *why* something works, not just *that* it works

---

*Next module: [Module 1 — Video Pipeline](../modules/01-video-pipeline.md)*