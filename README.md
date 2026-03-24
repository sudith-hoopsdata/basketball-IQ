# basketball-IQ
A PyQt5 based program that acts as a scouting tool. Tracking non-box score basketball metrics that makes team and player scouting easier.
# Vision-Based Basketball IQ Engine (Contextual Analytics)

### The Problem
Traditional basketball analytics rely on "box score" events (points, rebounds, assists). These metrics fail to capture **Process vs. Result**. A player making the right read against a 'Drop Coverage' is a high-IQ play even if the shot is missed. Currently, this data is trapped in raw video and requires expensive manual labor or $100k+ optical camera arrays (e.g., Hawk-Eye).

### The Solution
My project is a **Contextual Data Acquisition Engine** designed to bridge the gap between raw broadcast footage and structured datasets.

**Key Technical Features:**
* **Multi-Player Tagging:** A custom PyQt5 interface allowing for simultaneous event-attribution across multiple player IDs (e.g., tagging a P&R screener and ball-handler in one action).
* **Non-Linear Video Control:** Integrated OpenCV buffering with frame-accurate keyboard shortcuts for efficient film scrubbing.
* **Proprietary IQ Rubric:** A 28-point logic framework that weights player decisions based on shot-clock pressure, defensive positioning, and historical efficiency (e.g., Pass to >35% 3PT Shooter).

### Future Roadmap: From Manual to Automated
This engine serves as the **Ground Truth Generator**. By manually tagging elite college and NBA film, I am building a proprietary dataset to:
1. Fine-tune a **Vision Transformer (ViT)** to recognize player jersey numbers in broadcast frames.
2. Utilize **GPT-4o / Gemini 1.5 Pro** via API to analyze offensive "spacing" and "gravity" from single-angle video.

### Summary
I am building a platform that captures the 'hidden' layer of basketball—the decision-making that basic statistics miss. By merging my background as a basketball player with custom software development, I’ve created a framework that evaluates Process over Result.
Traditionally, scouts spend hours of their day manually tagging film. My product digitizes this workflow into a structured scoring system for **Basketball IQ**. While a standard engineer can write code, they lack the expertise to define what a 'Correct Read' looks like in a high-level Pick & Roll. This tool is the bridge between elite basketball intuition and scalable data science. My ultimate goal is to move from this 'Human-in-the-Loop' tagging system to a fully automated AI model that can scout a player's IQ instantly from any broadcast feed.

## How to Run
1. Ensure you have Python installed.
2. Install dependencies: `pip install PyQt5 opencv-python pandas`
3. Clone this repo and add your own `.mp4` or `.webm` basketball film.
4. Update the file path in `iq_scout_engine.py` and run: `python iq_scout_engine.py`
