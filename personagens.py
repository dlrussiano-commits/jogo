
import pygame
 
from config import (
    TILE, VELOCIDADE, PASTA_ASSETS, ARQUIVOS_JOGADOR,
    BAIXO, CIMA, ESQUERDA, DIREITA,
)
from utilidades import sinal
 
 
def carregar_quadros():
    quadros = {}
    for direcao, nomes in ARQUIVOS_JOGADOR.items():
        caminhos = [PASTA_ASSETS / nome for nome in nomes]
        if all(c.exists() for c in caminhos):
            quadros[direcao] = [pygame.image.load(c).convert_alpha() for c in caminhos]
 
    if CIMA not in quadros:
        quadros[CIMA] = quadros[BAIXO]
 
    quadros[ESQUERDA] = [pygame.transform.flip(q, True, False) for q in quadros[DIREITA]]
    return quadros
 
 
def desenhar_personagem(tela, imagem, x, y, camera_x, camera_y):
    largura, altura = imagem.get_size()
    mundo_x = x + (TILE - largura) // 2
    mundo_y = y + TILE - altura
    tela.blit(imagem, (mundo_x - camera_x, mundo_y - camera_y))
 
 
class Personagem:
    def __init__(self, tile_x, tile_y):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = tile_x * TILE
        self.y = tile_y * TILE
 
    def imagem_atual(self):
        raise NotImplementedError("Toda filha de Personagem precisa definir imagem_atual()")
 
    def y_dos_pes(self):
        return self.y + TILE
 
    def desenhar(self, tela, camera_x, camera_y):
        desenhar_personagem(tela, self.imagem_atual(), self.x, self.y, camera_x, camera_y)
 
 
class NPC(Personagem):
    def __init__(self, tile_x, tile_y, imagem, falas):
        super().__init__(tile_x, tile_y)      
        self.imagem = imagem
        self.falas = falas
 
    def imagem_atual(self):
        return self.imagem
 
 
class Jogador(Personagem):
    def __init__(self, tile_x, tile_y, quadros, mapa):
        super().__init__(tile_x, tile_y)      
        self.quadros = quadros
        self.mapa = mapa
        self.andando = False
        self.olhando = BAIXO
        self.pe = 0
 
    def atualizar(self, direcao):
        dx, dy = direcao
 
        if not self.andando and (dx != 0 or dy != 0):
            self.olhando = direcao
 
            novo_x = self.tile_x + dx
            novo_y = self.tile_y + dy
            if self.mapa.eh_livre(novo_x, novo_y):
                self.tile_x = novo_x
                self.tile_y = novo_y
                self.andando = True
                self.pe = 1 - self.pe
 
        if self.andando:
            alvo_x = self.tile_x * TILE
            alvo_y = self.tile_y * TILE
            self.x += sinal(alvo_x - self.x) * VELOCIDADE
            self.y += sinal(alvo_y - self.y) * VELOCIDADE
            if self.x == alvo_x and self.y == alvo_y:
                self.andando = False
 
    def imagem_atual(self):
        quadro = 0
        if self.andando:
            restante = abs(self.tile_x * TILE - self.x) + abs(self.tile_y * TILE - self.y)
            percorrido = TILE - restante
            if percorrido < TILE // 2:
                quadro = 1 + self.pe
        return self.quadros[self.olhando][quadro]
 
 
def chave_profundidade(objeto):
    return objeto.y_dos_pes()
 
 
def tentar_conversar(jogador, npcs, caixa):
    if jogador.andando:
        return
    frente_x = jogador.tile_x + jogador.olhando[0]
    frente_y = jogador.tile_y + jogador.olhando[1]
    for npc in npcs:
        if npc.tile_x == frente_x and npc.tile_y == frente_y:
            caixa.abrir(npc.falas)
            return
from config import (
    TILE, VELOCIDADE, PASTA_ASSETS, ARQUIVOS_JOGADOR,
    BAIXO, CIMA, ESQUERDA, DIREITA,
)
from utilidades import sinal


def carregar_quadros():
    quadros = {}
    for direcao, nomes in ARQUIVOS_JOGADOR.items():
        caminhos = [PASTA_ASSETS / nome for nome in nomes]
        if all(c.exists() for c in caminhos):
            quadros[direcao] = [pygame.image.load(c).convert_alpha() for c in caminhos]

    if CIMA not in quadros:
        quadros[CIMA] = quadros[BAIXO]

    quadros[ESQUERDA] = [pygame.transform.flip(q, True, False) for q in quadros[DIREITA]]
    return quadros


def desenhar_personagem(tela, imagem, x, y, camera_x, camera_y):
    largura, altura = imagem.get_size()
    mundo_x = x + (TILE - largura) // 2
    mundo_y = y + TILE - altura
    tela.blit(imagem, (mundo_x - camera_x, mundo_y - camera_y))


class NPC:
    def __init__(self, tile_x, tile_y, imagem, falas):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = tile_x * TILE
        self.y = tile_y * TILE
        self.imagem = imagem
        self.falas = falas

    def y_dos_pes(self):
        return self.y + TILE

    def desenhar(self, tela, camera_x, camera_y):
        desenhar_personagem(tela, self.imagem, self.x, self.y, camera_x, camera_y)


class Jogador:
    def __init__(self, tile_x, tile_y, quadros, mapa):
        self.quadros = quadros
        self.mapa = mapa
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = tile_x * TILE
        self.y = tile_y * TILE
        self.andando = False
        self.olhando = BAIXO
        self.pe = 0

    def atualizar(self, direcao):
        dx, dy = direcao

        if not self.andando and (dx != 0 or dy != 0):
            self.olhando = direcao

            novo_x = self.tile_x + dx
            novo_y = self.tile_y + dy
            if self.mapa.eh_livre(novo_x, novo_y):
                self.tile_x = novo_x
                self.tile_y = novo_y
                self.andando = True
                self.pe = 1 - self.pe

        if self.andando:
            alvo_x = self.tile_x * TILE
            alvo_y = self.tile_y * TILE
            self.x += sinal(alvo_x - self.x) * VELOCIDADE
            self.y += sinal(alvo_y - self.y) * VELOCIDADE
            if self.x == alvo_x and self.y == alvo_y:
                self.andando = False

    def imagem_atual(self):
        quadro = 0
        if self.andando:
            restante = abs(self.tile_x * TILE - self.x) + abs(self.tile_y * TILE - self.y)
            percorrido = TILE - restante
            if percorrido < TILE // 2:
                quadro = 1 + self.pe
        return self.quadros[self.olhando][quadro]

    def y_dos_pes(self):
        return self.y + TILE

    def desenhar(self, tela, camera_x, camera_y):
        desenhar_personagem(tela, self.imagem_atual(), self.x, self.y, camera_x, camera_y)


def chave_profundidade(objeto):
    return objeto.y_dos_pes()


def tentar_conversar(jogador, npcs, caixa):
    if jogador.andando:
        return
    frente_x = jogador.tile_x + jogador.olhando[0]
    frente_y = jogador.tile_y + jogador.olhando[1]
    for npc in npcs:
        if npc.tile_x == frente_x and npc.tile_y == frente_y:
            caixa.abrir(npc.falas)
            return
