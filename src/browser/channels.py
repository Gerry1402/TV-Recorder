CHANNELS: dict = {
    "Cuatro": {
        "url": "https://www.cuatro.com/en-directo/",
        "pattern": r"^https://[^?]*\.ts(?:\?.*)?$",
        "suffix": ".ts",
        "selectors": {
            "player": ".videoPlayer",
            "start": "[data-agth='playerPreplayer']",
            # "mute": "[data-agth='playerMutedButton']",
            "fullscreen": "[data-agth='playerFullScreenOnButton']",
        },
    },
    "Antena 3": {
        "url": "https://www.atresplayer.com/directos/antena3/",
        "pattern": r"^https?://atres-live-ssai\.atresmedia\.com[^?]*-video=\d+-\d+\.ts(?:\?.*)?$",
        "suffix": ".ts",
        "selectors": {
            "startfirst": True,
            "player": ".playerContainer",
            "start": "button[aria-label='Directo']",
            # "fullscreen": "[data-agth='playerFullScreenOnButton']",
        },
    },
}
