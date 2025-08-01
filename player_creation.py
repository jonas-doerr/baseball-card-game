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

    def __init__(self, avg, slug, sbs, homers, onbase, doubles, triples, pos):
        self.batter_batting_avg = avg
        self.batter_slugging = slug
        self.batter_stolenbases = sbs
        self.batter_homers = homers
        self.batter_onbase = onbase
        self.batter_doubles = doubles
        self.batter_triples = triples
        self.position = pos

class pitcher():
    pitcher_era = 4.08
    pitcher_whip = 1.29
    pitcher_games_pitched = 0
    pitcher_strikeouts = 0
    pitcher_innings = 0

    def __init__(self, era, whip, strikeouts, games_pitched, innings):
        self.pitcher_era = era
        self.pitcher_whip = whip
        self.pitcher_games_pitched = strikeouts
        self.pitcher_strikeouts = games_pitched
        self.pitcher_innings = innings

sample_lineup_one = [batter(.250, .300, 0, 30, .400, 5, 6, 'CF'), 
                     batter(.250, .300, 0, 30, .400, 5, 6, 'LF'), 
                     batter(.250, .300, 0, 30, .400, 5, 6, 'RF'), 
                     batter(.250, .300, 0, 30, .400, 5, 6, '1B'), 
                     batter(.250, .300, 0, 30, .400, 5, 6, '2B'),
                     batter(.250, .300, 0, 30, .400, 5, 6, '3B'),
                     batter(.250, .300, 0, 30, .400, 5, 6, 'C'),
                     batter(.250, .300, 0, 30, .400, 5, 6, 'SS'),
                     batter(.250, .300, 0, 30, .400, 5, 6, 'DH'),
                     pitcher(3.50, 1.60, 80, 4, 16)]

sample_lineup_two = [batter(.250, .300, 0, 30, .400, 5, 6, 'CF'), 
                     batter(.250, .300, 0, 30, .400, 5, 6, 'LF'), 
                     batter(.250, .300, 0, 30, .400, 5, 6, 'RF'), 
                     batter(.250, .300, 0, 30, .400, 5, 6, '1B'), 
                     batter(.250, .300, 0, 30, .400, 5, 6, '2B'),
                     batter(.250, .300, 0, 30, .400, 5, 6, '3B'),
                     batter(.250, .300, 0, 30, .400, 5, 6, 'C'),
                     batter(.250, .300, 0, 30, .400, 5, 6, 'SS'),
                     batter(.250, .300, 0, 30, .400, 5, 6, 'DH'),
                     pitcher(3.50, 1.60, 80, 4, 16)]