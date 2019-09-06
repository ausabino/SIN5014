################################################################################
#       ARQUIVO: editorimagem.py
#
#     DESCRIÇÃO: Programa para edição de imagens
#
#        OPÇÕES: ---
#    REQUISITOS: openCV
#         NOTAS: Biblioteca 'openCV' pode apresentar problemas com
#                distribuições Linux com interface baseada em Qt
#         AUTOR: Alan U. Sabino <alan.sabino@usp.br>
#        VERSÃO: 1.1
#       CRIAÇÃO: 04/09/2019
#       REVISÃO: 06/09/2019 Alan U. Sabino <alan.sabino@usp.br> (2)
#                05/09/2019 Alan U. Sabino <alan.sabino@usp.br> (1)
################################################################################

import cv2 as biblimagem
import numpy as np
from matplotlib import pyplot as grafico
from copy import deepcopy as copiar
from random import randrange

from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

CANAIS=3
VALOR_CANAL=256

def histograma(matriz_pixels):
    altura, largura = matriz_pixels.shape[0:2]
    histograma = np.zeros((CANAIS, VALOR_CANAL))
    for cor in range(0, CANAIS):
        for linha in range(0, altura):
            for coluna in range(0, largura):
                histograma[cor][matriz_pixels[linha][coluna][cor]] += 1
    return np.matrix(histograma)

def filtro_brilho(matriz_pixels, valor):
    nova_matriz_pixels = np.copy(matriz_pixels)
    altura, largura = nova_matriz_pixels.shape[0:2]
    for linha in range(0, altura):
        for coluna in range(0, largura):
            for cor in range(0,CANAIS):
                if (nova_matriz_pixels[linha][coluna][cor] + valor) >= 255:
                    nova_matriz_pixels[linha][coluna][cor] = 255
                elif  (nova_matriz_pixels[linha][coluna][cor] + valor) <= 0:
                    nova_matriz_pixels[linha][coluna][cor] = 0
                else:
                    nova_matriz_pixels[linha][coluna][cor] += valor
    return nova_matriz_pixels

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
    return nova_matriz_pixels.astype('uint8')

def frequencia_acumulada(histograma):
    canais, valor_canal = histograma.shape[0:2]
    histograma_acumulado = np.zeros((canais, valor_canal))
    for cor in range(0, canais):
        histograma_acumulado[cor][0] = copiar(np.array(histograma[cor])[0][0])
        for valor_pixel in range(1, valor_canal):
            histograma_acumulado[cor][valor_pixel] =  histograma_acumulado[cor][valor_pixel-1] + np.array(histograma[cor])[0][valor_pixel]
    return np.matrix(histograma_acumulado)

def filtro_equalizacao(matriz_pixels):
    nova_matriz_pixels = np.copy(matriz_pixels)
    altura, largura = nova_matriz_pixels.shape[0:2]
    numero_pixels = altura * largura
    numero_ideal_nivel = numero_pixels / (VALOR_CANAL-1)
    distribuicao_cumulativa = frequencia_acumulada(histograma(nova_matriz_pixels))
    for linha in range(0, altura):
        for coluna in range(0, largura):
            for cor in range(0, CANAIS):
                nova_matriz_pixels[linha][coluna][cor] = max(0, round(np.array(distribuicao_cumulativa[cor])[0][nova_matriz_pixels[linha][coluna][cor]] / numero_ideal_nivel)-1)
    return nova_matriz_pixels.astype('uint8')

def grafico_histograma(histograma):
    indice = np.arange(histograma[0].shape[1])
    cores = ['b','g','r']
    for cor in range(0, CANAIS):
        grafico.figure(randrange(1000))
        grafico.xlabel('Valor do pixel no canal', fontsize=10)
        grafico.ylabel('Frequência', fontsize=10)
        grafico.title('Histograma da imagem')
        grafico.bar(indice, np.array(histograma[cor])[0], color=cores[cor], alpha=1)
        grafico.show(block=False)

