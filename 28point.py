import pandas as pd

def calculate_iq_score(row):
    iq_score = 0
    notes = []
    
    # Standardize inputs
    action = str(row.get('action_type', '')).lower()
    location = str(row.get('location', '')).lower()
    result = str(row.get('result', '')).lower()
    defense = str(row.get('defense_type', '')).lower()
    shot_clock = float(row.get('shot_clock', 15.0))
    player_efg = float(row.get('player_efg', 50.0))
    teammate_efg = float(row.get('teammate_efg', 50.0)) # Treating > 53.0 as an elite shooter
    is_open = bool(row.get('is_open', False))

    # ==========================================
    # 🧠 SHOT SELECTION LOGIC
    # ==========================================
    if action == "shot":
        # 1. Corner 3 Dynamics (The most valuable shot in basketball)
        if location == "corner_3":
            if is_open:
                iq_score += 2.0
                notes.append("Excellent Read: Took Open Corner 3")
            elif not is_open and shot_clock > 5.0:
                iq_score -= 1.5
                notes.append("Forced Contested Corner 3 (Time remaining)")
        
        # 2. Wing / Above Break 3 Dynamics
        elif location == "above_break":
            if is_open and player_efg > 50.0:
                iq_score += 1.5
                notes.append("Systematic Wing 3 (Good Shooter, Open)")
            elif not is_open and shot_clock > 10.0:
                iq_score -= 1.5
                notes.append("Bad Shot: Contested Wing 3 Early in Clock")

        # 3. Paint / Rim Dynamics
        elif location == "paint":
            if defense == "drop":
                iq_score += 1.0
                notes.append("Attacked Drop Coverage at the Rim")
            if not is_open and result == "miss":
                iq_score -= 1.0
                notes.append("Forced Shot into Paint Traffic")

        # 4. Mid-Range Dynamics (The Analytics Killer)
        elif location == "mid_range":
            if not is_open:
                iq_score -= 2.0
                notes.append("Terrible Shot: Contested Mid-Range")
            elif is_open and player_efg < 45.0:
                iq_score -= 1.0
                notes.append("Bailed out Defense: Low-Efficiency Shooter took Mid-Range")
            elif is_open and player_efg >= 45.0:
                iq_score += 0.5
                notes.append("Acceptable Open Mid-Range for Elite Shooter")

    # ==========================================
    # 🧠 PLAYMAKING & PASSING LOGIC
    # ==========================================
    elif action == "pass":
        # 5. Elite Spacing Reads
        if is_open and teammate_efg > 53.0: # Simulating passing to a >35% 3PT shooter
            iq_score += 2.5
            notes.append(f"Elite Playmaking: Found Open Elite Shooter (eFG {teammate_efg})")
        
        # 6. Beating the Blitz
        elif defense in ["blitz", "hedge"]:
            iq_score += 2.0
            notes.append("High IQ: Escaped Blitz/Hedge with Pass")
            
        # 7. The "Grenade" Pass
        elif not is_open and shot_clock < 4.0:
            iq_score -= 2.0
            notes.append("Grenade Pass: Dumped ball to covered teammate late in clock")
            
        # 8. Routine ball movement
        elif is_open:
            iq_score += 0.5
            notes.append("Good Ball Movement (Found open man)")

    # ==========================================
    # 🧠 CLOCK MANAGEMENT PENALTIES/BONUSES
    # ==========================================
    if shot_clock < 3.0 and result == "make":
        iq_score += 1.0
        notes.append("Bailout Shot Clock Make")
    elif shot_clock > 20.0 and not is_open and action == "shot":
        iq_score -= 2.5
        notes.append("Hero Ball: Jacked up contested shot instantly")

    # Fallback if no rules trigger
    if iq_score == 0:
        notes.append("Neutral Play / Routine Execution")

    return pd.Series([iq_score, " | ".join(notes)])

def run_engine(input_csv, output_csv):
    print(f"🏀 Loading raw plays from {input_csv}...")
    df = pd.read_csv(input_csv)
    
    print("🧠 Running Expanded 28-Point Contextual Logic Engine...")
    df[['iq_score', 'engine_notes']] = df.apply(calculate_iq_score, axis=1)
    
    leaderboard = df.groupby('player_id')['iq_score'].sum().reset_index()
    leaderboard = leaderboard.sort_values(by='iq_score', ascending=False)
    
    df.to_csv(output_csv, index=False)
    print(f"✅ Success! Generated {len(df)} heavily nuanced data points.")
    print(f"📊 Results saved to {output_csv}\n")
    print("🏆 CURRENT IQ LEADERBOARD (Top 5):")
    print(leaderboard.head(5).to_string(index=False))
    
    # Just to show you it's working, let's print out the last 3 non-neutral plays
    print("\n🔍 SAMPLE GRADES:")
    sample = df[df['iq_score'] != 0].tail(3)
    for index, row in sample.iterrows():
        print(f"Player: {row['player_id']} | Play: {row['action_type']} from {row['location']} | Score: {row['iq_score']}")
        print(f"Logic: {row['engine_notes']}\n")

if __name__ == "__main__":
    run_engine("raw_plays.csv", "graded_scouting_report.csv")