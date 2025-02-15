import pandas as pd
from pybaseball import playerid_lookup
from pybaseball import statcast_pitcher
import re


def read_data():
    # read tables using pd and concat
    table = pd.read_html("https://www.espn.com/mlb/stats/player/_/view/pitching")
    player_stats1 = pd.concat(table[:2], axis=1)
    return player_stats1

# used for extracting team from player name
def extract_player_name(name):
    return re.sub(r'[A-Z]{2,3}(?:/[A-Z]{2,3})?$', '', name).strip()


def classify_pitch(description):
    strike_values = {
            'foul_tip', 'foul', 'called_strike', 'hit_into_play',
       'swinging_strike', 'swinging_strike_blocked',
      'foul_bunt', 'missed_bunt',
       'bunt_foul_tip'
    }
    ball_values = {
        "ball", "blocked_ball", "intent_ball", "pitchout"
    }

    if description in strike_values:
        return "S"
    else:
        return "B"
def classify_hit(outcome):

    hit_key = {"single", "double", "home_run", "triple"}
    out_key = {
                "field_out", "force_out", "strikeout", "grounded_into_double_play",
                "fielders_choice", "double_play", "field error"}
    nan_key = {"walk", "hit_by_pitch", "sac_fly"}


    if outcome in hit_key:
        return 1  # Counts as a hit
    elif outcome in out_key:
        return 0  # Counts as an out
    elif outcome in nan_key:
        return None  # Does not count as an official at-bat
    

def game_stats(player_stats1):

    df = pd.DataFrame()

    for name in player_stats1["Player Name"]:
        
        # find first and last name
        space = name.find(" ")
        last = name[space:].strip()

        # some errors with diatrical marks on with player names
        # so create dict to avoid those errors when plugging into API
        known = {
            "Sanchez": 650911,
            "King": 650633,
            "Berrios": 621244,
            "Cortes": 641482,
            "Rodon": 607074,
            "Lopez": 641154
        }
        # if known, then use that as player id
        if last in known.keys():
            pitcher_id = known[last]
        else:
            # find id of player by last name
            player = playerid_lookup(last, name[:space].strip())
            pitcher_id = player.key_mlbam.values[0] 

        # call API and get stats for last year
        data = statcast_pitcher(start_dt="2024-04-01", end_dt="2024-09-30", player_id=pitcher_id)

        data["s_or_b"] = data["description"].apply(classify_pitch)
        data["outcome"] = data["events"].apply(classify_hit)
        
        cols = [
            "pitch_type", "game_date",
            "release_speed", "plate_x",
            "plate_z", "player_name", 
            "stand", "outcome", "s_or_b",
            "description", "events"
        ]
        data = data[cols]
        df = pd.concat([df,data])

    df.to_csv("player_data.csv", index=False)




def main():
    player_stats = read_data()
    player_stats["Player Name"] = player_stats["Name"].apply(extract_player_name)
    game_stats(player_stats)

if __name__ == "__main__":
    main()