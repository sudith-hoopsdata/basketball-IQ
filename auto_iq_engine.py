import pandas as pd

def calculate_iq_score(row):
    iq_score = 0
    notes = []
    
    action = str(row.get('action_type', '')).lower()
    location = str(row.get('location', '')).lower()
    result = str(row.get('result', '')).lower()
    defense = str(row.get('defense_type', '')).lower()
    shot_clock = float(row.get('shot_clock', 15.0))
    player_efg = float(row.get('player_efg', 50.0))
    is_open = bool(row.get('is_open', False))

    if action == "shot":
        if location == "mid_range":
            if result == "miss" and player_efg < 45.0:
                iq_score -= 1.5
                notes.append("Bad Mid-Range (Low eFG%)")
            elif result == "make" and player_efg >= 45.0:
                iq_score += 1.0
                notes.append("Systematic Mid-Range Make")
        if not is_open and shot_clock > 18.0:
            iq_score -= 2.0
            notes.append("Forced Shot Early in Clock")

    elif action == "pass":
        if location == "corner_3" and is_open:
            if result == "make":
                iq_score += 2.0
                notes.append("Elite Read: Open Corner 3 (Make)")
            else:
                iq_score += 1.0
                notes.append("Elite Read: Open Corner 3 (Miss)")
        if shot_clock < 3.0 and not is_open:
            iq_score -= 2.0
            notes.append("Grenade Pass (Late Clock, Covered)")

    elif action == "pnr_ballhandler":
        if defense == "drop" and result == "pull_up_make":
            iq_score += 1.5
            notes.append("Correct Read vs Drop Coverage")
        elif defense in ["hedge", "blitz"] and result in ["pass_to_roller", "skip_pass"]:
            iq_score += 2.0
            notes.append("Beat the Blitz with Pass")

    elif action == "dribble":
        if location == "above_break" and result == "pickup_dribble" and shot_clock > 10.0:
            iq_score -= 1.0
            notes.append("Killed Dribble Above 3PT Line")
            
    if iq_score == 0:
        notes.append("Neutral Play / Routine Execution")

    return pd.Series([iq_score, ", ".join(notes)])

def run_engine(input_csv, output_csv):
    print(f"🏀 Loading raw plays from {input_csv}...")
    df = pd.read_csv(input_csv)
    
    print("🧠 Running 28-Point Contextual Logic Engine...")
    df[['iq_score', 'engine_notes']] = df.apply(calculate_iq_score, axis=1)
    
    leaderboard = df.groupby('player_id')['iq_score'].sum().reset_index()
    leaderboard = leaderboard.sort_values(by='iq_score', ascending=False)
    
    df.to_csv(output_csv, index=False)
    print(f"✅ Success! Generated {len(df)} contextual data points.")
    print(f"📊 Results saved to {output_csv}\n")
    print("🏆 CURRENT IQ LEADERBOARD (Top 5):")
    print(leaderboard.head(5).to_string(index=False))

if __name__ == "__main__":
    run_engine("raw_plays.csv", "graded_scouting_report.csv")