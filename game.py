import random
import player_creation

lineup_one = player_creation.sample_lineup_one
lineup_two = player_creation.sample_lineup_two
batter_up_vis = lineup_one[0]
batter_up_home = lineup_two[0]
batter_up = [batter_up_vis, batter_up_home]
batter_up_index = 0
inning = 1
vis_score = 0
home_score = 0
outs = 0
hit_types = ['single', 'double', 'triple', 'home run']

def atbat():
    # Determine which team is batting
    current_batter = batter_up[batter_up_index]
    if batter_up_index == 0:
        # Visitors batting, home pitcher
        opposing_pitcher = lineup_two[9]  # Adjust as needed for actual pitcher
    else:
        # Home batting, visitor pitcher
        opposing_pitcher = lineup_one[9]  # Adjust as needed for actual pitcher

    # Calculate hit probability (simple example: higher avg, lower ERA = more likely hit)
    # Normalize ERA to a 0-1 scale (lower ERA = better pitcher)
    # pitcher_effect = max(0.1, min(1.0, 5.0 - opposing_pitcher.pitcher_era) / 5.0)
    pitcher_hit_effect = max(min((opposing_pitcher.pitcher_whip - 1.29) * 0.2, 0.2), -0.7)
    hit_chance = current_batter.batter_batting_avg + pitcher_hit_effect

    # Roll for hit
    roll = random.random()
    print(roll)
    if roll < hit_chance:
        print("Hit!")
        hit_value = slugged(roll, current_batter, opposing_pitcher)
        print(hit_types[hit_value - 1])

        return True
    else:
        print("Out!")
        inning_over()
        return False

def can_steal():
    #allows the runner to steal if SB is high enough
    pass

def steal():
    #determines whether a stolen base is successful
    pass

def inning_over():
    global outs
    if outs >= 3:
        batter_up_index += 1
        if batter_up_index >= 2:
            batter_up_index = 0
        outs = 0
        inning += 1
    return

def got_out():
    global outs 
    outs += 1
    return True

def game_over():
    if (inning > 9 and vis_score != home_score) or (inning >= 9 and batter_up_index == 1 and home_score > vis_score):
        print(f'Final score:\nVisitors {vis_score}\nHome {home_score}')
        inning = 1
        home_score = 0
        vis_score = 0
    return

def slugged(random_roll, batter, pitcher):
    #if there's a hit, this function determines whether it's for extra bases
    #check for pitcher effect
    pitcher_slug_effect = max(min((pitcher.pitcher_era - 4.08) * 0.2, 0.2), -0.7)
    slug_chance = batter.batter_slugging - batter.batter_batting_avg - pitcher_slug_effect

    #check if roll was low enough for a slug
    if random_roll <= slug_chance:
        #check for double, triple, or home run
        slug_roll = random.randint(0, 50)
        print(slug_roll)
        if slug_roll > min(10, max(batter.batter_triples, 1)) + min(25, max(batter.batter_homers / 2, 1)):
            return 2
        elif slug_roll > min(25, max(batter.batter_homers / 2, 1)):
            return 3
        return 4
    else:
        return 1

def struck_out():
    #if batter is out, this function determines whether it's a strikeout
    pass


atbat()