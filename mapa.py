
import json

import pygame

from config import (
    TILE, LARGURA_JOGO, ALTURA_JOGO, MASCARA_GID,
    CAMADA_CHAO, CAMADA_OBJETOS, CAMADA_COPAS, CAMADA_COLISAO,
)


class Tileset:
    def __init__(self, dados, pasta):
        if dados["tilewidth"] != TILE or dados["tileheight"] != TILE:
            raise ValueError(f"O tileset precisa ter tiles de {TILE}x{TILE} pixels")
        self.primeiro_gid = dados["firstgid"]
        self.colunas = dados["columns"]
        self.quantidade = dados["tilecount"]
        caminho_imagem = (pasta / dados["image"]).resolve()
        self.imagem = pygame.image.load(caminho_imagem).convert_alpha()

    def tem(self, gid):
        return self.primeiro_gid <= gid < self.primeiro_gid + self.quantidade

    def recortar(self, gid):
        indice = gid - self.primeiro_gid
        coluna = indice % self.colunas
        linha = indice // self.colunas
        return self.imagem.subsurface((coluna * TILE, linha * TILE, TILE, TILE))


def carregar_tileset(referencia, pasta_do_mapa):
    primeiro_gid = referencia["firstgid"]
    if "source" in referencia:
        caminho = pasta_do_mapa / referencia["source"]
        if caminho.suffix != ".tsj":
            raise ValueError(
                f"Tileset externo '{caminho.name}' não está em JSON."
            )
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        pasta = caminho.parent
    else:
        dados = referencia
        pasta = pasta_do_mapa
    dados = dict(dados, firstgid=primeiro_gid)
    return Tileset(dados, pasta)


class Mapa:
    def __init__(self, caminho):
        pasta = caminho.parent
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        if dados.get("infinite"):
            raise ValueError("Mapa infinito não é suportado")

        self.colunas = dados["width"]
        self.linhas = dados["height"]
        self.largura = self.colunas * TILE
        self.altura = self.linhas * TILE

        self.tilesets = [carregar_tileset(ref, pasta) for ref in dados["tilesets"]]

        self.chao = pygame.Surface((self.largura, self.altura))
        self.objetos = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self.copas = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        destinos = {
            CAMADA_CHAO: self.chao,
            CAMADA_OBJETOS: self.objetos,
            CAMADA_COPAS: self.copas,
        }

        self.paredes = set()           
        self.tiles_ocupados = set()   

        for camada in dados["layers"]:
            if camada["type"] != "tilelayer":
                continue
            nome = camada["name"]
            if nome == CAMADA_COLISAO:
                self._ler_colisao(camada)
            elif nome in destinos and camada.get("visible", True):
                self._pintar_camada(camada, destinos[nome])

        self.grade = self._criar_grade()

    def _achar_tile(self, gid):
        for tileset in self.tilesets:
            if tileset.tem(gid):
                return tileset.recortar(gid)
        raise ValueError(f"Nenhum tileset tem o tile {gid}.")

    def _percorrer(self, camada):
        for i, gid in enumerate(camada["data"]):
            gid = gid & MASCARA_GID
            if gid != 0:
                yield i % self.colunas, i // self.colunas, gid

    def _pintar_camada(self, camada, superficie):
        for tile_x, tile_y, gid in self._percorrer(camada):
            superficie.blit(self._achar_tile(gid), (tile_x * TILE, tile_y * TILE))

    def _ler_colisao(self, camada):
        for tile_x, tile_y, _ in self._percorrer(camada):
            self.paredes.add((tile_x, tile_y))

    def _criar_grade(self):
        grade = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        for tile_x, tile_y in self.paredes:
            grade.fill((255, 0, 0, 80), (tile_x * TILE, tile_y * TILE, TILE, TILE))
        cor = (255, 255, 255)
        for x in range(0, self.largura, TILE):
            pygame.draw.line(grade, cor, (x, 0), (x, self.altura - 1))
        for y in range(0, self.altura, TILE):
            pygame.draw.line(grade, cor, (0, y), (self.largura - 1, y))
        return grade

    def bloquear(self, tile_x, tile_y):
        self.tiles_ocupados.add((tile_x, tile_y))

    def eh_livre(self, tile_x, tile_y):
        fora_do_mapa = not (0 <= tile_x < self.colunas and 0 <= tile_y < self.linhas)
        if fora_do_mapa:
            return False
        if (tile_x, tile_y) in self.paredes:
            return False
        return (tile_x, tile_y) not in self.tiles_ocupados

    def desenhar_base(self, tela, camera_x, camera_y, com_grade):
        janela = pygame.Rect(camera_x, camera_y, LARGURA_JOGO, ALTURA_JOGO)
        tela.blit(self.chao, (0, 0), area=janela)
        tela.blit(self.objetos, (0, 0), area=janela)
        if com_grade:
            tela.blit(self.grade, (0, 0), area=janela)

    def desenhar_copas(self, tela, camera_x, camera_y):
        janela = pygame.Rect(camera_x, camera_y, LARGURA_JOGO, ALTURA_JOGO)
        tela.blit(self.copas, (0, 0), area=janela)
