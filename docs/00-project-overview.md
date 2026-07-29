
# Project Overview: Building a modular video processing pipeline (First application:Video Privacy Masker)

## Why this Project Exists

Modern Life is recorded, video has become one of the dominant ways humans record, communicate, and analyze the world—from smartphones and body cameras to medical procedures, autonomous vehicles, and public surveillance.

- Surveillance cameras vover public spaces
- Dashcams capture every intersection
- Body cameras record every interaction
- Research datasets contain bystanders who never consented
- Citizen journalists film protests where faces mean risk


The standard solution to privacy in video is ** blur everything**. But that destroys context. A blurry figure running tells you something. A blurry crowd has texture. A blurry face still carries skin tone, clothing, gait and temporal information.

**Blurring is not anonymization. It's degradation.**

This project asks a different questions:

Can we remove identity while preserving  *Behavior*?

## The Problem

Given a video containing one or more identifiable subjects, produce an output where:

1. **Individuals cannot be visually identified** (faces, skin, identifiable features are masked)
2. **Actions remain interpretable** (walking, gesturing, interacting with objects)
3. **Scene context remains intact** (environment, objects, spatial relationships)
4. **Temporal coherence is maintained** (no flickering masks between frames)

This is harder than it sounds.

## Current Approaches (and Their Limitations)

|  Approach              |  What It Does                       | Why it fails

|------------------------|-------------------------------------|--------------------------

Full-frame blur           | Gaussian blur entire frame         |Destroys all context. Useless for behavior analysis.
| Face detection + blur | Detect faces, blur bounding boxes | Fails on profiles, occlusion, distance. Body identity remains. |
| Full body segmentation + blur | Segment person, blur entire silhouette | Person becomes a ghost. Motion visible but identity stripped of behavioral nuance. |
| Deep privacy (GAN-based) | Replace faces with synthetic ones | Computationally expensive. Can hallucinate. New identity might be problematic. |
| This project | Track individuals, apply structured masking | Built from first principles. Controllable. Transparent about what's removed. |


## Our Approach

**Track first, mask second, preserve structure.**

1. **Video Pipeline** — Reliable frame-by-frame ingestion with metadata preservation
2. **ROI Selection** — User defines regions of interest (not everything needs masking)
3. **Object Tracking** — Follow individuals across frames with persistent IDs
4. **Privacy Masking** — Apply configurable masks (solid, pixelated, silhouette, edge-only)
5. **Visualization** — Overlay tracking information, bounding boxes, mask boundaries

The insight: **tracking persistence enables masking consistency**. A tracked person with ID #4 should have the same mask style, same color, same boundary across all 300 frames they appear in.

## Expected Outcomes

### Primary
- A working application that processes video files and outputs privacy-masked versions
- Configurable masking strategies (full block, pixelation, edge-preserving)
- Persistent tracking with minimal ID switches

### Secondary
- A documented engineering process showing how computer vision systems are built from primitives
- A modular architecture where components (tracker, masker) can be swapped independently
- Understanding of *why* each component exists, not just *how* to call the API

### Non-Goals
- Real-time processing (optimization comes after correctness)
- Perfect tracking (even CSRT, KCF, DeepSORT have failure modes)
- Production deployment (this is a learning system)


## System Architecture (Conceptual)
┌──────────────┐
│ Video File │
└──────┬───────┘
│
▼
┌──────────────────┐
│ VideoReader │ ← Module 1: Frame ingestion
└──────┬───────────┘
│ frame
▼
┌──────────────────┐
│ ROI Selector │ ← Module 2: Define masking zones
└──────┬───────────┘
│ masked region
▼
┌──────────────────┐
│ Object Tracker │ ← Module 3: Multi-object tracking
└──────┬───────────┘
│ tracked objects with IDs
▼
┌──────────────────┐
│ Privacy Masker │ ← Module 4: Apply masking strategies
└──────┬───────────┘
│ masked frame
▼
┌──────────────────┐
│ VideoWriter │ ← Output: Privacy-preserved video
└──────────────────┘



Each arrow is a clean interface. Each box is independently testable.

## The Philosophy

This project is built on a few beliefs:

1. **Understanding beats importing.** If you can't explain why a tracker needs frame dimensions, you don't understand tracking.

2. **Failure modes matter more than success rates.** A 95% accurate tracker that silently fails on 5% of frames is worse than an 80% tracker that *knows* when it's uncertain.

3. **Privacy is contextual.** Masking a face in a crowd vs. masking a face in a private conversation require different strategies. One tool cannot fit all.

4. **Documentation is for future-you.** In six months, you won't remember why you chose MOSSE over CSRT. Write it down.

---

*Next: [01-system-design.md](./01-system-design.md)*