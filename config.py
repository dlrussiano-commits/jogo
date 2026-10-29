
from pathlib import Path

import pygame

LARGURA_JOGO = 256
ALTURA_JOGO = 192
ESCALA = 4
TILE = 16
FPS = 60
VELOCIDADE = 1        

PASTA_RAIZ = Path(__file__).parent
PASTA_ASSETS = PASTA_RAIZ / "assets"
PASTA_MAPAS = PASTA_RAIZ / "mapas"
MAPA_INICIAL = "campus.tmj"


CAMADA_CHAO = "chao"
CAMADA_OBJETOS = "objetos"
CAMADA_COPAS = "copas"
CAMADA_COLISAO = "colisao"

MASCARA_GID = 0x1FFFFFFF

TECLAS_AGIR = (pygame.K_z, pygame.K_RETURN, pygame.K_SPACE)

FONTE_TAMANHO = 16
COR_TEXTO = (40, 40, 40)
COR_CAIXA_FUNDO = (248, 248, 248)
COR_CAIXA_BORDA = (60, 60, 80)
LINHAS_POR_PAGINA = 2
ALTURA_LINHA = 14
CAIXA = pygame.Rect(4, 148, 248, 40)
MARGEM_TEXTO = 8
LARGURA_TEXTO = CAIXA.width - 2 * MARGEM_TEXTO

BAIXO = (0, 1)
CIMA = (0, -1)
ESQUERDA = (-1, 0)
DIREITA = (1, 0)

ARQUIVOS_JOGADOR = {
BAIXO: ["jogador_baixo_0.png", "jogador_baixo_1.png", "jogador_baixo_2.png"],
    CIMA: ["jogador_cima_0.png", "jogador_cima_1.png", "jogador_cima_2.png"],
    DIREITA: ["jogador_direita_0.png", "jogador_direita_1.png", "jogador_direita_2.png"],
}
