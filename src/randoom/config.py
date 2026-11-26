"""
    Configurações globais e constantes do jogo.
"""

from pathlib import Path
import math

SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
FPS: int = 20
TITLE: str = "RanDOOM"
DEFAULT_FOV: float = math.pi / 3
DEFAULT_SPEED: float = 0.2

CAMINHO_PAREDE_LIMPA: Path = Path(__file__).parent / "assets" / "Parede_limpa.png"
CAMINHO_PAREDE: Path = Path(__file__).parent / "assets" / "Parede.png"
CAMINHO_CEU: Path = Path(__file__).parent / "assets" / "Sky.jpg"
CAMINHO_INIMIGO: Path = Path(__file__).parent / "assets" / "averiguando-possivel-resenha.png"