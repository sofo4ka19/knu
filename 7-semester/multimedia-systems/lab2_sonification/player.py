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


def play(path: str) -> None:
    pygame = _pygame()
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
    except pygame.error as e:
        raise PlayerError(f"Could not play the file: {e}")


def stop() -> None:
    pygame = _pygame()
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()


def is_playing() -> bool:
    pygame = _pygame()
    return bool(pygame.mixer.get_init() and pygame.mixer.music.get_busy())


def position_seconds() -> float:
    pygame = _pygame()
    if not pygame.mixer.get_init():
        return 0.0
    return max(0, pygame.mixer.music.get_pos()) / 1000.0