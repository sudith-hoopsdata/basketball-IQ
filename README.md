# Basketball-IQ
A Python-based reasoning engine that acts as an autonomous scouting tool. Working to track non-box score basketball metrics to make high-level evaluation scalable.
# Vision-Based Basketball IQ Engine (Contextual Analytics)

### The Problem
Traditional basketball analytics rely on "box score" events (points, rebounds, assists). These metrics fail to capture **Process vs. Result**. A player making the right read against a 'Drop Coverage' is a high-IQ play even if the shot is missed. Currently, this data is trapped in raw video and requires expensive manual labor or $100k+ optical camera arrays (e.g., Hawk-Eye).

### The Solution
My project is a **Contextual Data Acquisition Engine** designed to bridge the gap between raw broadcast footage and structured datasets.

**Key Technical Features:**
* **NBA API V3 Integration:** A streamlined data acquisition pipeline that fetches live play-by-play data, providing the foundational "Ground Truth" for every possession.
* **Proprietary 28-Point IQ Rubric:** A multi-variable logic framework that weights player decisions based on shot-clock pressure, defensive positioning, teammate efficiency, and more.
* **AI Training Pipeline:** An automated data formatter that translates hardcoded scouting logic into JSONL conversational datasets, specifically designed to fine tune Large Language Models on elite basketball philosopy.

### Future Roadmap: From Manual to Automated
This engine currently serves as the Decision-Making Brain. By grading thousands of real NBA possessions, I am building the proprietary dataset required to:
1. **Automate the Eyes**: Integrate YOLOv8 and ByteTrack to extract spatial coordinates directly from raw broadcast footage, repalcing the need for API-based event data.
2. **Fine-Tune a Custom GPT**: Move from rigid Python logic to a fine-tuned LLM that "intuitively" understands spacing, gravity, and read quality and thinks like a basketball scout. All from natural language descriptions of video frames.

### Summary
I am building a platform that captures the "hidden" layer of basketball—the decision-making that basic statistics miss. By merging my background as a basketball player with custom software development, I’ve created a framework that evaluates Process over Result.

While a standard engineer can write code, they often lack the expertise to define what a "Correct Read" looks like in a high-level Pick & Roll. This tool is the bridge between elite basketball intuition and scalable data science. My ultimate goal is to move from this structured data ingestion to a fully autonomous AI scout that can evaluate a player's IQ instantly from any gym in the world.

## How to Run
1. Ensure you have Python installed.
2. Install dependencies: `bash pip install pandas nba_api`
3. Fetch real-world game data: python3 fetch_real_nba_data.py
4. Run 28-Point Logic Engine: python3 auto_iq_engine.py
5. Generate JSONL dataset for OpenAI: python3 28point.py


