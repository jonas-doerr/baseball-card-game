class batter():
    batter_batting_avg = 0.249
    batter_slugging = 0.414
    batter_stolenbases = 0
    batter_homers = 0
    batter_onbase = 0.315
    batter_doubles = 0
    batter_triples = 0
    statistics = {'AVG': 0.000, 'OBP': 0.000, 'SLG': 0.000, 'HR': 0, 'H': 0, 
                    '2B' : 0, '3B': 0, 'K': 0, 'RBI': 0, 'R': 0}

    def __init__(self, avg, slug, sbs, homers, onbase, doubles, triples, pos, name):
        self.batter_batting_avg = avg
        self.batter_slugging = slug
        self.batter_stolenbases = sbs
        self.batter_homers = homers
        self.batter_onbase = onbase
        self.batter_doubles = doubles
        self.batter_triples = triples
        self.position = pos
        self.name = name
        self.speed = min(int(self.batter_stolenbases / 3), 10)

class pitcher():
    pitcher_era = 4.08
    pitcher_whip = 1.29
    pitcher_games_pitched = 0
    pitcher_strikeouts = 0
    pitcher_innings = 0

    def __init__(self, era, whip, strikeouts, games_pitched, innings, name):
        self.pitcher_era = era
        self.pitcher_whip = whip
        self.pitcher_games_pitched = strikeouts
        self.pitcher_strikeouts = games_pitched
        self.pitcher_innings = innings
        self.name = name

sample_lineup_one = [batter(.250, .300, 0, 30, .400, 5, 6, 'CF', "Jackson Chourio"), 
                     batter(.250, .300, 0, 30, .400, 5, 6, 'LF', "Isaac Collins"), 
                     batter(.250, .300, 0, 30, .400, 5, 6, 'RF', "Sal Frelick"), 
                     batter(.250, .300, 0, 30, .400, 5, 6, '1B', "Andrew Vaughn"), 
                     batter(.250, .300, 0, 30, .400, 5, 6, '2B', "Brice Turang"),
                     batter(.250, .300, 0, 30, .400, 5, 6, '3B', "Caleb Durbin"),
                     batter(.250, .300, 0, 30, .400, 5, 6, 'C', "William Contreras"),
                     batter(.250, .300, 0, 30, .400, 5, 6, 'SS', "Joey Ortiz"),
                     batter(.250, .300, 0, 30, .400, 5, 6, 'DH', "Christian Yelich"),
                     pitcher(3.50, 1.60, 80, 4, 16, "Freddy Peralta")]

sample_lineup_two = [batter(.250, .300, 0, 30, .400, 5, 6, 'CF', "Willie Mays"), 
                     batter(.250, .300, 0, 30, .400, 5, 6, 'LF', "Joe Dimaggio"), 
                     batter(.250, .300, 0, 30, .400, 5, 6, 'RF', "Babe Ruth"), 
                     batter(.250, .300, 0, 30, .400, 5, 6, '1B', "Lou Gehrig"), 
                     batter(.250, .300, 0, 30, .400, 5, 6, '2B', "Rickie Weeks"),
                     batter(.250, .300, 0, 30, .400, 5, 6, '3B', "Robinson Cano"),
                     batter(.250, .300, 0, 30, .400, 5, 6, 'C', "Mike Piazza"),
                     batter(.250, .300, 0, 30, .400, 5, 6, 'SS', "Derek Jeter"),
                     batter(.250, .300, 0, 30, .400, 5, 6, 'DH', "Jim Edmonds"),
                     pitcher(3.50, 1.60, 80, 4, 16, "Mariano Rivera")]