def selecionar_imagem():
    global painelA, caminho
    caminho = filedialog.askopenfilename()
    if len(caminho) > 0:
        imagem_original = biblimagem.imread(caminho)
        imagem = biblimagem.cvtColor(imagem_original, biblimagem.COLOR_BGR2RGB)
        imagem = Image.fromarray(imagem)
        imagem = ImageTk.PhotoImage(imagem)
        ver_histograma = messagebox.askquestion ('Histograma','Deseja ver histograma?')
        if painelA is None:
            painelA = Label(image=imagem)
            painelA.image = imagem
            painelA.pack(side="left", padx=10, pady=10)
            if ver_histograma == 'yes':
                grafico_histograma(histograma(imagem_original))
        else:
            painelA.configure(image=imagem)
            painelA.image = imagem
            if ver_histograma == 'yes':
                grafico_histograma(histograma(imagem_original))
            if painelB is not None:
                painelB.configure(image='')

def mediana():
    global painelB
    if len(caminho) > 0:
        imagem_tratada_original = filtro_mediana(biblimagem.imread(caminho))
        imagem_tratada = biblimagem.cvtColor(imagem_tratada_original, biblimagem.COLOR_BGR2RGB)
        imagem_tratada = Image.fromarray(imagem_tratada)
        imagem_tratada = ImageTk.PhotoImage(imagem_tratada)
        ver_histograma = messagebox.askquestion ('Histograma','Deseja ver histograma?')
        if painelB is None:
            painelB = Label(image=imagem_tratada)
            painelB.image = imagem_tratada
            painelB.pack(side="right", padx=10, pady=10)
            if ver_histograma == 'yes':
                grafico_histograma(histograma(imagem_tratada_original))
        else:
            painelB.configure(image=imagem_tratada)
            painelB.image = imagem_tratada
            if ver_histograma == 'yes':
                grafico_histograma(histograma(imagem_tratada_original))

def equalizacao():
    global painelB
    if len(caminho) > 0:
        imagem_tratada_original = filtro_equalizacao(biblimagem.imread(caminho))
        imagem_tratada = biblimagem.cvtColor(imagem_tratada_original, biblimagem.COLOR_BGR2RGB)
        imagem_tratada = Image.fromarray(imagem_tratada)
        imagem_tratada = ImageTk.PhotoImage(imagem_tratada)
        ver_histograma = messagebox.askquestion ('Histograma','Deseja ver histograma?')
        if painelB is None:
            painelB = Label(image=imagem_tratada)
            painelB.image = imagem_tratada
            painelB.pack(side="right", padx=10, pady=10)
            if ver_histograma == 'yes':
                grafico_histograma(histograma(imagem_tratada_original))
        else:
            painelB.configure(image=imagem_tratada)
            painelB.image = imagem_tratada
            if ver_histograma == 'yes':
                grafico_histograma(histograma(imagem_tratada_original))

def brilho():
    global painelB
    if len(caminho) > 0:
        valor = simpledialog.askstring("Valor de entrada", "Digite valor de alteração do brilho. Valores positivos para clarear e negativos para escurecer.")
        if valor is not None:
            imagem_tratada_original = filtro_brilho(biblimagem.imread(caminho), int(valor))
            imagem_tratada = biblimagem.cvtColor(imagem_tratada_original, biblimagem.COLOR_BGR2RGB)
            imagem_tratada = Image.fromarray(imagem_tratada)
            imagem_tratada = ImageTk.PhotoImage(imagem_tratada)
            ver_histograma = messagebox.askquestion ('Histograma','Deseja ver histograma?')
            if painelB is None:
                painelB = Label(image=imagem_tratada)
                painelB.image = imagem_tratada
                painelB.pack(side="right", padx=10, pady=10)
                if ver_histograma == 'yes':
                    grafico_histograma(histograma(imagem_tratada_original))
            else:
                painelB.configure(image=imagem_tratada)
                painelB.image = imagem_tratada
                if ver_histograma == 'yes':
                    grafico_histograma(histograma(imagem_tratada_original))

root = Tk()
painelA = None
painelB = None

abrir_imagem = Button(root, text="Selecionar Imagem", command=selecionar_imagem)
abrir_imagem.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
aplicar_mediana = Button(root, text="Aplicar filtro de mediana", command=mediana)
aplicar_mediana.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
aplicar_equalizacao = Button(root, text="Aplicar equalização", command=equalizacao)
aplicar_equalizacao.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
aplicar_brilho = Button(root, text="Aplicar brilho", command=brilho)
aplicar_brilho.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

root.mainloop()
