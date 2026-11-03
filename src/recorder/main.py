import logging
from config import setup_logging

setup_logging()
from datetime import datetime

from browser import Player
from epg import EPG

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting TV Recorder")
    epg = EPG()
    # if programme := epg["Cuatro"].now():
    if programme := epg["Cuatro"]["Horizonte diarios"].actual():
        print(programme)
        player = Player(programme.channel, programme.title)
        player.record(programme.start, programme.end)
    logger.info("TV Recorder finished")

if __name__ == "__main__":
    main()
