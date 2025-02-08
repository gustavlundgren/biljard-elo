import json
from server.src import db
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

    #games = read_game_data(HISTORY_PATH)
    #player_data = read_player_data(ELO_PATH)

    #elo_tracker = EloTracker.new(player_data)
    #elo_tracker.process_games(games)

    #write_to_file(ELO_PATH, elo_tracker.players)

    #print(f"Elo ratings updated and saved to '{ELO_PATH}'")


def read_player_data(filepath):
    try:
        return load_from_file(filepath)
    except (OSError, json.JSONDecodeError) as e:
        raise Exception(f"Failed to read {filepath}: {e}")

def read_game_data(filepath):    
    try:
        with open(filepath, "r") as file:
            history_data = file.read()
            return [game(**game) for game in json.loads(history_data)]
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

class Game:
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
    def process_games(self, games):
        sorted_games = sorted(games, key=lambda game: game.time)
        for m in sorted_games:
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
def process_game():
    doc_games_ref = db.collection("games")
    
    games = [doc.to_dict() for doc in doc_games_ref.get()]

    verified_games=[]
    print("ahamdulilah")
    print(games[0])

    if games:
        for game in games:
            if game['verified']:
                players = game['players']
                winner = game['winner']
                if players[0] == winner:
                    loser = players[1]
                else:
                    loser = players[0]
                pass
                verified_games.append(Game(winner, loser, game['time']))

    doc_players_ref = db.collection("players")
    
    players = [(doc.id, doc.to_dict()) for doc in doc_players_ref.get()]

    
    #print(games[0])
    player_data = {}
    if players:
        for doc_id, player in players:
            player_data[player[doc_id]] = player['elo']

    elo_tracker = EloTracker.new(player_data)
    elo_tracker.process_games(games)

    for doc_id, new_elo in player_data.items():
        player_ref = doc_players_ref.document(doc_id)
        player_ref.update({'elo': new_elo})



    #write_to_file(elo_path, elo_tracker.players)


