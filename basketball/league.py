import random
import time

# my imports
from data import *

class Player:
    def __init__(self, name, offense, defense, star):
        self.name = name
        self.defense = defense
        self.offense = offense
        self.star = star

    def __str__(self):
        return self.name

class Team:
    def __init__(self):
        self.captain = None
        self.players = []

    def __str__(self):
        return f"Team {self.captain.name}"

    def set_captain(self, player):
        assert player in self.players, "To set as captain, player must be in the team."
        self.captain = player

    def add_player(self, player):
        assert len(self.players) < 5, "This team is full."
        self.players.append(player)

    def remove_player(self, player):
        assert player in self.players, "This player is not in the team."
        assert player != self.captain, "You have to transfer the captainhood first."
        self.players.remove(player)

class Match:
    def __init__(self, home, away, halves=2, tiebraker=False):
        # Game setup
        self.home = home
        self.away = away
        self.halves = halves
        self.tiebraker = tiebraker

        # Roster setup
        self.home_roster = home.players.copy()
        self.away_roster = away.players.copy()

        # Endgame values
        self.home_score = 0
        self.away_score = 0
        self.commentary = []

        # Play the game
        self.play()

    def play(self):
        # Print pre-game information
        self.commentary.append(f"Matchday: {self.home} vs. {self.away}")
        self.commentary.append("--------------------")

        # Play the first half
        self.play_first_half()
        self.commentary.append("--------------------")

        # If wanted, play the second half
        if self.halves == 2:
            self.play_second_half()
            self.commentary.append("--------------------")

        # If wanted and necessary, play tiebrakers
        if self.tiebraker and self.home_score == self.away_score:
            self.play_tiebraker()
            self.commentary.append("--------------------")

        # Print post-game information
        if self.home_score > self.away_score:
            self.commentary.append(f"{self.home} wins! Final score is {self.home_score} - {self.away_score}")
        elif self.home_score < self.away_score:
            self.commentary.append(f"{self.away} wins! Final score is {self.home_score} - {self.away_score}")
        else:
            self.commentary.append(f"It's a draw! Final score is {self.home_score} - {self.away_score}")
        self.commentary.append("--------------------")

    def play_first_half(self):
        # Roster shuffle
        random.shuffle(self.home_roster)
        random.shuffle(self.away_roster)

        # Shots and defenses
        self.shoot(0)
        self.defend(1)
        self.shoot(2)
        self.defend(3)
        self.shoot(4)

    def play_second_half(self):
        # Roster shuffle
        random.shuffle(self.home_roster)
        random.shuffle(self.away_roster)

        # Shots and defenses
        self.defend(0)
        self.shoot(1)
        self.defend(2)
        self.shoot(3)
        self.defend(4)

    def play_tiebraker(self):
        attempt = 0
        # Keep playing until one team gets ahead
        while attempt % 2 or self.home_score == self.away_score:
            # Roster shuffle every 5 attempts
            if attempt % 5 == 0:
                random.shuffle(self.home_roster)
                random.shuffle(self.away_roster)

            # Shot/defense
            if not attempt % 2: shot(attempt % 5)
            else: defend(attempt % 5)

    def shoot(self, x):
        if self.home_roster[x].offense > self.away_roster[x].defense:
            self.home_score += 1
            self.commentary.append(f"{self.home_roster[x]} scores over {self.away_roster[x]}, the score is {self.home_score} - {self.away_score}")
        else:
            self.commentary.append(f"{self.home_roster[x]} is blocked by {self.away_roster[x]}, the score is {self.home_score} - {self.away_score}")

    def defend(self, x):
        if self.home_roster[x].defense < self.away_roster[x].offense:
            self.away_score += 1
            self.commentary.append(f"{self.home_roster[x]} is scored over by {self.away_roster[x]}, the score is {self.home_score} - {self.away_score}")
        else:
            self.commentary.append(f"{self.home_roster[x]} blocks {self.away_roster[x]}, the score is {self.home_score} - {self.away_score}")

    def result(self):
        if self.home_score > self.away_score:
            return 1
        elif self.home_score < self.away_score:
            return 2
        else:
            return 0

    def commentate(self, sleep=1):
        for comment in self.commentary:
            print(comment)
            time.sleep(sleep)

