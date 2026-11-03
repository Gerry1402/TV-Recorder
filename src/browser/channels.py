CHANNELS: dict = {
    "Cuatro": {
        "url": "https://www.cuatro.com/en-directo/",
        "pattern": r"^https://[^?]*\.ts(?:\?.*)?$",
        "suffix": ".ts",
        "selectors": {
            "player": ".videoPlayer",
            # "message": ".message",
            "start": "[data-agth='playerPreplayer']",
            "fullscreen": "[data-agth='playerFullScreenOnButton']",
        },
    },
    "Antena 3": {
        "url": "https://www.atresplayer.com/directos/antena3/",
        "pattern": r"^https?://atres-live-ssai\.atresmedia\.com[^?]*-video=\d+-\d+\.ts(?:\?.*)?$",
        "suffix": ".ts",
        "selectors": {
            "player": ".playerContainer",
            "message": ".message",
            "start": "button[aria-label='Directo']",
            # "fullscreen": "[data-agth='playerFullScreenOnButton']",
        },
    },
}
