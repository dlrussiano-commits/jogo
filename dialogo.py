
import pygame

from config import (
    CAIXA, MARGEM_TEXTO, LARGURA_TEXTO, LINHAS_POR_PAGINA, ALTURA_LINHA,
    COR_TEXTO, COR_CAIXA_FUNDO, COR_CAIXA_BORDA,
)
from utilidades import quebrar_texto


class CaixaDialogo:
    def __init__(self, fonte):
        self.fonte = fonte
        self.ativa = False
        self.paginas = []
        self.indice = 0

    def abrir(self, falas):
        self.paginas = []
        for fala in falas:
            linhas = quebrar_texto(fala, self.fonte, LARGURA_TEXTO)
            for inicio in range(0, len(linhas), LINHAS_POR_PAGINA):
                self.paginas.append(linhas[inicio:inicio + LINHAS_POR_PAGINA])
        if not self.paginas:
            return
        self.indice = 0
        self.ativa = True

    def avancar(self):
        self.indice += 1
        if self.indice >= len(self.paginas):
            self.ativa = False

    def desenhar(self, tela):
        if not self.ativa:
            return
        pygame.draw.rect(tela, COR_CAIXA_FUNDO, CAIXA)
        pygame.draw.rect(tela, COR_CAIXA_BORDA, CAIXA, 2)

        pagina = self.paginas[self.indice]
        for numero, linha in enumerate(pagina):
            imagem_texto = self.fonte.render(linha, False, COR_TEXTO)
            pos_x = CAIXA.x + MARGEM_TEXTO
            pos_y = CAIXA.y + 6 + numero * ALTURA_LINHA
            tela.blit(imagem_texto, (pos_x, pos_y))

        if self.indice < len(self.paginas) - 1:
            x = CAIXA.right - 14
            y = CAIXA.bottom - 12
            pygame.draw.polygon(tela, COR_CAIXA_BORDA, [(x, y), (x + 8, y), (x + 4, y + 5)])
