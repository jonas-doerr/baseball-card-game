# Baseball Card Game Simulator
This is a python version of a tabletop game I previously designed, in which two teams create a lineup of baseball cards to face off.

Play the game on the website: [Here!](https://baseball-card-simulator.streamlit.app/)

As it is a working game, with all bugs worked out (that I know of), I have decided to stop here and move on to a new project in order to learn a new skillset. It was a great exercise for developing my fundamental coding skills, as this project used loops, classes, functions, and plenty of other basic python concepts. But the part that got really complicated was when I tried to develop it into a website, since a lot of the code ran differently once I tried to put it into the streamlit framework. I had to rewrite several functions and variables, particularly because streamlit runs through the entire script every time an action is taken and resets all variables not stored in st.session_state. I think the streamlit library is not designed for running games, so I spent a lot of time debugging what were simple issues when I just ran the game in terminal. But, in the end, it is a working simulator!

## Goals
- Create the ability to input lineups with statistics
- Save previously inputted players for future games
- Create gameplay mechanics through random number generators and player statistics [DONE]
- Record player statistics and include a leaderboard
- Develop into an app or website using the streamlit package [DONE]

## Skills Learned
- how to use classes, global variables, list manipulation, and a lot more nit-picky stuff
- basic development with streamlit
- using basic math formulas to create a sports simulation
- how to not smack my head on a wall when I keep getting bugs because I rush through streamlit without really knowing how it works
