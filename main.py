
import pygame

from config import (
    LARGURA_JOGO, ALTURA_JOGO, ESCALA, FPS, FONTE_TAMANHO,
    PASTA_MAPAS, MAPA_INICIAL, TECLAS_AGIR, BAIXO,)

from utilidades import tingir
from mapa import Mapa
from personagens import ( NPC, Jogador, carregar_quadros, chave_profundidade, tentar_conversar,)
from dialogo import CaixaDialogo
from camera import calcular_camera
from entrada import ler_direcao


def main():
    pygame.init()
    janela = pygame.display.set_mode((LARGURA_JOGO * ESCALA, ALTURA_JOGO * ESCALA))
    relogio = pygame.time.Clock()
    tela = pygame.Surface((LARGURA_JOGO, ALTURA_JOGO))

    quadros = carregar_quadros()
    fonte = pygame.font.Font(None, FONTE_TAMANHO)
    mapa = Mapa(PASTA_MAPAS / MAPA_INICIAL)
    jogador = Jogador(16, 12, quadros, mapa)

    parado_de_frente = quadros[BAIXO][0]
    npcs = [
        NPC(19, 12, tingir(parado_de_frente, (255, 150, 150)), [
            "Ei, calouro! Dá para ver de longe que você chegou agora",
            "Um conselho, nunca deixe para estudar na véspera da prova",
        ]),
        NPC(10, 8, tingir(parado_de_frente, (170, 255, 170)), [
            "Estou procurando a minha sala faz meia hora...",
            "Se você achar, me avisa!",
        ]),
    ]
    for npc in npcs:
        mapa.bloquear(npc.tile_x, npc.tile_y)

    caixa = CaixaDialogo(fonte)
    mostrar_grade = False
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif evento.key == pygame.K_g:
                    mostrar_grade = not mostrar_grade
                elif evento.key in TECLAS_AGIR:
                    if caixa.ativa:
                        caixa.avancar()
                    else:
                        tentar_conversar(jogador, npcs, caixa)

        direcao = (0, 0) if caixa.ativa else ler_direcao()
        jogador.atualizar(direcao)
        camera_x, camera_y = calcular_camera(jogador, mapa)

       
        mapa.desenhar_base(tela, camera_x, camera_y, mostrar_grade)     

        personagens = npcs + [jogador]                                  
        personagens.sort(key=chave_profundidade)
        for personagem in personagens:
            personagem.desenhar(tela, camera_x, camera_y)

        mapa.desenhar_copas(tela, camera_x, camera_y)                  
        caixa.desenhar(tela)

       
        pygame.transform.scale(tela, janela.get_size(), janela)
        pygame.display.flip()
        pygame.display.set_caption(f"Pokémon Rural - tile ({jogador.tile_x}, {jogador.tile_y})")

        
        relogio.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
