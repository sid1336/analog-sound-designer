# Analog Circuit Sound Designer 🎸

**Live app:** [https://a-log-sound-design.streamlit.app/](https://a-log-sound-design.streamlit.app/)

## Overview

Analog Circuit Sound Designer is a web application that connects the world of audio analysis with hands-on analog circuit design.  
Upload your own audio (WAV or MP3), and the app will:

- Analyze key features of your sound (brightness, loudness, noise, and bass/treble balance)
- Suggest an analog audio circuit (such as a filter, limiter, or noise gate) to shape or improve your sound
- Auto-generate a live schematic diagram for the recommended circuit using SchemDraw
- Show an interactive, zoomable plot of your audio waveform

No installation required—just open the app in your browser!

## Who is this for?

- **Musicians** and producers interested in analog hardware and effects
- **Audio and electronics students** who want to learn sound-to-circuit mapping
- **Makers, hackers, and tinkerers** looking for quick analog audio prototypes
- **Educators** demonstrating real-world applications of audio DSP and electronics

## Features

- Real-time audio analysis with feature extraction (Spectral Centroid, RMS, Zero Crossing Rate, Bass/Treble Ratio)
- Rule-based “AI” system for recommending classic analog circuits (Low-Pass/High-Pass filters, Limiter, Noise Gate, etc.)
- Instant schematic generation using SchemDraw (no static images)
- Interactive waveform visualization powered by Plotly
- Runs entirely in the cloud, accessible from any device

## How it works

1. **Upload** any short WAV or MP3 file
2. The app analyzes your audio and calculates key sound features
3. Based on the analysis, the app recommends the most suitable analog circuit to shape your sound
4. View the automatically generated schematic, ready for breadboarding, learning, or further design

## How to run locally

1. Clone this repository:
    ```
    git clone https://github.com/sid1336/analog-sound-designer.git
    cd analog-sound-designer
    ```
2. Install the requirements:
    ```
    pip install -r requirements.txt
    ```
3. Start the app:
    ```
    streamlit run app.py
    ```

## Tech stack

- Python
- Streamlit
- SchemDraw
- Librosa
- Plotly

## License

This project is for educational and creative purposes.  
Created by Sid Sachdeva. Connect via [GitHub](https://github.com/sid1336).

---

**Try it now:** [https://a-log-sound-design.streamlit.app/](https://a-log-sound-design.streamlit.app/)
