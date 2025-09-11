import streamlit as st
import game
import pandas as pd
import random
import math
import player_creation

# Initialize session state for game variables
if "outs" not in st.session_state:
    st.session_state.outs = game.outs
if "inning" not in st.session_state:
    st.session_state.inning = game.inning
if "vis_score" not in st.session_state:
    st.session_state.vis_score = game.vis_score
if "home_score" not in st.session_state:
    st.session_state.home_score = game.home_score
if "bases" not in st.session_state:
    st.session_state.home_score = game.bases

def dynamic_input_data_editor(data, key, **_kwargs):
    """
    Wraps streamlit's data_editor to fix issue where the first edit doesn't persist.
    """
    changed_key = f'{key}__changed_flag'
    initial_data_key = f'{key}__initial_data'

    def on_data_editor_changed():
        if 'on_change' in _kwargs:
            args = _kwargs.get('args', ())
            kwargs = _kwargs.get('kwargs', {})
            _kwargs['on_change'](*args, **kwargs)
        st.session_state[changed_key] = True

    # If we have recorded that the editor changed previously, re-use the initial data
    if changed_key in st.session_state and st.session_state[changed_key]:
        data_to_pass = st.session_state.get(initial_data_key, data)
        # Reset the flag so we go back to normal behavior
        st.session_state[changed_key] = False
    else:
        data_to_pass = data
        st.session_state[initial_data_key] = data

    # Use the same key, but force on_change so we can capture that we edited
    _editor_kwargs = _kwargs.copy()
    _editor_kwargs.update({'data': data_to_pass, 'key': key, 'on_change': on_data_editor_changed})

    return st.data_editor(**_editor_kwargs)

