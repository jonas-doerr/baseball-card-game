import streamlit as st
import game
import pandas as pd

# Initialize session state for game variables
if "outs" not in st.session_state:
    st.session_state.outs = game.outs
if "inning" not in st.session_state:
    st.session_state.inning = game.inning
if "vis_score" not in st.session_state:
    st.session_state.vis_score = game.vis_score
if "home_score" not in st.session_state:
    st.session_state.home_score = game.home_score

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

show_bases = st.checkbox("Show Bases", value=True)
if show_bases:
    base_graphic(game.bases)

if st.button("Play Next At-Bat"):
    result = game.atbat()
    # Update session state if needed, e.g.:
    st.session_state.outs = game.outs
    st.session_state.inning = game.inning
    st.session_state.vis_score = game.vis_score
    st.session_state.home_score = game.home_score
    st.write(f"Result: {result}")

# Display scores and outs
st.write(f"Inning: {st.session_state.inning}")
st.write(f"Outs: {st.session_state.outs}")
st.write(f"Score: Visitors {st.session_state.vis_score} - Home {st.session_state.home_score}")