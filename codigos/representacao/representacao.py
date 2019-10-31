################################################################################
#       ARQUIVO: representacao.py
#
#     DESCRIÇÃO: Aplicar tecnicas de representação e descrição
#
#        OPÇÕES: ---
#    REQUISITOS: openCV
#         NOTAS: Biblioteca 'openCV' pode apresentar problemas com
#                distribuições Linux com interface baseada em Qt
#         AUTOR: Alan U. Sabino <alan.sabino@usp.br>
#        VERSÃO: 1.0
#       CRIAÇÃO: 31/10/2019
#       REVISÃO: ---
################################################################################

import cv2 as biblimagem
import numpy as np
import math
from copy import deepcopy as copiar

from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

import sys
sys.setrecursionlimit(10000)

def esqueletizacao(matriz_pixels):
    nova_matriz_pixels = np.copy(matriz_pixels)
    altura, largura = nova_matriz_pixels.shape[0:2]
    parada=False
    mudanca=False
    rodada = 0
    while(!parada):
        for linha in range(1, altura-1):
            for coluna in range(1, largura-1):
                if nova_matriz_pixels[linha,coluna] == 0:
                    if vizihos_nao_fundo(nova_matriz_pixels, linha, coluna):
                        if quantidade_transicoes(nova_matriz_pixels, linha, coluna):
                            if produto_zero_primeiro(nova_matriz_pixels, linha, coluna):
                                nova_matriz_pixels[linha,coluna] = 255
                                mudanca = True
        for linha in range(1, altura-1):
            for coluna in range(1, largura-1):
                if nova_matriz_pixels[linha,coluna] == 0:
                    if vizihos_nao_fundo(nova_matriz_pixels, linha, coluna):
                        if quantidade_transicoes(nova_matriz_pixels, linha, coluna):
                            if produto_zero_segundo(nova_matriz_pixels, linha, coluna):
                                nova_matriz_pixels[linha,coluna] = 255
                                mudanca = True
        if mudanca == True:
            mudanca = False
        else:
            rodada += 1
            if rodada > 1:
                parada = True
    return nova_matriz_pixels

def vizihos_nao_fundo(matriz_pixels, linha coluna):
    contador = 0
    if matriz_pixels[linha-1, coluna] == 0:
        contador += 1
    if matriz_pixels[linha-1, coluna+1] == 0:
        contador += 1
    if matriz_pixels[linha, coluna-1] == 0:
        contador += 1
    if matriz_pixels[linha, coluna+1] == 0:
        contador += 1
    if matriz_pixels[linha+1, coluna-1] == 0:
        contador += 1
    if matriz_pixels[linha+1, coluna] == 0:
        contador += 1
    if matriz_pixels[linha+1, coluna+1] == 0:
        contador += 1
    if contador >= 2 and contador <= 6:
        return True
    else:
        return False

def quantidade_transicoes(matriz_pixels, linha coluna):
    return True or False

def produto_zero_primeiro(matriz_pixels, linha coluna):
    return True or False

def produto_zero_segundo(matriz_pixels, linha coluna):
    return True or False

def selecionar_imagem():
    global painelA, caminho
    caminho = filedialog.askopenfilename()
    if len(caminho) > 0:
        imagem_original = biblimagem.imread(caminho)
        imagem = biblimagem.cvtColor(imagem_original, biblimagem.COLOR_BGR2GRAY)
        imagem = Image.fromarray(imagem)
        imagem = ImageTk.PhotoImage(imagem)
        if painelA is None:
            painelA = Label(image=imagem)
            painelA.image = imagem
            painelA.pack(side="left", padx=10, pady=10)
        else:
            painelA.configure(image=imagem)
            painelA.image = imagem
            if painelB is not None:
                painelB.configure(image='')

def realce():
    global painelB
    if len(caminho) > 0:
        #imagem_tratada = ligacao(borda_diferenciacao(filtro_mediana(biblimagem.imread(caminho))))
        imagem_tratada = borda_diferenciacao(filtro_mediana(biblimagem.imread(caminho)))
        imagem_tratada = Image.fromarray(imagem_tratada)
        imagem_tratada = ImageTk.PhotoImage(imagem_tratada)
        if painelB is None:
            painelB = Label(image=imagem_tratada)
            painelB.image = imagem_tratada
            painelB.pack(side="right", padx=10, pady=10)
        else:
            painelB.configure(image=imagem_tratada)
            painelB.image = imagem_tratada

root = Tk()
painelA = None
painelB = None

#verificar_posicionamento = Button(root, text="Verificar posicionamento", command=posicionamento)
#verificar_posicionamento.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
#contar_objetos = Button(root, text="Contar objetos", command=contagem)
#contar_objetos.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
#ligacao_bordas = Button(root, text="Emendar bordas", command=realce)
#ligacao_bordas.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
abrir_imagem = Button(root, text="Selecionar Imagem", command=selecionar_imagem)
abrir_imagem.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

root.mainloop()