def base_graphic(bases):
    # bases: [first, second, third]
    # Use emojis for bases and show runner names if present
    base_icons = []
    for i, runner in enumerate(bases):
        if runner:
            base_icons.append(f"🟢 {runner.name}")
        else:
            base_icons.append("⚪️ None")
    # Layout: third base (left), second (top), first (right)
    st.markdown(f"""
    <div style="text-align:center;">
        <div>{base_icons[1]}</div>
        <div style="display:flex; justify-content:space-between;">
            <span>{base_icons[2]}</span>
            <span>{base_icons[0]}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def restart_game():
    # Reset game.py variables
    game.outs = 0
    game.inning = 1
    game.vis_score = 0
    game.home_score = 0
    game.bases = [None, None, None]
    game.batter_up_vis_index = 0
    game.batter_up_home_index = 0
    game.batter_up_index = 0

    # Reset Streamlit session state
    st.session_state.outs = game.outs
    st.session_state.inning = game.inning
    st.session_state.vis_score = game.vis_score
    st.session_state.home_score = game.home_score
    st.session_state.bases = game.bases

def steal(og_base): #insert INDEX of base (0-2) being stolen from
    #determines whether a stolen base is successful
    bases = st.session_state.bases
    chances = st.session_state.get("chances", 0)
    roll = random.randint(0, 100)
    if roll <= chances:
        if og_base != 2:
            st.session_state.bases[og_base + 1] = st.session_state.bases[og_base]
            st.session_state.bases[og_base] = None
        else:
            st.session_state.bases[og_base] = None
            game.score_run(1)
        st.write("Safe!")
        return 
    else:
        st.session_state.bases[og_base] = None
        st.write("Caught Stealing!")
        game.got_out()
        return
    
def game_over():
    game.game_over()
    # st.write(f"Final Score: {st.session_state.vis_score}:{st.session_state.home_score}")

st.title("Baseball Card Game Simulator")
st.write("Here is a place to simulate baseball card games online and track statistics.")

show_lineups = st.checkbox("Show Lineups", value=True)
if show_lineups:
    #batters and pitchers for visiting team
    st.write("Lineup One:")
    desired_order = ["name", "position", "batter_batting_avg", "batter_onbase", "batter_slugging", "batter_triples", "batter_homers", "batter_stolenbases"]

    if "lineup_one_df" not in st.session_state:
        st.session_state.lineup_one_df = pd.DataFrame([vars(player) for player in game.lineup_one[:9]])[desired_order]

    st.session_state.lineup_one_df = dynamic_input_data_editor(
        st.session_state.lineup_one_df,
        key="batter1_editor",
        hide_index=True,
        column_config={
            "batter_batting_avg": st.column_config.NumberColumn("AVG", min_value=0.000, max_value=1.000, step=0.001, format="%.3f"),
            "batter_onbase": st.column_config.NumberColumn("OBP", min_value=0.000, max_value=1.000, step=0.001, format="%.3f"),
            "batter_slugging": st.column_config.NumberColumn("SLG", min_value=0.000, max_value=4.000, step=0.001, format="%.3f"),
            "batter_homers": st.column_config.NumberColumn("HR", min_value=0, max_value=100, step=1),
            "batter_stolenbases": st.column_config.NumberColumn("SB", min_value=0, max_value=200, step=1),
            "batter_triples": st.column_config.NumberColumn("3B", min_value=0, max_value=100, step=1)
        }
    )

    st.session_state.lineup_one = []
    for _, row in st.session_state.lineup_one_df.iterrows():
        st.session_state.lineup_one.append(player_creation.batter(
            float(row["batter_batting_avg"]),
            float(row["batter_slugging"]),
            int(row["batter_stolenbases"]),
            int(row["batter_homers"]),
            float(row["batter_onbase"]),
            5,
            int(row["batter_triples"]),
            row["position"],
            row["name"]
        ))
    game.batter_up_vis[:9] = st.session_state.lineup_one

    # Make the pitcher
    desired_order_pitchers = ["name", "pitcher_games_pitched", "pitcher_innings", "pitcher_era", "pitcher_whip", "pitcher_strikeouts"]
    if "pitcher1_df" not in st.session_state:
        st.session_state.pitcher1_df = pd.DataFrame([vars(game.lineup_one[9])])[desired_order_pitchers]
    edited_pitcher1_df = dynamic_input_data_editor(
        st.session_state.pitcher1_df, 
        key = "pitcher1_editor",
        column_config={
            "pitcher_games_pitched": st.column_config.NumberColumn("Games Pitched", min_value = 1, max_value = 200, step = 1),
            "pitcher_era": st.column_config.NumberColumn("ERA", min_value = 0.00, max_value = 100.00, step = 0.01),
            "pitcher_whip": st.column_config.NumberColumn("WHIP",min_value = 0.00,max_value = 3.00,step = 0.01)
        })
    st.session_state.pitcher1_df = edited_pitcher1_df

    row = edited_pitcher1_df.iloc[0]
    st.session_state.vis_pitcher = player_creation.pitcher(
        float(row["pitcher_era"]),
        float(row["pitcher_whip"]),
        int(row["pitcher_strikeouts"]),
        int(row["pitcher_games_pitched"]),
        float(row["pitcher_innings"]),
        row["name"]
    )
    game.batter_up_vis[9] = st.session_state.vis_pitcher

    #home team
    if "lineup_two_df" not in st.session_state:
        st.session_state.lineup_two_df = pd.DataFrame([vars(player) for player in game.lineup_two[:9]])[desired_order]

    st.session_state.edited_batters2_df = dynamic_input_data_editor(
        st.session_state.lineup_two_df,
        key = "batter2_editor",
        hide_index = True,
        column_config = {
            "batter_batting_avg": st.column_config.NumberColumn("AVG", min_value = 0.000, max_value = 1.000, step = 0.001),
            "batter_onbase": st.column_config.NumberColumn("OBP", min_value = 0.000, max_value = 1.000, step = 0.001),
            "batter_slugging": st.column_config.NumberColumn("SLG", min_value = 0.000, max_value = 4.000, step = 0.001),
            "batter_homers": st.column_config.NumberColumn("HR", min_value = 0, max_value = 100, step = 1),
            "batter_stolenbases": st.column_config.NumberColumn("SB", min_value = 0, max_value = 200, step = 1),
            "batter_triples": st.column_config.NumberColumn("3B", min_value = 0, max_value = 100, step = 1)
        }
    )
    st.session_state.lineup_two_df = st.session_state.edited_batters2_df

    st.session_state.lineup_two = []
    for _, row in st.session_state.edited_batters2_df.iterrows():
        st.session_state.lineup_two.append(player_creation.batter(
            float(row["batter_batting_avg"]),
            float(row["batter_slugging"]),
            int(row["batter_stolenbases"]),
            int(row["batter_homers"]),
            float(row["batter_onbase"]),
            5,
            int(row["batter_triples"]),
            row["position"],
            row["name"]
        ))
    game.batter_up_home[:9] = st.session_state.lineup_two
    #home team pitchers
    if "pitcher2_df" not in st.session_state:
        st.session_state.pitcher2_df = pd.DataFrame([vars(game.lineup_two[9])])[desired_order_pitchers]

    edited_pitcher2_df = dynamic_input_data_editor(
        st.session_state.pitcher2_df,
        key="pitcher2_editor",
        column_config={
            "pitcher_games_pitched": st.column_config.NumberColumn("Games Pitched", min_value=1, max_value=200, step=1),
            "pitcher_era": st.column_config.NumberColumn("ERA", min_value=0.00, max_value=100.00, step=0.01),
            "pitcher_whip": st.column_config.NumberColumn("WHIP", min_value=0.00, max_value=3.00, step=0.01),
        }
    )

    st.session_state.pitcher2_df = edited_pitcher2_df

    row2 = edited_pitcher2_df.iloc[0]
    st.session_state.home_pitcher = player_creation.pitcher(
        float(row2["pitcher_era"]),
        float(row2["pitcher_whip"]),
        int(row2["pitcher_strikeouts"]),
        int(row2["pitcher_games_pitched"]),
        float(row2["pitcher_innings"]),
        row2["name"]
    )
    game.batter_up_home[9] = st.session_state.home_pitcher


col1, col2, col3, col4 = st.columns(4)
steal_which_base = 0
can_steal_a_base = False
chances = 0
hit_value = 0

with col1:
    if st.button("Play Next At-Bat "): 
        result, hit_value = game.atbat()
        can_steal_a_base = False
        # Update session state if needed, e.g.:
        st.session_state.outs = game.outs
        st.session_state.inning = game.inning
        st.session_state.vis_score = game.vis_score
        st.session_state.home_score = game.home_score
        st.session_state.bases = game.bases
        st.write(f"Result: {result}")
        # Check for if you can steal
        steal_which_base, can_steal_a_base = game.can_steal(st.session_state.bases, st.session_state.outs, st.session_state.vis_score, st.session_state.home_score)
        st.session_state.can_steal_a_base = can_steal_a_base
        st.session_state.steal_which_base = steal_which_base
        if can_steal_a_base:
            st.session_state.chances = min(65 - random.randint(0, 40) - ((steal_which_base - 1) * 20) + int(math.sqrt(st.session_state.bases[steal_which_base - 1].batter_stolenbases) * 5), 90)
            st.write(f"Steal Base {steal_which_base + 1}? {st.session_state.chances}% chance of success.")
        else:
            st.session_state.chances = 0

with col2:
    if st.button("Reset Game"): #start the game over
        restart_game()
with col3:
    if st.button("Steal"):
        if st.session_state.get("can_steal_a_base", False):
            steal(st.session_state.get("steal_which_base", 1) - 1)
            hit_value = 0
with col4:  
    st.session_state.bases = game.bases
    if "extra_chances" not in st.session_state:
        st.session_state.extra_chances = 0
    if st.session_state.bases[2] and (st.session_state.bases[1] or st.session_state.bases[0]) and hit_value > 0:
        st.session_state.extra_chances = min(95, 60 - random.randint(0, 50) + st.session_state.bases[2].speed * 5)
        if st.session_state.outs == 2:
            st.session_state.extra_chances = min(95, st.session_state.extra_chances + 15)
        st.write(f"Try for home?\n{st.session_state.extra_chances}% chance of success")
    if st.session_state.bases[1] and st.session_state.bases[0] and not st.session_state.bases[2] and hit_value > 0:
        st.session_state.extra_chances = min(95, 60 - random.randint(0, 50) + st.session_state.bases[1].speed * 5)
        if st.session_state.outs == 2:
            st.session_state.extra_chances = min(95, st.session_state.extra_chances + 15)
        st.write(f"Try for third?\n{st.session_state.extra_chances}% chance of success")
    if st.button("Extra Base"):
        advancing_result = game.st_advance_runners(hit_value, st.session_state.extra_chances)
        if advancing_result:   
            st.write(advancing_result)
        st.session_state.bases = game.bases
        st.session_state.outs = game.outs
        st.session_state.vis_score = game.vis_score
        st.session_state.home_score = game.home_score

show_bases = st.checkbox("Show Bases", value=True)
if show_bases:
    base_graphic(game.bases)

# Display scores and outs
top_bottom = ["Top", "Bottom"]
st.session_state.batter_up_index = game.batter_up_index
st.write(f"Inning: {top_bottom[st.session_state.batter_up_index]} of {st.session_state.inning}")
st.write(f"Outs: {st.session_state.outs}")
game_over()
st.write(f"Score: Visitors {st.session_state.vis_score} - Home {st.session_state.home_score}")