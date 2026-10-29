
from config import TILE, LARGURA_JOGO, ALTURA_JOGO


def calcular_camera(jogador, mapa):
    centro_x = jogador.x + TILE // 2
    centro_y = jogador.y + TILE // 2
    camera_x = centro_x - LARGURA_JOGO // 2
    camera_y = centro_y - ALTURA_JOGO // 2
    camera_x = max(0, min(camera_x, mapa.largura - LARGURA_JOGO))
    camera_y = max(0, min(camera_y, mapa.altura - ALTURA_JOGO))
    return camera_x, camera_y
