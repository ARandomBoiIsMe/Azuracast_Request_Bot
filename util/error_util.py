from enum import Enum

class ErrorType(Enum):
    SongIsNotRequestable = 1
    FailedToRequestSong = 2
    FailedToFetchRequestableSongs = 3
    FailedToFetchStations = 4
    FailedToFetchCurrentlyPlayingSong = 5
    UnexpectedError = 6

class AzuracastError:
    def __init__(self, type: ErrorType, description: str):
        self.type = type
        self.description = description

    def __str__(self):
        return f"{self.type.name}: {self.description}"