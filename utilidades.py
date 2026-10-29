
import pygame


def sinal(n):
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0


def tingir(imagem, cor):
    copia = imagem.copy()
    copia.fill(cor, special_flags=pygame.BLEND_RGB_MULT)
    return copia


def quebrar_texto(texto, fonte, largura_max):
    linhas = []
    linha_atual = ""
    for palavra in texto.split():
        tentativa = (linha_atual + " " + palavra).strip()
        if fonte.size(tentativa)[0] <= largura_max:
            linha_atual = tentativa
        else:
            if linha_atual:
                linhas.append(linha_atual)
            linha_atual = palavra
    if linha_atual:
        linhas.append(linha_atual)
    return linhas
