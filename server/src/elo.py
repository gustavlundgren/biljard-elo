import json
import os

class EloTrackerError(Exception):
    """Base class for all exceptions in the EloTracker application."""
    pass

class PlayerDoesNotHaveEloError(EloTrackerError):
    def init(self, player):
        self.player = player
        self.message = f"Player {self.player} does not have elo."
        super.__init__(self.message)

class CannotUpdateEloError(EloTrackerError):
    def init(self, player):
        self.player = player
        self.message = f"Cannot update elo of player: {self.player}."
        super.__init__(self.message)

def main():
    HISTORY_PATH = "./history.json"
    ELO_PATH = "./elo.json"

    matches = read_match_data(HISTORY_PATH)
    player_data = read_player_data(ELO_PATH)

    elo_tracker = EloTracker.new(player_data)
    elo_tracker.process_matches(matches)

    write_to_file(ELO_PATH, elo_tracker.players)

    print(f"Elo ratings updated and saved to '{ELO_PATH}'")


def read_player_data(filepath):
    try:
        return load_from_file(filepath)
    except (OSError, json.JSONDecodeError) as e:
        raise Exception(f"Failed to read {filepath}: {e}")

def read_match_data(filepath):    
    try:
        with open(filepath, "r") as file:
            history_data = file.read()
            return [Match(**match) for match in json.loads(history_data)]
    except (OSError, json.JSONDecodeError) as e:
        raise Exception(f"Failed to read {filepath}: {e}")

def load_from_file(file_path: str):
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    
def write_to_file(file_path: str, data):
    json_data = json.dumps(data, indent=4)
    with open(file_path, 'w') as file:
        file.write(json_data)

class Match:
    def __init__(self, winner: str, loser: str, time: int):
        self.winner = winner
        self.loser = loser
        self.time = time

class EloTracker:
    def __init__(self, players):
        if players is not None:
            print("Successful load")
            print(players)
            self.players = players
        else:
            print("Failed to load or new instance created")
            self.players = {}



    #@staticmethod
    def process_matches(self, matches):
        sorted_matches = sorted(matches, key=lambda match: match.time)
        for m in sorted_matches:
            self.update_elo(m.winner, m.loser)
    
    #@staticmethod
    def update_elo(self, winner, loser):
        k = 32.0
        try:
            winner_elo = self.get_elo(winner)
            loser_elo = self.get_elo(loser)
        except PlayerDoesNotHaveEloError as err:
            print(err)
            raise CannotUpdateEloError(err.player)


        expected_winnner = 1.0 / (1.0 + 10.0 ** ((loser_elo - winner_elo) / 400.0))
        expected_loser   = 1.0 / (1.0 + 10.0 ** ((winner_elo - loser_elo) / 400.0))

        new_winner_elo = winner_elo + k * (1 - expected_winnner)
        new_loser_elo  = loser_elo  + k * (1 - expected_loser)

        self.players[winner] = new_winner_elo
        self.players[loser]  = new_loser_elo

    def get_elo(self, player):
        if self.players[player]:
            return self.players[player]
        raise PlayerDoesNotHaveEloError

#unsafe
#do not us 
def process_match(match, history_path, elo_path):
    matches = read_match_data(history_path)
    matches.append(match)  
    with open(history_path, "w") as file:
        json.dump(matches, file, indent=4)
        
    player_data = read_player_data(elo_path)

    elo_tracker = EloTracker.new(player_data)
    elo_tracker.process_matches(matches)

    write_to_file(elo_path, elo_tracker.players)