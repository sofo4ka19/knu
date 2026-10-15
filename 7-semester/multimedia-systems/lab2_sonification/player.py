import os


class PlayerError(Exception):
    """Raised when playback is not possible (e.g. pygame is not installed)."""


def _pygame():
    try:
        os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
        import pygame
        return pygame
    except ImportError:
        raise PlayerError("pygame is not installed. Run: pip install pygame")


class MidiPlayer:
    def __init__(self):
        self.paused = False
        self.paused_at = 0.0        # position (in seconds) where the music was paused
        self.offset = 0.0           # correction (in seconds) for pygame's position

    def play(self, path):
        """Start the file from the beginning."""
        pygame = _pygame()
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        except pygame.error as e:
            raise PlayerError(f"Could not play the file: {e}")
        self.paused = False
        self.offset = 0.0

    def pause(self):
        """Pause the music; resume() continues from the same place."""
        if self.paused or not self.is_playing():
            return
        self.paused_at = self.position()
        _pygame().mixer.music.pause()
        self.paused = True

    def resume(self):
        """Continue the music after pause()."""
        if not self.paused:
            return
        pygame = _pygame()
        pygame.mixer.music.unpause()
        # if pygame went on counting during the pause, this cancels the jump
        self.offset = self.paused_at - self._pygame_position(pygame)
        self.paused = False

    def stop(self):
        """Stop the music; the next play() starts from the beginning."""
        pygame = _pygame()
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
        self.paused = False
        self.offset = 0.0

    def is_playing(self):
        """True while the music sounds (not paused and not finished)."""
        pygame = _pygame()
        return (not self.paused and bool(pygame.mixer.get_init())
                and bool(pygame.mixer.music.get_busy()))

    def position(self):
        """Position in seconds. It does not change while the music is paused."""
        if self.paused:
            return self.paused_at
        pygame = _pygame()
        if not pygame.mixer.get_init():
            return 0.0
        return self._pygame_position(pygame) + self.offset

    @staticmethod
    def _pygame_position(pygame):
        return max(0, pygame.mixer.music.get_pos()) / 1000.0