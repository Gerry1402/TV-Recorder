import atexit

from playwright.sync_api import Page, sync_playwright


class Stream:
    # Compartidos por TODAS las instancias
    _pw = None
    _browser = None
    _context = None
    _launch_kwargs = {
        "headless": False,
        "args": [
            "--window-position=-32000,-32000",
            "--window-size=1280,720",
            "--mute-audio",
        ],
    }
    _context_kwargs = {
        "no_viewport": True,
        "locale": "es-ES",
    }
    
    _pages: dict[str, Page] = {}
    _state: dict[str, bool] = {}


    def __init__(self, channel: str):
        self.channel = channel
    
    @classmethod
    def playwright(cls):
        if cls._pw is None:
            cls._pw = sync_playwright().start()
        return cls._pw
    
    @classmethod
    def browser(cls):
        if cls._browser is None or not cls._browser.is_connected():
            cls._browser = cls.playwright().chromium.launch(**cls._launch_kwargs)
            atexit.register(cls.close)
        return cls._browser
    
    @classmethod
    def context(cls):
        if cls._context is None or cls._context.is_closed():
            cls._context = cls.browser().new_context(**cls._context_kwargs)
        return cls._context

    @property
    def page(self) -> Page:
        if self.channel not in self._pages or self._pages[self.channel].is_closed():
            self._pages[self.channel] = self.context().new_page()
        return self._pages[self.channel]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.stop()

    def stop(self):
        if self.channel in self._pages and not self._pages[self.channel].is_closed():
            self._pages[self.channel].close()
        self._pages.pop(self.channel, None)

    @classmethod
    def close(cls):
        if cls._browser is not None and cls._pw is not None and cls._context is not None:
            try:
                cls._context.close()
                cls._browser.close()
                cls._pw.stop()
            finally:
                cls._pw = cls._browser = cls._context = None
