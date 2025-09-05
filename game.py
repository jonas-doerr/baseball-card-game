import random
import player_creation
import math

lineup_one = player_creation.sample_lineup_one
lineup_two = player_creation.sample_lineup_two
batter_up_vis_index = 0
batter_up_home_index = 0
batter_up_vis = lineup_one
batter_up_home = lineup_two
batter_up = [batter_up_vis[batter_up_vis_index], batter_up_home[batter_up_home_index]]
batter_up_index = 0
inning = 1
vis_score = 0
home_score = 0
outs = 0
quit_game = False
hit_types = ['single', 'double', 'triple', 'home run']
bases = [None, None, None] #first, second, third

def atbat():
    # Determine which team is batting
    global batter_up_vis_index, batter_up_home_index, batter_up
    batter_up = [batter_up_vis[batter_up_vis_index], batter_up_home[batter_up_home_index]]
    current_batter = batter_up[batter_up_index]
    if batter_up_index == 0:
        # Visitors batting, home pitcher
        opposing_pitcher = batter_up_home[9]  # Adjust as needed for actual pitcher
    else:
        # Home batting, visitor pitcher
        opposing_pitcher = batter_up_vis[9]  # Adjust as needed for actual pitcher

    # Calculate hit probability (simple example: higher avg, lower ERA = more likely hit)
    # Normalize ERA to a 0-1 scale (lower ERA = better pitcher)
    # pitcher_effect = max(0.1, min(1.0, 5.0 - opposing_pitcher.pitcher_era) / 5.0)
    pitcher_hit_effect = max(min((opposing_pitcher.pitcher_whip - 1.29) * 0.2, 0.2), -0.7)
    hit_chance = current_batter.batter_batting_avg + pitcher_hit_effect
    walk_chance = current_batter.batter_onbase + pitcher_hit_effect

    # Roll for hit
    roll = random.random()
    # print(roll)
    if roll < hit_chance:
        print("Hit!")
        hit_value = slugged(roll, current_batter, opposing_pitcher)
        print(hit_types[hit_value - 1])
        advance_runners(hit_value, current_batter) #move runners along and add new
        runners_on_base = [runner.name if runner else "None" for runner in bases]
        print(runners_on_base)
        print(f"{vis_score} : {home_score}, {outs} out(s)")
        cycle_hitters()
        return True
    elif roll < walk_chance:
        print("Walk.")
        advance_runners(1, current_batter, walk = True)
        runners_on_base = [runner.name if runner else "None" for runner in bases]
        print(runners_on_base)
        print(f"{vis_score} : {home_score}, {outs} out(s)")
        cycle_hitters()
        return True
    else:
        print("Out!")
        cycle_hitters()
        got_out()
        print(f"{vis_score} : {home_score}, {outs} out(s)")
        inning_over()
        return False

def cycle_hitters():
    global batter_up_vis_index, batter_up_home_index
    if batter_up_index == 0:
        if batter_up_vis_index >= 8:
            batter_up_vis_index = 0
        else:
            batter_up_vis_index += 1
    if batter_up_index == 1:
        if batter_up_home_index >= 8:
            batter_up_home_index = 0
        else:
            batter_up_home_index += 1


def can_steal(runner_list, outs, score_one, score_two):
    #allows the runner to steal if SB is high enough
    condition_of_steal = 0 # 0: no steal, 1:steal 2nd, 2: steal 3rd, 3: steal home
    #4: steal 2nd and 3rd #5 steal 2nd or home
    stealability = False
    if runner_list[0] and not (runner_list[1]):
        condition_of_steal = 1
    elif runner_list[1] and not runner_list[2]:
        condition_of_steal = 2
    elif runner_list[2]:
        condition_of_steal = 3
    else:
        return condition_of_steal, stealability
    situation = runner_list[condition_of_steal - 1].speed - abs(score_one - score_two) + outs - condition_of_steal
    if situation > 0:
        stealability = True
    return condition_of_steal, stealability

