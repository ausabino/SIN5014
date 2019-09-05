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
#       REVISÃO:  05/09/2019 Alan U. Sabino <alan.sabino@usp.br> (1)
################################################################################

import cv2 as biblimagem
import numpy as np
from matplotlib import pyplot as grafico
from copy import deepcopy as copiar

CANAIS=3
VALOR_CANAL=256

#imagem = biblimagem.imread("imgs/estacao.jpg", biblimagem.IMREAD_COLOR)
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
    # TODO: incluir alteração de brilho da biblioteca openCV
    nova_matriz_pixels = np.copy(matriz_pixels)
    altura, largura = nova_matriz_pixels.shape[0:2]
    if valor >= 0:
        for linha in range(0, altura):
            for coluna in range(0, largura):
                for cor in range(0,CANAIS):
                    if (nova_matriz_pixels[linha][coluna][cor] + valor) > 255:
                        nova_matriz_pixels[linha][coluna][cor] = 255
                    else:
                        nova_matriz_pixels[linha][coluna][cor] += valor
    else:
        for linha in range(0, altura):
            for coluna in range(0, largura):
                for cor in range(0,CANAIS):
                    if (nova_matriz_pixels[linha][coluna][cor] + valor) < 0:
                        nova_matriz_pixels[linha][coluna][cor] = 0
                    else:
                        nova_matriz_pixels[linha][coluna][cor] += valor
    figura_dupla = np.hstack((matriz_pixels, nova_matriz_pixels))
    biblimagem.imshow('Lado a Lado', figura_dupla)
    biblimagem.waitKey()
    grafico.show()

#histograma(imagem)
#brilho(imagem, -155)

def filtro_mediana(matriz_pixels):
    altura, largura = matriz_pixels.shape[0:2]
    nova_matriz_pixels = np.zeros((altura, largura, CANAIS))
    vizinhos_canais = np.zeros((CANAIS, 8))
    for linha in range(1, altura-1):
        for coluna in range(1, largura-1):
            for cor in range(0, CANAIS):
                vizinhos_canais[cor][0] = copiar(matriz_pixels[linha-1][coluna-1][cor])
                vizinhos_canais[cor][1] = copiar(matriz_pixels[linha-1][coluna][cor])
                vizinhos_canais[cor][2] = copiar(matriz_pixels[linha-1][coluna+1][cor])
                vizinhos_canais[cor][3] = copiar(matriz_pixels[linha][coluna-1][cor])
                vizinhos_canais[cor][4] = copiar(matriz_pixels[linha][coluna+1][cor])
                vizinhos_canais[cor][5] = copiar(matriz_pixels[linha+1][coluna-1][cor])
                vizinhos_canais[cor][6] = copiar(matriz_pixels[linha+1][coluna][cor])
                vizinhos_canais[cor][7] = copiar(matriz_pixels[linha+1][coluna+1][cor])
            vizinhos_canais = np.sort(vizinhos_canais)
            nova_matriz_pixels[linha][coluna][0] = copiar(vizinhos_canais[0][3])
            nova_matriz_pixels[linha][coluna][1] = copiar(vizinhos_canais[1][3])
            nova_matriz_pixels[linha][coluna][2] = copiar(vizinhos_canais[2][3])
    nova_matriz_pixels = nova_matriz_pixels.astype('uint8')
    figura_dupla = np.hstack((matriz_pixels, nova_matriz_pixels))
    biblimagem.imshow('Lado a Lado', figura_dupla)
    biblimagem.waitKey()
    grafico.show()

imagem = biblimagem.imread("imgs/ruido.jpg", biblimagem.IMREAD_COLOR)
filtro_mediana(imagem)

#mediana = biblimagem.medianBlur(imagem,3)
#biblimagem.imshow('Teste', mediana)
#biblimagem.waitKey()
#grafico.show()
