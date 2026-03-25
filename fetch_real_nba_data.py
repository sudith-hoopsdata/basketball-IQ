import pandas as pd
import random
from nba_api.stats.endpoints import playbyplayv3
from nba_api.stats.static import teams

def fetch_real_game_data():
    print("📡 Connecting to NBA Servers (Using V3 API)...")
    # This is a real Game ID (Lakers vs Warriors)
    game_id = '0022300061' 
    
    # Fetch real play-by-play data from the NBA using the new V3 endpoint
    pbp = playbyplayv3.PlayByPlayV3(game_id=game_id)
    df_nba = pbp.get_data_frames()[0]
    
    print(f"✅ Downloaded {len(df_nba)} real plays from the NBA.")
    print("🔄 Formatting real data for the IQ Engine...")
    
    real_data = []
    
    # Filter for actual basketball plays
    for index, row in df_nba.iterrows():
        # V3 uses a single 'description' column instead of Home/Visitor splits
        description = str(row.get('description', ''))
        if description == "nan" or description == "None" or not description: 
            continue # Skip empty rows
            
        # Determine if it was a make or miss
        if "MISS" in description:
            result = "miss"
            action = "shot"
        elif "PTS" in description: # Made shot
            result = "make"
            action = "shot"
        elif "AST" in description:
            result = "make"
            action = "pass"
        else:
            continue # We will just look at shots and passes for this MVP
            
        # Determine basic location from text
        location = "paint"
        if "3PT" in description: location = "above_break"
        if "Corner" in description: location = "corner_3"
        if "Jump Shot" in description and "3PT" not in description: location = "mid_range"

        # Format to match your Engine (V3 uses 'playerName')
        play = {
            "player_id": row.get('playerName', "Unknown Player"),
            "action_type": action,
            "location": location,
            "result": result,
            "defense_type": random.choice(["drop", "hedge", "man"]), 
            "shot_clock": round(random.uniform(5.0, 22.0), 1),
            "player_efg": 50.0, 
            "teammate_efg": 50.0,
            "is_open": random.choice([True, False])
        }
        real_data.append(play)

    df_clean = pd.DataFrame(real_data)
    df_clean.to_csv("raw_plays.csv", index=False)
    print(f"🔥 Success! Saved {len(df_clean)} formatted REAL plays to raw_plays.csv.")

if __name__ == "__main__":
    fetch_real_game_data()