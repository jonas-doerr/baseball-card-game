import streamlit as st
import game
import pandas as pd
import random
import math

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

st.title("Baseball Card Game Simulator")
st.write("Here is a place to simulate baseball card games online and track statistics.")

show_lineups = st.checkbox("Show Lineups", value=True)
if show_lineups:
    #batters and pitchers for visiting team
    desired_order = ["name", "position", "batter_batting_avg", "batter_onbase", "batter_slugging", "batter_triples", "batter_homers", "batter_stolenbases"]
    batters_df = pd.DataFrame([vars(player) for player in game.lineup_one[:9]])[desired_order]
    batters_df["batter_batting_avg"] = batters_df["batter_batting_avg"].apply(lambda x: f"{x:.3f}")
    batters_df["batter_onbase"] = batters_df["batter_onbase"].apply(lambda x: f"{x:.3f}")
    batters_df["batter_slugging"] = batters_df["batter_slugging"].apply(lambda x: f"{x:.3f}")
    st.write("Lineup One:")
    st.write(batters_df)
    desired_order_pitchers = ["name", "pitcher_games_pitched", "pitcher_innings", "pitcher_era", "pitcher_whip", "pitcher_strikeouts"]
    pitcher1_df = pd.DataFrame([vars(game.lineup_one[9])])[desired_order_pitchers]
    pitcher1_df["pitcher_era"] = pitcher1_df["pitcher_era"].apply(lambda x: f"{x:.2f}")
    pitcher1_df["pitcher_whip"] = pitcher1_df["pitcher_whip"].apply(lambda x: f"{x:.2f}")
    st.write(pitcher1_df)

    #home team
    st.write("Lineup Two:")
    # st.write(pd.DataFrame([vars(player) for player in game.lineup_two[:9]]))
    # st.write(pd.DataFrame([vars(game.lineup_two[9])]))
    batters2_df = pd.DataFrame([vars(player) for player in game.lineup_two[:9]])[desired_order]
    batters2_df["batter_batting_avg"] = batters2_df["batter_batting_avg"].apply(lambda x: f"{x:.3f}")
    batters2_df["batter_onbase"] = batters2_df["batter_onbase"].apply(lambda x: f"{x:.3f}")
    batters2_df["batter_slugging"] = batters2_df["batter_slugging"].apply(lambda x: f"{x:.3f}")
    st.write(batters2_df)
    pitcher2_df = pd.DataFrame([vars(game.lineup_two[9])])[desired_order_pitchers]
    pitcher2_df["pitcher_era"] = pitcher2_df["pitcher_era"].apply(lambda x: f"{x:.2f}")
    pitcher2_df["pitcher_whip"] = pitcher2_df["pitcher_whip"].apply(lambda x: f"{x:.2f}")
    st.write(pitcher2_df)


col1, col2, col3, col4 = st.columns(4)
steal_which_base = 0
can_steal_a_base = False
chances = 0

with col1:
    if st.button("Play Next At-Bat "): 
        result = game.atbat()
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
    if st.button("Reset Game"):
        # your code here
        restart_game()
with col3:
    if st.button("Steal"):
        if st.session_state.get("can_steal_a_base", False):
            steal(st.session_state.get("steal_which_base", 1) - 1)
with col4:
    if st.button("Extra Base"):
        pass

show_bases = st.checkbox("Show Bases", value=True)
if show_bases:
    base_graphic(game.bases)

# Display scores and outs
top_bottom = ["Top", "Bottom"]
st.session_state.batter_up_index = game.batter_up_index
st.write(f"Inning: {top_bottom[st.session_state.batter_up_index]} of {st.session_state.inning}")
st.write(f"Outs: {st.session_state.outs}")
st.write(f"Score: Visitors {st.session_state.vis_score} - Home {st.session_state.home_score}")