class RoundRobin:
    def __init__(self):
        self.teams = []
        self.data = {}

    def add_team(self, team):
        self.teams.append(team)
        self.data[team] = {'w': 0, "d": 0, "l": 0, "ps": 0, "pc": 0, "p": 0}

    def set_rule(self, rounds=2, halves=1, tiebraker=False):
        self.rounds = rounds
        self.halves = halves
        self.tiebraker = tiebraker

    def generate_fixture(self):
         # prepare teams
        teams = self.teams.copy()
        random.shuffle(teams)
        if len(teams) % 2 == 1:
            teams.append("dummy")
        n = len(teams)

        # create fixture
        rnd1 = []
        for wk in range(n-1):
            week = []

            if teams[n-1] != "dummy":
                week.append(Match(teams[wk], teams[n-1], self.halves, self.tiebraker))
            order = teams[wk+1 : n-1] + teams[:wk]

            for i in range(n//2 - 1):
                week.append(Match(order[i], order[-i-1], self.halves, self.tiebraker))
            rnd1.append(week)

        # more rounds
        rnd2 = []
        if self.rounds == 2:
            for week in rnd1:
                rnd2.append([Match(game.away, game.home, self.halves, self.tiebraker) for game in week])

        self.fixture = rnd1 + rnd2
        self.position = 0, 0

    def reset(self):
        for team in self.teams:
            for key in self.data[team]:
                self.data[team][key] = 0

        self.position = 0, 0

    def next(self):
        # Get the game
        week, game = self.position
        assert week < len(self.fixture) and game < len(self.fixture[week]), "There is no such game."
        match = self.fixture[week][game]

        # Add the result
        if match.result() == 1:
            self.data[match.home]['w'] += 1
            self.data[match.away]['l'] += 1
        elif match.result() == 0:
            self.data[match.home]['d'] += 1
            self.data[match.away]['d'] += 1
        elif match.result() == 2:
            self.data[match.home]['l'] += 1
            self.data[match.away]['w'] += 1

        # Add the scores
        self.data[match.home]["ps"] += match.home_score
        self.data[match.home]["pc"] += match.away_score
        self.data[match.away]["ps"] += match.away_score
        self.data[match.away]["pc"] += match.home_score

        # Calculate points
        self.data[match.home]["p"] = self.data[match.home]["w"] * 2 + self.data[match.home]["d"]
        self.data[match.away]["p"] = self.data[match.away]["w"] * 2 + self.data[match.away]["d"]

        # Move position
        if game == len(self.fixture[week]) - 1:
            self.position = week + 1, 0
        else:
            self.position = week, game + 1

        return match

    def move_to(self, week, game):
        if (week, game) < self.position:
            self.reset()

        while self.position != (week, game):
            self.next()

    def get_table(self):
        table = self.teams.copy()
        table.sort(key=lambda x: (self.data[x]["p"], self.data[x]["ps"] - self.data[x]["pc"], self.data[x]["w"], self.data[x]["ps"]), reverse=True)
        table = [(x, self.data[x]["w"], self.data[x]["d"], self.data[x]["l"], self.data[x]["ps"], self.data[x]["pc"], self.data[x]["p"]) for x in table]
        return table

    def print_table(self):
        table = self.get_table()
        for i, (team, w, d, l, ps, pc, p) in enumerate(table):
            print(f"{i+1:2d}. {str(team):<25}  {w:2d}  {d:2d}  {l:2d}  {ps:3d}  {pc:3d}  {p:2d}")

    def get_team(self, position):
        table = self.get_table()
        return table[position][0]

def load_players(player_data):
    return [Player(*p) for p in player_data]

def get_captains(player_list):
    players = player_list.copy()
    random.shuffle(players)
    players.sort(key=lambda p:(-p.star, -(p.offense+p.defense)/2, abs(p.offense-p.defense), p.name))
    return players

def build_teams(player_list):
    teams = []
    commentary = []

    commentary.append("--------------------")
    commentary.append("Welcome to the team lottery!")
    commentary.append("--------------------")

    players = get_captains(player_list)
    captains = players[:60]

    for i, captain in enumerate(captains):
        new_team = Team()
        new_team.add_player(captain)
        new_team.set_captain(captain)

        teams.append(new_team)
        commentary.append(f"Welcome team {i+1}: {new_team}")
    commentary.append("--------------------")

    rest = players[60:]
    random.shuffle(rest)

    for phase in range(4):
        commentary.append(f"Drafting: phase {phase}")
        commentary.append("")

        for i, team in enumerate(teams):
            player = rest[phase * 60 + i]
            team.add_player(player)

            commentary.append(f"{team} welcomes: {player}")
            commentary.append("")

            for player in team.players:
                commentary.append(f"{player.name} {player.offense} {player.defense}")
            commentary.append("")
        commentary.append("--------------------")

    return teams, commentary

def build_league(team_list):
    league = RoundRobin()
    for team in team_list:
        league.add_team(team)
    league.set_rule()
    league.generate_fixture()
    return league


players = load_players(player_data)
teams, commentary = build_teams(players)
league = build_league(teams)
