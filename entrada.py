import pygame

from config import BAIXO, CIMA, ESQUERDA, DIREITA


def ler_direcao():
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        return CIMA
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        return BAIXO
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        return ESQUERDA
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        return DIREITA
    return (0, 0)
