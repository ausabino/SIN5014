################################################################################
#       ARQUIVO: editorimagem.py
#
#     DESCRIÇÃO: Programa para edição de imagens
#
#        OPÇÕES:  ---
#    REQUISITOS: openCV
#         NOTAS: Biblioteca 'openCV' pode apresentar problemas com
#               distribuições Linux com interface baseada em Qt
#         AUTOR:  Alan U. Sabino <alan.sabino@usp.br>
#        VERSÃO:  0.1
#       CRIAÇÃO:  04/09/2019
#       REVISÃO:  ---
################################################################################

import cv2 as biblimagem
import numpy as np
from matplotlib import pyplot as grafico

CANAIS=3
VALOR_CANAL=256

imagem = biblimagem.imread("imgs/estacao.jpg", biblimagem.IMREAD_COLOR)
#imagem = biblimagem.imread("imgs/cidade.jpg", biblimagem.IMREAD_COLOR)

def histograma(matriz_pixels):
    # TODO: Colocar legenda nos eixos e titulo
    altura, largura = matriz_pixels.shape[0:2]
    histograma_azul = np.zeros((1,VALOR_CANAL))
    histograma_verde = np.zeros((1,VALOR_CANAL))
    histograma_vermelho = np.zeros((1,VALOR_CANAL))
    for linha in range(0, altura):
        for coluna in range(0, largura):
            histograma_azul[0][matriz_pixels[linha][coluna][0]] += 1
            histograma_verde[0][matriz_pixels[linha][coluna][1]] += 1
            histograma_vermelho[0][matriz_pixels[linha][coluna][2]] += 1
    grafico.plot(histograma_azul[0], 'b')
    grafico.plot(histograma_verde[0], 'g')
    grafico.plot(histograma_vermelho[0], 'r')
    grafico.xlim([0,VALOR_CANAL])
    grafico.show()

##Calcular histograma com biblioteca openCV
#histograma_azul = biblimagem.calcHist([imagem], [0], None, [256], [0,256])
#histograma_verde = biblimagem.calcHist([imagem], [1], None, [256], [0,256])
#histograma_vermelho = biblimagem.calcHist([imagem], [2], None, [256], [0,256])

def brilho(matriz_pixels, valor):
    nova_matriz_pixels = np.copy(matriz_pixels)
    altura, largura = nova_matriz_pixels.shape[0:2]
    if valor >= 0:
        for linha in range(0, altura):
            for coluna in range(0, largura):
                for cor in range(0,CANAIS):
                    if (nova_matriz_pixels[linha][coluna][cor] + valor) > 255:
                        nova_matriz_pixels[linha][coluna][cor] = 255
                    else:
                        nova_matriz_pixels[linha][coluna][cor] = nova_matriz_pixels[linha][coluna][cor] + valor
    else:
        for linha in range(0, altura):
            for coluna in range(0, largura):
                for cor in range(0,CANAIS):
                    if (nova_matriz_pixels[linha][coluna][cor] + valor) < 0:
                        nova_matriz_pixels[linha][coluna][cor] = 0
                    else:
                        nova_matriz_pixels[linha][coluna][cor] = nova_matriz_pixels[linha][coluna][cor] + valor
    figura_dupla = np.concatenate((matriz_pixels, nova_matriz_pixels), axis=1)
    biblimagem.imshow('Lado a Lado', figura_dupla)
    biblimagem.waitKey()
    grafico.show()

histograma(imagem)
brilho(imagem, -255)

