from browser import Player
from epg import EPG
from datetime import datetime


def main():
    epg = EPG()
    # if programme := epg["Cuatro"].now():
    if programme := epg["Cuatro"]["Horizonte diarios"].actual():
        print(programme)
        player = Player(programme.channel, programme.title)
        player.record(programme.start, programme.end)