def steal(og_base): #insert INDEX of base (0-2) being stolen from
    #determines whether a stolen base is successful
    global bases
    chances = min(65 - random.randint(0, 40) - (og_base * 20) + int(math.sqrt(bases[og_base].batter_stolenbases) * 5), 90)
    steal_input = input(f"Steal Base {og_base + 2}? {chances}% chance of success. y/n")
    if steal_input.lower() == "y":
        roll = random.randint(0, 100)
        if roll <= chances:
            if og_base != 2:
                bases[og_base + 1] = bases[og_base]
                bases[og_base] = None
            else:
                bases[og_base] = None
                score_run(1)
            bases_names = [guy.name if guy else "None" for guy in bases]
            print("Safe!")
            print(bases_names)
            return bases_names
        else:
            bases[og_base] = None
            print("Caught Stealing!")
            got_out()
            return
    else:
        return

def inning_over():
    global outs, batter_up_index, inning, bases
    if outs >= 3:
        batter_up_index += 1
        if batter_up_index >= 2:
            batter_up_index = 0
            inning += 1
        outs = 0
        bases = [None, None, None]
        if batter_up_index == 0:
            print(f"\nTop of {inning}")
        else:
            print(f"\nBottom of {inning}")
    return

def got_out():
    global outs 
    outs += 1
    inning_over()
    return True

def game_over():
    global inning, home_score, vis_score
    if (inning > 9 and vis_score > home_score) or (inning >= 9 and batter_up_index == 1 and home_score > vis_score):
        print(f'Final score:\nVisitors {vis_score}\nHome {home_score}')
        inning = 1
        home_score = 0
        vis_score = 0
        return False
    else:
        return True

def slugged(random_roll, batter, pitcher):
    #if there's a hit, this function determines whether it's for extra bases
    #check for pitcher effect
    pitcher_slug_effect = max(min((pitcher.pitcher_era - 4.08) * 0.2, 0.2), -0.7)
    slug_chance = batter.batter_slugging - batter.batter_batting_avg - pitcher_slug_effect

    #check if roll was low enough for a slug
    if random_roll <= slug_chance:
        #check for double, triple, or home run
        slug_roll = random.randint(0, 50)
        # print(slug_roll)
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

def score_run(runs):
    global vis_score, home_score
    if batter_up_index == 0:
        vis_score += runs
    else:
        home_score += runs
    return

def advance_runners(hit_value, batter, walk = False):
    global bases, vis_score, home_score, quit_game
    if walk is False:
        for i in reversed(range(3)): #easier to go 3rd to 1st
            runner = bases[i]
            if runner is not None:
                new_base = i + hit_value
                if new_base >= 3:
                    #Runner scores
                    score_run(1)
                else:
                    bases[new_base] = runner
            bases[i] = None
    else:
        advancing_walk_runners = 0
        for i in range(3):
            if bases[i] is None:
                break
            advancing_walk_runners += 1
        for i in reversed(range(advancing_walk_runners)):
            if i < 2:  
                bases[i + 1] = bases[i]
                bases[i] = None
            else:
                score_run(1)

    if walk is False and hit_value <= 2: #advancing the baserunner
        if bases[2]:
            chances = min(95, 60 - random.randint(0, 50) + bases[2].speed * 5)
            if outs == 2:
                chances = min(95, chances + 15)
            advancing = input(f"Try for home? y/n/quit\n{chances}% chance of success\n")
            if advancing == 'y':
                roll = random.randint(1, 100)
                if roll <= chances:
                    score_run(1)
                    bases[2] = None
                    print("Safe at home!")
                else:
                    got_out()
                    print("Out at home!")
            if advancing == 'quit':
                quit_game = True
        if bases[1] and not bases[2]:
            chances = min(95, 60 - random.randint(0, 50) + bases[1].speed * 5)
            if outs == 2:
                chances = min(95, chances + 15)
            advancing = input(f"Try for third? y/n/quit\n{chances}% chance of success\n")
            if advancing == 'y':
                roll = random.randint(1, 100)
                if roll <= chances:
                    bases[2] = bases[1]
                    bases[1] = None
                    print("Safe at third!")
                else:
                    got_out()
                    print("Out at third!")
            if advancing == 'quit': 
                quit_game = True


    if hit_value < 4: #batter goes on base if not homer
        bases[hit_value - 1] = batter
    else:
        score_run(1)

def playing_game():
    while game_over() and not quit_game:
    # while batter_up_index == 0:
        atbat()
        steal_which_base, can_steal_a_base = can_steal(bases, outs, vis_score, home_score)
        if not can_steal_a_base:
            continue_game = input("Press Enter to continue, q to quit")
            if continue_game.lower() == 'q':
                break
        else:
            steal(steal_which_base - 1)


# atbat()
playing_game()