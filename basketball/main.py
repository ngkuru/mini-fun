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

    def play(self):
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

def load_players(player_data):
    return [Player(*p) for p in player_data]

def get_captains(player_list):
    players = player_list.copy()
    random.shuffle(players)
    players.sort(key=lambda p:(-p.star, -(p.offense+p.defense)/2, abs(p.offense-p.defense), p.name))
    return players

def build_teams(player_list):
    teams = []
    history = []

    history.append("--------------------")
    history.append("Welcome to the team lottery!")
    history.append("--------------------")

    players = get_captains(player_list)
    captains = players[:60]

    for i, captain in enumerate(captains):
        new_team = Team()
        new_team.add_player(captain)
        new_team.set_captain(captain)

        teams.append(new_team)
        history.append(f"Welcome team {i+1}: {new_team}")
    history.append("--------------------")

    rest = players[60:]
    random.shuffle(rest)

    for phase in range(4):
        history.append(f"Drafting: phase {phase}")
        history.append("")

        for i, team in enumerate(teams):
            player = rest[phase * 60 + i]
            team.add_player(player)

            history.append(f"{team} welcomes: {player}")
            history.append("")

            for player in team.players:
                history.append(f"{player.name} {player.offense} {player.defense}")
            history.append("")
        history.append("--------------------")
    
    return teams, history

def build_league(team_list):
    league = RoundRobin()
    for team in team_list:
        league.add_team(team)
    league.set_rule()
    league.play()
    return league


players = load_players(player_data)
teams, history = build_teams(players)
league = build_league(teams)

match = league.fixture[0][0]
for comment in match.commentary:
    print(comment)