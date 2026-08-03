                    app.py
                       │
        ┌──────────────┴──────────────┐
        │                             │
   VideoReader                  VideoWriter
        │                             ▲
        │                             │
        └──────► FrameProcessor ◄─────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
     Tracker      Masker      Visualizer